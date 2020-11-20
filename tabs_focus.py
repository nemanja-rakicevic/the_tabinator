
"""
Author:         Nemanja Rakicevic
Date:           November 2020
Description:
                Script that traverses open tabs and closes the ones from the
                procrastination list.
"""


import pdb

import os
import argparse
import webbrowser


START_AFTER = 1


def keep_active_window(func):
    """Make sure to return the focus on the window which was active."""
    def wrap(*args, **kwargs):
        active_id = os.popen('xdotool getactivewindow').read()
        func(*args, **kwargs)
        os.system('xdotool windowactivate {}'.format(active_id))
    return wrap


def get_args():
    """Extract script arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument('-b', '--browser_name',
                        default='Chrome',
                        help="Browser name.")

    parser.add_argument('-r', '--remove_list',
                        nargs='+', default=['facebook', 'youtube'],
                        help="Exclude certain websites.")

    return parser.parse_args()


def xvkbd_command(window_id, cmd):
    """Simplify the xvkbd command."""
    os.system(
        'xvkbd -no-jump-pointer -window {} -xsendevent -text "{}"'
        ' 2>> /dev/null'.format(window_id, cmd))


@keep_active_window
def prune_tabs(browser_name, remove_list, **kwargs):
    """
    Access all the open browser windows and their tabs,
    copy tab titles and URLs and save to json file.
    """
    browser_name = webbrowser.get().__class__.__name__ \
        if browser_name is None else browser_name
    # Get open window ids
    ids = os.popen('wmctrl -l | grep -oP "(?<=)(0x\w+)(?=.*{})"'.format(
        args.browser_name)).read()
    open_windows = ids.split('\n')[:-1]
    num_windows = len(open_windows)
    # Loop through the windows and tabs
    n_removed = 0
    for wi, window_id in enumerate(open_windows):
        print("\n\n=== Saving window id: {} [{}/{}] ===".format(
            window_id, wi + 1, num_windows))
        tabs_list = []
        # Focus on first tab
        xvkbd_command(window_id, '\C1')
        cnt_d = 0
        tab_id = 0
        tabs_list = []
        tabs_dupl = []
        while True and tab_id < 20 and tab_id > -5:
            tab_id += 1
            xvkbd_command(window_id, '\Cl')
            xvkbd_command(window_id, '\Cc')
            url = os.popen('xclip -out -selection clipboard').read()
            title = os.popen(
                "xwininfo -id {} | grep xwininfo".format(window_id)).read()
            title = title.split('"')[1]
            # Exclude websites that are in the remove_list
            if len(remove_list) and sum([rd in url for rd in remove_list]):
                xvkbd_command(window_id, '\Cw')
                n_removed += 1
                print("\nRemoved Tab {}\n> title:  '{}'\n> url:    {}".format(
                    tab_id, title, url))
                tab_id -= 1
                continue
            # Try to figure our if back in the beginning, or duplicates
            if len(tabs_list) > START_AFTER and url == tabs_list[cnt_d]['url']:
                cnt_d += 1                
                tabs_dupl.append(
                    {'window_id': wi + 1, 'title': title, 'url': url})
                # If the list has been repeated
                if len(tabs_dupl) == len(tabs_list):
                    break
            else:
                if len(tabs_dupl):
                    tabs_list = tabs_list + tabs_dupl
                    tabs_dupl = []
                    cnt_d = 0
                    # Stay at the same tab to double-check
                    tab_id -= 1
                    continue
                # Add tab to collection
                tabs_list.append(
                    {'window_id': wi + 1, 'title': title, 'url': url})
            if len(tabs_dupl) == 0:
                print("\nOK tab {}".format(tab_id))
                # print("\nTab {}\n> title:  '{}'\n> url:    {}".format(
                #     tab_id, title, url))
            # Go to next tab
            xvkbd_command(window_id, '\C\[Next]')
    # Save list
    print("\n\n>>> DONE. Removed {} tabs\n".format(n_removed))


if __name__ == "__main__":
    args = get_args()
    prune_tabs(**vars(args))
