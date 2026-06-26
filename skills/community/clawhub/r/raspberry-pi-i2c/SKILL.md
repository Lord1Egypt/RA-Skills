---
name: Raspberry Pi I2C Sensor Development
description: >
  树莓派 I2C 传感器开发实战指南。覆盖 Raspberry Pi 4B / Zero 的 GPIO 引脚定义、
  标准 I2C 与软件 I2C (bit-banging) 的选型与陷阱、gpiod 库使用、BMI270 6轴 IMU
  和 MAX30205 温度传感器的驱动开发经验、性能瓶颈分析与常见故障排查。
  来源：Raspberry Pi 官方文档、pinout.xyz、以及 BMI270 + MAX30205 实际项目踩坑记录。
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# 树莓派 I2C 传感器开发实战指南

## 一、GPIO 引脚速查表（多来源核对）

Raspberry Pi 4B / Zero / Zero 2 W / 3B+ 均采用 **40-pin GPIO Header**，引脚布局完全兼容。
引脚编号规则：USB 口朝下时，**Pin 1 在左上角**（方焊盘），按书页顺序编号。

> **来源核对**：Raspberry Pi 官方文档 [raspberrypi.com](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html)、
> [pinout.xyz](https://pinout.xyz/)、[Wevolver Pi 4 Pinout Guide](https://www.wevolver.com/article/raspberry-pi-4-pinout-a-comprehensive-guide-for-engineers)、
> [Electronics for You GPIO 指南](https://electronicsforyou.com/blog/all-about-raspberry-pi-gpio-pins/)

### 1.1 通信接口引脚（I2C / SPI / UART）

| 协议 | 信号 | BCM GPIO | 物理引脚 | 关键说明 |
|------|------|----------|----------|----------|
| **I2C-1** | SDA | GPIO2 | **Pin 3** | 默认 I2C 总线；板载 **1.8kΩ 固定上拉** 到 3.3V |
| **I2C-1** | SCL | GPIO3 | **Pin 5** | 同上；同时是 **唤醒引脚**（拉低可唤醒关机状态的 Pi） |
| **SPI0** | MOSI | GPIO10 | **Pin 19** | 主出从入 |
| **SPI0** | MISO | GPIO9 | **Pin 21** | 主入从出 |
| **SPI0** | SCLK | GPIO11 | **Pin 23** | 时钟 |
| **SPI0** | CE0 | GPIO8 | **Pin 24** | 片选 0 |
| **SPI0** | CE1 | GPIO7 | **Pin 26** | 片选 1 |
| **UART0** | TXD | GPIO14 | **Pin 8** | 默认串口控制台；如需他用需先禁用 console |
| **UART0** | RXD | GPIO15 | **Pin 10** | 默认串口控制台 |
| **I2C-0** | ID_SD | GPIO0 | **Pin 27** | 保留给 HAT ID EEPROM，**不要占用** |
| **I2C-0** | ID_SC | GPIO1 | **Pin 28** | 保留给 HAT ID EEPROM，**不要占用** |

### 1.2 电源与通用 GPIO 引脚

| 物理引脚 | 功能 | 物理引脚 | 功能 |
|----------|------|----------|------|
| 1 | 3.3V | 2 | 5V |
| 4 | 5V | 6 | GND |
| 7 | GPIO4 | 9 | GND |
| 11 | GPIO17 | 12 | GPIO18 (PWM0) |
| 13 | GPIO27 | 14 | GND |
| 15 | GPIO22 | 16 | GPIO23 |
| 17 | 3.3V | 18 | GPIO24 |
| 20 | GND | 22 | GPIO25 |
| 25 | GND | 26 | GPIO7 (CE1) |
| 29 | GPIO5 | 30 | GND |
| 31 | GPIO6 | 32 | GPIO12 (PWM0) |
| 33 | GPIO13 (PWM1) | 34 | GND |
| 35 | GPIO19 (PCM_FS / SPI1) | 36 | GPIO16 (SPI1 CE2) |
| 37 | GPIO26 | 38 | GPIO20 (PCM_DIN / SPI1) |
| 39 | GND | 40 | GPIO21 (PCM_DOUT / SPI1) |

### 1.3 电气特性（必须遵守）

- **3.3V 逻辑电平**：所有 GPIO 通信引脚（SDA/SCL/MOSI/MISO/TX/RX）均为 **3.3V**，**不兼容 5V**。直接接 5V 会烧毁 GPIO。
- **GPIO2/GPIO3 固定上拉**：这两个引脚有 **~1.8kΩ 板载上拉电阻** 到 3.3V，因此：
  - 不能配置为下拉或浮空输入
  - 非常适合 I2C（I2C 规范要求 SDA/SCL 上拉）
  - 如果当普通 GPIO 用，默认就是高电平
- **3.3V 电源限制**：总输出电流约 **800mA**，5V 引脚直通 USB 供电。
- **Zero 系列**：Zero / Zero W / Zero 2 W 出厂 **不焊排针**，需自行焊接或使用带排针版本（WH）。

---

## 二、I2C 总线选型：标准 I2C vs 软件 I2C

### 2.1 标准 I2C（/dev/i2c-1）

使用硬件 I2C 控制器，驱动由 Linux 内核管理。

```bash
# 启用
sudo raspi-config  # -> Interface Options -> I2C -> Enable
# 或修改 /boot/config.txt 添加：
# dtparam=i2c_arm=on
```

| 优点 | 缺点 |
|------|------|
| 稳定可靠，400kHz 标准速率 | 只能使用固定的 GPIO2/GPIO3（pin3/5） |
| 内核管理时钟拉伸、仲裁 | 无法启用内部上拉（树莓派已带物理上拉，通常够用） |
| Python `smbus2` / C `ioctl` 直接可用 | 如需其他 GPIO 做 I2C，必须用软件方案 |
| **性能瓶颈在 Linux I2C 子系统**（~1.3ms/事务） | 不是 C 语言 vs Python 的差距 |

### 2.2 软件 I2C（Bit-Banging）

通过 GPIO 手动翻转电平模拟 I2C 时序，可使用任意 GPIO。

**适用场景**：
- 标准 I2C-1 已被其他设备占用
- 传感器需要接到非标准引脚（如 GPIO8/9）
- 需要与 SPI 引脚复用（GPIO8/9 同时也是 SPI0 CE0/MISO）

**两种实现方式**：

| 方式 | 实现 | 内部上拉支持 | 性能 | 推荐度 |
|------|------|--------------|------|--------|
| **内核 i2c-gpio overlay** | `dtoverlay=i2c-gpio` | **不支持**（重大陷阱） | 一般 | 不推荐 |
| **用户态 gpiod 库** | Python `gpiod` / C `libgpiod` | **支持** `GPIOD_LINE_REQUEST_FLAG_BIAS_PULL_UP` | ~50kHz (10us 延时) | 推荐 |

**内核 overlay 陷阱**：`i2c-gpio` 设备树叠加层无法启用 SoC 内部上拉电阻。如果外接传感器没有外部上拉，I2C 总线会处于浮空状态，导致设备扫描不到、通信失败。**必须用 gpiod 库在用户态实现**。

### 2.3 性能对比（实测数据）

以 BMI270 读取 12 字节（accel + gyro）为例：

| 方案 | 单次读取耗时 | 理论最高频率 | 备注 |
|------|-------------|-------------|------|
| Python + `smbus2` (标准 I2C) | ~2-3ms | ~400Hz | 内核 I2C 开销 |
| C + `ioctl` (标准 I2C) | ~1.3ms | ~700Hz | **与 Python 同数量级** |
| Python + gpiod bit-banging | ~3-4ms | ~250Hz | 10us/bit 延时 |
| C + gpiod bit-banging | ~3-4ms | ~250Hz | 10us/bit 延时 |

**关键结论**：
- C 并不比 Python 快多少，**瓶颈在 Linux I2C 内核层**（系统调用 + 调度）
- Bit-banging 的瓶颈是 GPIO 翻转延时（微秒级 sleep），C 和 Python 性能接近
- 要达到 200Hz 连续采集，**必须用标准 I2C（/dev/i2c-1）+ 块读取**，且 BMI270 必须接在 pin3/5

---

## 三、gpiod 库使用指南

### 3.1 安装

```bash
# Python
pip3 install gpiod

# C
sudo apt install libgpiod-dev
```

### 3.2 Python：SMBus 兼容层

用 gpiod 实现一个与 `smbus2.SMBus` 接口兼容的类，可 monkey-patch 替换原驱动中的 SMBus：

```python
import gpiod
from gpiod.line import Direction, Value, Bias

class SMBus:
    """gpiod-based bit-banging I2C compatible with smbus2.SMBus"""
    def __init__(self, bus=None):
        self.chip = gpiod.Chip('/dev/gpiochip0')
        self.scl_pin = 9   # GPIO9 (物理 pin21)
        self.sda_pin = 8   # GPIO8 (物理 pin24)
        self.addr = 0

    def _delay(self):
        import time
        time.sleep(0.00001)  # 10us = ~50kHz

    def _start(self):
        # SCL=1 时 SDA 从高变低
        ...

    def _stop(self):
        # SCL=1 时 SDA 从低变高
        ...

    def write_byte_data(self, addr, reg, value):
        self.addr = addr
        self._start()
        self._write_raw(addr << 1)      # ADDR + W
        self._write_raw(reg)
        self._write_raw(value)
        self._stop()

    def read_i2c_block_data(self, addr, reg, length):
        self.addr = addr
        self._start()
        self._write_raw(addr << 1)      # ADDR + W
        self._write_raw(reg)
        self._start()                   # Repeated START
        self._write_raw((addr << 1) | 1)  # ADDR + R
        data = [self._read_raw(ack=1) for _ in range(length-1)]
        data.append(self._read_raw(ack=0))  # 最后字节发 NACK
        self._stop()
        return data

    def write_i2c_block_data(self, addr, reg, data):
        self.addr = addr
        self._start()
        self._write_raw(addr << 1)
        self._write_raw(reg)
        for b in data:
            self._write_raw(b)
        self._stop()
```

**关键技巧**：
- SDA 引脚需要在 **输出模式**（带内部上拉）和 **输入模式**（带内部上拉）之间切换
- 输出模式用 `GPIOD_LINE_REQUEST_FLAG_BIAS_PULL_UP`
- 输入模式也用 `GPIOD_LINE_REQUEST_FLAG_BIAS_PULL_UP`
- 不要共用输入/输出 line 对象，release 后再 re-request

### 3.3 C：libgpiod 接口

```c
#include <gpiod.h>

#define SDA_GPIO  8
#define SCL_GPIO  9

struct gpiod_chip *chip = gpiod_chip_open("/dev/gpiochip0");
struct gpiod_line *scl = gpiod_chip_get_line(chip, SCL_GPIO);

// SCL 固定为输出（带上拉）
gpiod_line_request_output_flags(scl, "i2c_driver",
    GPIOD_LINE_REQUEST_FLAG_BIAS_PULL_UP, 1);

// SDA 读时切为输入（带上拉）
gpiod_line_request_input_flags(sda_in, "i2c_driver",
    GPIOD_LINE_REQUEST_FLAG_BIAS_PULL_UP);

// SDA 写时切为输出（带上拉）
gpiod_line_request_output_flags(sda_out, "i2c_driver",
    GPIOD_LINE_REQUEST_FLAG_BIAS_PULL_UP, 1);
```

---

## 四、BMI270 6轴 IMU 专项

### 4.1 基本信息

| 参数 | 值 |
|------|-----|
| I2C 地址 | **0x68** (SDO 接 GND) / **0x69** (SDO 接 VCC) |
| CHIP_ID | **0x24** |
| 供电 | 1.8V ~ 3.6V，树莓派 3.3V 可直接驱动 |
| 量程 | Accel: ±2/4/8/16g；Gyro: ±125/250/500/1000/2000 dps |

### 4.2 初始化流程（关键！必须严格遵循）

BMI270 **每次上电或软复位后必须加载 8KB config 文件**，否则无法工作。

```
1. 读 CHIP_ID (0x00) -> 应返回 0x24
2. 写 PWR_CONF (0x7C) = 0x00     # 禁用高级省电模式
3. 延时 1ms
4. 写 INIT_CTRL (0x59) = 0x00    # 准备加载 config
5. 延时 1ms
6. 【循环 256 次】每次写 32 字节到 INIT_DATA (0x5E)
   - 写 INIT_ADDR_0 (0x5B) = 0x00
   - 写 INIT_ADDR_1 (0x5C) = page (0~255)
   - burst write: 0x5E + 32 bytes config data
   - 每页延时 30us
7. 写 INIT_CTRL (0x59) = 0x01    # 完成加载
8. 延时 30ms
9. 轮询 INTERNAL_STATUS (0x21) 直到 == 0x01（最多等 2 秒）
10. 写 PWR_CTRL (0x7D) = 0x07   # 启用 Accel + Gyro + Temp
11. 配置 ODR 和量程
```

### 4.3 Config 文件加载技巧

- Config 文件为二进制 `.bin`，**8192 字节**，由 Bosch 官方提供
- 不能 byte-by-byte 写入，太慢且不可靠。应使用 **块写入**（burst write）
- 标准 I2C 下：直接用 `write(i2c_fd, buf, 33)`，buf[0]=0x5E, buf[1..32]=config data
- 块写入时序：START -> ADDR+W -> REG(0x5E) -> 32 bytes data -> STOP
- 每页（32 字节）写完后延时 **30us**，全部 256 页约需 200ms+

### 4.4 数据读取与转换

**寄存器布局**（从 0x0C 开始连续读取 12 字节）：

| 字节 | 内容 | 说明 |
|------|------|------|
| 0-1 | Accel X | little-endian int16 |
| 2-3 | Accel Y | little-endian int16 |
| 4-5 | Accel Z | little-endian int16 |
| 6-7 | Gyro X | little-endian int16 |
| 8-9 | Gyro Y | little-endian int16 |
| 10-11 | Gyro Z | little-endian int16 |

**转换公式**：

```c
// Accel (量程 ±16g, REG_ACC_RANGE=0x03)
float scale = 16.0f / 32768.0f;  // ≈ 0.000488 g/LSB

// Gyro (量程 ±2000 dps, REG_GYR_RANGE=0x00)
float scale = 2000.0f / 32768.0f;  // ≈ 0.061 dps/LSB

// 温度 (寄存器 0x22, 2字节)
// 实际驱动中常用简化公式：23.0 + (raw * 0.5f / 512.0f)
```

### 4.5 配置寄存器参考

| 寄存器 | 地址 | 常用值 | 含义 |
|--------|------|--------|------|
| ACC_CONF | 0x40 | 0x0A | ODR=200Hz, BWP=normal |
| ACC_RANGE | 0x41 | 0x03 | ±16g |
| GYR_CONF | 0x42 | 0x0A | ODR=200Hz |
| GYR_RANGE | 0x43 | 0x00 | ±2000 dps |

---

## 五、MAX30205 温度传感器专项

### 5.1 基本信息

| 参数 | 值 |
|------|-----|
| I2C 地址 | **0x48** ~ **0x4B**（由 A0/A1/A2 引脚接地/接 VCC 决定） |
| 默认地址 | **0x48**（三个地址引脚全部接地） |
| 精度 | ±0.1°C（典型值） |
| 分辨率 | 0.00390625°C（16-bit） |

### 5.2 温度读取

```python
import smbus
bus = smbus.SMBus(1)
data = bus.read_i2c_block_data(0x48, 0x00, 2)  # 从寄存器 0x00 读 2 字节
raw = (data[0] << 8) | data[1]
if raw > 0x7FFF:
    raw -= 0x10000
temp_c = raw / 256.0
```

**C 语言版本**：

```c
int fd = open("/dev/i2c-1", O_RDWR);
ioctl(fd, I2C_SLAVE, 0x48);
uint8_t reg = 0x00;
write(fd, &reg, 1);
uint8_t data[2];
read(fd, data, 2);
int16_t raw = (data[0] << 8) | data[1];
if (raw > 0x7FFF) raw -= 0x10000;
float temp = raw / 256.0f;
```

### 5.3 关键寄存器

| 寄存器 | 地址 | 说明 |
|--------|------|------|
| Temperature | 0x00 | 温度值（只读，2 字节） |
| Configuration | 0x01 | 配置寄存器 |
| THYST | 0x02 | 温度下限阈值 |
| TOS | 0x03 | 温度上限阈值（中断用） |

---

## 六、常见问题排查清单

### 6.1 I2C 设备扫描不到

| 检查项 | 方法 |
|--------|------|
| I2C 是否启用？ | `ls /dev/i2c-*` 应有 `/dev/i2c-1` |
| 设备是否上电？ | 万用表量 VCC/GND 之间是否有 3.3V |
| 地址是否正确？ | `sudo i2cdetect -y 1` 扫描总线 |
| 接线是否松动？ | SDA/SCL 是否反接？ |
| 上拉电阻？ | GPIO2/GPIO3 有板载上拉，其他 GPIO 需外接上拉或 gpiod 内部上拉 |
| 设备是否被占用？ | `lsof /dev/i2c-1` 检查是否有其他进程占用 |

### 6.2 BMI270 初始化失败

| 现象 | 原因 | 解决 |
|------|------|------|
| CHIP_ID = 0x00 | I2C 通信失败 | 检查接线、上拉、地址 |
| Config timeout | 8KB config 未正确写入 | 确保 burst write，检查每页延时 |
| Write failed at page N | I2C 写入中断 | 检查总线稳定性，减小每块大小 |
| INTERNAL_STATUS != 0x01 | Config 文件错误 | 使用 Bosch 官方提供的 config bin 文件 |
| 软复位后必须重新加载 config | 这是设计特性 | 每次 POR/软复位后都要走完整加载流程 |

### 6.3 GPIO Bit-Banging 问题

| 现象 | 原因 | 解决 |
|------|------|------|
| 设备偶尔 ACK 失败 | SDA 切换输出/输入时序不对 | 确保 SDA 在 SCL 低电平时切换 |
| 完全无响应 | 缺少上拉电阻 | gpiod 必须带 `BIAS_PULL_UP` 标志 |
| "Device or resource busy" | GPIO 被其他进程占用 | `sudo killall python3` 或释放 gpiod line |
| 速度太慢 | usleep 粒度大 | 树莓派 Linux 下 `usleep(10)` 实际约 60-100us |

### 6.4 Flask / Python 特定问题

| 现象 | 原因 | 解决 |
|------|------|------|
| `No module named 'bmi270'` | sudo 使用 root 的 Python path | 不用 sudo 运行 Flask，或设置 PYTHONPATH |
| gpiod 权限不足 | 用户不在 gpio 组 | `sudo usermod -aG gpio ubuntu` |
| SMBus monkey-patch 不生效 | 导入顺序问题 | 必须先 patch `sys.modules` 再 import BMI270 |

---

## 七、实战接线对照表

本项目实际接线（BMI270 + MAX30205 共存）：

| 传感器 | 信号 | BCM GPIO | 物理引脚 | 总线类型 |
|--------|------|----------|----------|----------|
| MAX30205 | SDA | GPIO2 | **Pin 3** | 标准 I2C-1 |
| MAX30205 | SCL | GPIO3 | **Pin 5** | 标准 I2C-1 |
| BMI270 | SDA | GPIO8 | **Pin 24** | 软件 I2C (gpiod) |
| BMI270 | SCL | GPIO9 | **Pin 21** | 软件 I2C (gpiod) |
| 共地 | GND | — | Pin 6/9/14/20/25/30/34/39 | — |
| 供电 | 3.3V | — | Pin 1/17 | — |

**注意**：GPIO8/9 同时也是 SPI0 的 CE0/MISO。如果同时使用 SPI 设备，需避免冲突。

---

## 八、性能优化建议

1. **块读取优先**：BMI270 的 accel+gyro 共 12 字节连续寄存器，用一次 `read_i2c_block_data(0x0C, 12)` 比 6 次单字节读取快 5 倍以上
2. **温度读取可降频**：BMI270 内部温度变化慢，不需要每帧都读
3. **C 语言不等于高性能**：如果瓶颈在 I2C 总线或 OS 调度，改用 C 提升有限
4. **如需 200Hz+**：BMI270 必须接标准 I2C-1（pin3/5），且用 C + 块读取
5. **config 只加载一次**：BMI270 初始化后不要重复加载 8KB config，耗时 200ms+

---

## 九、参考资源

- [Raspberry Pi 官方 GPIO 文档](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html)
- [pinout.xyz 交互式引脚图](https://pinout.xyz/)
- [BMI270 数据手册 (Bosch)](https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmi270-ds000.pdf)
- [BMI270 官方 GitHub 驱动](https://github.com/boschsensortec/BMI270-Sensor-API)
- [MAX30205 数据手册 (Analog Devices/Maxim)](https://www.analog.com/en/products/max30205.html)
- [libgpiod 文档](https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git/)
