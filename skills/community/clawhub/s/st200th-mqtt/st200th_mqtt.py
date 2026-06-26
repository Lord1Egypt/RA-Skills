#!/usr/bin/env python3
"""
ST200TH 温湿度变送器 MQTT 全功能查询与管理工具
基于立控 MQTT 协议文档: https://docv2.likong-iot.com/products/transmitters/ST200TH/mqtt

子命令:
    query       查询传感器数据（温度、湿度、气压、海拔）及系统信息
    customize   查询设备当前配置（MQTT/TCP/HTTP参数）
    compensate  设置传感器补偿参数
    restart     重启设备
    reset       恢复出厂设置
    ota         OTA固件升级
    custom      修改设备协议配置（MQTT/TCP/HTTP）
    add         添加设备到本地列表
    remove      从本地列表删除设备
    list        列出本地已保存的设备
"""

import os
import sys
import json
import uuid
import time
import argparse
import threading
from pathlib import Path

try:
    import paho.mqtt.client as mqtt
except ImportError:
    print(json.dumps({
        "success": False,
        "error": "缺少依赖 paho-mqtt，请执行: pip3 install paho-mqtt"
    }, ensure_ascii=False))
    sys.exit(1)

# ── MQTT 连接配置 ──────────────────────────────────────────────
MQTT_BROKER = "mqtt.likong-iot.com"
MQTT_PORT = 1883
MQTT_USERNAME = "public"
MQTT_PASSWORD = "Aa123456"
TIMEOUT_SECONDS = 10

# 设备列表持久化（与脚本同目录）
CONFIG_FILE = Path(__file__).parent / "devices.json"


# ══════════════════════════════════════════════════════════════
#  设备列表管理
# ══════════════════════════════════════════════════════════════

def load_devices() -> dict:
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_devices(devices: dict):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(devices, f, indent=2, ensure_ascii=False)


def normalize_mac(mac: str) -> str:
    return mac.lower().replace(":", "").replace("-", "").strip()


def validate_mac(mac: str) -> bool:
    return len(mac) == 12 and all(c in "0123456789abcdef" for c in mac)


def resolve_mac(mac_arg, query_all=False):
    """根据参数和已保存设备解析出要操作的 MAC 列表。失败时返回 error dict。"""
    devices = load_devices()

    if mac_arg:
        mac = normalize_mac(mac_arg)
        if not validate_mac(mac):
            return {"success": False, "error": f"MAC 地址格式无效: {mac}（需要12位十六进制字符）"}
        return [mac]

    if query_all:
        if not devices:
            return {"success": False, "error": "暂无已保存的设备。请先添加: python3 st200th_mqtt.py add <MAC> --name <名称>"}
        return list(devices.keys())

    if not devices:
        return {"success": False, "error": "暂无已保存的设备。请先添加: python3 st200th_mqtt.py add <MAC> --name <名称>"}

    if len(devices) == 1:
        return [list(devices.keys())[0]]

    return {
        "success": False,
        "error": "存在多个设备，请指定 --mac 或使用 --all",
        "devices": [{"mac": m, "name": d.get("name", m)} for m, d in devices.items()]
    }


# ══════════════════════════════════════════════════════════════
#  MQTT 通信核心
# ══════════════════════════════════════════════════════════════

