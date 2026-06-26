# =============================================================================
# sensor.py — AX100 气体探测控制器 业务读取类
# 封装所有与控制器交互的寄存器操作，返回结构化数据供 main.py 使用
# =============================================================================

import math
import utime
from usr.config import (
    MODBUS_SLAVE,
    REG_SENSOR_LOGIN_CNT, REG_MAX_LOGIN_CNT,
    REG_SYS_STAT, REG_CTL_STAT_BASE, REG_FOREIGN_ALARM,
    REG_SENSOR_STAT_BASE, REG_SENSOR_DENS_BASE,
    REG_WRITE_IMEI, REG_WRITE_IMSI, REG_WRITE_SIGNAL,
    MODBUS_RETRY_MAX,
)


# ── 工具函数 ──────────────────────────────────────────────────────────────────

def _hex_list_to_int(hex_list):
    """把十六进制字符串列表拼接后转成整数，例如 ['00', 'FF'] → 255。"""
    return int("0x" + "".join(hex_list), 16)


def _hex_list_to_bits(hex_list):
    """
    把十六进制字符串列表展开成 bit 列表（高位在前）。
    例如 ['01', 'A0'] → 16 个 0/1 的列表。
    """
    bits = []
    for h in hex_list:
        val = int("0x" + h, 16)
        for j in range(7, -1, -1):               # 高位先出
            bits.append(1 if (val >> j) & 1 else 0)
    return bits


def _str_to_byte_pairs(s):
    """
    把字符串转成每两个字符一组的字节列表（用于写 ASCII 字符串到寄存器）。
    例如 "ABCDE" → [65, 66, 67, 68, 69, 0]
    奇数长度末尾补 0x00。
    """
    codes = [ord(c) for c in s]
    if len(codes) % 2 != 0:
        codes.append(0)
    return codes


# ── 主类 ──────────────────────────────────────────────────────────────────────

