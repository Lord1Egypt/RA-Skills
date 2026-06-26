---
name: raspberry-pi-gpio
description: "在树莓派中配置和使用GPIO. 何时触发: 需要对 LED, Button 这类简单外设进行控制时, 需要对 Servo, Motors 进行简单控制时, 或需要直接控制GPIO时. 不要触发: 当硬件载体不是树莓派时, 当需要精确控制 Servo, Motors时."
---

# Raspberry Pi GPIO Skill

如果需要了解有关 GPIO 硬件的信息, 请参阅 [GPIO 硬件](references/raspberry-pi-gpio.md).

使用 gpiozero 库可以轻松地用 Python 控制 GPIO 设备.  
gpiozero 是其他 GPIO 库（RPi.GPIO, pigpio, lgpio）的封装。它提供了一个通用的 API，这样就可以使用任何适合的后端库，而无需更改代码。

随着树莓派硬件(特别是 Raspberry Pi 5)的架构演变, lgpio 正在逐渐取代 RPi.GPIO 成为新的标准.  
自 Release 2.0 (2023-09-12) 起, lgpio 是 gpiozero 的默认后端.

RPi.GPIO 是树莓派早期的经典 GPIO 库, 直接通过访问硬件寄存器（/dev/mem）来控制引脚.  
而 lgpio 是基于现代 Linux 内核的 gpiochip 接口开发的库, 不依赖特定的硬件地址.

## 首次使用前检查

### gpiozero 

gpiozero 在树莓派操作系统中已经默认安装.  
如果发现没有安装, 则执行下列命令进行安装: 

```bash
sudo apt update
sudo apt install python3-gpiozero
```

### rpi-lgpio

rpi-lgpio 在莓派操作系统中已经默认安装.  
如果发现没有安装, 则需要检查 RPi.GPIO 是否已经安装了。
**因为不能在同一 Python 环境中同时安装 rpi-lgpio 和 rpi-gpio, 因为这两个包都试图安装一个名为 RPi.GPIO 的模块**

如果硬件是 **Raspberry Pi 5** 之前的系列, 可以直接使用 RPi.GPIO.  
否则需要先卸载 RPi.GPIO: 

```bash
sudo apt remove python3-rpi.gpio
```

再执行下列命令进行安装 rpi-lgpio: 

```bash
sudo apt update
sudo apt install python3-rpi-lgpio
```

### RPi.GPIO

如果硬件是 **Raspberry Pi 5** 或之后的系列, 则 RPi.GPIO 已经不能使用, 必须需要安装 rpi-lgpio

RPi.GPIO 在旧版的莓派操作系统中已经默认安装. 

如果发现没有安装, 因为 RPi.GPIO 已经不推荐使用，如果 Linux 内核支持 gpiochip, 则直接安装 rpi-lgpio.  
否则执行下列命令进行安装 RPi.GPIO: 

```bash
sudo apt update
sudo apt install python3-rpi.gpio
```

## 使用 gpiozero

gpiozero 是一个用于树莓派 GPIO 设备的简单接口.  
该库包含了许多简单日常组件的接口，还有一些更复杂的东西，比如传感器、模数转换器、全彩 LED、机器人套件等等.

### GPIO输入 - 读取按钮

```python
from gpiozero import Button
from time import sleep

button = Button(17, pull_up=True)

while True:
    if button.is_pressed:
        print("按钮被按下！")
    sleep(0.1)
```

### GPIO输出 - 控制LED

```python
from gpiozero import LED
from time import sleep

led = LED(18)

# LED闪烁
try:
    while True:
        led.on()
        sleep(0.5)
        led.off()
        sleep(0.5)
except KeyboardInterrupt:
    pass
```

### 事件处理 - 按钮回调

```python
from gpiozero import Button, LED
from signal import pause

button = Button(17)
led = LED(18)

# 按下开灯，松开关灯
button.when_pressed = led.on
button.when_released = led.off

pause()  # 保持程序运行，等待事件
```

### PWM控制

```python
from gpiozero import PWMLED, Servo
from time import sleep

# LED亮度渐变
led = PWMLED(18)
for b in range(0, 101, 5):
    led.value = b / 100
    sleep(0.1)

# 舵机控制
servo = Servo(18)
servo.value = -1   # 0度
sleep(0.5)
servo.value = 0    # 90度
sleep(0.5)
servo.value = 1    # 180度
servo.detach()  # 停止脉冲
```

## 使用 lgpio

lgpio 是树莓派的现代GPIO库, 使用 `/dev/gpiochip` Linux标准接口, 是gpiozero的默认后端.  
仅当遇到 gpiozero 实现不了的复杂需求时, 才能使用它. 

### GPIO基础操作

```python
import lgpio

# 打开 gpiochip0
h = lgpio.gpiochip_open(0)

# 配置GPIO12为输出
lgpio.gpio_claim_output(h, 12)
lgpio.gpio_write(h, 12, 1)  # 高电平
lgpio.gpio_write(h, 12, 0)  # 低电平

# 配置GPIO17为输入（带内部上拉）
lgpio.gpio_claim_input(h, 17, lgpio.SET_PULL_UP)
value = lgpio.gpio_read(h, 17)

# 释放资源
lgpio.gpio_free(h, 12)
lgpio.gpiochip_close(h)
```

### PWM控制

```python
import lgpio

h = lgpio.gpiochip_open(0)

# 在GPIO12上启动PWM: 50Hz, 7.5%占空比
lgpio.tx_pwm(h, 12, 50, 7.5)

# 停止PWM
lgpio.tx_pwm(h, 12, 0, 0)

lgpio.gpiochip_close(h)
```

### 舵机控制

```python
import lgpio
import time

h = lgpio.gpiochip_open(0)

# 脉宽对应角度: 500us=0°, 1500us=90°, 2500us=180°
lgpio.tx_servo(h, 12, 1500)   # 90度
time.sleep(1)
lgpio.tx_servo(h, 12, 500)    # 0度
time.sleep(1)
lgpio.tx_servo(h, 12, 2500)   # 180度

# 停止发送脉冲
lgpio.tx_servo(h, 12, 0)
lgpio.gpiochip_close(h)
```

⚠️ **注意**: `tx_servo` 使用软件定时，会有轻微抖动，仅适合测试。长期使用建议配置硬件PWM。

### 中断/回调

```python
import lgpio

def callback(chip, gpio, level, timestamp):
    """
    中断回调函数
    level: 0=低电平, 1=高电平, 2=边沿变化
    """
    print(f"GPIO {gpio} 状态变为 {level}")

h = lgpio.gpiochip_open(0)

# 配置GPIO17为输入
lgpio.gpio_claim_input(h, 17, lgpio.SET_PULL_UP)

# 添加边沿检测回调
# BOTH_EDGES: 双边沿触发
# RISING_EDGE: 上升沿触发
# FALLING_EDGE: 下降沿触发
cb = lgpio.callback(h, 17, lgpio.BOTH_EDGES, callback)

# 程序运行中...
# 停止回调: cb.cancel()

lgpio.gpiochip_close(h)
```

## 更多示例与故障排错

- 尝试通过 `web_search` 获取更多信息
- 尝试通过 `web_fetch` 访问官方文档来获取精确信息

参考文档:

- [gpiozero](https://gpiozero.readthedocs.io)
- [rpi-lgpio](https://rpi-lgpio.readthedocs.io)