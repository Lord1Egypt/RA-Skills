# =============================================================================
# LED.py — LED 指示灯封装
# 提供亮/灭/翻转三个方法，内部记录当前状态
# =============================================================================

import machine


class LED:
    """单个 LED 的控制封装，基于 machine.Pin 输出模式。"""

    def __init__(self, pin_num):
        """
        参数:
            pin_num: GPIO 引脚编号（对应 machine.Pin 的 GPIOn）
        """
        self.pin   = machine.Pin(pin_num, machine.Pin.OUT, machine.Pin.PULL_DISABLE, 0)
        self.state = False  # False=灭, True=亮

    def on(self):
        """点亮 LED。"""
        self.pin.write(1)
        self.state = True

    def off(self):
        """熄灭 LED。"""
        self.pin.write(0)
        self.state = False

    def toggle(self):
        """翻转 LED 状态。"""
        if self.state:
            self.off()
        else:
            self.on()
