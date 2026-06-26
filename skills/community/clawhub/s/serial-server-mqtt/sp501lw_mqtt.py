#!/usr/bin/env python3
"""
SP501LW 串口网关纯 MQTT 管理工具

通过 MQTT 协议完全控制立控 SP501LW 串口网关，支持：
- mqtt_tcp 模式：AI 当作虚拟串口使用
- modbus_rtu 模式：AI 当作数据采集器使用
"""

import os
import sys
import json
import time
import argparse
import threading
import uuid
import tempfile
from pathlib import Path
from datetime import datetime
from contextlib import contextmanager

try:
    import fcntl  # Linux/macOS 文件锁
except ImportError:
    fcntl = None

try:
    import paho.mqtt.client as mqtt
except ImportError:
    mqtt = None

# 常量
CONFIG_FILE = Path(__file__).parent / "devices.json"
LOCK_FILE = CONFIG_FILE.with_suffix(".lock")
DEFAULT_BROKER_HOST = "mqtt.likong-iot.com"
DEFAULT_BROKER_PORT = 1883
DEFAULT_BROKER_USER = "public"
DEFAULT_BROKER_PASS = "Aa123456"
MQTT_TIMEOUT = 10
ACK_TIMEOUT = 3

VALID_DATA_FORMATS = {"HEX", "Signed", "Unsigned", "Float", "Long", "Double"}
VALID_REPORT_FORMATS = {"mqtt", "tcp", "http"}
VALID_CHECK_BITS = {"None", "Odd", "Even"}
VALID_STOP_BITS = {"1", "1.5", "2"}
VALID_DATA_BITS = {5, 6, 7, 8}
VALID_SERIAL_BAUD_RATES = {1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200}
MQTT_IMPORT_ERROR = "缺少依赖 paho-mqtt，请执行: pip3 install paho-mqtt>=2.0.0"

# ============================================================================
# 设备存储管理
# ============================================================================

@contextmanager
def _devices_lock():
    """设备文件锁，避免并发写导致损坏"""
    lock_fh = None
    try:
        lock_fh = open(LOCK_FILE, "a+", encoding="utf-8")
        if fcntl is not None:
            fcntl.flock(lock_fh.fileno(), fcntl.LOCK_EX)
        yield
    finally:
        if lock_fh is not None:
            try:
                if fcntl is not None:
                    fcntl.flock(lock_fh.fileno(), fcntl.LOCK_UN)
            finally:
                lock_fh.close()


def _load_devices_unlocked() -> dict:
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as exc:
            print(
                json.dumps(
                    {"success": False, "warning": f"devices.json 解析失败，已按空配置处理: {exc}"},
                    ensure_ascii=False,
                ),
                file=sys.stderr,
            )
            return {}
        except IOError as exc:
            print(
                json.dumps(
                    {"success": False, "warning": f"读取 devices.json 失败，已按空配置处理: {exc}"},
                    ensure_ascii=False,
                ),
                file=sys.stderr,
            )
            return {}
    return {}


def load_devices() -> dict:
    """加载已保存的设备列表"""
    with _devices_lock():
        return _load_devices_unlocked()


def get_modbus_items(device_id: str) -> list:
    """获取设备本地缓存的 Modbus 轮询项"""
    device = get_device(device_id)
    if not device:
        return []
    return device.get("modbus_items", [])


def update_modbus_items(device_id: str, items: list):
    """更新设备的 Modbus 轮询项缓存"""
    with _devices_lock():
        devices = _load_devices_unlocked()
        if device_id in devices:
            devices[device_id]["modbus_items"] = items
            devices[device_id]["last_config_sync"] = datetime.now().isoformat()
            _save_devices_unlocked(devices)