def mqtt_send(mac, request, wait_response=True):
    """
    向设备发送 MQTT 消息。

    Args:
        mac: 12位MAC地址
        request: 要发送的 JSON 请求
        wait_response: 是否等待响应（restart/reset/compensate/ota 无响应）

    Returns:
        {"success": bool, "error": str|None, "data": dict|None}
    """
    mac = normalize_mac(mac)
    topic_cmd = f"/public/{mac}/publish"
    topic_rsp = f"/public/{mac}/subscribe"
    # ClientID: openclaw_ 前缀 + 每次随机，避免与设备冲突
    client_id = f"openclaw_{uuid.uuid4().hex[:12]}"

    result = {"success": False, "error": None, "data": None}
    connected_event = threading.Event()
    subscribed_event = threading.Event()

    def on_connect(client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            connected_event.set()
            if wait_response:
                client.subscribe(topic_rsp, qos=1)
            else:
                subscribed_event.set()
        else:
            result["error"] = f"MQTT 连接失败 (rc={reason_code})"
            connected_event.set()

    def on_subscribe(client, userdata, mid, rc_list, properties):
        subscribed_event.set()

    def on_message(client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode("utf-8"))
            result["data"] = payload
            result["success"] = True
            client.disconnect()
        except json.JSONDecodeError as e:
            result["error"] = f"JSON 解析失败: {e}"
            client.disconnect()

    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id=client_id,
    )
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
    except Exception as e:
        return {"success": False, "error": f"无法连接 MQTT: {e}", "data": None}

    client.loop_start()

    # 严格按顺序：等连接 → 等订阅 → 再发送
    if not connected_event.wait(timeout=5):
        client.loop_stop()
        return {"success": False, "error": "MQTT 连接超时", "data": None}
    if result["error"]:
        client.loop_stop()
        return result

    if not subscribed_event.wait(timeout=5):
        client.loop_stop()
        return {"success": False, "error": "MQTT 订阅超时", "data": None}

    # 订阅确认后再发送命令
    time.sleep(0.3)
    info = client.publish(topic_cmd, json.dumps(request), qos=1)
    info.wait_for_publish(timeout=5)

    if wait_response:
        deadline = time.time() + TIMEOUT_SECONDS
        while not result["success"] and result["error"] is None and time.time() < deadline:
            time.sleep(0.1)
        if not result["success"] and result["error"] is None:
            result["error"] = f"查询超时（{TIMEOUT_SECONDS}s），设备可能离线"
    else:
        time.sleep(1)
        result["success"] = True
        result["data"] = {"message": "命令已发送（该命令无响应返回）"}

    client.loop_stop()
    try:
        client.disconnect()
    except Exception:
        pass

    return result


# ══════════════════════════════════════════════════════════════
#  各命令实现
# ══════════════════════════════════════════════════════════════

def cmd_query(mac: str) -> dict:
    """查询设备传感器数据和系统信息。"""
    request = {
        "messageid": str(uuid.uuid4()).upper(),
        "param": {"type": "info"}
    }
    return mqtt_send(mac, request, wait_response=True)


def cmd_customize(mac: str) -> dict:
    """查询设备当前协议配置。"""
    request = {
        "messageid": str(uuid.uuid4()).upper(),
        "param": {"type": "customize"}
    }
    return mqtt_send(mac, request, wait_response=True)


def cmd_restart(mac: str) -> dict:
    """重启设备（立即生效，无返回）。"""
    request = {
        "messageid": "",
        "param": {"type": "restart"}
    }
    return mqtt_send(mac, request, wait_response=False)


def cmd_reset(mac: str) -> dict:
    """恢复出厂设置（立即生效，无返回）。"""
    request = {
        "messageid": "",
        "param": {"type": "reset"}
    }
    return mqtt_send(mac, request, wait_response=False)


def cmd_compensate(mac: str, t: float = 0, h: float = 0, p: float = 0) -> dict:
    """
    设置传感器补偿参数（立即生效，无返回）。

    Args:
        t: 温度补偿 -20 ~ +20 °C
        h: 湿度补偿 -20 ~ +20 %
        p: 气压补偿 -500 ~ +500 hPa
    """
    if not (-20 <= t <= 20):
        return {"success": False, "error": f"温度补偿超出范围: {t}（允许 -20 ~ +20）", "data": None}
    if not (-20 <= h <= 20):
        return {"success": False, "error": f"湿度补偿超出范围: {h}（允许 -20 ~ +20）", "data": None}
    if not (-500 <= p <= 500):
        return {"success": False, "error": f"气压补偿超出范围: {p}（允许 -500 ~ +500）", "data": None}

    request = {
        "messageid": "",
        "param": {
            "type": "compensate",
            "t_compensate": t,
            "h_compensate": h,
            "p_compensate": p
        }
    }
    return mqtt_send(mac, request, wait_response=False)


