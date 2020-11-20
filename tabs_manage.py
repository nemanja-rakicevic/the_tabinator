
"""
Author:         Nemanja Rakicevic
Date:           November 2020
Description:
                Script that saves and loads currently open browser tabs,
                to and from a json file, on Ubuntu.
"""

import os
import json
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

    parser.add_argument('-load', '--load_path',
                        default=None,
                        help="Path to the tab json file.")

    parser.add_argument('-save', '--save_path',
                        default=None,
                        help="Path to the tab json file.")

    parser.add_argument('-b', '--browser_name',
                        default=None,
                        help="Browser name, if None, default browser is used.")

    parser.add_argument('-g', '--group_tabs',
                        default=False,
                        help="Group tabs by website.")

    parser.add_argument('-r', '--remove_list',
                        nargs='+', default=['facebook', 'instagram'],
                        help="Exclude certain websites.")

    return parser.parse_args()


def xvkbd_command(window_id, cmd):
    """Simplify the xvkbd command."""
    os.system(
        'xvkbd -no-jump-pointer -window {} -xsendevent -text "{}"'
        ' 2>> /dev/null'.format(window_id, cmd))


@keep_active_window
def save_tabs(save_path, browser_name, remove_list, group_tabs, **kwargs):
    """
    Access all the open browser windows and their tabs,
    copy tab titles and URLs and save to json file.
    """
    save_path = os.path.join(os.path.dirname(__file__), "backup_tabs.json") \
        if save_path is None else save_path
    browser_name = webbrowser.get().__class__.__name__ \
        if browser_name is None else browser_name
    replace_str = ' - Google Chrome' if browser_name == 'Chrome' else ''
    # Get open window ids
    ids = os.popen('wmctrl -l | grep -oP "(?<=)(0x\w+)(?=.*{})"'.format(
        browser_name)).read()
    open_windows = ids.split('\n')[:-1]
    num_windows = len(open_windows)
    windows_list = []
    # Loop through the windows
    for wi, window_id in enumerate(open_windows):
        print("\n\n=== Saving window id: {} [{}/{}] ===".format(
            window_id, wi + 1, num_windows))
        # Focus on first tab
        xvkbd_command(window_id, '\C1')
        cnt_d = 0
        tab_id = 0
        tabs_list = []
        tabs_dupl = []
        # Loop through tabs within the window
        while True and tab_id < 20 and cnt_d < 100:
            tab_id += 1
            xvkbd_command(window_id, '\Cl')
            xvkbd_command(window_id, '\Cc')
            url = os.popen('xclip -out -selection clipboard').read()
            title = os.popen(
                "xwininfo -id {} | grep xwininfo".format(window_id)).read()
            title = title.split('"')[1].replace(replace_str, '')

            # Exclude websites that are in the remove_list
            if len(remove_list) and sum([rd in url for rd in remove_list]):
                print("\nSkipping blacklisted website: '{}'".format(title))
                xvkbd_command(window_id, '\C\[Next]')
                continue
            # Try to figure our if back in the beginning or duplicates
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
                print("\nTab {}\n> title:  '{}'\n> url:    {}".format(
                    tab_id, title, url))
            # Go to next tab
            xvkbd_command(window_id, '\C\[Next]')
        # Remove duplicates
        tabs_list = list({tl['url']: tl for tl in tabs_list}.values())
        # Group tabs (sorting by URL)
        if group_tabs:
            tabs_list = sorted(tabs_list, key=lambda k: k['url'])
        windows_list.append(tabs_list)
    # Save list
    print("\n\n>>> DONE. Saving to file: {}\n".format(save_path))
    with open(save_path, 'w') as outfile:
        json.dump(windows_list, outfile, sort_keys=True, indent=4)


@keep_active_window
def load_tabs(load_path):
    """Load the saved tabs list, restore the same window-tab hierarchy."""
    with open(load_path, 'r') as f:
        window_list = json.load(f)
    num_windows = len(window_list)
    # Loop through windows
    for w, tabs_list in enumerate(window_list):
        print("\n=== Restoring window [{}/{}] ===".format(w + 1, num_windows))
        num_tabs = len(tabs_list)
        # Loop through tabs
        for ti, tab_dict in enumerate(tabs_list):
            title = tab_dict['title']
            url = tab_dict['url']
            print("\nTab [{}/{}]\n> title:  '{}'\n> url:    {}".format(
                ti + 1, num_tabs, title, url))
            # Keep the window-tab hierarchy
            webbrowser.open_new_tab(url) if ti else webbrowser.open_new(url)
    print("\n\n>>> DONE. All tabs restored from file: {}\n".format(load_path))


if __name__ == "__main__":
    args = get_args()
    if args.load_path is not None:
        load_tabs(load_path=args.load_path)
    else:
        save_tabs(**vars(args))