def _save_devices_unlocked(devices: dict):
    """原子写入，避免中断时留下坏文件"""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=".devices.", suffix=".tmp", dir=str(CONFIG_FILE.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(devices, f, indent=2, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_name, CONFIG_FILE)
    finally:
        if os.path.exists(tmp_name):
            try:
                os.remove(tmp_name)
            except OSError:
                pass


def save_devices(devices: dict):
    """保存设备列表"""
    with _devices_lock():
        _save_devices_unlocked(devices)


def get_device(device_id: str) -> dict:
    """获取设备信息"""
    devices = load_devices()
    if device_id not in devices:
        return None
    return devices[device_id]


# ============================================================================
# MQTT 通信核心
# ============================================================================

class MQTTClient:
    """MQTT 客户端封装"""

    def __init__(self, broker_host, broker_port, username, password, client_id=None):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.username = username
        self.password = password
        self.client_id = client_id or f"openclaw_{uuid.uuid4().hex[:12]}"
        self.client = None
        self.connected = False
        self.last_connect_reason = None
        self.last_message = None
        self.lock = threading.Lock()
        self.connect_event = threading.Event()
        self.subscribe_event = threading.Event()
        self.subscribe_mid = None

    def _cleanup_client(self):
        """清理 MQTT 客户端资源，避免连接失败后的线程泄漏"""
        if self.client:
            try:
                self.client.loop_stop()
            except Exception:
                pass
            try:
                self.client.disconnect()
            except Exception:
                pass
            self.client = None

    def connect(self):
        """连接到 MQTT Broker"""
        if mqtt is None:
            return False, MQTT_IMPORT_ERROR

        self.connected = False
        self.last_connect_reason = None
        self.connect_event.clear()
        try:
            self.client = mqtt.Client(
                callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
                client_id=self.client_id,
            )
            self.client.username_pw_set(self.username, self.password)
            self.client.on_connect = self._on_connect
            self.client.on_disconnect = self._on_disconnect
            self.client.on_subscribe = self._on_subscribe
            self.client.connect(self.broker_host, self.broker_port, keepalive=60)
            self.client.loop_start()

            # 等待连接事件，避免轮询误判
            if not self.connect_event.wait(MQTT_TIMEOUT):
                self._cleanup_client()
                return False, "MQTT 连接超时"
            if not self.connected:
                self._cleanup_client()
                return False, f"MQTT 连接失败，reason_code={self.last_connect_reason}"
            return True, None
        except Exception as e:
            self._cleanup_client()
            return False, f"MQTT 连接失败: {e}"

    def _on_connect(self, client, userdata, connect_flags, reason_code, properties):
        """连接回调"""
        normalized_reason = None
        # paho-mqtt 2.x 的 reason_code 可能是 ReasonCode 对象（例如 "Success"）
        value_attr = getattr(reason_code, "value", None)
        if isinstance(value_attr, int):
            normalized_reason = value_attr
        else:
            try:
                normalized_reason = int(reason_code)
            except (TypeError, ValueError):
                normalized_reason = str(reason_code)

        self.last_connect_reason = normalized_reason
        if normalized_reason == 0 or normalized_reason == "Success":
            self.connected = True
        else:
            self.connected = False
        self.connect_event.set()

    def _on_disconnect(self, client, userdata, disconnect_flags, reason_code, properties):
        """断开连接回调"""
        self.connected = False

    def _on_subscribe(self, client, userdata, mid, reason_code_list, properties):
        """订阅确认回调"""
        if self.subscribe_mid is None or mid == self.subscribe_mid:
            self.subscribe_event.set()

    def publish(self, topic, payload, qos=1):
        """发布消息"""
        if not self.connected:
            return False, "MQTT 未连接"
        try:
            info = self.client.publish(topic, payload, qos=qos)
            if info.rc != mqtt.MQTT_ERR_SUCCESS:
                return False, f"发布失败: rc={info.rc}"
            info.wait_for_publish(timeout=5)
            if not info.is_published():
                return False, "发布超时（未收到客户端发布确认）"
            if info.rc != mqtt.MQTT_ERR_SUCCESS:
                return False, f"发布失败: rc={info.rc}"
            return True, None
        except Exception as e:
            return False, f"发布失败: {e}"

    def subscribe(self, topic, qos=1):
        """订阅主题"""
        if not self.connected:
            return False, "MQTT 未连接"
        try:
            self.subscribe_event.clear()
            result, mid = self.client.subscribe(topic, qos=qos)
            if result != mqtt.MQTT_ERR_SUCCESS:
                return False, f"订阅失败: rc={result}"
            self.subscribe_mid = mid
            if not self.subscribe_event.wait(2):
                return False, "订阅确认超时"
            return True, None
        except Exception as e:
            return False, f"订阅失败: {e}"

    def set_message_callback(self, callback):
        """设置消息回调"""
        self.client.on_message = callback

    def disconnect(self):
        """断开连接"""
        self._cleanup_client()


# ============================================================================
# 命令实现
# ============================================================================

def cmd_add(args):
    """添加设备"""
    device_id = args.id
    cmd_topic = args.cmd_topic
    data_topic = args.data_topic
    broker_host = args.broker_host or DEFAULT_BROKER_HOST
    broker_port = args.broker_port or DEFAULT_BROKER_PORT
    username = args.username or DEFAULT_BROKER_USER
    password = args.password or DEFAULT_BROKER_PASS

    with _devices_lock():
        devices = _load_devices_unlocked()

        if device_id in devices:
            print(json.dumps({
                "success": False,
                "error": f"设备已存在: {device_id}"
            }, ensure_ascii=False))
            return

        devices[device_id] = {
            "id": device_id,
            "cmd_topic": cmd_topic,
            "data_topic": data_topic,
            "broker_host": broker_host,
            "broker_port": broker_port,
            "broker_username": username,
            "broker_password": password,
            "last_seen": datetime.now().isoformat()
        }
        _save_devices_unlocked(devices)

    print(json.dumps({
        "success": True,
        "message": f"设备已添加: {device_id}",
        "device": devices[device_id]
    }, ensure_ascii=False))


def cmd_list(args):
    """列出设备"""
    devices = load_devices()

    if not devices:
        print("暂无已保存的设备")
        return

    print("\n已保存的设备：")
    print("-" * 80)
    for device_id, info in devices.items():
        print(f"  ID: {device_id}")
        print(f"     命令主题: {info['cmd_topic']}")
        print(f"     数据主题: {info['data_topic']}")
        print(f"     Broker: {info['broker_host']}:{info['broker_port']}")
        print()


def cmd_remove(args):
    """删除设备"""
    device_id = args.id
    with _devices_lock():
        devices = _load_devices_unlocked()

        if device_id not in devices:
            print(json.dumps({
                "success": False,
                "error": f"设备不存在: {device_id}"
            }, ensure_ascii=False))
            return

        del devices[device_id]
        _save_devices_unlocked(devices)

    print(json.dumps({
        "success": True,
        "message": f"设备已删除: {device_id}"
    }, ensure_ascii=False))


def cmd_update(args):
    """更新设备信息"""
    device_id = args.id
    with _devices_lock():
        devices = _load_devices_unlocked()

        if device_id not in devices:
            print(json.dumps({
                "success": False,
                "error": f"设备不存在: {device_id}"
            }, ensure_ascii=False))
            return

        device = devices[device_id]

        if args.cmd_topic:
            device["cmd_topic"] = args.cmd_topic
        if args.data_topic:
            device["data_topic"] = args.data_topic
        if args.broker_host:
            device["broker_host"] = args.broker_host
        if args.broker_port:
            device["broker_port"] = args.broker_port
        if args.username:
            device["broker_username"] = args.username
        if args.password:
            device["broker_password"] = args.password

        device["last_seen"] = datetime.now().isoformat()
        _save_devices_unlocked(devices)

    print(json.dumps({
        "success": True,
        "message": f"设备已更新: {device_id}",
        "device": device
    }, ensure_ascii=False))


def _send_config(device_id, config_data):
    """发送配置到设备（内部函数）"""
    device = get_device(device_id)
    if not device:
        return False, f"设备不存在: {device_id}"

    mqtt_client = MQTTClient(
        device["broker_host"],
        device["broker_port"],
        device["broker_username"],
        device["broker_password"]
    )

    success, error = mqtt_client.connect()
    if not success:
        return False, error

    try:
        # 先订阅响应主题，避免发布后 ACK 在订阅前丢失
        ack_event = threading.Event()
        publish_started_at = None

        def on_message(client, userdata, msg):
            nonlocal publish_started_at
            try:
                response = json.loads(msg.payload.decode("utf-8"))
                # 仅接受“本次发布之后”收到的标准 ACK，过滤订阅前/历史缓存消息
                if (
                    publish_started_at is not None
                    and time.monotonic() >= publish_started_at
                    and response.get("code") == 200
                    and response.get("msg") == "config updated"
                ):
                    ack_event.set()
            except Exception:
                pass

        mqtt_client.set_message_callback(on_message)
        success, error = mqtt_client.subscribe(device["data_topic"], qos=1)
        if not success:
            mqtt_client.disconnect()
            return False, f"订阅响应主题失败: {error}"

        # 构建配置消息（符合 mqtt.md 的识别规则）
        message = {
            "action": "config",
            "data": config_data
        }

        payload = json.dumps(message, ensure_ascii=False)
        publish_started_at = time.monotonic()
        success, error = mqtt_client.publish(device["cmd_topic"], payload, qos=1)

        if not success:
            mqtt_client.disconnect()
            return False, error

        # ACK 是配置成功的唯一确认信号；超时必须判定失败，不能“假成功”
        if not ack_event.wait(ACK_TIMEOUT):
            mqtt_client.disconnect()
            return False, f"未收到设备 ACK（超时 {ACK_TIMEOUT} 秒）"

        mqtt_client.disconnect()
        return True, None
    except Exception as e:
        mqtt_client.disconnect()
        return False, str(e)


def cmd_set_mode(args):
    """切换工作模式"""
    device_id = args.id
    mode = args.mode

    if mode not in ["mqtt_tcp", "modbus_tcp", "modbus_rtu"]:
        print(json.dumps({
            "success": False,
            "error": f"无效的工作模式: {mode}"
        }, ensure_ascii=False))
        return

    success, error = _send_config(device_id, {"work_mode": mode})

    if success:
        print(json.dumps({
            "success": True,
            "message": f"工作模式已切换为: {mode}，设备将在 5-30 秒内重启"
        }, ensure_ascii=False))
    else:
        print(json.dumps({
            "success": False,
            "error": error
        }, ensure_ascii=False))


def cmd_send(args):
    """发送串口数据（mqtt_tcp/modbus_tcp 模式）"""
    device_id = args.id
    data_str = args.data
    fmt = args.format or "text"

    device = get_device(device_id)
    if not device:
        print(json.dumps({
            "success": False,
            "error": f"设备不存在: {device_id}"
        }, ensure_ascii=False))
        return

    # 转换数据格式
    if fmt == "hex":
        try:
            data_bytes = bytes.fromhex(data_str.replace(" ", ""))
        except ValueError:
            print(json.dumps({
                "success": False,
                "error": "HEX 格式无效"
            }, ensure_ascii=False))
            return
    else:
        data_bytes = data_str.encode("utf-8")

    # 连接并发送
    mqtt_client = MQTTClient(
        device["broker_host"],
        device["broker_port"],
        device["broker_username"],
        device["broker_password"]
    )

    success, error = mqtt_client.connect()
    if not success:
        print(json.dumps({
            "success": False,
            "error": error
        }, ensure_ascii=False))
        return

    try:
        success, error = mqtt_client.publish(device["cmd_topic"], data_bytes, qos=1)
        mqtt_client.disconnect()

        if success:
            print(json.dumps({
                "success": True,
                "message": f"已发送 {len(data_bytes)} 字节",
                "data": data_str
            }, ensure_ascii=False))
        else:
            print(json.dumps({
                "success": False,
                "error": error
            }, ensure_ascii=False))
    except Exception as e:
        mqtt_client.disconnect()
        print(json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False))