def cmd_ota(mac: str, uri: str) -> dict:
    """
    OTA 固件升级（立即生效，无返回）。

    Args:
        uri: 固件下载地址（最长128字符，仅HTTP）
    """
    if len(uri) > 128:
        return {"success": False, "error": f"URI 长度超限: {len(uri)}字符（最大128）", "data": None}

    request = {
        "id": str(uuid.uuid4()).upper(),
        "param": {
            "type": "ota",
            "uri": uri
        }
    }
    return mqtt_send(mac, request, wait_response=False)


def cmd_custom_mqtt(mac: str, **kwargs) -> dict:
    """修改设备 MQTT 配置（重启后生效）。"""
    param = {"type": "custom", "protocol": "mqtt"}
    allowed = ["enable", "mqtt_server", "mqtt_port", "client_id", "username",
               "password", "publish", "subcribe", "qos", "retain",
               "timed_report", "interval_time"]
    for k in allowed:
        if k in kwargs and kwargs[k] is not None:
            param[k] = kwargs[k]

    request = {"messageid": str(uuid.uuid4()).upper(), "param": param}
    return mqtt_send(mac, request, wait_response=True)


def cmd_custom_tcp(mac: str, **kwargs) -> dict:
    """修改设备 TCP 配置（重启后生效）。"""
    param = {"type": "custom", "protocol": "tcp"}
    allowed = ["enable", "tcp_server", "tcp_port", "timed_report", "interval_time"]
    for k in allowed:
        if k in kwargs and kwargs[k] is not None:
            param[k] = kwargs[k]

    request = {"messageid": str(uuid.uuid4()).upper(), "param": param}
    return mqtt_send(mac, request, wait_response=True)


def cmd_custom_http(mac: str, **kwargs) -> dict:
    """修改设备 HTTP 配置（重启后生效）。"""
    param = {"type": "custom", "protocol": "http"}
    allowed = ["enable", "http_uri", "timed_report", "interval_time"]
    for k in allowed:
        if k in kwargs and kwargs[k] is not None:
            param[k] = kwargs[k]
    if "http_uri" in param and len(str(param["http_uri"])) > 32:
        return {"success": False, "error": "HTTP URI 长度不能超过32字符", "data": None}

    request = {"messageid": str(uuid.uuid4()).upper(), "param": param}
    return mqtt_send(mac, request, wait_response=True)


# ══════════════════════════════════════════════════════════════
#  格式化输出
# ══════════════════════════════════════════════════════════════

