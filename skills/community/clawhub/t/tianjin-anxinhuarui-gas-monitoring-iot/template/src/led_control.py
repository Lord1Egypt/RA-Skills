# -*- coding: utf-8 -*-
"""
LED 指示灯控制模块
提供 GPIO 引脚的 LED 开关、闪烁控制
"""
import machine
import utime


class LED:
    """LED 指示灯控制类"""
    
    def __init__(self, pin_number):
        """
        初始化 LED
        
        参数:
            pin_number: GPIO 引脚编号
        """
        self.pin = machine.Pin(pin_number, machine.Pin.OUT)
        self.state = False  # 初始状态为关闭

    def on(self):
        """打开 LED"""
        self.pin.write(1)
        self.state = True

    def off(self):
        """关闭 LED"""
        self.pin.write(0)
        self.state = False

    def toggle(self):
        """切换 LED 状态"""
        if self.state:
            self.off()
        else:
            self.on()

    def flash(self, on_time, off_time, times):
        """
        闪烁 LED
        
        参数:
            on_time: 点亮时间 (秒)
            off_time: 熄灭时间 (秒)
            times: 闪烁次数
        """
        for _ in range(times):
            self.on()
            utime.sleep(on_time)
            self.off()
            utime.sleep(off_time)
