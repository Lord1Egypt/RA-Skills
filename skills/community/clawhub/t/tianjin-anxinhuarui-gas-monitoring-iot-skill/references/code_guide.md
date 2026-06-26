# AX100 气体探测控制器上报程序 — 代码结构说明

## 概述

本套代码运行在移远通信（Quectel）QuecPython 物联网模组上（如 EC600N/EC600U 系列）。
设备通过 RS485/Modbus RTU 读取安信华瑞 AX100 系列气体报警控制器，将数据通过 4G HTTP 上报到客户平台。

---

## 文件职责划分

```
项目目录/
├── config.py     — 全部可调参数（地址/URL/周期/引脚），唯一需要修改的文件
├── LED.py        — LED 指示灯封装（亮/灭/闪），不需要修改
├── modbus.py     — Modbus RTU 底层驱动（收发/CRC），不需要修改
├── sensor.py     — AX100Controller 业务类（寄存器读写封装），一般不修改
└── main.py       — 主流程（初始化/循环/组包/上报/OTA），定制上报格式时修改
```

---

## config.py — 配置项说明（定制时只改这里）

### 设备/厂商信息
| 配置项 | 说明 | 示例 |
|--------|------|------|
| `MANUFACTURER` | 厂商名称，上报给平台 | `"天津安信华瑞科技有限公司"` |
| `TERMINAL_TYPE` | 终端型号 | `"JB-TB-AX100"` |
| `MANUFACTURER_ID` | 厂商ID/联系方式 | `"18513099902"` |
| `SAAS_VERSION` | 对接平台协议版本号 | `"20230913"` |
| `FW_VERSION` | 固件版本号 | `"61.12"` |

### 串口/Modbus 参数
| 配置项 | 说明 | 常用值 |
|--------|------|--------|
| `MODBUS_UART` | UART 通道号 | `2`（UART2） |
| `MODBUS_BAUD` | 波特率 | `9600` |
| `MODBUS_BITS` | 数据位 | `8` |
| `MODBUS_PARITY` | 校验位 | `0`=无, `1`=偶, `2`=奇 |
| `MODBUS_STOP` | 停止位 | `1` |
| `MODBUS_FLOW` | 流控 | `0`=无 |
| `MODBUS_SLAVE` | 从机地址 | `1` |

### 寄存器地址（十进制/十六进制）
| 配置项 | 默认地址 | 说明 |
|--------|----------|------|
| `REG_SENSOR_LOGIN_CNT` | `0x0292` | 当前已登录探头数量 |
| `REG_MAX_LOGIN_CNT` | `0x0294` | 最大登录探头数量上限 |
| `REG_SYS_STAT` | `0x0297` | 系统状态字（16bit） |
| `REG_CTL_STAT_BASE` | `0x0281` | 联动控制状态（连续5个寄存器） |
| `REG_FOREIGN_ALARM` | `0x029C` | 外部报警输入 |
| `REG_SENSOR_STAT_BASE` | `0x0101` | 探头状态起始地址（每探头2个寄存器） |
| `REG_SENSOR_DENS_BASE` | `0x0102` | 探头浓度起始地址（每探头2个寄存器） |
| `REG_WRITE_IMEI` | `1000` | 写IMEI到控制器（8个寄存器） |
| `REG_WRITE_IMSI` | `1009` | 写IMSI到控制器（10个寄存器） |
| `REG_WRITE_SIGNAL` | `1020` | 写信号强度到控制器（1个寄存器） |

### LED 引脚
| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `LED_NET_PIN` | `36` | 网络状态指示灯引脚 |
| `LED_BUS_PIN` | `44` | Modbus通信指示灯引脚 |

### 上报 URL（最常修改）
| 配置项 | 说明 |
|--------|------|
| `URL_CLIENT` | 数据上报地址（客户平台接收接口） |
| `URL_OTA` | OTA升级检查地址（可选，无OTA需求可保留空字符串） |