def cmd_listen(args):
    """监听设备数据"""
    device_id = args.id
    timeout = args.timeout or 60
    fmt = args.format or "hex"

    device = get_device(device_id)
    if not device:
        print(json.dumps({
            "success": False,
            "error": f"设备不存在: {device_id}"
        }, ensure_ascii=False))
        return

    mqtt_client = MQTTClient(
        device["broker_host"],
        device["broker_port"],
        device["broker_username"],
        device["broker_password"]
    )

    success, error = mqtt_client.connect()
    if not success:
        print(json.dumps({
            "success": False,
            "error": error
        }, ensure_ascii=False))
        return

    print(f"[*] 开始监听 {device_id}，超时 {timeout} 秒（Ctrl+C 停止）")
    print(f"[*] 数据主题: {device['data_topic']}")
    print("-" * 80)

    def on_message(client, userdata, msg):
        try:
            # 尝试作为 JSON 解析
            if fmt == "json":
                try:
                    data = json.loads(msg.payload.decode("utf-8"))
                    print(f"[RX JSON] {json.dumps(data, ensure_ascii=False)}")
                except:
                    # 作为 HEX 显示
                    hex_str = msg.payload.hex()
                    print(f"[RX HEX] {' '.join(hex_str[i:i+2].upper() for i in range(0, len(hex_str), 2))}")
            elif fmt == "hex":
                hex_str = msg.payload.hex()
                print(f"[RX HEX] {' '.join(hex_str[i:i+2].upper() for i in range(0, len(hex_str), 2))}")
            else:
                try:
                    text = msg.payload.decode("utf-8")
                    print(f"[RX] {text}")
                except:
                    hex_str = msg.payload.hex()
                    print(f"[RX HEX] {' '.join(hex_str[i:i+2].upper() for i in range(0, len(hex_str), 2))}")
        except Exception as e:
            print(f"[ERROR] {e}")

    mqtt_client.set_message_callback(on_message)
    success, error = mqtt_client.subscribe(device["data_topic"], qos=1)

    if not success:
        print(json.dumps({
            "success": False,
            "error": error
        }, ensure_ascii=False))
        mqtt_client.disconnect()
        return

    try:
        start_time = time.time()
        while time.time() - start_time < timeout:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n[*] 已停止监听")
    finally:
        mqtt_client.disconnect()