def format_query(data: dict, device_name: str = "", mac: str = "") -> str:
    """格式化 info 响应。"""
    lines = []

    header = device_name or data.get("type", "ST200TH")
    if mac:
        header += f" ({mac})"
    lines.append(f"== {header} ==")

    if "type" in data:
        lines.append(f"  设备型号: {data['type']}")

    if "data" in data:
        d = data["data"]
        lines.append("[传感器数据]")
        if "temperature" in d:
            lines.append(f"  温度: {d['temperature']} °C")
        if "humidity" in d:
            lines.append(f"  湿度: {d['humidity']} %")
        if "pressure" in d:
            lines.append(f"  气压: {d['pressure']} hPa")
        if "altitude" in d:
            lines.append(f"  海拔: {d['altitude']} m")

    if "compensate" in data:
        c = data["compensate"]
        lines.append("[补偿参数]")
        lines.append(f"  温度补偿: {c.get('t_compensate', 0)} °C（范围 -20 ~ +20）")
        lines.append(f"  湿度补偿: {c.get('h_compensate', 0)} %（范围 -20 ~ +20）")
        lines.append(f"  气压补偿: {c.get('p_compensate', 0)} hPa（范围 -500 ~ +500）")

    if "set" in data:
        s = data["set"]
        lines.append("[定时上报]")
        lines.append(f"  MQTT: {'启用' if s.get('mqtt_timed_report') else '未启用'}，间隔 {s.get('mqtt_interval_time', 5)}s")
        lines.append(f"  TCP:  {'启用' if s.get('tcp_timed_report') else '未启用'}，间隔 {s.get('tcp_interval_time', 5)}s")
        lines.append(f"  HTTP: {'启用' if s.get('http_timed_report') else '未启用'}，间隔 {s.get('http_interval_time', 5)}s")

    if "net" in data:
        n = data["net"]
        lines.append("[网络信息]")
        conn = "以太网" if n.get("connmethed") == "eth" else ("WiFi" if n.get("connmethed") == "wifi" else n.get("connmethed", "N/A"))
        lines.append(f"  连接方式: {conn}")
        lines.append(f"  IP 地址:  {n.get('ip', 'N/A')}")
        lines.append(f"  DHCP:     {'启用' if n.get('dhcp') else '静态'}")
        if n.get("ssid") and n["ssid"] != "---":
            lines.append(f"  WiFi SSID: {n['ssid']}")

    if "sys" in data:
        s = data["sys"]
        lines.append("[系统信息]")
        lines.append(f"  固件版本:  {s.get('version', 'N/A')}")
        runtime = s.get("runtime", 0)
        if isinstance(runtime, (int, float)) and runtime > 0:
            hours, remainder = divmod(int(runtime), 3600)
            minutes, secs = divmod(remainder, 60)
            lines.append(f"  运行时间:  {hours}h{minutes}m{secs}s（{runtime}秒）")
        else:
            lines.append(f"  运行时间:  {runtime}s")
        if "eth_mac" in s:
            lines.append(f"  以太网MAC: {s['eth_mac']}")
        if "sta_mac" in s:
            lines.append(f"  WiFi MAC:  {s['sta_mac']}")

    if "protocol" in data:
        p = data["protocol"]
        lines.append("[协议状态]")
        lines.append(f"  MQTT:       {'启用' if p.get('mqtt') else '未启用'}")
        lines.append(f"  HTTP:       {'启用' if p.get('http') else '未启用'}")
        lines.append(f"  TCP Server: {'启用' if p.get('tcpserver') else '未启用'}")
        lines.append(f"  TCP Client: {'启用' if p.get('tcpclient') else '未启用'}")

    return "\n".join(lines)


def format_customize(data: dict, device_name: str = "", mac: str = "") -> str:
    """格式化 customize 响应。"""
    lines = []

    header = device_name or data.get("type", "ST200TH")
    if mac:
        header += f" ({mac})"
    lines.append(f"== {header} 配置信息 ==")

    if "mqtt_info" in data:
        m = data["mqtt_info"]
        lines.append("[MQTT 配置]")
        lines.append(f"  启用:     {'是' if m.get('enable') else '否'}")
        lines.append(f"  服务器:   {m.get('mqtt_server', 'N/A')}:{m.get('mqtt_port', 'N/A')}")
        lines.append(f"  ClientID: {m.get('client_id', 'N/A')}")
        lines.append(f"  用户名:   {m.get('username', 'N/A')}")
        lines.append(f"  发布主题: {m.get('publish', 'N/A')}")
        lines.append(f"  订阅主题: {m.get('subcribe', 'N/A')}")
        lines.append(f"  QoS:      {m.get('qos', 0)}")
        lines.append(f"  Retain:   {'是' if m.get('retain') else '否'}")
        lines.append(f"  定时上报: {'启用' if m.get('timed_report') else '未启用'}，间隔 {m.get('interval_time', 5)}s")

    if "tcp_info" in data:
        t = data["tcp_info"]
        lines.append("[TCP 配置]")
        lines.append(f"  启用:     {'是' if t.get('enable') else '否'}")
        lines.append(f"  服务器:   {t.get('tcp_server', 'N/A')}:{t.get('tcp_port', 'N/A')}")
        lines.append(f"  定时上报: {'启用' if t.get('timed_report') else '未启用'}，间隔 {t.get('interval_time', 5)}s")

    if "http_info" in data:
        h = data["http_info"]
        lines.append("[HTTP 配置]")
        lines.append(f"  启用:     {'是' if h.get('enable') else '否'}")
        lines.append(f"  URI:      {h.get('http_uri', 'N/A')}")
        lines.append(f"  定时上报: {'启用' if h.get('timed_report') else '未启用'}，间隔 {h.get('interval_time', 5)}s")

    if "compensate" in data:
        c = data["compensate"]
        lines.append("[补偿参数]")
        lines.append(f"  温度: {c.get('t_compensate', 0)} °C")
        lines.append(f"  湿度: {c.get('h_compensate', 0)} %")
        lines.append(f"  气压: {c.get('p_compensate', 0)} hPa")

    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════
