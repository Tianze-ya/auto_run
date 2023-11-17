import os
import sys
import winreg
import win32api
import win32con


def auto_run():
    """
    开机自启
    """
    #是否管理员权限
    if not os.geteuid() == 0:
        raise BaseException("请使用管理员身份运行此程序")
    #注册表位置
    location = f"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
    BaseName = os.path.basename(sys.argv[0])
    #判断是否已经自启
    def is_auto_run() ->bool:
        # 获取注册表该位置的所有键值
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, location)
        i = 0
        while True:
            try:
                # 获取注册表对应位置的键和值
                if winreg.EnumValue(key, i)[0] == BaseName:
                    return True
                i += 1
            except OSError:
                winreg.CloseKey(key) #关闭注册表
                break
        return False

    if not is_auto_run():
        sys.setrecursionlimit(1000000) #设置递归深度
        commnd = os.path.join(os.getcwd(),BaseName) #启动软件的命令
        name = BaseName
        #打开注册表
        key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, location, 0, win32con.KEY_ALL_ACCESS)
        #设置注册表
        win32api.RegSetValueEx(key, name, 0, win32con.REG_SZ, commnd)
        win32api.RegCloseKey(key) #关闭注册表

auto_run()
