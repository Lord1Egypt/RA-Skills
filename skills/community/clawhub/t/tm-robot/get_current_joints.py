import sys
sys.path.insert(0, '.')
from tm_robot import SVRParser
import asyncio

parser = SVRParser('192.168.1.13')
print('Connecting to SVR...')
if parser.connect(timeout=10):
    print('Connected!')
    joints = parser.get_value('Joint_Angle')
    if joints:
        print('\n当前关节坐标:')
        print(f'  J1 = {joints[0]:7.3f}°')
        print(f'  J2 = {joints[1]:7.3f}°')
        print(f'  J3 = {joints[2]:7.3f}°')
        print(f'  J4 = {joints[3]:7.3f}°')
        print(f'  J5 = {joints[4]:7.3f}°')
        print(f'  J6 = {joints[5]:7.3f}°')
    else:
        print('读取失败：Joint_Angle = None')
    parser.disconnect()
else:
    print('连接失败')
