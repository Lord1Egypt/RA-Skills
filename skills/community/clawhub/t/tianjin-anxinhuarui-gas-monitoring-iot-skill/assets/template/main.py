# =============================================================================
# main.py — 主程序入口
# 职责：初始化 → 网络连接 → 循环读取传感器 → HTTP 上报 → OTA 检查 → 喂看门狗
# =============================================================================

from machine import UART, WDT
from misc import Power
import gc
import utime
import ujson
import request
import modem
import checkNet
import sim
import net
import app_fota

from usr.config import (
    MANUFACTURER, TERMINAL_TYPE, MANUFACTURER_ID, SAAS_VERSION, FW_VERSION,
    MODBUS_UART, MODBUS_BAUD, MODBUS_BITS, MODBUS_PARITY, MODBUS_STOP, MODBUS_FLOW,
    LED_NET_PIN, LED_BUS_PIN,
    URL_CLIENT, URL_OTA,
    REPORT_CYCLE_MIN, DATA_FRESH_SEC, MAX_FAIL_TIMES,
    WDT_TIMEOUT_SEC, BOOT_DELAY_SEC,
    SENSOR_TYPE, SENSOR_LOW_LIMIT, SENSOR_HIGH_LIMIT, SENSOR_RANGE, SENSOR_UNIT, SENSOR_POINT,
)
from usr.LED import LED
from usr.modbus import ModbusRTU
from usr.sensor import AX100Controller


# ── 开机延时（等待模组初始化完成） ────────────────────────────────────────────
utime.sleep(BOOT_DELAY_SEC)


# ── 版本信息 ──────────────────────────────────────────────────────────────────
PROJECT_NAME    = "Tianjin Anxin Huarui Technology"
PROJECT_VERSION = FW_VERSION + " anxin shenzhen"


# ── 硬件初始化 ────────────────────────────────────────────────────────────────
led_net = LED(LED_NET_PIN)          # 网络状态指示灯
led_bus = LED(LED_BUS_PIN)          # Modbus 通信指示灯
wdt     = WDT(WDT_TIMEOUT_SEC)     # 看门狗，超时自动重启

bus     = ModbusRTU(MODBUS_UART, MODBUS_BAUD, MODBUS_BITS, MODBUS_PARITY, MODBUS_STOP, MODBUS_FLOW)
ctrl    = AX100Controller(bus, led_bus)  # 气体控制器业务类

checknet = checkNet.CheckNetwork(PROJECT_NAME, PROJECT_VERSION)


# ── 全局运行状态 ──────────────────────────────────────────────────────────────
report_fail_cnt    = 0    # 连续上报失败次数，超过阈值重启
max_sensor_count   = 0    # 最大探头登录数量（开机读一次）
last_payload       = None # 上次组好的上报包（dict）
last_payload_ts    = 0    # 上次组包的时间戳（秒）
cell_info          = {}   # 网络 / SIM 信息


# =============================================================================
# 工具函数
# =============================================================================

def feed_dog():
    """喂看门狗，并打印当前时间（方便日志定位）。"""
    print("[WDT] 喂狗", utime.localtime())
    wdt.feed()


def led_flash(led, on_sec, off_sec, times):
    """
    让指定 LED 闪烁。

    参数:
        led    : LED 实例
        on_sec : 亮灯时长（秒）
        off_sec: 灭灯时长（秒）
        times  : 闪烁次数
    """
    for _ in range(times):
        led.on()
        utime.sleep(on_sec)
        led.off()
        utime.sleep(off_sec)


# =============================================================================
# 网络功能
# =============================================================================

def get_signal():
    """
    获取当前 LTE 信号参数。
    返回字典：{"sinr": int, "rsrp": int}；取不到则返回 0。
    """
    info = {"sinr": 0, "rsrp": 0}
    for item in net.getSignal(1):
        if len(item) == 5 and item[0] != 99:
            return {"sinr": item[3], "rsrp": item[1]}
    return info


def get_cell_id():
    """从 getCellInfo 中提取第一个有效小区 ID，取不到返回 0。"""
    for group in net.getCellInfo():
        for cell in group:
            if cell:
                return cell[1]
    return 0


