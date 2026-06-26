---
name: raspberry-pi-servo
description: "通过硬件PWM来控制树莓派上的舵机. 何时触发: 当需要精确控制舵机时."
---

# Raspberry Pi Servo Skill

## rpi-hardware-pwm

rpi-hardware-pwm 是一个专门用于访问树莓派硬件 PWM 功能的 Python 库.  
与常见的通过 GPIO 库实现的软件 PWM 不同, 它直接调用树莓派内核提供的硬件控制接口.

### 检查硬件 PWM 是否启用

1. 运行 `lsmod | grep pwm` 来检查系统内核是否启用了 PWM 模块.

2. 硬件 PWM 开启后, 内核会在 `/sys/class/pwm/` 下创建控制目录. 执行以下命令: 

    ```bash
    ls /sys/class/pwm/
    ```

    如果返回空或文件夹不存在, 则硬件 PWM 未开启.

### 启用硬件 PWM

如果硬件 PWM 未开启, 则执行下列流程: 

1. 向 `/boot/firmware/config.txt` 文件添加 `dtoverlay=pwm-2chan`.  

    > config.txt 是什么?
    > 树莓派设备使用一个名为 config.txt 的配置文件, 而不是传统 PC 上的 BIOS.
    > 树莓派操作系统会在位于 /boot/firmware/ 的启动分区中查找此文件.
    > **注意: 在 Raspberry Pi OS Bookworm 之前，Raspberry Pi OS 将启动分区存储在 /boot/ 中.**

    默认情况下, GPIO_18 作为 PWM0 的引脚, GPIO_19 作为 PWM1 的引脚.  
    或者，可以使用 `dtoverlay=pwm-2chan,pin=12,func=4,pin2=13,func2=4` 将 GPIO_18 更改为 GPIO_12，将 GPIO_19 更改为 GPIO_13。

    在 树莓派5 上, 分别使用通道 0 和 1 来控制 GPIO_12 和 GPIO_13; 分别使用通道 2 和 3 来控制 GPIO_18 和 GPIO_19.  
    在所有其他型号上, 分别使用通道 0 和 1 来控制 GPIO_18 和 GPIO_19.

2. 申请重启树莓派
    **注意: 不要擅自重启, 必须向用户提出申请.**

### 安装

1. 激活 python 虚拟环境

    判断在用户目录下是否存在 `.venv` 目录

    如果不存在则执行下列命令进行创建:

    ```bash
    python3 -m venv ~/.venv
    ```
    最后, 执行下列命令激活虚拟环境:

    ```bash
    source ~/.venv/bin/activate
    ```

2. 执行 pip 安装命令

    ```bash
    pip install rpi-hardware-pwm
    ```

### 使用指南

注意, 每次使用前都得确保激活位于 `~/.venv` 的 python venv: 

查看当前激活的是哪个虚拟环境:

```bash
echo $VIRTUAL_ENV
```

激活默认虚拟环境:
```bash
source ~/.venv/bin/activate
```

```python
from rpi_hardware_pwm import HardwarePWM

pwm = HardwarePWM(pwm_channel=0, hz=60, chip=0)
pwm.start(100) # full duty cycle

pwm.change_duty_cycle(50)
pwm.change_frequency(25_000)

pwm.stop()
```

### 排错指南

遇到错误的时候立刻阅读 [troubleshooting](references/troubleshooting.md) 了解更多信息.