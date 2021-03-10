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


def close(hwnd, mouse):
    global js_window_exist
    if IsWindow(hwnd) and IsWindowVisible(hwnd):
        windowtext =GetWindowText(hwnd).decode('gbk')
        if windowtext.find('JavaScript')>=0 or windowtext.find(u'���Գ���')>=0:
            js_window_exist = True

    if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
        # classname =GetClassName(hwnd)
        windowtext =GetWindowText(hwnd).decode('gbk')
        if windowtext.find(u'��Ӹ���')>=0:
            cl = get_child_windows(hwnd)
            print '*'*50
            for c in cl:
                t = GetWindowText(c).decode('gbk')
                if t.find(u'ȡ��')>=0:
                    win32gui.SendMessage(c, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
                    win32gui.SendMessage(c, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 0)
        if windowtext.find(u'��ȫ�Ծ���')>=0 or windowtext.find(u'��ȫ�Խ�ֹ')>=0:
            cl = get_child_windows(hwnd)
            for c in cl:
                t = GetWindowText(c).decode('gbk')
                if t.startswith(u'��ֹ'):
                    win32gui.SendMessage(c, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
                    win32gui.SendMessage(c, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 0)
                elif t.startswith(u'ȷ��'):
                    win32gui.SendMessage(c, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
                    win32gui.SendMessage(c, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 0)
                    print 'close queding'
                pass
        if windowtext.find('Acrobat') >= 0 \
                or windowtext.find(u'����') >= 0 and windowtext.find('JavaScript') >= 0 \
                or windowtext.find(u'����Ķ���')>=0 or windowtext.startswith('Foxit Reader'):
            cl = get_child_windows(hwnd)
            for c in cl:
                t = GetWindowText(c).decode('gbk')
                if t == u'ȷ��' or t.startswith(u'ȷ��') or t.startswith('&OK'):
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


if __name__ == '__main__':
    main()