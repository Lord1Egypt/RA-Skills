---
name: zynq-linux-dev
description: |
  Zynq-7000 / Zynq UltraScale+ 硬件调试技能。用于在 Xilinx Zynq (Cortex-A9/A53 + FPGA) Linux 环境下调试 I2C、I2S、UART、GPIO 等硬件外设。包括设备树配置、内核驱动、用户空间调试工具、交叉编译和常见问题排查。适用于 PetaLinux、Debian 或自定义 Linux 系统的 Zynq 平台硬件调试。
---

# Zynq Linux 硬件调试

## 概述

Zynq-7000 (Cortex-A9) 和 Zynq UltraScale+ (Cortex-A53/A55) 是 Xilinx 的 ARM + FPGA 异构计算平台。Linux 运行在 ARM 处理器上，FPGA 部分通过 AXI 总线与 CPU 交互。

## 交叉编译环境

### 工具链

```bash
# Zynq-7000 (Cortex-A9) - 32-bit
export ARCH=arm
export CROSS_COMPILE=arm-linux-gnueabihf-
arm-linux-gnueabihf-gcc -o app main.c

# Zynq UltraScale+ (Cortex-A53) - 64-bit
export ARCH=arm64
export CROSS_COMPILE=aarch64-linux-gnu-
aarch64-linux-gnu-gcc -o app main.c
```

### 编译内核模块

```bash
# 编译 external kernel module
export KERNEL=/lib/modules/$(uname -m)/build
make -C $KERNEL ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- M=$(pwd) modules
```

## I2C 调试

### 设备检测

```bash
# 列出所有 I2C 总线
i2cdetect -l

# 扫描总线上的设备 (总线编号从 0 开始)
i2cdetect -y 0

# 读取指定设备寄存器
i2cget -y 0 0x68 0x00    # 设备地址 0x68, 寄存器 0x00
i2cget -y 0 0x68 0x00 w  # 16-bit 寄存器

# 写入寄存器
i2cset -y 0 0x68 0x06 0x00

# 读取连续多个寄存器
i2cdump -y 0 0x68 s 0x00 0x10
```

### 用户空间驱动

```c
// /dev/i2c-0 用户空间访问
#include <linux/i2c.h>
#include <linux/i2c-dev.h>

int fd = open("/dev/i2c-0", O_RDWR);
struct i2c_msg msgs[] = {
    { .addr = 0x68, .flags = 0, .len = 1, .buf = &reg },
    { .addr = 0x68, .flags = I2C_M_RD, .len = 4, .buf = data },
};
struct i2c_rdwr_ioctl_data msgset = { .msgs = msgs, .nmsgs = 2 };
ioctl(fd, I2C_RDWR, &msgset);
close(fd);
```

### 内核设备树配置

```dts
&i2c0 {
    status = "okay";
    clock-frequency = <400000>;
    i2c-mux@70 {
        compatible = "nxp,pca9542";
        reg = <0x70>;
        #address-cells = <1>;
        #size-cells = <0>;
        sensor@0 {
            compatible = "bosch,bme280";
            reg = <0x76>;
            interrupts = <0 25 IRQ_TYPE_EDGE_FALLING>;
        };
    };
};
```

## I2S 调试

### ALSA 设备

```bash
# 列出音频设备
aplay -l
arecord -l

# 测试录音
arecord -f S16_LE -r 48000 -c 2 -d 5 test.wav

# 播放录音
aplay test.wav

# 查看 ALSA 驱动日志
dmesg | grep -i "asoc\|snd\|i2s"
```

### 调试接口

```bash
# 使用 amixer 调节音量
amixer -c 0 sset "Master" 50%
amixer -c 0 sset "Capture" 70%

# 查看详细设备信息
cat /proc/asound/card0/pcm0c/info
cat /proc/asound/card0/pcm0p/info
```

### 内核设备树配置 (I2S)

```dts
&i2s {
    status = "okay";
    #sound-dai-cells = <0>;
};

sound: sound {
    compatible = "simple-audio-card";
    simple-audio-card,name = "Zynq-I2S";
    simple-audio-card,format = "i2s";
    simple-audio-card,frame-master = <&cpu_dai>;
    simple-audio-card,bitclock-master = <&cpu_dai>;
    cpu_dai: cpu@0 {
        sound-dai = <&i2s>;
    };
};
```

## UART 调试

### 设备节点

```bash
# 串口设备通常是 /dev/ttyPS0, ttyS0, ttyUSB0
ls -l /dev/tty[SU]*

# 配置波特率
stty -F /dev/ttyPS0 speed 115200 cs8 -parenb -cstopb cread

# 读取
cat /dev/ttyPS0 &

# 写入
echo "test" > /dev/ttyPS0
```

### minicom

```bash
minicom -D /dev/ttyPS0 -b 115200
```

### 内核设备树配置

```dts
&uart0 {
    status = "okay";
};
```

## GPIO 调试

### sysfs 接口

```bash
# 导出 GPIO (编号基于 SoC)
echo 54 > /sys/class/gpio/export
echo "out" > /sys/class/gpio/gpio54/direction
echo 1 > /sys/class/gpio/gpio54/value
echo "in" > /sys/class/gpio/gpio54/direction
cat /sys/class/gpio/gpio54/value
```

### libgpiod

```bash
# 列出 GPIO 芯片
gpiodetect

# 读取 GPIO 状态
gpioinfo gpiochip0

# 读取单个 GPIO
gpioget gpiochip0 54

# 设置 GPIO
gpioset gpiochip0 54=1
```

### 内核设备树配置

```dts
gpio {
    compatible = "xlnx,pmod-gpio";
    gpio-controller;
    #gpio-cells = <2>;
    ngpios = <8>;
    gpio-line-names = "", "LED1", "LED2", "", "", "", "", "", "";
};
```

## FPGA 调试

### /dev/fpga0

```bash
# 加载.bit 文件
cat design.bit > /dev/fpga0

# 检查状态
cat /sys/class/fpga0/fpga0/status
```

### 查看 FPGA 寄存器

```bash
# AXI 总线地址映射通常在 0x40000000 ~ 0x80000000
devmem 0x40000000
devmem2 0x40000000 w 0x12345678
```

## 常用命令速查

```bash
# 内核模块
lsmod
modprobe <module>
rmmod <module>
dmesg | tail -50

# 设备树
ls /proc/device-tree/

# 内存
devmem <addr> [w <value>]
cat /proc/cmdline
cat /proc/iomem

# CPU 信息
cat /proc/cpuinfo
```

## 常见问题排查

| 症状 | 可能原因 | 排查方法 |
|------|---------|---------|
| I2C 设备无响应 | 地址错误/SCL/SDA 浮空 | 逻辑分析仪测 SDA/SCL 波形 |
| I2S 无声音 | 时钟配置/格式不匹配 | 检查 LRCLK/BCLK 频率 |
| UART 无输出 | 波特率/流控 | 用示波器测 TX 引脚 |
| GPIO 无响应 | 未导出/权限 | 检查 /sys/class/gpio/ |
| FPGA 加载失败 | .bit 文件损坏 | 检查校验和 |