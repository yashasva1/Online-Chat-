import os

comm = ''

for i in range(10001,10005):
    comm += f'adb connect 192.168.0.103:{i} &&'

os.system(f'cmd /k "{comm}"') 