def cmd_set_poll_time(args):
    """设置轮询周期（modbus_rtu 模式）"""
    device_id = args.id
    poll_time = args.poll_time

    # 验证范围
    if poll_time < 1000 or poll_time > 3600000:
        print(json.dumps({
            "success": False,
            "error": f"轮询周期必须在 1000-3600000 毫秒之间（当前: {poll_time}）"
        }, ensure_ascii=False))
        return

    success, error = _send_config(device_id, {"poll_time": str(poll_time)})

    if success:
        print(json.dumps({
            "success": True,
            "message": f"轮询周期已设置为 {poll_time} ms ({poll_time/1000:.1f} 秒)，设备将重启"
        }, ensure_ascii=False))
    else:
        print(json.dumps({
            "success": False,
            "error": error
        }, ensure_ascii=False))


def validate_serial_args(args):
    """校验 set-serial 参数"""
    errors = []

    if (
        args.baud_rate is None
        and args.data_bit is None
        and args.stop_bit is None
        and args.check_bit is None
        and args.frame_time is None
        and args.frame_len is None
    ):
        errors.append("请至少提供一个串口参数（如 --baud-rate 或 --data-bit）")

    if args.baud_rate is not None and args.baud_rate not in VALID_SERIAL_BAUD_RATES:
        errors.append(
            f"baud-rate 必须是 {sorted(VALID_SERIAL_BAUD_RATES)} 之一（当前: {args.baud_rate}）"
        )

    if args.data_bit is not None and args.data_bit not in VALID_DATA_BITS:
        errors.append(f"data-bit 必须是 {sorted(VALID_DATA_BITS)} 之一（当前: {args.data_bit}）")

    if args.stop_bit is not None and str(args.stop_bit) not in VALID_STOP_BITS:
        errors.append(f"stop-bit 必须是 {sorted(VALID_STOP_BITS)} 之一（当前: {args.stop_bit}）")

    if args.check_bit is not None and args.check_bit not in VALID_CHECK_BITS:
        errors.append(f"check-bit 必须是 {sorted(VALID_CHECK_BITS)} 之一（当前: {args.check_bit}）")

    if args.frame_time is not None and args.frame_time <= 0:
        errors.append(f"frame-time 必须大于 0（当前: {args.frame_time}）")

    if args.frame_len is not None:
        if args.frame_len <= 0:
            errors.append(f"frame-len 必须大于 0（当前: {args.frame_len}）")
        elif args.frame_len > 4096:
            errors.append(f"frame-len 建议不超过 4096（当前: {args.frame_len}）")

    if errors:
        return "；".join(errors)
    return None