### 时间/周期控制
| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `REPORT_CYCLE_MIN` | `3` | 正常上报周期（分钟） |
| `DATA_FRESH_SEC` | `70` | 数据新鲜度阈值（超过此秒数不上报） |
| `MAX_FAIL_TIMES` | `15` | 连续失败超过此次数自动重启 |
| `WDT_TIMEOUT_SEC` | `600` | 看门狗超时（秒），建议不小于上报周期×2 |
| `BOOT_DELAY_SEC` | `20` | 开机延时（秒），等待模组初始化 |

### 传感器上报参数（协议字段）
| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `SENSOR_TYPE` | `11` | 传感器类型编码（平台协议约定） |
| `SENSOR_LOW_LIMIT` | `25` | 低报阈值（%LEL） |
| `SENSOR_HIGH_LIMIT` | `50` | 高报阈值（%LEL） |
| `SENSOR_RANGE` | `100` | 量程 |
| `SENSOR_UNIT` | `1` | 浓度单位编码 |
| `SENSOR_POINT` | `1` | 小数位数 |

---

## main.py — 上报数据包格式

`build_payload()` 函数组装的 JSON 结构（可按客户平台协议调整）：

```json
{
  "type": 2,
  "device_id": "后12位IMEI",
  "device_information": {
    "ccid": "SIM卡ICCID",
    "imei": "完整IMEI",
    "moduleType": 4,
    "programVersion": "固件版本号"
  },
  "device_operation": {
    "signal": 18,
    "state": 2
  },
  "real_time_data": {
    "cycle": 1,
    "cycle_unit": 2,
    "detector": [
      {
        "detector_number": 1,
        "sensor": [{
          "number": 1,
          "sensorType": 11,
          "sensorCon": 0.0,
          "lowerLimit": 25,
          "upperLimit": 50,
          "rangeValue": 100,
          "sensorUnit": 1,
          "sensorPoint": 1,
          "state": 2
        }]
      }
    ],
    "io": []
  },
  "mqtt": 0
}
```

### 整机状态码（device_operation.state）
| 状态码 | 含义 |
|--------|------|
| `0x02` | 正常 |
| `0x08` | 无探头/通信故障 |
| `0x11` | 主电故障或备电工作 |
| `0x12` | 备电故障/欠压 |
| `0x13` | 传感器故障 |
| `0x14` | 二级报警 |
| `0x15` | 一级报警 |

### 探头状态码（sensor[].state）
| 状态码 | 含义 |
|--------|------|
| `2` | 正常 |
| `3` | 一级报警 |
| `4` | 二级报警 |
| `5` | 通信故障或屏蔽 |
| `13` | 传感器故障 |

---

## 定制步骤（快速上手）

1. **复制模板代码**到设备项目目录（通常为 `usr/` 下）
2. **只修改 `config.py`**：
   - 改 `URL_CLIENT` 为客户平台接收地址
   - 改 `REPORT_CYCLE_MIN` 为约定的上报频率（分钟）
   - 改 `MANUFACTURER`、`TERMINAL_TYPE` 等设备标识
   - 如寄存器地址与控制器实际不符，修改对应 `REG_*` 常量
3. **如客户平台 JSON 格式不同**，修改 `main.py` 中 `build_payload()` 函数
4. **上传到模组**：使用 QPYcom 工具将所有 `.py` 文件上传到 `/usr/` 目录，运行 `main.py`

---

## QuecPython 开发注意事项

- 所有自定义模块必须放在 `/usr/` 目录，import 时用 `from usr.xxx import ...`
- 串口号对应关系：UART0=调试口, UART1=蓝牙, UART2=主串口（RS485常用此口）
- `machine.Pin` GPIO 编号与实际硬件引脚对应关系以具体模组手册为准
- `WDT` 看门狗一旦启动不能关闭，必须定期调用 `.feed()` 否则自动重启
- QuecPython 使用 MicroPython，标准库有裁剪，`math.pow()` 返回 float，注意与 `**` 的区别
- `request` 模块为流式读取，`response.text` 需要迭代读取，不能直接 `response.text[0]`
