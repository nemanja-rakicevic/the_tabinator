
__Have you ever been overwhelmed with a vast number of open tabs ...__
<br>
__...but never had the time to go through them, and felt sad to close them?__

Cheer up, the answer you've been looking for is in front of you!
<br>
These scripts allow you to delegate this task to the future you, as many times as you'd like.
<br>
You can save your open tabs to a .json file, and inspect, edit or restore them later. 
<br>
You can even share them with your friends and family!

### Description

Scripts for manipulating the open browser tabs:

__tabs_manage.py__:
<br>
Saves or restores the currently opened tabs from a json file, while preserving the window organisation.
Duplicate tabs are removed.
It is possible to pass additional arguments:
<br>
-load, --load_path: loads the windows/tabs from the specified file path.
<br>
-g, --group_tabs:  allows grouping by url.
<br>
-r, --remove_list: does not save tabs with domains from this list, in order to prune useless websites.


__tabs_focus.py__:
<br>
Traverses all the open tabs and prunes the ones from remove_list (no saving).

NOTE: The script assumes there can be maximum two duplicate tabs in a row,
If more than three tabs repeat, it assumes that it has circled back to the starting tab, so it stops.

### Prerequisites

Current version works on Ubuntu.

Following window managing packages need to be installed:

`sudo apt-get install wmctrl xvkbd xclip xdotool`

wmctrl version (1.07-7build1);
xvkbd version (3.9-1);
xclip version (0.12+svn84-4build1);
xdotool version (1:3.20160805.1-3);


### Resources:

- http://xahlee.info/linux/linux_xvkbd_tutorial.html
- https://unix.stackexchange.com/questions/241658/is-there-a-way-to-get-the-url-from-current-tab-in-google-chrome
- https://unix.stackexchange.com/questions/237626/is-there-a-way-to-activate-a-particular-tab-of-chrome-via-bash
- https://linux.die.net/man/1/xwininfo
- https://olaraundeuord.wordpress.com/2017/08/04/save-and-reload-all-open-chrome-tabs-with-copyallurlspythonapplescript/