#  CLI 入口
# ══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="ST200TH 温湿度变送器 MQTT 全功能管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="subcmd")

    # ── query: 查询传感器数据 ──
    p_q = sub.add_parser("query", help="查询传感器数据（温度/湿度/气压/海拔）及系统信息")
    p_q.add_argument("--mac", help="指定设备 MAC")
    p_q.add_argument("--all", action="store_true", help="查询所有已保存设备")
    p_q.add_argument("--json", action="store_true", dest="use_json", help="输出 JSON")

    # ── customize: 查询设备配置 ──
    p_c = sub.add_parser("customize", help="查询设备当前配置（MQTT/TCP/HTTP）")
    p_c.add_argument("--mac", help="指定设备 MAC")
    p_c.add_argument("--json", action="store_true", dest="use_json", help="输出 JSON")

    # ── compensate: 设置补偿参数 ──
    p_comp = sub.add_parser("compensate", help="设置传感器补偿参数（立即生效）")
    p_comp.add_argument("--mac", help="指定设备 MAC")
    p_comp.add_argument("--all", action="store_true", help="对所有设备生效")
    p_comp.add_argument("-t", type=float, default=0, help="温度补偿 -20~+20°C（默认0）")
    p_comp.add_argument("-hu", type=float, default=0, help="湿度补偿 -20~+20%%（默认0）")
    p_comp.add_argument("-p", type=float, default=0, help="气压补偿 -500~+500hPa（默认0）")

    # ── restart: 重启设备 ──
    p_r = sub.add_parser("restart", help="重启设备（立即生效）")
    p_r.add_argument("--mac", help="指定设备 MAC")

    # ── reset: 恢复出厂设置 ──
    p_rs = sub.add_parser("reset", help="恢复出厂设置（立即生效，谨慎操作）")
    p_rs.add_argument("--mac", help="指定设备 MAC")

    # ── ota: 固件升级 ──
    p_ota = sub.add_parser("ota", help="OTA 固件升级（立即生效）")
    p_ota.add_argument("--mac", help="指定设备 MAC")
    p_ota.add_argument("--uri", required=True, help="固件下载地址（HTTP，最长128字符）")

    # ── custom: 修改协议配置 ──
    p_cu = sub.add_parser("custom", help="修改设备协议配置（重启后生效）")
    p_cu.add_argument("--mac", help="指定设备 MAC")
    p_cu.add_argument("--protocol", required=True, choices=["mqtt", "tcp", "http"], help="要修改的协议")
    p_cu.add_argument("--enable", type=int, choices=[0, 1], help="启用/禁用")
    p_cu.add_argument("--server", help="服务器地址")
    p_cu.add_argument("--port", type=int, help="服务器端口")
    p_cu.add_argument("--client-id", help="MQTT ClientID")
    p_cu.add_argument("--username", help="MQTT 用户名")
    p_cu.add_argument("--password", help="MQTT 密码")
    p_cu.add_argument("--publish-topic", help="MQTT 发布主题")
    p_cu.add_argument("--subscribe-topic", help="MQTT 订阅主题")
    p_cu.add_argument("--qos", type=int, choices=[0, 1, 2], help="MQTT QoS")
    p_cu.add_argument("--retain", type=int, choices=[0, 1], help="MQTT Retain")
    p_cu.add_argument("--timed-report", type=int, choices=[0, 1], help="定时上报 0/1")
    p_cu.add_argument("--interval", type=int, help="上报间隔秒数（建议>=5，最低2）")
    p_cu.add_argument("--http-uri", help="HTTP 接口地址（最长32字符）")
    p_cu.add_argument("--json", action="store_true", dest="use_json", help="输出 JSON")

    # ── add / remove / list: 本地设备管理 ──
    p_add = sub.add_parser("add", help="添加设备到本地列表")
    p_add.add_argument("mac", help="设备 WiFi MAC 地址")
    p_add.add_argument("--name", default="", help="设备备注名称")

    p_rm = sub.add_parser("remove", help="从本地列表删除设备")
    p_rm.add_argument("mac", help="设备 WiFi MAC 地址")

    sub.add_parser("list", help="列出本地已保存设备")


    args = parser.parse_args()

    # 无子命令默认 query
    if args.subcmd is None:
        args.subcmd = "query"
        args.mac = None
        args.all = False
        args.use_json = False

    # ── 设备列表管理 ──
    if args.subcmd == "add":
        mac = normalize_mac(args.mac)
        if not validate_mac(mac):
            _err(f"MAC 地址格式无效: {mac}")
        devices = load_devices()
        devices[mac] = {"mac": mac, "name": args.name or mac}
        save_devices(devices)
        print(json.dumps({"success": True, "message": f"设备已添加: {args.name or mac} ({mac})"}, ensure_ascii=False))
        return

    if args.subcmd == "remove":
        mac = normalize_mac(args.mac)
        devices = load_devices()
        if mac not in devices:
            _err(f"设备不存在: {mac}")
        name = devices[mac].get("name", mac)
        del devices[mac]
        save_devices(devices)
        print(json.dumps({"success": True, "message": f"设备已删除: {name} ({mac})"}, ensure_ascii=False))
        return

    if args.subcmd == "list":
        devices = load_devices()
        if not devices:
            print("暂无已保存的设备，请先添加: python3 st200th_mqtt.py add <MAC> --name <名称>")
        else:
            for mac, info in devices.items():
                print(f"  {info.get('name', mac):20s}  {mac}")
        return

    # ── 需要 MAC 的命令 ──
    devices = load_devices()

    if args.subcmd == "query":
        macs = resolve_mac(args.mac, args.all)
        if isinstance(macs, dict):
            print(json.dumps(macs, ensure_ascii=False))
            sys.exit(1)

        for mac in macs:
            r = cmd_query(mac)
            name = devices.get(mac, {}).get("name", "")
            if not r["success"]:
                print(json.dumps({"mac": mac, "name": name, "success": False, "error": r["error"]}, ensure_ascii=False))
            elif args.use_json:
                out = r["data"]
                out["_device_name"] = name
                out["_mac"] = mac
                print(json.dumps(out, indent=2, ensure_ascii=False))
            else:
                print(format_query(r["data"], name, mac))
            if len(macs) > 1:
                print()

    elif args.subcmd == "customize":
        macs = resolve_mac(args.mac)
        if isinstance(macs, dict):
            print(json.dumps(macs, ensure_ascii=False))
            sys.exit(1)
        mac = macs[0]
        r = cmd_customize(mac)
        name = devices.get(mac, {}).get("name", "")
        if not r["success"]:
            _err(r["error"])
        if args.use_json:
            print(json.dumps(r["data"], indent=2, ensure_ascii=False))
        else:
            print(format_customize(r["data"], name, mac))

    elif args.subcmd == "compensate":
        macs = resolve_mac(args.mac, args.all)
        if isinstance(macs, dict):
            print(json.dumps(macs, ensure_ascii=False))
            sys.exit(1)
        for mac in macs:
            r = cmd_compensate(mac, t=args.t, h=args.hu, p=args.p)
            name = devices.get(mac, {}).get("name", mac)
            if r["success"]:
                print(f"[{name}] 补偿参数已设置: 温度={args.t}°C 湿度={args.hu}% 气压={args.p}hPa")
            else:
                print(f"[{name}] 错误: {r['error']}")

    elif args.subcmd == "restart":
        macs = resolve_mac(args.mac)
        if isinstance(macs, dict):
            print(json.dumps(macs, ensure_ascii=False))
            sys.exit(1)
        mac = macs[0]
        r = cmd_restart(mac)
        name = devices.get(mac, {}).get("name", mac)
        print(f"[{name}] {'重启命令已发送' if r['success'] else '错误: ' + r['error']}")

    elif args.subcmd == "reset":
        macs = resolve_mac(args.mac)
        if isinstance(macs, dict):
            print(json.dumps(macs, ensure_ascii=False))
            sys.exit(1)
        mac = macs[0]
        r = cmd_reset(mac)
        name = devices.get(mac, {}).get("name", mac)
        print(f"[{name}] {'恢复出厂设置命令已发送' if r['success'] else '错误: ' + r['error']}")

    elif args.subcmd == "ota":
        macs = resolve_mac(args.mac)
        if isinstance(macs, dict):
            print(json.dumps(macs, ensure_ascii=False))
            sys.exit(1)
        mac = macs[0]
        r = cmd_ota(mac, args.uri)
        name = devices.get(mac, {}).get("name", mac)
        print(f"[{name}] {'OTA升级命令已发送，固件: ' + args.uri if r['success'] else '错误: ' + r['error']}")

    elif args.subcmd == "custom":
        macs = resolve_mac(args.mac)
        if isinstance(macs, dict):
            print(json.dumps(macs, ensure_ascii=False))
            sys.exit(1)
        mac = macs[0]
        name = devices.get(mac, {}).get("name", mac)

        if args.protocol == "mqtt":
            kwargs = {
                "enable": args.enable,
                "mqtt_server": args.server,
                "mqtt_port": args.port,
                "client_id": args.client_id,
                "username": args.username,
                "password": args.password,
                "publish": args.publish_topic,
                "subcribe": args.subscribe_topic,
                "qos": args.qos,
                "retain": args.retain,
                "timed_report": args.timed_report,
                "interval_time": args.interval,
            }
            r = cmd_custom_mqtt(mac, **kwargs)
        elif args.protocol == "tcp":
            kwargs = {
                "enable": args.enable,
                "tcp_server": args.server,
                "tcp_port": args.port,
                "timed_report": args.timed_report,
                "interval_time": args.interval,
            }
            r = cmd_custom_tcp(mac, **kwargs)
        elif args.protocol == "http":
            kwargs = {
                "enable": args.enable,
                "http_uri": args.http_uri,
                "timed_report": args.timed_report,
                "interval_time": args.interval,
            }
            r = cmd_custom_http(mac, **kwargs)

        if not r["success"]:
            print(f"[{name}] 错误: {r['error']}")
            sys.exit(1)
        if hasattr(args, "use_json") and args.use_json:
            print(json.dumps(r["data"], indent=2, ensure_ascii=False))
        else:
            print(f"[{name}] {args.protocol.upper()} 配置已发送（重启后生效）")
            if r["data"]:
                print(json.dumps(r["data"], indent=2, ensure_ascii=False))


def _err(msg):
    print(json.dumps({"success": False, "error": msg}, ensure_ascii=False))
    sys.exit(1)


if __name__ == "__main__":
    main()