def cmd_set_serial(args):
    """设置设备串口参数"""
    device_id = args.id

    validation_error = validate_serial_args(args)
    if validation_error:
        print(json.dumps({
            "success": False,
            "error": validation_error
        }, ensure_ascii=False))
        return

    config_data = {}
    if args.baud_rate is not None:
        config_data["baud_rate"] = str(args.baud_rate)
    if args.data_bit is not None:
        config_data["data_bit"] = str(args.data_bit)
    if args.stop_bit is not None:
        config_data["stop_bit"] = str(args.stop_bit)
    if args.check_bit is not None:
        config_data["check_bit"] = args.check_bit
    if args.frame_time is not None:
        config_data["frame_time"] = str(args.frame_time)
    if args.frame_len is not None:
        config_data["frame_len"] = str(args.frame_len)

    success, error = _send_config(device_id, config_data)

    if success:
        print(json.dumps({
            "success": True,
            "message": "串口参数已更新，设备将在 5-30 秒内重启",
            "config": config_data
        }, ensure_ascii=False))
    else:
        print(json.dumps({
            "success": False,
            "error": error
        }, ensure_ascii=False))


def validate_modbus_args(args, partial=False):
    """校验 Modbus 参数边界，避免下发无效配置"""
    errors = []

    def check_range(field_name, value, min_val, max_val):
        if value is None:
            return
        if value < min_val or value > max_val:
            errors.append(f"{field_name} 必须在 {min_val}-{max_val} 之间（当前: {value}）")

    def check_positive(field_name, value):
        if value is None:
            return
        if value <= 0:
            errors.append(f"{field_name} 必须大于 0（当前: {value}）")

    # add-modbus 为必填，edit-modbus 为可选
    slave_addr = getattr(args, "slave_addr", None)
    function_code = getattr(args, "function_code", None)
    register_addr = getattr(args, "register_addr", None)
    register_num = getattr(args, "register_num", None)
    interval = getattr(args, "interval", None)
    timeout = getattr(args, "timeout", None)
    data_format = getattr(args, "data_format", None)
    report_format = getattr(args, "report_format", None)
    baud_rate = getattr(args, "baud_rate", None)
    data_bit = getattr(args, "data_bit", None)
    stop_bit = getattr(args, "stop_bit", None)
    check_bit = getattr(args, "check_bit", None)
    enabled = getattr(args, "enabled", None)

    if not partial or slave_addr is not None:
        check_range("slave-addr", slave_addr, 1, 247)
    if not partial or function_code is not None:
        check_range("function-code", function_code, 1, 6)
    if not partial or register_addr is not None:
        check_range("register-addr", register_addr, 0, 65535)
    if not partial or register_num is not None:
        check_range("register-num", register_num, 1, 125)
    if not partial or interval is not None:
        check_positive("interval", interval)
    if not partial or timeout is not None:
        check_positive("timeout", timeout)
    if not partial or baud_rate is not None:
        check_positive("baud-rate", baud_rate)

    if data_bit is not None and data_bit not in VALID_DATA_BITS:
        errors.append(f"data-bit 必须是 {sorted(VALID_DATA_BITS)} 之一（当前: {data_bit}）")

    if stop_bit is not None and str(stop_bit) not in VALID_STOP_BITS:
        errors.append(f"stop-bit 必须是 {sorted(VALID_STOP_BITS)} 之一（当前: {stop_bit}）")

    if check_bit is not None and check_bit not in VALID_CHECK_BITS:
        errors.append(f"check-bit 必须是 {sorted(VALID_CHECK_BITS)} 之一（当前: {check_bit}）")

    if enabled is not None and enabled not in (0, 1):
        errors.append(f"enabled 必须是 0 或 1（当前: {enabled}）")

    if data_format is not None and data_format not in VALID_DATA_FORMATS:
        errors.append(f"data-format 必须是 {sorted(VALID_DATA_FORMATS)} 之一（当前: {data_format}）")

    if report_format is not None and report_format not in VALID_REPORT_FORMATS:
        errors.append(f"report-format 必须是 {sorted(VALID_REPORT_FORMATS)} 之一（当前: {report_format}）")

    if errors:
        return "；".join(errors)
    return None