def check_network():
    """
    等待网络就绪（最多 30 秒），并收集 SIM/信号信息。

    返回: 包含信号/IMEI/IMSI 等字段的字典；网络不通则返回 None。
    """
    stage, state = checknet.wait_network_connected(30)
    sim_status   = sim.getStatus()

    if stage == 3 and state == 1 and sim_status == 1:
        checknet.poweron_print_once()
        print("[Net] 网络连接成功")
        led_net.on()

        sig = get_signal()
        return {
            "signal"   : net.csqQueryPoll(),      # CSQ 信号强度
            "cell_id"  : get_cell_id(),            # 小区 ID
            "pci"      : net.getServingCi(),       # 物理小区标识
            "sinr"     : sig["sinr"],              # SINR
            "rsrp"     : sig["rsrp"],              # RSRP
            "IMEI"     : modem.getDevImei(),       # IMEI
            "IMSI"     : sim.getImsi(),            # IMSI
            "ccid"     : sim.getIccid(),           # SIM ICCID
            "manu"     : MANUFACTURER,
            "product"  : TERMINAL_TYPE,
            "manu_id"  : MANUFACTURER_ID,
            "saas_ver" : SAAS_VERSION,
        }
    else:
        print("[Net] 网络连接失败 stage={} state={} sim={}".format(stage, state, sim_status))
        led_net.off()
        led_flash(led_net, 0.1, 0.1, 5)
        utime.sleep(10)
        return None


# =============================================================================
# 数据组包
# =============================================================================

# 探头状态码映射（用于 state 字段）
STATE_NORMAL   = 2    # 正常
STATE_ALARM_1  = 3    # 一级报警
STATE_ALARM_2  = 4    # 二级报警
STATE_COM_ERR  = 5    # 通信/屏蔽
STATE_FAIL     = 13   # 传感器故障

# 主机整机状态码
MAIN_STATE_NORMAL       = 0x02
MAIN_STATE_NO_SENSOR    = 0x08
MAIN_STATE_POWER_ERR    = 0x11
MAIN_STATE_BACK_PWR_ERR = 0x12
MAIN_STATE_SENSOR_FAIL  = 0x13
MAIN_STATE_ALARM_2      = 0x14
MAIN_STATE_ALARM_1      = 0x15


def _calc_main_state(sys_stat, sensor_stats):
    """
    根据系统状态字和探头列表，计算整机上报 state。
    优先级：主电故障 > 备电故障/欠压 > 二级报警 > 一级报警 > 传感器故障 > 通信故障 > 正常。
    """
    if max_sensor_count == 0:
        return MAIN_STATE_NO_SENSOR

    state = MAIN_STATE_NORMAL
    if sys_stat["main_power_fail"] == 1 or sys_stat["back_power_on"] == 1:
        state = MAIN_STATE_POWER_ERR
    elif sys_stat["back_power_fail"] == 1 or sys_stat["back_power_low"] == 1:
        state = MAIN_STATE_BACK_PWR_ERR
    elif sys_stat["has_level_2_alarm"] == 1:
        state = MAIN_STATE_ALARM_2
    elif sys_stat["has_level_1_alarm"] == 1:
        state = MAIN_STATE_ALARM_1

    # 根据探头状态进一步更新（探头状态优先级高于系统字）
    for s in sensor_stats:
        if s["alarm_2"] == 1:
            state = MAIN_STATE_ALARM_2
            break
        elif s["alarm_1"] == 1 and state not in [MAIN_STATE_ALARM_2]:
            state = MAIN_STATE_ALARM_1
        elif s["com_err"] == 1 and state not in [MAIN_STATE_ALARM_2, MAIN_STATE_ALARM_1, MAIN_STATE_NO_SENSOR]:
            state = MAIN_STATE_NO_SENSOR
        elif s["sensor_fail"] == 1 and state not in [MAIN_STATE_ALARM_2, MAIN_STATE_ALARM_1, MAIN_STATE_SENSOR_FAIL]:
            state = MAIN_STATE_SENSOR_FAIL

    return state