class AX100Controller:
    """
    AX100 气体报警控制器 Modbus 读写封装。

    使用方式:
        bus = ModbusRTU(...)        # 来自 modbus.py
        ctrl = AX100Controller(bus, led_bus)
        count = ctrl.read_max_count()
        stats = ctrl.read_sensor_stat(count)
    """

    def __init__(self, bus, led_bus):
        """
        参数:
            bus     : ModbusRTU 实例（来自 modbus.py）
            led_bus : LED 实例，用于通信状态指示
        """
        self.bus     = bus
        self.led_bus = led_bus
        self.slave   = MODBUS_SLAVE

    # ── 内部重试读 ────────────────────────────────────────────────────────────

    def _read(self, addr, count, retry=0):
        """
        带重试的寄存器读取。
        返回十六进制字符串列表，失败则返回空列表。
        """
        result = self.bus.read_regs(self.slave, addr, count)
        if result["ok"] and len(result["data"]) >= count * 2:
            self.led_bus.on()
            return result["data"]

        # 读取失败
        self.led_bus.off()
        if retry < MODBUS_RETRY_MAX:
            utime.sleep_ms(300)
            return self._read(addr, count, retry + 1)

        print("[Sensor] 寄存器 0x{:04X} 读取失败，已重试 {} 次".format(addr, MODBUS_RETRY_MAX))
        return []

    # ── 公开读取接口 ──────────────────────────────────────────────────────────

    def read_max_count(self):
        """
        读取控制器允许的最大探头登录数量（寄存器 0x0294）。
        返回: 1~256 之间的整数；读失败或超界时返回 1（保底）。
        """
        data = self._read(REG_MAX_LOGIN_CNT, 1)
        if not data:
            return 1

        count = _hex_list_to_int(data)
        if count < 1 or count > 256:
            print("[Sensor] 最大探头数量异常:", count, "，使用保底值 1")
            return 1

        print("[Sensor] 最大探头数量:", count)
        return count

    def read_login_count(self):
        """
        读取当前已登录的探头数量（寄存器 0x0292）。
        返回: 整数；失败返回 0。
        """
        data = self._read(REG_SENSOR_LOGIN_CNT, 1)
        if not data:
            return 0
        return _hex_list_to_int(data)

    def read_sys_stat(self):
        """
        读取系统状态字（寄存器 0x0297，1个寄存器=2字节=16bit）。

        返回字典，key 为状态名称，value 为 0 或 1：
            back_power_on    : 备电工作中
            back_power_low   : 备电欠压
            back_power_fail  : 备电故障
            main_power_fail  : 主电故障
            has_blind        : 有屏蔽探头
            has_union        : 有联动
            has_level_1_alarm: 有一级报警
            has_level_2_alarm: 有二级报警
            has_fail         : 有故障
        失败时各字段返回 -1。
        """
        default = {k: -1 for k in [
            "back_power_on", "back_power_low", "back_power_fail", "main_power_fail",
            "has_blind", "has_union", "has_level_1_alarm", "has_level_2_alarm", "has_fail"
        ]}

        data = self._read(REG_SYS_STAT, 1)
        if not data:
            return default

        bits = _hex_list_to_bits(data)
        # 位映射（高位在前，bit[0]=最高位）：
        # bit[4]=备电工作, [5]=备电欠压, [6]=备电故障, [7]=主电故障
        # bit[9]=有屏蔽,  [10]=有联动,  [11]=有二级报警, [12]=有一级报警, [13]=有故障
        print("[Sensor] 系统状态位列表:", bits)
        return {
            "back_power_on"   : bits[4],
            "back_power_low"  : bits[5],
            "back_power_fail" : bits[6],
            "main_power_fail" : bits[7],
            "has_blind"       : bits[9],
            "has_union"       : bits[10],
            "has_level_2_alarm": bits[11],
            "has_level_1_alarm": bits[12],
            "has_fail"        : bits[13],
        }

    def read_ctl_stat(self):
        """
        读取联动控制状态（寄存器 0x0281，连续5个寄存器）。
        只取每个字节的 bit[1]（次高位）。

        返回字典：
            wind_union_ctl      : 风机联动
            ac220_no_val        : AC220 常开阀联动
            low_alarm_union     : 低报联动
            high_alarm_union    : 高报联动
            dc24_no_val         : DC24 常开阀联动
        失败时各字段返回 -1。
        """
        default = {k: -1 for k in [
            "wind_union_ctl", "ac220_no_val", "low_alarm_union",
            "high_alarm_union", "dc24_no_val"
        ]}

        data = self._read(REG_CTL_STAT_BASE, 5)
        if not data:
            return default

        keys = ["wind_union_ctl", "ac220_no_val", "low_alarm_union", "high_alarm_union", "dc24_no_val"]
        result = {}
        for i, key in enumerate(keys):
            bits = _hex_list_to_bits([data[i]])
            result[key] = bits[1]    # 取 bit[1]（次高位）

        return result

    def read_foreign_alarm(self):
        """
        读取外部报警输入（寄存器 0x029C，1个寄存器）。
        返回: 0=无报警, 1=有报警；失败返回 0。
        """
        data = self._read(REG_FOREIGN_ALARM, 1)
        if not data:
            return 0

        val = _hex_list_to_int(data)
        if val > 256:
            print("[Sensor] 外部报警值异常:", val)
            return 0
        return val

    def read_sensor_stat(self, count):
        """
        逐个读取 count 个探头的状态寄存器。

        返回列表，每个元素为字典：
            sensor_index  : 探头索引（0 开始）
            sensor_addr   : Modbus 寄存器地址
            is_blind      : 是否屏蔽（1=屏蔽）
            alarm_1       : 一级报警（1=报警）
            alarm_2       : 二级报警（1=报警）
            com_err       : 通信故障（1=故障）
            sensor_fail   : 传感器故障（1=故障）
        """
        results = []
        for i in range(count):
            addr = REG_SENSOR_STAT_BASE + i * 2
            data = self._read(addr, 1)

            if not data or len(data) < 2:
                print("[Sensor] 探头 {} 状态读取失败，跳过".format(i))
                continue

            bits = _hex_list_to_bits(data)
            # 位映射（高位在前）：
            # bits[6]=二级报警, bits[7]=一级报警, bits[8]=屏蔽
            # bits[3]=通信故障, bits[4]=传感器故障
            results.append({
                "sensor_index": i,
                "sensor_addr" : addr,
                "is_blind"    : bits[8],
                "alarm_1"     : bits[7],
                "alarm_2"     : bits[6],
                "com_err"     : bits[3],
                "sensor_fail" : bits[4],
            })
            print("[Sensor] 探头 {} 状态:".format(i), results[-1])

        return results

    def read_sensor_dens(self, count):
        """
        逐个读取 count 个探头的浓度寄存器。

        返回列表，每个元素为字典：
            sensor_index : 探头索引
            sensor_addr  : Modbus 寄存器地址（浓度）
            density      : 浓度值（float，单位 %LEL，精度 0.1）
        """
        results = []
        for i in range(count):
            addr = REG_SENSOR_DENS_BASE + i * 2
            data = self._read(addr, 1)

            if not data or len(data) < 2:
                print("[Sensor] 探头 {} 浓度读取失败，跳过".format(i))
                continue

            raw = _hex_list_to_int(data)
            density = round(raw / 10.0, 1)
            results.append({
                "sensor_index": i,
                "sensor_addr" : addr,
                "density"     : density,
            })

        return results

    def write_device_info(self, imei, imsi, signal):
        """
        把 IMEI、IMSI、信号强度写入控制器寄存器（供控制器本地显示）。

        参数:
            imei   : IMEI 字符串（15位数字）
            imsi   : IMSI 字符串（15位数字）
            signal : 信号强度整数（CSQ 值）
        """
        self.bus.write_regs(self.slave, REG_WRITE_IMEI,   _str_to_byte_pairs(imei))
        self.bus.write_regs(self.slave, REG_WRITE_IMSI,   _str_to_byte_pairs(imsi))
        self.bus.write_regs(self.slave, REG_WRITE_SIGNAL, _str_to_byte_pairs(str(signal)))
        print("[Sensor] 设备信息已写入控制器寄存器")