def cmd_add_modbus(args):
    """添加 Modbus 轮询项"""
    device_id = args.id

    validation_error = validate_modbus_args(args, partial=False)
    if validation_error:
        print(json.dumps({
            "success": False,
            "error": validation_error
        }, ensure_ascii=False))
        return

    # 读取本地缓存的配置
    current_items = get_modbus_items(device_id)

    # 检查是否超过上限
    if len(current_items) >= 50:  # MODBUS_ITEM_MAX
        print(json.dumps({
            "success": False,
            "error": "轮询项已达到上限 (50)，无法继续添加。请删除不需要的项。"
        }, ensure_ascii=False))
        return

    new_item = {
        "enabled": args.enabled,
        "slave_addr": str(args.slave_addr),
        "function_code": str(args.function_code),
        "register_addr": str(args.register_addr),
        "register_num": str(args.register_num),
        "timeout": str(args.timeout),
        "interval_time": str(args.interval),
        "data_format": args.data_format,
        "report_format": args.report_format,
        "baud_rate": str(args.baud_rate),
        "data_bit": str(args.data_bit),
        "stop_bit": str(args.stop_bit),
        "check_bit": args.check_bit
    }

    # 添加新项到现有配置
    updated_items = current_items + [new_item]

    # 发送完整配置（不是单个项）
    success, error = _send_config(device_id, {"modbus_items": updated_items})

    if success:
        # 更新本地缓存
        update_modbus_items(device_id, updated_items)

        print(json.dumps({
            "success": True,
            "message": f"Modbus 轮询项已添加 (索引 {len(current_items)})，设备将在 5-30 秒内重启",
            "warning": "⚠️ 关键信息：设备在修改配置时会重启。在此期间无法接收其他指令。",
            "item_index": len(current_items),
            "total_items": len(updated_items)
        }, ensure_ascii=False))
    else:
        print(json.dumps({
            "success": False,
            "error": error
        }, ensure_ascii=False))


def cmd_edit_modbus(args):
    """编辑 Modbus 轮询项"""
    device_id = args.id
    index = args.index

    validation_error = validate_modbus_args(args, partial=True)
    if validation_error:
        print(json.dumps({
            "success": False,
            "error": validation_error
        }, ensure_ascii=False))
        return

    # 读取本地缓存的配置
    current_items = get_modbus_items(device_id)

    # 检查索引是否有效
    if index < 0 or index >= len(current_items):
        print(json.dumps({
            "success": False,
            "error": f"索引无效: {index}（当前有 {len(current_items)} 个项）"
        }, ensure_ascii=False))
        return

    # 修改指定项
    item = current_items[index].copy()

    # 更新指定字段
    if args.slave_addr is not None:
        item["slave_addr"] = str(args.slave_addr)
    if args.function_code is not None:
        item["function_code"] = str(args.function_code)
    if args.register_addr is not None:
        item["register_addr"] = str(args.register_addr)
    if args.register_num is not None:
        item["register_num"] = str(args.register_num)
    if args.interval is not None:
        item["interval_time"] = str(args.interval)
    if args.timeout is not None:
        item["timeout"] = str(args.timeout)
    if args.data_format is not None:
        item["data_format"] = args.data_format
    if args.report_format is not None:
        item["report_format"] = args.report_format
    if args.baud_rate is not None:
        item["baud_rate"] = str(args.baud_rate)
    if args.data_bit is not None:
        item["data_bit"] = str(args.data_bit)
    if args.stop_bit is not None:
        item["stop_bit"] = str(args.stop_bit)
    if args.check_bit is not None:
        item["check_bit"] = args.check_bit
    if args.enabled is not None:
        item["enabled"] = args.enabled

    # 替换项
    updated_items = current_items.copy()
    updated_items[index] = item

    # 发送完整配置
    success, error = _send_config(device_id, {"modbus_items": updated_items})

    if success:
        # 更新本地缓存
        update_modbus_items(device_id, updated_items)

        print(json.dumps({
            "success": True,
            "message": f"Modbus 轮询项 (索引 {index}) 已编辑，设备将在 5-30 秒内重启",
            "warning": "⚠️ 关键信息：设备在修改配置时会重启。在此期间无法接收其他指令。",
            "item_index": index,
            "updated_item": item
        }, ensure_ascii=False))
    else:
        print(json.dumps({
            "success": False,
            "error": error
        }, ensure_ascii=False))


def cmd_remove_modbus(args):
    """删除 Modbus 轮询项"""
    device_id = args.id
    index = args.index

    # 读取本地缓存的配置
    current_items = get_modbus_items(device_id)

    # 检查索引是否有效
    if index < 0 or index >= len(current_items):
        print(json.dumps({
            "success": False,
            "error": f"索引无效: {index}（当前有 {len(current_items)} 个项）"
        }, ensure_ascii=False))
        return

    # 记录被删除的项
    removed_item = current_items[index]

    # 删除项
    updated_items = current_items[:index] + current_items[index+1:]

    # 发送完整配置
    success, error = _send_config(device_id, {"modbus_items": updated_items})

    if success:
        # 更新本地缓存
        update_modbus_items(device_id, updated_items)

        print(json.dumps({
            "success": True,
            "message": f"Modbus 轮询项 (索引 {index}) 已删除，设备将在 5-30 秒内重启",
            "warning": "⚠️ 关键信息：设备在修改配置时会重启。在此期间无法接收其他指令。",
            "removed_item_index": index,
            "removed_item": removed_item,
            "total_items": len(updated_items)
        }, ensure_ascii=False))
    else:
        print(json.dumps({
            "success": False,
            "error": error
        }, ensure_ascii=False))