def build_payload(sensor_stats, sensor_dens, sys_stat, foreign_alarm):
    """
    把所有读取到的数据组装成符合深圳平台协议的上报包（dict）。

    参数:
        sensor_stats  : read_sensor_stat 返回的列表
        sensor_dens   : read_sensor_dens 返回的列表
        sys_stat      : read_sys_stat 返回的字典
        foreign_alarm : 外部报警输入（0/1）

    返回: 上报包 dict，可直接 ujson.dumps。
    """
    main_state = _calc_main_state(sys_stat, sensor_stats)

    # 构建探头列表
    detectors = []
    # 浓度按地址建立快速查找表
    dens_map = {d["sensor_addr"]: d["density"] for d in sensor_dens}

    for s in sensor_stats:
        # 计算单个探头状态码
        if s["alarm_2"] == 1:
            det_state = STATE_ALARM_2
        elif s["alarm_1"] == 1:
            det_state = STATE_ALARM_1
        elif s["com_err"] == 1 or s["is_blind"] == 1:
            det_state = STATE_COM_ERR
        elif s["sensor_fail"] == 1:
            det_state = STATE_FAIL
        else:
            det_state = STATE_NORMAL

        # 浓度寄存器地址 = 状态寄存器地址 + 1
        density = dens_map.get(s["sensor_addr"] + 1, 0.0)

        detectors.append({
            "detector_number": s["sensor_index"] + 1,   # 探头编号从 1 开始
            "sensor": [{
                "number"     : 1,
                "sensorType" : SENSOR_TYPE,
                "sensorCon"  : density,
                "lowerLimit" : SENSOR_LOW_LIMIT,
                "upperLimit" : SENSOR_HIGH_LIMIT,
                "rangeValue" : SENSOR_RANGE,
                "sensorUnit" : SENSOR_UNIT,
                "sensorPoint": SENSOR_POINT,
                "state"      : det_state,
            }],
        })

    # 外部报警：作为第 256 号虚拟探头上报（仅在有报警时追加）
    if foreign_alarm == 1:
        detectors.append({
            "detector_number": 256,
            "sensor": [{
                "number"     : 1,
                "sensorType" : SENSOR_TYPE,
                "sensorCon"  : 0,
                "lowerLimit" : SENSOR_LOW_LIMIT,
                "upperLimit" : SENSOR_HIGH_LIMIT,
                "rangeValue" : SENSOR_RANGE,
                "sensorUnit" : SENSOR_UNIT,
                "sensorPoint": SENSOR_POINT,
                "state"      : STATE_ALARM_2,
            }],
        })

    payload = {
        "type"      : 2,
        "device_id" : cell_info["IMEI"][-12:],      # 取 IMEI 末 12 位作设备 ID
        "device_information": {
            "ccid"          : cell_info["ccid"],
            "imei"          : cell_info["IMEI"],
            "moduleType"    : 4,
            "programVersion": FW_VERSION,
        },
        "device_operation": {
            "signal": cell_info["signal"],
            "state" : main_state,
        },
        "real_time_data": {
            "cycle"     : 1,
            "cycle_unit": 2,
            "detector"  : detectors,
            "io"        : [],
        },
        "mqtt": 0,
    }
    return payload


# =============================================================================
# HTTP 上报
# =============================================================================

def http_post(url, body_dict, tag=""):
    """
    向指定 URL POST JSON 数据。
    会先检查数据新鲜度，超时（DATA_FRESH_SEC）则不上报。

    参数:
        url       : 请求地址
        body_dict : 要发送的字典（内部转换为 JSON 字符串）
        tag       : 日志标签，用于区分 client/ota

    返回: True=成功, False=失败
    """
    global report_fail_cnt

    now_ts = utime.mktime(utime.localtime())
    age    = now_ts - last_payload_ts
    print("[HTTP] 数据新鲜度: {}s (阈值 {}s)".format(age, DATA_FRESH_SEC))

    if age >= DATA_FRESH_SEC:
        print("[HTTP] 数据过期，跳过上报")
        return False

    headers = {"Content-Type": "application/json"}
    body    = ujson.dumps(body_dict)

    led_net.off()
    try:
        resp = request.post(url, data=body, headers=headers)
        print("[HTTP][{}] 状态码: {}".format(tag, resp.status_code))

        if resp.status_code != 200:
            led_flash(led_net, 0.1, 0.1, 3)
            report_fail_cnt += 1
            return False

        # 成功
        led_flash(led_net, 0.25, 0.25, 4)
        led_net.on()
        report_fail_cnt = 0

        # 解析响应（流式读取）
        for chunk in resp.text:
            try:
                ret = ujson.loads(chunk)
                print("[HTTP][{}] 响应:".format(tag), ret)
                # OTA 升级检测
                if tag == "ota" and ret.get("code") == 200:
                    file_list = ret.get("file_list", [])
                    if file_list:
                        _run_ota(file_list)
            except:
                pass

        return True

    except Exception as e:
        print("[HTTP][{}] 请求异常:".format(tag), e)
        report_fail_cnt += 1
        return False


# =============================================================================
# OTA 升级
# =============================================================================

def _run_ota(file_list):
    """下载文件列表并触发 OTA 重启。"""
    print("[OTA] 开始升级，文件列表:", file_list)
    try:
        fota = app_fota.new()
        fota.bulk_download(file_list)
        fota.set_update_flag()
        Power.powerRestart()
    except Exception as e:
        print("[OTA] 升级失败:", e)


