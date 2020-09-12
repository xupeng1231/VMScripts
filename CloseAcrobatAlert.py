# -*- coding: gbk -*-
from win32gui import *
import win32gui
import win32con
import time


def get_child_windows(parent):
    if not parent:
        return
    hwndChildList = []
    win32gui.EnumChildWindows(parent, lambda hwnd, param: param.append(hwnd),  hwndChildList)
    return hwndChildList

js_window_exist=False
def close(hwnd, mouse):
    global js_window_exist
    if IsWindow(hwnd) and IsWindowVisible(hwnd):
        windowtext =GetWindowText(hwnd).decode('gbk')
        if windowtext.find('JavaScript')>=0 or windowtext.find(u'调试程序')>=0:
            js_window_exist = True

    if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
        # classname =GetClassName(hwnd)
        windowtext =GetWindowText(hwnd).decode('gbk')
        if windowtext.find('Acrobat')>=0:
            cl = get_child_windows(hwnd)
            for c in cl:
                t = GetWindowText(c).decode('gbk')
                if t == u'确定':
                    win32gui.SendMessage(c, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
                    win32gui.SendMessage(c, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 0)


def close_acrobat_alert():
    global js_window_exist
    js_window_exist = False
    EnumWindows(close, 0)
    return js_window_exist


def main():
    global js_window_exist
    while True:
        js_window_exist = False
        close_acrobat_alert()
        time.sleep(0.1)
        print js_window_exist


if __name__ == '__main__':
    main()