# ============================================================================
# 主程序入口
# ============================================================================

def main():
    def int_range(min_value, max_value, field_name):
        def _validator(value):
            try:
                int_value = int(value)
            except ValueError as exc:
                raise argparse.ArgumentTypeError(f"{field_name} 必须是整数") from exc
            if int_value < min_value or int_value > max_value:
                raise argparse.ArgumentTypeError(
                    f"{field_name} 必须在 {min_value}-{max_value} 之间（当前: {int_value}）"
                )
            return int_value
        return _validator

    def positive_int(field_name):
        def _validator(value):
            try:
                int_value = int(value)
            except ValueError as exc:
                raise argparse.ArgumentTypeError(f"{field_name} 必须是整数") from exc
            if int_value <= 0:
                raise argparse.ArgumentTypeError(f"{field_name} 必须大于 0（当前: {int_value}）")
            return int_value
        return _validator

    parser = argparse.ArgumentParser(
        description="SP501LW 串口网关纯 MQTT 管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="命令")

    # ---- 设备管理命令 ----
    add_parser = subparsers.add_parser("add", help="添加设备")
    add_parser.add_argument("--id", required=True, help="设备标识")
    add_parser.add_argument("--cmd-topic", required=True, help="命令主题")
    add_parser.add_argument("--data-topic", required=True, help="数据主题")
    add_parser.add_argument("--broker-host", help=f"Broker 地址（默认: {DEFAULT_BROKER_HOST}）")
    add_parser.add_argument("--broker-port", type=int, help=f"Broker 端口（默认: {DEFAULT_BROKER_PORT}）")
    add_parser.add_argument("--username", help=f"用户名（默认: {DEFAULT_BROKER_USER}）")
    add_parser.add_argument("--password", help=f"密码（默认: {DEFAULT_BROKER_PASS}）")
    add_parser.set_defaults(func=cmd_add)

    list_parser = subparsers.add_parser("list", help="列出设备")
    list_parser.set_defaults(func=cmd_list)

    remove_parser = subparsers.add_parser("remove", help="删除设备")
    remove_parser.add_argument("--id", required=True, help="设备标识")
    remove_parser.set_defaults(func=cmd_remove)

    update_parser = subparsers.add_parser("update", help="更新设备信息")
    update_parser.add_argument("--id", required=True, help="设备标识")
    update_parser.add_argument("--cmd-topic", help="命令主题")
    update_parser.add_argument("--data-topic", help="数据主题")
    update_parser.add_argument("--broker-host", help="Broker 地址")
    update_parser.add_argument("--broker-port", type=int, help="Broker 端口")
    update_parser.add_argument("--username", help="用户名")
    update_parser.add_argument("--password", help="密码")
    update_parser.set_defaults(func=cmd_update)

    # ---- 工作模式命令 ----
    mode_parser = subparsers.add_parser("set-mode", help="切换工作模式")
    mode_parser.add_argument("mode", choices=["mqtt_tcp", "modbus_tcp", "modbus_rtu"], help="工作模式")
    mode_parser.add_argument("--id", required=True, help="设备标识")
    mode_parser.set_defaults(func=cmd_set_mode)

    # ---- 串口透传命令 ----
    send_parser = subparsers.add_parser("send", help="发送串口数据")
    send_parser.add_argument("--id", required=True, help="设备标识")
    send_parser.add_argument("--data", required=True, help="数据内容")
    send_parser.add_argument("--format", choices=["text", "hex"], default="text", help="数据格式")
    send_parser.set_defaults(func=cmd_send)

    listen_parser = subparsers.add_parser("listen", help="监听设备数据")
    listen_parser.add_argument("--id", required=True, help="设备标识")
    listen_parser.add_argument("--timeout", type=int, default=60, help="超时时间（秒）")
    listen_parser.add_argument("--format", choices=["text", "hex", "json"], default="hex", help="数据格式")
    listen_parser.set_defaults(func=cmd_listen)

    # ---- Modbus 配置命令 ----
    poll_parser = subparsers.add_parser("set-poll-time", help="设置轮询周期")
    poll_parser.add_argument("poll_time", type=int, help="轮询周期（毫秒）")
    poll_parser.add_argument("--id", required=True, help="设备标识")
    poll_parser.set_defaults(func=cmd_set_poll_time)

    # ---- 串口参数命令 ----
    serial_parser = subparsers.add_parser("set-serial", help="设置串口参数")
    serial_parser.add_argument("--id", required=True, help="设备标识")
    serial_parser.add_argument(
        "--baud-rate",
        type=int,
        choices=sorted(VALID_SERIAL_BAUD_RATES),
        help="波特率",
    )
    serial_parser.add_argument("--data-bit", type=int, choices=sorted(VALID_DATA_BITS), help="数据位")
    serial_parser.add_argument("--stop-bit", type=str, choices=sorted(VALID_STOP_BITS), help="停止位")
    serial_parser.add_argument("--check-bit", choices=sorted(VALID_CHECK_BITS), help="校验位")
    serial_parser.add_argument("--frame-time", type=positive_int("帧间隔"), help="帧间隔（毫秒）")
    serial_parser.add_argument("--frame-len", type=positive_int("帧长度"), help="帧长度（字节）")
    serial_parser.set_defaults(func=cmd_set_serial)

    add_modbus_parser = subparsers.add_parser("add-modbus", help="添加 Modbus 轮询项")
    add_modbus_parser.add_argument("--id", required=True, help="设备标识")
    add_modbus_parser.add_argument("--slave-addr", type=int_range(1, 247, "从站地址"), required=True, help="从站地址（1-247）")
    add_modbus_parser.add_argument("--function-code", type=int_range(1, 6, "功能码"), required=True, help="功能码（1-6）")
    add_modbus_parser.add_argument("--register-addr", type=int_range(0, 65535, "起始寄存器地址"), required=True, help="起始寄存器地址")
    add_modbus_parser.add_argument("--register-num", type=int_range(1, 125, "读取数量"), required=True, help="读取数量")
    add_modbus_parser.add_argument("--interval", type=positive_int("轮询间隔"), required=True, help="轮询间隔（毫秒）")
    add_modbus_parser.add_argument("--timeout", type=positive_int("响应超时"), default=1000, help="响应超时（毫秒）")
    add_modbus_parser.add_argument("--data-format", default="Unsigned", choices=sorted(VALID_DATA_FORMATS), help="数据格式")
    add_modbus_parser.add_argument("--report-format", default="mqtt", choices=sorted(VALID_REPORT_FORMATS), help="上报方式")
    add_modbus_parser.add_argument("--baud-rate", type=positive_int("波特率"), default=9600, help="波特率")
    add_modbus_parser.add_argument("--data-bit", type=int, choices=sorted(VALID_DATA_BITS), default=8, help="数据位")
    add_modbus_parser.add_argument("--stop-bit", type=str, choices=sorted(VALID_STOP_BITS), default="1", help="停止位")
    add_modbus_parser.add_argument("--check-bit", choices=sorted(VALID_CHECK_BITS), default="None", help="校验位")
    add_modbus_parser.add_argument("--enabled", type=int, choices=[0, 1], default=1, help="是否启用")
    add_modbus_parser.set_defaults(func=cmd_add_modbus)

    edit_modbus_parser = subparsers.add_parser("edit-modbus", help="编辑 Modbus 轮询项")
    edit_modbus_parser.add_argument("--id", required=True, help="设备标识")
    edit_modbus_parser.add_argument("--index", type=int, required=True, help="项目索引（0-49）")
    edit_modbus_parser.add_argument("--slave-addr", type=int_range(1, 247, "从站地址"), help="从站地址（1-247）")
    edit_modbus_parser.add_argument("--function-code", type=int_range(1, 6, "功能码"), help="功能码（1-6）")
    edit_modbus_parser.add_argument("--register-addr", type=int_range(0, 65535, "起始寄存器地址"), help="起始寄存器地址")
    edit_modbus_parser.add_argument("--register-num", type=int_range(1, 125, "读取数量"), help="读取数量")
    edit_modbus_parser.add_argument("--interval", type=positive_int("轮询间隔"), help="轮询间隔（毫秒）")
    edit_modbus_parser.add_argument("--timeout", type=positive_int("响应超时"), help="响应超时（毫秒）")
    edit_modbus_parser.add_argument("--data-format", choices=sorted(VALID_DATA_FORMATS), help="数据格式")
    edit_modbus_parser.add_argument("--report-format", choices=sorted(VALID_REPORT_FORMATS), help="上报方式")
    edit_modbus_parser.add_argument("--baud-rate", type=positive_int("波特率"), help="波特率")
    edit_modbus_parser.add_argument("--data-bit", type=int, choices=sorted(VALID_DATA_BITS), help="数据位")
    edit_modbus_parser.add_argument("--stop-bit", type=str, choices=sorted(VALID_STOP_BITS), help="停止位")
    edit_modbus_parser.add_argument("--check-bit", choices=sorted(VALID_CHECK_BITS), help="校验位")
    edit_modbus_parser.add_argument("--enabled", type=int, choices=[0, 1], help="是否启用")
    edit_modbus_parser.set_defaults(func=cmd_edit_modbus)

    remove_modbus_parser = subparsers.add_parser("remove-modbus", help="删除 Modbus 轮询项")
    remove_modbus_parser.add_argument("--id", required=True, help="设备标识")
    remove_modbus_parser.add_argument("--index", type=int, required=True, help="项目索引（0-49）")
    remove_modbus_parser.set_defaults(func=cmd_remove_modbus)

    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