def check_ota():
    """
    向 OTA 服务上报当前版本信息，服务端决定是否下发升级包。
    """
    now = utime.localtime()
    ota_body = {
        "time"     : "{}-{}-{} {}:{}:{}".format(*now[:6]),
        "ts"       : utime.mktime(now),
        "imei"     : cell_info.get("IMEI", ""),
        "imsi"     : cell_info.get("IMSI", ""),
        "manu"     : MANUFACTURER,
        "product"  : TERMINAL_TYPE,
        "project"  : PROJECT_NAME,
        "softver"  : PROJECT_VERSION,
        "http_body": last_payload,
    }
    print("[OTA] 检查 OTA 更新...")
    http_post(URL_OTA, ota_body, tag="ota")


# =============================================================================
# 主流程
# =============================================================================

def init():
    """初始化：网络连接、读取最大探头数、写设备信息到控制器。"""
    global cell_info, max_sensor_count, last_payload_ts

    cell_info = check_network()
    if not cell_info:
        print("[Main] 网络初始化失败，将在循环中重试")
        cell_info = {}

    gc.enable()    # 开启自动垃圾回收

    # 首次读取最大探头数（读不到则保底 1）
    max_sensor_count = ctrl.read_max_count()

    # 把 IMEI/IMSI/信号写入控制器（供控制器本地显示）
    if cell_info:
        ctrl.write_device_info(
            cell_info.get("IMEI", ""),
            cell_info.get("IMSI", ""),
            cell_info.get("signal", 0),
        )

    # 触发一次 OTA 检查（为了让 OTA 数据有新鲜度，临时更新时间戳）
    last_payload_ts = utime.mktime(utime.localtime())
    check_ota()

    utime.sleep(3)


def loop():
    """主循环：每 10 秒跑一次，按分钟控制读 modbus 和上报。"""
    global last_payload, last_payload_ts, report_fail_cnt
    global max_sensor_count, cell_info

    # 用 IMEI 末4位做偏移，避免所有设备同时上报（错峰）
    imei_offset   = int(cell_info.get("IMEI", "0000")[-4:]) if cell_info else 0

    last_modbus_min = -1    # 上次读 modbus 的分钟
    last_report_min = -1    # 上次成功上报的分钟
    last_ota_day    = -1    # 上次检查 OTA 的日期

    while True:
        now    = utime.localtime()
        now_ts = utime.mktime(now)
        minute = now[4]
        day    = now[2]

        feed_dog()

        # ── 每天按偏移时间检查一次 OTA + 刷新网络信息 ─────────────────────────
        if last_ota_day != day and (now_ts % 10000) > imei_offset:
            print("[Main] 每日 OTA 检查")
            cell_info    = check_network() or cell_info
            last_ota_day = day
            check_ota()

        # ── 每分钟读一次 Modbus（分钟变化时触发） ─────────────────────────────
        if last_modbus_min != minute:
            print("[Main] 读取 Modbus 数据，分钟:", minute)

            # 最大探头数如果还是 0 或 1，尝试重新读一次
            if max_sensor_count < 2:
                max_sensor_count = ctrl.read_max_count()

            # 读传感器状态与浓度
            sensor_stats  = ctrl.read_sensor_stat(max_sensor_count)
            sensor_dens   = ctrl.read_sensor_dens(max_sensor_count)
            sys_stat      = ctrl.read_sys_stat()
            foreign_alarm = ctrl.read_foreign_alarm()

            # 同步写设备信息到控制器
            if cell_info:
                ctrl.write_device_info(
                    cell_info.get("IMEI", ""),
                    cell_info.get("IMSI", ""),
                    cell_info.get("signal", 0),
                )

            # 组包
            last_payload    = build_payload(sensor_stats, sensor_dens, sys_stat, foreign_alarm)
            last_payload_ts = now_ts
            last_modbus_min = minute

            print("[Main] 数据包已组好:", ujson.dumps(last_payload))

            # 垃圾回收（读完传感器后释放临时对象）
            gc.collect()

            # ── 上报判断：每 REPORT_CYCLE_MIN 分钟上报，或有报警时立即上报 ──
            has_alarm = last_payload["device_operation"]["state"] != MAIN_STATE_NORMAL
            due_report = (minute % REPORT_CYCLE_MIN == 0)

            if due_report or has_alarm:
                ok = http_post(URL_CLIENT, last_payload, tag="client")
                if ok:
                    last_report_min = minute
                else:
                    # 失败一次自动重试
                    print("[Main] 上报失败，重试一次")
                    http_post(URL_CLIENT, last_payload, tag="client")

                # 连续失败过多，重启
                if report_fail_cnt > MAX_FAIL_TIMES:
                    print("[Main] 连续上报失败 {} 次，重启".format(report_fail_cnt))
                    utime.sleep(5)
                    Power.powerRestart()

        utime.sleep(10)   # 主循环间隔 10 秒


# =============================================================================
# 入口
# =============================================================================

if __name__ == "__main__":
    init()
    loop()
