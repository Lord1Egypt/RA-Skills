# =============================================================================
# config.py — 项目全局配置
# 所有"重要参数"统一在此文件修改，其他文件只做 import，不硬编码数字/地址/URL
# =============================================================================

# ── 设备 / 厂商信息 ──────────────────────────────────────────────────────────
MANUFACTURER    = "天津安信华瑞科技有限公司"
TERMINAL_TYPE   = "JB-TB-AX100"
MANUFACTURER_ID = "18513099902"       # 厂商联系电话，用于平台鉴权
SAAS_VERSION    = "20230913"          # 对接平台的协议版本号
FW_VERSION      = "61.12"            # 固件版本号，上报给平台和OTA服务

# ── Modbus 串口参数 ──────────────────────────────────────────────────────────
MODBUS_UART     = 2        # UART 通道号（machine.UART.UART2）
MODBUS_BAUD     = 9600     # 波特率
MODBUS_BITS     = 8        # 数据位
MODBUS_PARITY   = 0        # 校验位：0=无
MODBUS_STOP     = 1        # 停止位
MODBUS_FLOW     = 0        # 流控：0=无
MODBUS_SLAVE    = 1        # 从机地址（默认 1）

# ── Modbus 寄存器地址（十进制） ───────────────────────────────────────────────
REG_SENSOR_LOGIN_CNT  = 0x0292   # 当前已登录探头数量
REG_MAX_LOGIN_CNT     = 0x0294   # 最大登录探头数量（上限256）
REG_SYS_STAT          = 0x0297   # 系统状态字
REG_CTL_STAT_BASE     = 0x0281   # 联动控制状态，连续5个寄存器
REG_FOREIGN_ALARM     = 0x029C   # 外部报警输入
REG_SENSOR_STAT_BASE  = 0x0101   # 探头状态寄存器起始地址（每探头2个寄存器）
REG_SENSOR_DENS_BASE  = 0x0102   # 探头浓度寄存器起始地址（每探头2个寄存器）
REG_WRITE_IMEI        = 1000     # 写IMEI到控制器的寄存器起始地址（8个寄存器）
REG_WRITE_IMSI        = 1009     # 写IMSI到控制器的寄存器起始地址（10个寄存器）
REG_WRITE_SIGNAL      = 1020     # 写信号强度到控制器的寄存器地址（1个寄存器）

# ── LED 引脚编号 ─────────────────────────────────────────────────────────────
LED_NET_PIN     = 36       # 网络状态 LED 引脚
LED_BUS_PIN     = 44       # Modbus 通信 LED 引脚

# ── 数据上报 URL ─────────────────────────────────────────────────────────────
URL_CLIENT = "https://iot.tranthing.com/api/dataAnalysis/parseData-4G-industry-gas"
URL_OTA    = "https://hu-wei-di-tu-a98abc-1258458441.ap-shanghai.app.tcloudbase.com/ota"

# ── 上报时间控制（分钟/秒） ───────────────────────────────────────────────────
REPORT_CYCLE_MIN   = 3     # 正常上报周期（每 N 分钟上报一次）
DATA_FRESH_SEC     = 70    # 数据新鲜度阈值（超过此秒数不上报，单位：秒）
MAX_FAIL_TIMES     = 15    # 连续上报失败超过此次数则重启

# ── 看门狗超时 ───────────────────────────────────────────────────────────────
WDT_TIMEOUT_SEC  = 600     # 看门狗超时时间（秒），超时未喂则自动重启

# ── 传感器固定参数（上报给平台的字段） ────────────────────────────────────────
SENSOR_TYPE       = 11     # 传感器类型编码
SENSOR_LOW_LIMIT  = 25     # 低报阈值（%LEL）
SENSOR_HIGH_LIMIT = 50     # 高报阈值（%LEL）
SENSOR_RANGE      = 100    # 量程（%LEL）
SENSOR_UNIT       = 1      # 浓度单位编码
SENSOR_POINT      = 1      # 小数位数

# ── 其他杂项 ─────────────────────────────────────────────────────────────────
BOOT_DELAY_SEC    = 20     # 开机等待（等模组初始化）
MODBUS_RETRY_MAX  = 5      # Modbus 读写最大重试次数
