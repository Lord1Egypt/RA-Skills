# -*- coding: utf-8 -*-
"""
拓安气体监测设备 - 配置文件

所有设备参数、通信配置、上报平台地址等集中管理
修改配置时无需改动业务代码
"""

# ==================== Modbus 通信参数 ====================
MODBUS_UART = 2              # UART 端口号 (UART1/UART2/UART3)
MODBUS_BAUDRATE = 9600       # 波特率
MODBUS_DATABITS = 8          # 数据位
MODBUS_PARITY = 0            # 校验位 (0=无校验，1=奇校验，2=偶校验)
MODBUS_STOPBIT = 1           # 停止位
MODBUS_FLOWCTL = 0           # 流控制 (0=无流控)

# ==================== 传感器设备参数 ====================
SENSOR_BASE_ADDR = 1000      # 传感器浓度数据起始地址
SENSOR_STAT_ADDR = 2000      # 传感器状态起始地址
SENSOR_MAX_COUNT = 32        # 最大传感器数量
BATTERY_STAT_ADDR = 0        # 电池状态地址
SENSOR_SLAVE_ADDR = 1        # Modbus 从站地址

# ==================== 数据上报平台 ====================
# 工厂 OTA 平台 (用于固件升级)
URL_OTA = "https://hu-wei-di-tu-a98abc-1258458441.ap-shanghai.app.tcloudbase.com/ota"

# 业务数据上报平台 (传感器数据)
URL_REPORT = "https://iot.tranthing.com/api/dataAnalysis/parseData-4G-industry-gas"

# ==================== 上报频率控制 ====================
REPORT_INTERVAL_SEC = 60     # 数据上报间隔 (秒)
NETWORK_CHECK_INTERVAL = 1   # 网络检查间隔 (小时)

# ==================== LED 指示灯引脚 ====================
LED_NET_PIN = 36             # 网络状态 LED 引脚 (GPIO36)
LED_MODBUS_PIN = 44          # Modbus 通信 LED 引脚 (GPIO44)

# ==================== 设备信息 ====================
MANUFACTURER_NAME = "天津安信华瑞"           # 厂商名称
TERMINAL_TYPE = "tuoan-gas"                  # 终端型号
PROJECT_NAME = "tuoan_demo_shenzhen"         # 项目名称
PROJECT_VERSION = "2026.3.26 tuoan-dingzhi"  # 项目版本
MANUFACTURER_ID = "18513099902"              # 厂商 ID (联系电话)
SAAS_VERSION = "20231213"                    # SaaS 平台版本

# ==================== 看门狗设置 ====================
WDT_TIMEOUT_MS = 320000      # 看门狗超时时间 (毫秒)，约 5.3 分钟

# ==================== 重试次数限制 ====================
MODBUS_RETRY_MAX = 5         # Modbus 通信最大重试次数
HTTP_RETRY_MAX = 2           # HTTP 上报最大重试次数
NETWORK_RETRY_MAX = 5        # 网络失败重试次数
SENSOR_SCAN_RETRY = 3        # 传感器扫描重试次数

# ==================== 调试开关 ====================
DEBUG_ENABLE = True          # 调试模式开关
DEBUG_MODBUS = False         # Modbus 调试开关
DEBUG_NETWORK = False        # 网络调试开关
DEBUG_HTTP = False           # HTTP 调试开关
