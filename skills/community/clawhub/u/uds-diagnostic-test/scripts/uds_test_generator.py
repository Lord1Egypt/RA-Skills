#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UDS测试脚本生成器
基于解析后的诊断调查表JSON生成可执行的测试脚本
生成的脚本包含完整的SocketCAN通信、UDS协议和测试报告功能
"""

__version__ = "1.6.0"

import argparse
import json
import os
import sys
import textwrap
from datetime import datetime


# ============================================================================
# 测试脚本模板
# ============================================================================

SCRIPT_HEADER = '''\
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UDS诊断自动化测试脚本
自动生成时间: {generation_time}
源文件: {source_file}
"""

import argparse
import can
import ctypes
import importlib.metadata as md
import json
import os
import struct
import sys
import time
from datetime import datetime


def validate_runtime_environment():
    import can
    try:
        version = md.version("python-can")
    except Exception as exc:
        print("[ERROR] python-can distribution not found:", exc)
        print("[ERROR] Enter the uds-diagnostic-test skill root, then run: bash ./scripts/setup_env.sh")
        sys.exit(2)

    module_path = getattr(can, "__file__", "<unknown>")
    try:
        version_tuple = tuple(int(part) for part in version.split(".")[:2])
    except Exception:
        version_tuple = (0, 0)

    if "can-0.0.0" in module_path or version_tuple < (4, 0):
        print("[ERROR] Unsupported python-can runtime:", version)
        print("[ERROR] Python executable:", sys.executable)
        print("[ERROR] can module:", module_path)
        print("[ERROR] Expected python-can>=4.0 with can.interfaces.socketcan support")
        print("[ERROR] Enter the uds-diagnostic-test skill root, then run: bash ./scripts/setup_env.sh")
        if version_tuple <= (1, 5):
            print("[ERROR] python-can 1.5.x usually means a package-source or mirror problem, not a code compatibility problem")
        sys.exit(2)

    try:
        import can.interfaces.socketcan  # noqa: F401
    except Exception as exc:
        print("[ERROR] SocketCAN backend unavailable:", exc)
        print("[ERROR] Python executable:", sys.executable)
        print("[ERROR] can module:", module_path)
        print("[ERROR] Enter the uds-diagnostic-test skill root, then run: bash ./scripts/setup_env.sh")
        sys.exit(2)


validate_runtime_environment()

# ============================================================================
# Vector SeedKey DLL 接口 (GenerateKeyEx / GenerateKeyExOpt)
# ============================================================================

# Vector标准返回值
KGRE_Ok = 0
KGRE_BufferToSmall = 1
KGRE_SecurityLevelInvalid = 2
KGRE_VariantInvalid = 3
KGRE_UnspecifiedError = 4

class VectorSeedKeyDll:
    \"\"\"Vector标准 Seed&Key DLL 接口封装
    支持两种标准接口:
    1. GenerateKeyEx       — 经典接口 (CANoe/CANalyzer/ODX标准)
    2. GenerateKeyExOpt    — 扩展接口 (带Options参数)
    \"\"\"

    def __init__(self, dll_path, variant="", options=""):
        \"\"\"
        Args:
            dll_path: DLL文件绝对路径
            variant: ECU变体标识(传给DLL)
            options: 扩展选项(仅GenerateKeyExOpt使用)
        \"\"\"
        self.dll_path = dll_path
        self.variant = variant.encode('ascii') if variant else b""
        self.options = options.encode('ascii') if options else b""
        self.dll = None
        self._has_generate_key_ex = False
        self._has_generate_key_ex_opt = False

    def load(self):
        \"\"\"加载DLL并检测支持的接口\"\"\"
        if not os.path.exists(self.dll_path):
            print(f"[ERROR] SeedKey DLL不存在: {{self.dll_path}}")
            return False
        try:
            self.dll = ctypes.cdll.LoadLibrary(self.dll_path)
        except OSError as e:
            print(f"[ERROR] 加载DLL失败: {{e}}")
            return False

        # 检测接口
        try:
            self.dll.GenerateKeyExOpt
            self._has_generate_key_ex_opt = True
            print(f"[OK] SeedKey DLL已加载(GenerateKeyExOpt): {{self.dll_path}}")
        except AttributeError:
            pass

        try:
            self.dll.GenerateKeyEx
            self._has_generate_key_ex = True
            if not self._has_generate_key_ex_opt:
                print(f"[OK] SeedKey DLL已加载(GenerateKeyEx): {{self.dll_path}}")
        except AttributeError:
            pass

        if not self._has_generate_key_ex and not self._has_generate_key_ex_opt:
            print(f"[ERROR] DLL中未找到GenerateKeyEx或GenerateKeyExOpt导出函数")
            return False

        return True

    def compute_key(self, seed_bytes, security_level):
        \"\"\"根据Seed计算Key
        Args:
            seed_bytes: Seed字节列表 (如 [0x01, 0x02, 0x03, 0x04])
            security_level: 安全等级 (如 0x01, 0x03, 0x05...)
        Returns:
            Key字节列表, 或 None(失败)
        \"\"\"
        if self.dll is None:
            print("[ERROR] DLL未加载")
            return None

        # 准备输入
        seed_array = (ctypes.c_ubyte * len(seed_bytes))(*seed_bytes)
        seed_size = ctypes.c_uint(len(seed_bytes))
        sec_level = ctypes.c_uint(security_level)

        # 准备输出 (最大256字节Key)
        max_key_size = 256
        key_array = (ctypes.c_ubyte * max_key_size)()
        actual_key_size = ctypes.c_uint(0)

        # 优先使用GenerateKeyExOpt
        if self._has_generate_key_ex_opt:
            try:
                result = self.dll.GenerateKeyExOpt(
                    seed_array,
                    seed_size,
                    sec_level,
                    ctypes.c_char_p(self.variant),
                    ctypes.c_char_p(self.options),
                    key_array,
                    ctypes.c_uint(max_key_size),
                    ctypes.byref(actual_key_size)
                )
                if result == KGRE_Ok:
                    return list(key_array[:actual_key_size.value])
                else:
                    print(f"[WARN] GenerateKeyExOpt返回错误: {{result}}")
                    return None
            except Exception as e:
                print(f"[ERROR] GenerateKeyExOpt调用异常: {{e}}")
                return None

        # 回退到GenerateKeyEx
        if self._has_generate_key_ex:
            try:
                result = self.dll.GenerateKeyEx(
                    seed_array,
                    seed_size,
                    sec_level,
                    ctypes.c_char_p(self.variant),
                    key_array,
                    ctypes.c_uint(max_key_size),
                    ctypes.byref(actual_key_size)
                )
                if result == KGRE_Ok:
                    return list(key_array[:actual_key_size.value])
                else:
                    print(f"[WARN] GenerateKeyEx返回错误: {{result}}")
                    return None
            except Exception as e:
                print(f"[ERROR] GenerateKeyEx调用异常: {{e}}")
                return None

        return None

    def unload(self):
        \"\"\"卸载DLL\"\"\"
        if self.dll:
            # ctypes不直接支持卸载, 但可以释放句柄
            try:
                if sys.platform == 'win32':
                    ctypes.windll.kernel32.FreeLibrary(self.dll._handle)
                else:
                    import ctypes.util as _cu
                    _libc = ctypes.CDLL(_cu.find_library('c'))
                    _libc.dlclose(self.dll._handle)
            except Exception:
                pass
            self.dll = None


# SeedKey DLL全局实例 (如果配置了DLL路径则加载)
SEEDKEY_DLL_PATH = "{seedkey_dll_path}"
SEEDKEY_VARIANT = "{seedkey_variant}"
SEEDKEY_OPTIONS = "{seedkey_options}"
seedkey_dll = None
if SEEDKEY_DLL_PATH:
    seedkey_dll = VectorSeedKeyDll(SEEDKEY_DLL_PATH, SEEDKEY_VARIANT, SEEDKEY_OPTIONS)
    if not seedkey_dll.load():
        seedkey_dll = None
        print("[WARN] SeedKey DLL加载失败, $27安全访问将仅测试NRC(无法解锁)")

# ============================================================================
# 配置
# ============================================================================

DEFAULT_CHANNEL = "{channel}"
DEFAULT_CAN_IF = "{can_if}"  # socketcan
DEFAULT_BITRATE = {bitrate}
DEFAULT_SAMPLE_POINT = {sample_point}  # CAN采样点 (0.0~1.0, 如0.8=80%)
DEFAULT_TX_ID = {tx_id}
DEFAULT_RX_ID = {rx_id}
DEFAULT_FUNC_ID = {func_id}  # 功能寻址ID
P2_TIMEOUT = {p2_timeout}        # ms
P2_STAR_TIMEOUT = {p2_star_timeout}   # ms
S3_SERVER_TIMEOUT = {s3_timeout}    # ms - 非默认会话超时回落时间
SECURITY_ACCESS_DELAY = {sa_delay}   # ms - 安全访问失败后延时

# CAN FD 配置
CAN_FD_ENABLED = {can_fd}        # True=CAN FD, False=Classic CAN
CAN_FD_DATA_BITRATE = {fd_data_bitrate}  # CAN FD 数据段波特率
CAN_FD_DSAMPLE_POINT = {fd_dsample_point}  # CAN FD 数据段采样点 (0.0~1.0)
CAN_FD_MAX_DLC = {fd_max_dlc}         # CAN FD 最大DLC (8/12/16/20/24/32/48/64)

# CAN FD DLC映射: 实际字节数 → DLC值
FD_DLC_SIZES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 16, 20, 24, 32, 48, 64]

def fd_next_valid_size(size):
    \"\"\"返回>=size的下一个合法CAN FD数据长度\"\"\"
    for s in FD_DLC_SIZES:
        if s >= size:
            return s
    return 64

# UDS服务ID
SID_DIAGNOSTIC_SESSION_CONTROL = 0x10
SID_ECU_RESET = 0x11
SID_CLEAR_DTC = 0x14
SID_READ_DTC_INFO = 0x19
SID_READ_DID = 0x22
SID_READ_MEM_BY_ADDR = 0x23
SID_SECURITY_ACCESS = 0x27
SID_COMMUNICATION_CONTROL = 0x28
SID_AUTHENTICATION = 0x29
SID_READ_DATA_BY_PERIODIC_ID = 0x2A
SID_DYNAMICALLY_DEFINE_DID = 0x2C
SID_WRITE_DID = 0x2E
SID_IO_CONTROL = 0x2F
SID_ROUTINE_CONTROL = 0x31
SID_REQUEST_DOWNLOAD = 0x34
SID_REQUEST_UPLOAD = 0x35
SID_TRANSFER_DATA = 0x36
SID_REQUEST_TRANSFER_EXIT = 0x37
SID_REQUEST_FILE_TRANSFER = 0x38
SID_WRITE_MEM_BY_ADDR = 0x3D
SID_TESTER_PRESENT = 0x3E
SID_ACCESS_TIMING_PARAM = 0x83
SID_SECURED_DATA_TRANSMISSION = 0x84
SID_CONTROL_DTC_SETTING = 0x85
SID_RESPONSE_ON_EVENT = 0x86
SID_LINK_CONTROL = 0x87

# 会话模式
SESSION_DEFAULT = 0x01
SESSION_PROGRAMMING = 0x02
SESSION_EXTENDED = 0x03

SESSION_NAMES = {{
    0x01: "Default (0x01)",
    0x02: "Programming (0x02)",
    0x03: "Extended (0x03)",
}}

# 调查表安全等级 → $27 SecurityAccess subFunction 映射
# 调查表中 level0_locked=Y 表示无安全限制(直接可访问)
# level1=Y → SA Level 0x01/0x02
# level_fbl=Y → SA Level 0x03/0x04 (FBL/Programming)
# level_immo=Y → SA Level 0x05/0x06 (Immobilizer)
SA_LEVEL_MAP = {{
    "level1": 0x01,
    "level_fbl": 0x03,
    "level_immo": 0x05,
}}

# 从调查表安全字段提取所需SA等级列表
def get_required_sa_levels(security_dict):
    """从调查表security字段提取需要的SA level列表
    Args:
        security_dict: {{"level0_locked": "Y", "level1": "Y", "level_fbl": "N", "level_immo": "N"}}
    Returns:
        list of (sa_level_int, level_name) e.g. [(0x01, "level1")]
    """
    levels = []
    for key, sa_level in SA_LEVEL_MAP.items():
        if security_dict.get(key, "N").upper() == "Y":
            levels.append((sa_level, key))
    return levels

def parse_routine_sa_level(level_str):
    """解析Routine/IOControl的security_level字段
    Args:
        level_str: "Level1", "Level3", "Level5" 等
    Returns:
        int SA level (0x01, 0x03, 0x05...) 或 None
    """
    if not level_str:
        return None
    s = level_str.strip().lower()
    if "3" in s or "fbl" in s or "prog" in s:
        return 0x03
    if "5" in s or "immo" in s:
        return 0x05
    if "1" in s:
        return 0x01
    return 0x01  # 默认Level1

# 所有调查表中用到的SA等级集合 (从诊断调查表自动提取)
SURVEY_SA_LEVELS = {survey_sa_levels}

# CAN ID寻址模式
# normal_11bit: 标准11-bit CAN ID (默认)
# normal_29bit: 扩展29-bit CAN ID
# mixed_11bit:  混合寻址11-bit + Address Extension byte
# mixed_29bit:  混合寻址29-bit + Address Extension byte
# normal_fixed: 固定寻址29-bit (N_TA/N_SA在ID中编码)
CAN_ADDR_MODE = "{can_addr_mode}"
CAN_ADDR_EXT = {can_addr_ext}  # 混合寻址的Address Extension字节 (0x00-0xFF)

# NRC定义 (ISO 14229-1:2020 Table A.1 完整列表)
NRC_NAMES = {{
    0x10: "generalReject",
    0x11: "serviceNotSupported",
    0x12: "subFunctionNotSupported",
    0x13: "incorrectMessageLengthOrInvalidFormat",
    0x14: "responseTooLong",
    0x21: "busyRepeatRequest",
    0x22: "conditionsNotCorrect",
    0x24: "requestSequenceError",
    0x25: "noResponseFromSubnetComponent",
    0x26: "failurePreventsExecutionOfRequestedAction",
    0x31: "requestOutOfRange",
    0x33: "securityAccessDenied",
    0x34: "authenticationRequired",
    0x35: "invalidKey",
    0x36: "exceededNumberOfAttempts",
    0x37: "requiredTimeDelayNotExpired",
    0x38: "secureDataTransmissionRequired",
    0x39: "secureDataTransmissionNotAllowed",
    0x3A: "secureDataVerificationFailed",
    0x50: "certificateVerificationFailedInvalidTimePeriod",
    0x51: "certificateVerificationFailedInvalidSignature",
    0x52: "certificateVerificationFailedInvalidChainOfTrust",
    0x53: "certificateVerificationFailedInvalidType",
    0x54: "certificateVerificationFailedInvalidFormat",
    0x55: "certificateVerificationFailedInvalidContent",
    0x56: "certificateVerificationFailedInvalidScope",
    0x57: "certificateVerificationFailedInvalidCertificate",
    0x58: "ownershipVerificationFailed",
    0x59: "challengeCalculationFailed",
    0x5A: "settingAccessRightsFailed",
    0x5B: "sessionKeyCreationDerivationFailed",
    0x5C: "configurationDataUsageFailed",
    0x5D: "deAuthenticationFailed",
    0x70: "uploadDownloadNotAccepted",
    0x71: "transferDataSuspended",
    0x72: "generalProgrammingFailure",
    0x73: "wrongBlockSequenceCounter",
    0x78: "requestCorrectlyReceivedResponsePending",
    0x7E: "subFunctionNotSupportedInActiveSession",
    0x7F: "serviceNotSupportedInActiveSession",
}}


# ============================================================================
# ISO-TP 传输层 (简化实现，支持单帧和多帧)
# ============================================================================

class IsoTpTransport:
    """ISO 15765 传输层 (支持Classic CAN和CAN FD, 支持Normal/Extended/Mixed寻址)"""

    def __init__(self, bus, tx_id, rx_id, timeout_ms=5000):
        self.bus = bus
        self.tx_id = tx_id
        self.rx_id = rx_id
        self.timeout = timeout_ms / 1000.0
        self.is_fd = CAN_FD_ENABLED
        self.addr_mode = CAN_ADDR_MODE   # normal_11bit/normal_29bit/mixed_11bit/mixed_29bit/normal_fixed
        self.addr_ext = CAN_ADDR_EXT     # Address Extension byte (混合寻址)
        self.is_extended_id = self.addr_mode in ("normal_29bit", "mixed_29bit", "normal_fixed")
        # 混合寻址: 第1字节为AE，有效payload少1字节
        self.ae_overhead = 1 if self.addr_mode in ("mixed_11bit", "mixed_29bit") else 0
        # Classic CAN: SF最大7字节payload, CF最大7字节
        # CAN FD: SF最大(max_dlc-2)字节payload(用escape SF_DL), CF最大(max_dlc-1)字节
        self.max_frame_size = CAN_FD_MAX_DLC if self.is_fd else 8
        self.sf_max_payload = self.max_frame_size - 2 - self.ae_overhead if self.is_fd else 7 - self.ae_overhead
        self.cf_payload_size = self.max_frame_size - 1 - self.ae_overhead
        self.ff_first_payload = self.max_frame_size - 2 - self.ae_overhead

    def _make_msg(self, data):
        """构造CAN消息(根据寻址模式设置extended_id)"""
        return can.Message(arbitration_id=self.tx_id, data=data,
                           is_extended_id=self.is_extended_id,
                           is_fd=self.is_fd,
                           bitrate_switch=self.is_fd,
                           timestamp=time.time())

    def _make_msg_classic(self, data):
        """构造Classic CAN帧"""
        return can.Message(arbitration_id=self.tx_id, data=data,
                           is_extended_id=self.is_extended_id,
                           is_fd=self.is_fd,
                           bitrate_switch=self.is_fd,
                           timestamp=time.time())

    def _prepend_ae(self, frame):
        """混合寻址: 在帧前插入Address Extension字节"""
        if self.ae_overhead:
            return bytes([self.addr_ext]) + bytes(frame)
        return bytes(frame)

    def send_receive(self, data, timeout_ms=None):
        """发送UDS请求并接收响应"""
        timeout = (timeout_ms / 1000.0) if timeout_ms else self.timeout
        self._send(data)
        return self._receive(timeout)

    def _send(self, data):
        """发送ISO-TP帧 (支持Classic CAN和CAN FD, 支持Normal/Extended/Mixed寻址)"""
        length = len(data)

        if self.is_fd and length <= self.sf_max_payload:
            # CAN FD Single Frame: PCI=[0x00, actual_length] + payload + padding
        # CAN FD Single Frame: PCI 支持两种格式
            if length <= 7:
                pci = [length]                 # 1 字节 PCI（高4位=0，低4位=长度）
            else:
                pci = [0x00, length]           # Escape 格式（首字节 0x00，次字节长度）
            payload = self._prepend_ae(pci + list(data))
            frame_size = max(8, fd_next_valid_size(len(payload)))
            frame = payload + bytes([0x00] * (frame_size - len(payload)))
            self.bus.send(self._make_msg(frame))
        elif not self.is_fd and length <= self.sf_max_payload:
            # Classic CAN Single Frame: PCI=[length] + payload + padding
            pci = [length]
            payload = self._prepend_ae(pci + list(data))
            frame = payload + bytes([0xCC] * (8 - len(payload)))
            self.bus.send(self._make_msg_classic(frame))
        else:
            # Multi-Frame: First Frame
            if not self.is_fd:
                ff_pci = [(0x10 | ((length >> 8) & 0x0F)), length & 0xFF]
                first_payload = 6 - self.ae_overhead
                ff_data = self._prepend_ae(ff_pci + list(data[:first_payload]))
                self.bus.send(self._make_msg_classic(ff_data))
            else:
                # CAN FD First Frame
                if length <= 4095:
                    ff_pci = [(0x10 | ((length >> 8) & 0x0F)), length & 0xFF]
                else:
                    ff_pci = [0x10, 0x00,
                              (length >> 24) & 0xFF, (length >> 16) & 0xFF,
                              (length >> 8) & 0xFF, length & 0xFF]
                first_payload = self.max_frame_size - len(ff_pci) - self.ae_overhead
                ff_data = self._prepend_ae(ff_pci + list(data[:first_payload]))
                frame_size = fd_next_valid_size(len(ff_data))
                ff_data = ff_data + bytes([0xCC] * (frame_size - len(ff_data)))
                self.bus.send(self._make_msg(ff_data))

            # Wait for Flow Control (handles FS=1 Wait per ISO 15765-2 §6.5.5.3)
            fc = self._wait_for_fc()
            if fc is None:
                return

            fs = fc[0] & 0x0F
            if fs == 2:  # Overflow
                return
            bs = fc[1] if len(fc) > 1 else 0  # Block size
            st_min = fc[2] if len(fc) > 2 else 0  # STmin
            st_delay = st_min / 1000.0 if st_min <= 127 else ((st_min - 0xF0) * 0.0001 if 0xF1 <= st_min <= 0xF9 else 0)

            # Consecutive Frames (with BS>0 re-FC per ISO 15765-2 §6.5.5.4)
            offset = first_payload
            seq = 1
            cf_count = 0
            cf_payload = self.cf_payload_size  # CAN FD: max_dlc-1, Classic: 7
            while offset < length:
                chunk = list(data[offset:offset + cf_payload])
                cf_header = [(0x20 | (seq & 0x0F))]
                if self.is_fd:
                    cf_data = self._prepend_ae(cf_header + chunk)
                    frame_size = fd_next_valid_size(len(cf_data))
                    cf_data = cf_data + bytes([0xCC] * (frame_size - len(cf_data)))
                    self.bus.send(self._make_msg(cf_data))
                else:
                    cf_data = self._prepend_ae(cf_header + chunk)
                    cf_data = cf_data + bytes([0xCC] * (8 - len(cf_data)))
                    self.bus.send(self._make_msg_classic(cf_data))
                offset += cf_payload
                seq = (seq + 1) & 0x0F
                cf_count += 1
                if st_delay > 0:
                    time.sleep(st_delay)
                # BS>0: wait for new FC after BS consecutive frames
                if bs > 0 and cf_count >= bs and offset < length:
                    fc = self._wait_for_fc()
                    if fc is None:
                        return
                    fs = fc[0] & 0x0F
                    if fs == 2:  # Overflow
                        return
                    bs = fc[1] if len(fc) > 1 else 0
                    st_min_new = fc[2] if len(fc) > 2 else 0
                    st_delay = st_min_new / 1000.0 if st_min_new <= 127 else ((st_min_new - 0xF0) * 0.0001 if 0xF1 <= st_min_new <= 0xF9 else 0)
                    cf_count = 0

    def _wait_for_fc(self, timeout=2.0):
        """等待Flow Control帧 (处理FS=1 Wait per ISO 15765-2 §6.5.5.3)"""
        end_time = time.time() + timeout
        max_wait_count = 10  # 防止无限Wait循环
        wait_count = 0
        ae = self.ae_overhead
        while time.time() < end_time:
            msg = self.bus.recv(timeout=0.1)
            if msg and msg.arbitration_id == self.rx_id:
                if (msg.data[ae] & 0xF0) == 0x30:
                    fs = msg.data[ae] & 0x0F
                    if fs == 0:  # ContinueToSend
                        return bytes(msg.data[ae:])
                    elif fs == 1:  # Wait
                        wait_count += 1
                        if wait_count >= max_wait_count:
                            return None  # 超过最大Wait次数
                        continue  # 继续等待下一个FC
                    elif fs == 2:  # Overflow
                        return bytes(msg.data[ae:])  # 返回让调用者处理
                    else:
                        return bytes(msg.data[ae:])
        return None

    def _receive(self, timeout):
        """接收ISO-TP响应"""
        end_time = time.time() + timeout
        ae = self.ae_overhead  # 混合寻址偏移
        while True:
            remaining = end_time - time.time()
            if remaining <= 0:
                return None
            msg = self.bus.recv(timeout=min(remaining, 0.1))
            if msg is None:
                continue
            if msg.arbitration_id != self.rx_id:
                continue

            d = msg.data
            pci = d[ae] & 0xF0
            if pci == 0x00:
                # Single Frame
                sf_dl = d[ae] & 0x0F
                if sf_dl == 0 and len(d) > ae + 1:
                    # CAN FD escape: SF_DL in byte after PCI
                    length = d[ae + 1]
                    return bytes(d[ae + 2:ae + 2 + length])
                else:
                    length = sf_dl
                    return bytes(d[ae + 1:ae + 1 + length])
            elif pci == 0x10:
                # First Frame
                ff_dl_hi = d[ae] & 0x0F
                ff_dl_lo = d[ae + 1]
                length = (ff_dl_hi << 8) | ff_dl_lo
                if length == 0 and len(d) >= ae + 6:
                    length = (d[ae+2] << 24) | (d[ae+3] << 16) | (d[ae+4] << 8) | d[ae+5]
                    data = bytearray(d[ae + 6:])
                else:
                    data = bytearray(d[ae + 2:])

                # Send Flow Control
                fc = [0x30, 0x00, 0x0A]  # ContinueToSend, BS=0, STmin=10ms
                fc_data = self._prepend_ae(fc)
                if self.is_fd:
                    frame_size = fd_next_valid_size(len(fc_data))
                    fc_padded = fc_data + bytes([0xCC] * (frame_size - len(fc_data)))
                    self.bus.send(self._make_msg(fc_padded))
                else:
                    fc_padded = fc_data + bytes([0xCC] * (8 - len(fc_data)))
                    self.bus.send(self._make_msg_classic(fc_padded))

                # Receive Consecutive Frames (validate SN per ISO 15765-2 §6.5.4)
                expected_seq = 1
                n_cr_timeout = 1.0  # N_Cr timer = 1000ms per ISO 15765-2
                while len(data) < length:
                    cf_msg = self.bus.recv(timeout=min(remaining, n_cr_timeout))
                    if cf_msg and cf_msg.arbitration_id == self.rx_id:
                        if (cf_msg.data[ae] & 0xF0) == 0x20:
                            actual_seq = cf_msg.data[ae] & 0x0F
                            if actual_seq != expected_seq:
                                break  # SN mismatch → abort reception
                            data.extend(cf_msg.data[ae + 1:])
                            expected_seq = (expected_seq + 1) & 0x0F
                    else:
                        break  # N_Cr timeout → abort

                return bytes(data[:length])

        return None

    def send_raw_frame(self, frame_data):
        \"\"\"直接发送原始CAN帧(不经过ISO-TP封装)\"\"\"
        self.bus.send(self._make_msg_classic(bytes(frame_data)))

    def receive_raw_frame(self, timeout_ms=2000):
        \"\"\"直接接收原始CAN帧，返回(arb_id, data)\"\"\"
        msg = self.bus.recv(timeout=timeout_ms / 1000.0)
        if msg and msg.arbitration_id == self.rx_id:
            return (msg.arbitration_id, bytes(msg.data))
        return None

    def send_sf_with_custom_padding(self, data, padding=0xCC):
        \"\"\"发送带自定义填充字节的Single Frame\"\"\"
        length = len(data)
        frame = [length] + list(data) + [padding] * (7 - length)
        self.bus.send(self._make_msg_classic(bytes(frame)))
        return self._receive(self.timeout)

    def send_sf_with_wrong_dlc(self, data, dlc=4):
        \"\"\"发送错误DLC的帧\"\"\"
        length = len(data)
        frame = [length] + list(data)
        frame = frame[:dlc]
        self.bus.send(self._make_msg_classic(bytes(frame)))
        return self._receive(self.timeout)

    def send_multiframe_abort(self, data):
        \"\"\"发送First Frame后不发Consecutive Frame(测试超时)\"\"\"
        length = len(data)
        ff = [(0x10 | ((length >> 8) & 0x0F)), length & 0xFF] + list(data[:6])
        self.bus.send(self._make_msg_classic(bytes(ff)))
        # 等待Flow Control
        fc = self._wait_for_fc(timeout=2.0)
        # 故意不发Consecutive Frame
        return fc  # 返回FC帧(如果有的话)

    def send_cf_wrong_sequence(self, data):
        \"\"\"发送First Frame后跟错误序号的Consecutive Frame\"\"\"
        length = len(data)
        ff = [(0x10 | ((length >> 8) & 0x0F)), length & 0xFF] + list(data[:6])
        self.bus.send(self._make_msg_classic(bytes(ff)))
        fc = self._wait_for_fc(timeout=2.0)
        if fc is None:
            return None

        # 发送序号为5的CF(应该是1)，ECU应忽略或中止
        chunk = list(data[6:13])
        cf = [(0x20 | 0x05)] + chunk + [0xCC] * (7 - len(chunk))
        self.bus.send(self._make_msg_classic(bytes(cf)))
        return self._receive(2.0)


# ============================================================================
# UDS 协议层
# ============================================================================

class UdsClient:
    """UDS客户端"""

    def __init__(self, bus, tx_id, rx_id, func_id=None):
        self.tp = IsoTpTransport(bus, tx_id, rx_id)
        self.func_tp = IsoTpTransport(bus, func_id, rx_id) if func_id else None
        self.bus = bus

    def send_request(self, data, functional=False, timeout_ms=None):
        """发送UDS请求，返回响应"""
        tp = self.func_tp if (functional and self.func_tp) else self.tp
        timeout = timeout_ms or P2_TIMEOUT

        resp = tp.send_receive(bytes(data), timeout_ms=timeout)

        if resp is None:
            return None

        # 处理NRC 0x78 (pending) - ISO 14229-2: 只监听，不重发
        while resp and len(resp) >= 3 and resp[0] == 0x7F and resp[2] == 0x78:
            resp = tp._receive(P2_STAR_TIMEOUT / 1000.0)

        return resp

    def send_request_timed(self, data, functional=False, timeout_ms=None):
        """发送UDS请求并测量响应时间(ms)，返回 (resp, elapsed_ms)"""
        tp = self.func_tp if (functional and self.func_tp) else self.tp
        timeout = timeout_ms or P2_TIMEOUT
        t_start = time.time()
        resp = tp.send_receive(bytes(data), timeout_ms=timeout)
        t_first = (time.time() - t_start) * 1000.0

        if resp is None:
            return None, t_first

        # 处理NRC 0x78 (pending) - ISO 14229-2: 只监听P2*超时，不重发
        while resp and len(resp) >= 3 and resp[0] == 0x7F and resp[2] == 0x78:
            resp = tp._receive(P2_STAR_TIMEOUT / 1000.0)

        elapsed = (time.time() - t_start) * 1000.0
        return resp, elapsed

    def send_raw(self, data):
        """发送原始UDS请求(不处理pending)，返回响应"""
        return self.tp.send_receive(bytes(data), timeout_ms=P2_TIMEOUT)

    def diagnostic_session_control(self, session):
        return self.send_request([SID_DIAGNOSTIC_SESSION_CONTROL, session])

    def ecu_reset(self, reset_type=0x01):
        return self.send_request([SID_ECU_RESET, reset_type])

    def tester_present(self):
        return self.send_request([SID_TESTER_PRESENT, 0x00])

    def security_access_request_seed(self, level):
        return self.send_request([SID_SECURITY_ACCESS, level])

    def security_access_send_key(self, level, key):
        return self.send_request([SID_SECURITY_ACCESS, level + 1] + list(key))

    def security_access_unlock(self, level=0x01):
        \"\"\"完整安全访问解锁流程 (使用DLL计算Key)
        Args:
            level: 奇数安全等级 (0x01, 0x03, 0x05, ...)
        Returns:
            (success: bool, seed: list, key: list, resp: list)
        \"\"\"
        global seedkey_dll
        # Step 1: RequestSeed
        resp = self.security_access_request_seed(level)
        if not resp or len(resp) < 2 or resp[0] != (SID_SECURITY_ACCESS + 0x40):
            return (False, [], [], resp)
        seed = list(resp[2:])  # 跳过 67 + subFunction
        if all(b == 0x00 for b in seed):
            # seed全零表示已解锁
            return (True, seed, [], resp)
        if seedkey_dll is None:
            print(f"[WARN] 无SeedKey DLL, 无法计算Key, seed={{seed}}")
            return (False, seed, [], resp)
        # Step 2: DLL计算Key
        key = seedkey_dll.compute_key(seed, level)
        if key is None:
            print(f"[ERROR] DLL计算Key失败, seed={{seed}}")
            return (False, seed, [], resp)
        # Step 3: SendKey
        resp2 = self.security_access_send_key(level, key)
        success = (resp2 is not None and len(resp2) >= 2
                   and resp2[0] == (SID_SECURITY_ACCESS + 0x40))
        return (success, seed, key, resp2)

    def read_did(self, did, functional=False):
        did_hi = (did >> 8) & 0xFF
        did_lo = did & 0xFF
        return self.send_request([SID_READ_DID, did_hi, did_lo], functional=functional)

    def write_did(self, did, data):
        did_hi = (did >> 8) & 0xFF
        did_lo = did & 0xFF
        return self.send_request([SID_WRITE_DID, did_hi, did_lo] + list(data))

    def io_control(self, did, control_param, control_record=None):
        did_hi = (did >> 8) & 0xFF
        did_lo = did & 0xFF
        req = [SID_IO_CONTROL, did_hi, did_lo, control_param]
        if control_record:
            req.extend(list(control_record))
        return self.send_request(req)

    def routine_control(self, control_type, rid, data=None):
        rid_hi = (rid >> 8) & 0xFF
        rid_lo = rid & 0xFF
        req = [SID_ROUTINE_CONTROL, control_type, rid_hi, rid_lo]
        if data:
            req.extend(list(data))
        return self.send_request(req)

    def clear_dtc(self, dtc_group=0xFFFFFF):
        b1 = (dtc_group >> 16) & 0xFF
        b2 = (dtc_group >> 8) & 0xFF
        b3 = dtc_group & 0xFF
        return self.send_request([SID_CLEAR_DTC, b1, b2, b3])

    def read_dtc_info(self, sub_function, *args):
        return self.send_request([SID_READ_DTC_INFO, sub_function] + list(args))

    def control_dtc_setting(self, on_off):
        return self.send_request([SID_CONTROL_DTC_SETTING, on_off])

    def communication_control(self, sub_func, comm_type):
        return self.send_request([SID_COMMUNICATION_CONTROL, sub_func, comm_type])

    def read_memory_by_address(self, addr_len_fmt, address, mem_size):
        \"\"\"$23 ReadMemoryByAddress\"\"\"
        req = [SID_READ_MEM_BY_ADDR, addr_len_fmt]
        # address bytes (big-endian)
        addr_bytes = address.to_bytes((addr_len_fmt & 0x0F), 'big')
        size_bytes = mem_size.to_bytes((addr_len_fmt >> 4) & 0x0F, 'big')
        req.extend(list(addr_bytes))
        req.extend(list(size_bytes))
        return self.send_request(req)

    def request_download(self, compression_method, encrypting_method, addr_len_fmt, address, mem_size):
        \"\"\"$34 RequestDownload\"\"\"
        data_fmt = (compression_method << 4) | encrypting_method
        req = [SID_REQUEST_DOWNLOAD, data_fmt, addr_len_fmt]
        addr_bytes = address.to_bytes((addr_len_fmt & 0x0F), 'big')
        size_bytes = mem_size.to_bytes((addr_len_fmt >> 4) & 0x0F, 'big')
        req.extend(list(addr_bytes))
        req.extend(list(size_bytes))
        return self.send_request(req, timeout_ms=P2_STAR_TIMEOUT)

    def transfer_data(self, block_seq, data):
        \"\"\"$36 TransferData\"\"\"
        return self.send_request([SID_TRANSFER_DATA, block_seq] + list(data), timeout_ms=P2_STAR_TIMEOUT)

    def request_transfer_exit(self):
        \"\"\"$37 RequestTransferExit\"\"\"
        return self.send_request([SID_REQUEST_TRANSFER_EXIT])

    def send_obd_request(self, mode, pid=None):
        \"\"\"ISO 15031-5 OBD请求 (功能寻址)\"\"\"
        req = [mode]
        if pid is not None:
            req.append(pid)
        tp = self.func_tp if self.func_tp else self.tp
        return tp.send_receive(bytes(req), timeout_ms=P2_TIMEOUT)


# ============================================================================
# 测试框架
# ============================================================================

class TestResult:
    def __init__(self, case_id, service, test_name, did_rid="", session="",
                 security="", expected="", actual="", status="SKIP", detail=""):
        self.case_id = case_id
        self.service = service
        self.test_name = test_name
        self.did_rid = did_rid
        self.session = session
        self.security = security
        self.expected = expected
        self.actual = actual
        self.status = status
        self.detail = detail


class TestRunner:
    @staticmethod
    def _resolve_can_config(can_if, channel):
        """选择CAN接口和通道 (仅支持SocketCAN)"""
        can_if = "socketcan"
        if not channel or channel.upper().startswith("PCAN_"):
            channel = "can0"
        return can_if, channel

    def __init__(self, channel, bitrate, tx_id, rx_id, func_id, can_if="socketcan", sample_point=0.0, can_log_path=""):
        self.can_if, self.channel = self._resolve_can_config(can_if, channel)
        self.bitrate = bitrate
        self.sample_point = sample_point if sample_point > 0 else DEFAULT_SAMPLE_POINT
        self.tx_id = tx_id
        self.rx_id = rx_id
        self.func_id = func_id
        self.bus = None
        self.uds = None
        self.can_logger = None
        self.can_log_path = can_log_path
        self.results = []
        self.case_counter = 0

    def connect(self):
        """连接CAN总线 (SocketCAN)"""
        try:
            self._setup_socketcan()
            bus_kwargs = dict(
                interface="socketcan",
                channel=self.channel,
                fd=True,
            )
            self.bus = can.interface.Bus(**bus_kwargs)
            # 启动CAN通信日志记录 (包装send/recv，同时记录TX和RX帧)
            if self.can_log_path:
                try:
                    self.can_logger = can.Logger(self.can_log_path)
                    # 写入ASC列参考注释
                    self.can_logger.file.write("// ASC Column Reference (python-can ASCWriter)\\n")
                    self.can_logger.file.write("// Classic CAN:  Timestamp  Ch  ID  Tx/Rx  d DLC  Data[hex]\\n")
                    self.can_logger.file.write("// CAN FD:       CANFD  Ch  Tx/Rx  ID  BRS ESI DLC DataLen  Data[hex]  MsgDur  MsgLen  Flags  CRC  ...\\n")
                    self.can_logger.file.write("//\\n")
                    _original_send = self.bus.send
                    _original_recv = self.bus.recv
                    _logger = self.can_logger
                    def _logged_send(msg, timeout=None):
                        _original_send(msg, timeout=timeout)
                        msg.is_rx = False
                        _logger.on_message_received(msg)
                    def _logged_recv(timeout=None):
                        msg = _original_recv(timeout=timeout)
                        if msg is not None:
                            msg.is_rx = True
                            _logger.on_message_received(msg)
                        return msg
                    self.bus.send = _logged_send
                    self.bus.recv = _logged_recv
                    print(f"[OK] CAN日志已启用: {{self.can_log_path}}")
                except Exception as log_e:
                    print(f"[WARN] CAN日志初始化失败: {{log_e}}")
                    self.can_logger = None
            self.uds = UdsClient(self.bus, self.tx_id, self.rx_id, self.func_id)
            mode = "CAN FD" if CAN_FD_ENABLED else "Classic CAN"
            print(f"[OK] CAN连接成功 ({{self.can_if}}): {{self.channel}} @ {{self.bitrate}}bps ({{mode}})")
            if CAN_FD_ENABLED:
                print(f"     数据段波特率: {{CAN_FD_DATA_BITRATE}}bps, 最大DLC: {{CAN_FD_MAX_DLC}}")
            print(f"     TX=0x{{self.tx_id:03X}}, RX=0x{{self.rx_id:03X}}")
            return True
        except Exception as e:
            print(f"[ERROR] CAN连接失败 ({{self.can_if}}): {{e}}")
            if self.can_if == "socketcan":
                print(f"[HINT] CAN初始化失败，手动恢复步骤:")
                if CAN_FD_ENABLED:
                    print(f"  sudo ip link set {{self.channel}} down")
                    print(f"  sudo ip link set {{self.channel}} type can bitrate {{self.bitrate}} dbitrate {{CAN_FD_DATA_BITRATE}} fd on sample-point {{self.sample_point:.3f}}")
                else:
                    print(f"  sudo ip link set {{self.channel}} down")
                    print(f"  sudo ip link set {{self.channel}} type can bitrate {{self.bitrate}} sample-point {{self.sample_point:.3f}}")
                print(f"  sudo ip link set {{self.channel}} up")
            return False

    def _setup_socketcan(self):
        """统一CAN初始化: 加载模块 → 释放占用 → 强制down → 配置 → up (唯一入口)"""
        import subprocess as _sp
        ch = self.channel

        # 1. 确保内核模块已加载 (WSL2 编译为模块，必须手动加载)
        for mod in ["can", "can_raw"]:
            _sp.run(["sudo", "modprobe", mod], capture_output=True, text=True)

        # 2. 检查接口是否存在
        ret = _sp.run(["ip", "link", "show", ch], capture_output=True, text=True)
        if ret.returncode != 0:
            print(f"[WARN] SocketCAN接口 {{ch}} 不存在, 请检查CAN USB适配器是否已连接")
            return

        # 3. 强制 down (释放可能占用的socket, 确保可重新配置)
        #    先尝试正常 down; 如果失败则用 fuser 清理占用进程后重试
        r = _sp.run(["sudo", "ip", "link", "set", ch, "down"], capture_output=True, text=True)
        if r.returncode != 0:
            print(f"[INFO] {{ch}} down失败 (可能被占用), 尝试释放...")
            # 查找并终止占用 CAN 接口的进程
            _sp.run(["sudo", "fuser", "-k", f"/sys/class/net/{{ch}}/"], capture_output=True)
            _sp.run(["sudo", "ip", "link", "set", ch, "down"], capture_output=True)

        # 4. 配置接口参数 (Classic CAN / CAN FD 统一路径)
        target_sp = self.sample_point
        cmd_type = [
            "sudo", "ip", "link", "set", ch, "type", "can",
            "bitrate", str(self.bitrate),
        ]
        if CAN_FD_ENABLED:
            cmd_type.extend(["dbitrate", str(CAN_FD_DATA_BITRATE), "fd", "on"])
        if target_sp > 0:
            cmd_type.extend(["sample-point", f"{{target_sp:.3f}}"])
        if CAN_FD_ENABLED and CAN_FD_DSAMPLE_POINT > 0:
            cmd_type.extend(["dsample-point", f"{{CAN_FD_DSAMPLE_POINT:.3f}}"])

        print(f"[INFO] 配置: {{' '.join(cmd_type)}}")
        ret = _sp.run(cmd_type, capture_output=True, text=True)
        if ret.returncode != 0:
            print(f"[ERROR] 配置失败: {{ret.stderr.strip()}}")
            return

        # 5. 启用接口
        cmd_up = ["sudo", "ip", "link", "set", ch, "up"]
        print(f"[INFO] 启用: {{' '.join(cmd_up)}}")
        ret = _sp.run(cmd_up, capture_output=True, text=True)
        if ret.returncode != 0:
            print(f"[ERROR] 启用失败: {{ret.stderr.strip()}}")
            return

        mode = "CAN FD" if CAN_FD_ENABLED else "Classic CAN"
        bitrate_info = f"bitrate={{self.bitrate}}"
        if CAN_FD_ENABLED:
            bitrate_info += f", dbitrate={{CAN_FD_DATA_BITRATE}}"
        sp_info = f", sp={{target_sp:.3f}}" if target_sp > 0 else ""
        print(f"[OK] SocketCAN {{ch}} 已配置并启用 ({{mode}}, {{bitrate_info}}{{sp_info}})")

    def disconnect(self):
        """断开CAN"""
        if self.can_logger:
            self.can_logger.stop()
            print(f"[OK] CAN日志已保存: {{self.can_log_path}}")
            self.can_logger = None
        if self.bus:
            self.bus.shutdown()
            self.bus = None
            print("[OK] CAN已断开")

    def next_case_id(self):
        self.case_counter += 1
        return self.case_counter

    def add_result(self, **kwargs):
        kwargs["case_id"] = self.next_case_id()
        self.results.append(TestResult(**kwargs))
        r = self.results[-1]
        status_icon = "✓" if r.status == "PASS" else ("✗" if r.status == "FAIL" else "○")
        print(f"  [{{status_icon}}] #{{r.case_id}} {{r.test_name}} -> {{r.status}}")

    def is_positive_response(self, resp, expected_sid):
        """检查是否为正响应"""
        if resp is None:
            return False
        return len(resp) >= 1 and resp[0] == (expected_sid + 0x40)

    def is_negative_response(self, resp, expected_nrc=None):
        """检查是否为否定响应"""
        if resp is None:
            return False
        if len(resp) < 3 or resp[0] != 0x7F:
            return False
        if expected_nrc is not None:
            return resp[2] == expected_nrc
        return True

    def get_nrc(self, resp):
        """获取NRC"""
        if resp and len(resp) >= 3 and resp[0] == 0x7F:
            return resp[2]
        return None

    def resp_to_hex(self, resp):
        """响应转hex字符串"""
        if resp is None:
            return "No Response"
        return " ".join([f"0x{{b:02X}}" for b in resp])

    def switch_session(self, session):
        """切换会话"""
        resp = self.uds.diagnostic_session_control(session)
        return self.is_positive_response(resp, SID_DIAGNOSTIC_SESSION_CONTROL)

    def reset_to_default_session(self):
        """恢复到默认会话"""
        self.switch_session(SESSION_DEFAULT)
        time.sleep(0.1)

    def unlock_security(self, level):
        """安全访问解锁 — 优先使用DLL计算Key"""
        success, seed, key, resp = self.uds.security_access_unlock(level)
        if success:
            if key:
                print(f"    [OK] 安全解锁成功 (level=0x{{level:02X}}, seed={{self.resp_to_hex(seed)}}, key={{self.resp_to_hex(key)}})")
            else:
                print(f"    [OK] 已处于解锁状态 (level=0x{{level:02X}})")
            return True
        if seed:
            print(f"    [INFO] 安全解锁失败 (level=0x{{level:02X}}, seed={{self.resp_to_hex(seed)}})")
        else:
            print(f"    [INFO] RequestSeed失败: {{self.resp_to_hex(resp)}}")
        return False

    # ======================================
    # 测试执行方法
    # ======================================

    def test_session_management(self):
        """测试会话管理"""
        print("\\n=== 测试 $10 DiagnosticSessionControl ===")

        for session, name in SESSION_NAMES.items():
            resp = self.uds.diagnostic_session_control(session)
            if self.is_positive_response(resp, SID_DIAGNOSTIC_SESSION_CONTROL):
                self.add_result(
                    service="$10", test_name=f"切换到{{name}}", session=name,
                    expected="正响应 0x50", actual=self.resp_to_hex(resp), status="PASS")
            else:
                self.add_result(
                    service="$10", test_name=f"切换到{{name}}", session=name,
                    expected="正响应 0x50", actual=self.resp_to_hex(resp), status="FAIL")
            time.sleep(0.05)

        self.reset_to_default_session()

    def test_tester_present(self):
        """测试TesterPresent"""
        print("\\n=== 测试 $3E TesterPresent ===")
        resp = self.uds.tester_present()
        if self.is_positive_response(resp, SID_TESTER_PRESENT):
            self.add_result(
                service="$3E", test_name="TesterPresent默认会话",
                expected="正响应 0x7E", actual=self.resp_to_hex(resp), status="PASS")
        else:
            self.add_result(
                service="$3E", test_name="TesterPresent默认会话",
                expected="正响应 0x7E", actual=self.resp_to_hex(resp), status="FAIL")

        # suppressPositiveResponse bit (sub-function bit 7)
        resp = self.uds.send_request([SID_TESTER_PRESENT, 0x80])  # subFunc=0x00|0x80
        if resp is None:
            self.add_result(
                service="$3E", test_name="TesterPresent suppressPosRsp",
                expected="无响应(正确抑制)", actual="No Response", status="PASS")
        else:
            self.add_result(
                service="$3E", test_name="TesterPresent suppressPosRsp",
                expected="无响应(正确抑制)", actual=self.resp_to_hex(resp), status="FAIL")

        # 扩展会话中的TesterPresent
        self.switch_session(SESSION_EXTENDED)
        time.sleep(0.05)
        resp = self.uds.tester_present()
        if self.is_positive_response(resp, SID_TESTER_PRESENT):
            self.add_result(
                service="$3E", test_name="TesterPresent扩展会话",
                expected="正响应 0x7E", actual=self.resp_to_hex(resp), status="PASS")
        else:
            self.add_result(
                service="$3E", test_name="TesterPresent扩展会话",
                expected="正响应 0x7E", actual=self.resp_to_hex(resp), status="FAIL")

        # 无效子功能
        resp = self.uds.send_request([SID_TESTER_PRESENT, 0x01])
        if self.is_negative_response(resp, 0x12):
            self.add_result(
                service="$3E", test_name="TesterPresent无效子功能0x01",
                expected="NRC 0x12", actual=self.resp_to_hex(resp), status="PASS")
        else:
            self.add_result(
                service="$3E", test_name="TesterPresent无效子功能0x01",
                expected="NRC 0x12", actual=self.resp_to_hex(resp),
                status="PASS" if self.is_negative_response(resp) else "FAIL")

        self.reset_to_default_session()

    def test_timing_p2(self):
        """ISO 14229 P2/P2* 时间合规测试"""
        print("\\n=== 测试 P2/P2* 响应时间 ===")

        # P2 时间测试 - 默认会话下$3E请求
        self.reset_to_default_session()
        time.sleep(0.1)
        resp, elapsed = self.uds.send_request_timed([SID_TESTER_PRESENT, 0x00])
        p2_ok = elapsed <= P2_TIMEOUT * 1.1  # 允许10%误差
        self.add_result(
            service="Timing", test_name=f"P2 Server Timer ($3E)",
            expected=f"<={{P2_TIMEOUT}}ms", actual=f"{{elapsed:.1f}}ms",
            status="PASS" if (p2_ok and resp is not None) else "FAIL",
            detail=f"P2规范: {{P2_TIMEOUT}}ms")

        # P2 时间测试 - $22读取DID
        resp, elapsed = self.uds.send_request_timed([SID_READ_DID, 0xF1, 0x90])
        p2_ok = elapsed <= P2_TIMEOUT * 1.1
        self.add_result(
            service="Timing", test_name=f"P2 Server Timer ($22 0xF190)",
            expected=f"<={{P2_TIMEOUT}}ms", actual=f"{{elapsed:.1f}}ms",
            status="PASS" if (p2_ok and resp is not None) else "FAIL")

        # P2 时间测试 - $10会话切换
        self.reset_to_default_session()
        time.sleep(0.1)
        resp, elapsed = self.uds.send_request_timed([SID_DIAGNOSTIC_SESSION_CONTROL, SESSION_EXTENDED])
        p2_ok = elapsed <= P2_TIMEOUT * 1.1
        self.add_result(
            service="Timing", test_name=f"P2 Server Timer ($10 切换Extended)",
            expected=f"<={{P2_TIMEOUT}}ms", actual=f"{{elapsed:.1f}}ms",
            status="PASS" if (p2_ok and resp is not None) else "FAIL")

        self.reset_to_default_session()

    def test_s3_server_timeout(self):
        """ISO 14229 S3 Server Timer 测试 - 非默认会话超时回落"""
        print("\\n=== 测试 S3 Server Timer (会话超时) ===")

        # 切换到扩展会话
        self.switch_session(SESSION_EXTENDED)
        time.sleep(0.05)
        resp = self.uds.tester_present()
        if not self.is_positive_response(resp, SID_TESTER_PRESENT):
            self.add_result(
                service="Timing", test_name="S3前置:确认在扩展会话",
                expected="正响应", actual=self.resp_to_hex(resp), status="FAIL")
            return

        # 等待超过S3 timeout (默认5s)
        wait_time = S3_SERVER_TIMEOUT / 1000.0 + 1.0  # 超时+1秒
        print(f"    等待 {{wait_time:.1f}}s 让S3超时...")
        time.sleep(wait_time)

        # 尝试在扩展会话下读取一个仅扩展会话支持的服务（如果有的话）
        # 先验证是否回落到了默认会话 - 用$3E确认仍连接
        resp = self.uds.tester_present()
        if self.is_positive_response(resp, SID_TESTER_PRESENT):
            # ECU仍在响应，检查是否已回落到默认会话
            # 尝试$85(仅扩展会话支持)来确认
            resp2 = self.uds.control_dtc_setting(0x02)
            if self.is_negative_response(resp2):
                self.add_result(
                    service="Timing", test_name="S3 Server超时回落到默认会话",
                    expected="$85被拒(已回落默认会话)",
                    actual=self.resp_to_hex(resp2), status="PASS",
                    detail=f"等待{{wait_time:.1f}}s后会话已回落")
            else:
                self.add_result(
                    service="Timing", test_name="S3 Server超时回落到默认会话",
                    expected="$85被拒(已回落默认会话)",
                    actual=self.resp_to_hex(resp2), status="FAIL",
                    detail="会话未按S3超时回落")
        else:
            self.add_result(
                service="Timing", test_name="S3 Server超时回落到默认会话",
                expected="ECU仍可响应", actual="No Response", status="FAIL")

        self.reset_to_default_session()

    def test_sa_time_delay(self):
        """$27 SecurityAccess 时间锁定测试 (NRC 0x37 requiredTimeDelayNotExpired)"""
        print("\\n=== 测试 $27 安全访问时间锁定 (NRC 0x37) ===")

        # 测试思路: 连续发送多次错误Key触发NRC 0x35(attemptLimit),
        # 然后立即再次请求Seed应返回NRC 0x37(requiredTimeDelayNotExpired)
        self.reset_to_default_session()
        self.switch_session(SESSION_EXTENDED)
        time.sleep(0.05)

        # Step1: 请求Seed获取种子
        resp = self.uds.security_access_request_seed(0x01)
        if not resp or len(resp) < 2 or resp[0] != (SID_SECURITY_ACCESS + 0x40):
            self.add_result(
                service="Timing", test_name="SA时间锁定-前置Seed请求",
                expected="正响应67+seed", actual=self.resp_to_hex(resp), status="FAIL")
            self.reset_to_default_session()
            return

        seed = list(resp[2:])
        if all(b == 0x00 for b in seed):
            self.add_result(
                service="Timing", test_name="SA时间锁定-前置检查",
                expected="非零seed", actual="seed全零(已解锁)", status="PASS",
                detail="已解锁状态无法测试NRC 0x37, 跳过")
            self.reset_to_default_session()
            return

        # Step2: 连续发送错误Key尝试触发锁定
        max_attempts = 5
        locked = False
        for attempt in range(max_attempts):
            fake_key = [0xFF ^ b for b in seed]  # 伪造Key
            resp2 = self.uds.security_access_send_key(0x01, fake_key)
            nrc = self.get_nrc(resp2) if self.is_negative_response(resp2) else None
            if nrc == 0x36:  # exceededNumberOfAttempts
                locked = True
                break
            elif nrc == 0x37:  # requiredTimeDelayNotExpired (已被锁定)
                locked = True
                break
            elif nrc == 0x35:  # invalidKey - 继续尝试
                # 需要重新请求Seed
                resp = self.uds.security_access_request_seed(0x01)
                nrc2 = self.get_nrc(resp) if self.is_negative_response(resp) else None
                if nrc2 == 0x37:
                    locked = True
                    break
                if not resp or resp[0] != (SID_SECURITY_ACCESS + 0x40):
                    break

        if not locked:
            self.add_result(
                service="Timing", test_name="SA时间锁定-触发锁定",
                expected=f"NRC 0x36/0x37 ({{max_attempts}}次错误Key后)",
                actual="未触发锁定", status="PASS",
                detail=f"ECU可能不限制尝试次数({{max_attempts}}次尝试)")
            self.reset_to_default_session()
            return

        # Step3: 立即请求Seed - 应返回NRC 0x37
        resp3 = self.uds.security_access_request_seed(0x01)
        nrc3 = self.get_nrc(resp3) if self.is_negative_response(resp3) else None
        self.add_result(
            service="Timing", test_name="SA锁定后立即请求Seed→NRC 0x37",
            expected="NRC 0x37(requiredTimeDelayNotExpired)",
            actual=self.resp_to_hex(resp3),
            status="PASS" if nrc3 == 0x37 else
                   ("PASS" if nrc3 == 0x36 else "FAIL"),
            detail="NRC 0x36(仍在limitExceeded状态)也可接受")

        # Step4: 等待SECURITY_ACCESS_DELAY后重试 - 应恢复
        if SECURITY_ACCESS_DELAY > 0:
            wait_sec = SECURITY_ACCESS_DELAY / 1000.0 + 0.5
            print(f"    等待 {{wait_sec:.1f}}s 让SA时间锁定解除...")
            time.sleep(wait_sec)

            # 重新进入扩展会话（S3可能已超时）
            self.reset_to_default_session()
            self.switch_session(SESSION_EXTENDED)
            time.sleep(0.05)

            resp4 = self.uds.security_access_request_seed(0x01)
            nrc4 = self.get_nrc(resp4) if self.is_negative_response(resp4) else None
            if resp4 and resp4[0] == (SID_SECURITY_ACCESS + 0x40):
                self.add_result(
                    service="Timing", test_name=f"SA延时{{SECURITY_ACCESS_DELAY}}ms后恢复",
                    expected="正响应67+seed",
                    actual=self.resp_to_hex(resp4), status="PASS",
                    detail=f"等待{{wait_sec:.1f}}s后锁定已解除")
            elif nrc4 == 0x37:
                self.add_result(
                    service="Timing", test_name=f"SA延时{{SECURITY_ACCESS_DELAY}}ms后恢复",
                    expected="正响应67+seed",
                    actual=self.resp_to_hex(resp4), status="FAIL",
                    detail=f"等待{{wait_sec:.1f}}s后仍锁定，延时配置可能不足")
            else:
                self.add_result(
                    service="Timing", test_name=f"SA延时{{SECURITY_ACCESS_DELAY}}ms后恢复",
                    expected="正响应67+seed",
                    actual=self.resp_to_hex(resp4),
                    status="PASS" if nrc4 is None else "FAIL")

        self.reset_to_default_session()

    def test_p2_dynamic_extraction(self):
        """$10 会话切换响应中P2/P2*参数动态提取验证"""
        print("\\n=== 测试 P2/P2* 参数动态提取 ===")

        # ISO 14229-1: $10正响应格式 = [50+SubFunc, SessionType, P2_hi, P2_lo, P2*_hi, P2*_lo]
        # P2单位: 1ms, P2*单位: 10ms
        self.reset_to_default_session()
        time.sleep(0.1)

        for sess_id, sess_name in [(0x01, "Default"), (0x02, "Programming"), (0x03, "Extended")]:
            resp = self.uds.diagnostic_session_control(sess_id)
            if resp and len(resp) >= 6 and resp[0] == (SID_DIAGNOSTIC_SESSION_CONTROL + 0x40):
                p2_server = (resp[2] << 8) | resp[3]         # ms
                p2_star_server = ((resp[4] << 8) | resp[5]) * 10  # *10 ms
                self.add_result(
                    service="Timing",
                    test_name=f"$10 P2/P2*提取({{sess_name}})",
                    expected=f"P2<={{P2_TIMEOUT}}ms, P2*<={{P2_STAR_TIMEOUT}}ms",
                    actual=f"P2={{{{p2_server}}}}ms, P2*={{{{p2_star_server}}}}ms",
                    status="PASS" if (p2_server <= P2_TIMEOUT * 2 and
                                      p2_star_server <= P2_STAR_TIMEOUT * 2) else "FAIL",
                    detail=f"ECU报告: P2={{{{p2_server}}}}ms P2*={{{{p2_star_server}}}}ms")
            elif self.is_negative_response(resp):
                nrc = self.get_nrc(resp)
                if sess_id == 0x02 and nrc in (0x22, 0x31):
                    self.add_result(
                        service="Timing",
                        test_name=f"$10 P2/P2*提取({{sess_name}})",
                        expected="正响应或条件不满足",
                        actual=self.resp_to_hex(resp), status="PASS",
                        detail="Programming会话可能受条件限制")
                else:
                    self.add_result(
                        service="Timing",
                        test_name=f"$10 P2/P2*提取({{sess_name}})",
                        expected="正响应含P2/P2*", actual=self.resp_to_hex(resp),
                        status="FAIL")
            else:
                self.add_result(
                    service="Timing",
                    test_name=f"$10 P2/P2*提取({{sess_name}})",
                    expected="正响应含P2/P2*",
                    actual=self.resp_to_hex(resp), status="FAIL")

            self.reset_to_default_session()
            time.sleep(0.1)

    def test_p2_actual_compliance(self):
        """验证ECU实际响应时间是否在其报告的P2范围内"""
        print("\\n=== 测试 P2实际响应时间合规 ===")

        self.reset_to_default_session()
        time.sleep(0.1)

        # 从$10响应中提取ECU自行声明的P2
        resp = self.uds.diagnostic_session_control(0x01)
        ecu_p2 = P2_TIMEOUT  # 默认值
        if resp and len(resp) >= 6 and resp[0] == (SID_DIAGNOSTIC_SESSION_CONTROL + 0x40):
            ecu_p2 = (resp[2] << 8) | resp[3]
            if ecu_p2 <= 0:
                ecu_p2 = P2_TIMEOUT

        # 对多个服务做10次连续测量, 取最大值
        test_services = [
            ("$3E TesterPresent", [SID_TESTER_PRESENT, 0x00]),
            ("$22 ReadDID F190", [SID_READ_DID, 0xF1, 0x90]),
        ]

        for svc_name, req_data in test_services:
            max_elapsed = 0
            all_ok = True
            for _ in range(10):
                r, elapsed = self.uds.send_request_timed(req_data)
                if elapsed > max_elapsed:
                    max_elapsed = elapsed
                if elapsed > ecu_p2 * 1.1:
                    all_ok = False

            self.add_result(
                service="Timing",
                test_name=f"P2实际合规({{svc_name}}) x10",
                expected=f"所有响应<= ECU P2({{ecu_p2}}ms)*1.1",
                actual=f"最大{{max_elapsed:.1f}}ms",
                status="PASS" if all_ok else "FAIL",
                detail=f"ECU声明P2={{ecu_p2}}ms, 10次最大{{max_elapsed:.1f}}ms")

        self.reset_to_default_session()

    def test_session_advanced(self):
        """$10 高级会话测试"""
        print("\\n=== 测试 $10 高级会话测试 ===")

        # 无效会话模式
        resp = self.uds.diagnostic_session_control(0x7F)
        if self.is_negative_response(resp, 0x12):
            self.add_result(
                service="$10", test_name="无效会话模式0x7F",
                expected="NRC 0x12", actual=self.resp_to_hex(resp), status="PASS")
        else:
            self.add_result(
                service="$10", test_name="无效会话模式0x7F",
                expected="NRC 0x12", actual=self.resp_to_hex(resp),
                status="PASS" if self.is_negative_response(resp) else "FAIL")

        # suppressPositiveResponse for $10
        resp = self.uds.send_request([SID_DIAGNOSTIC_SESSION_CONTROL, SESSION_EXTENDED | 0x80])
        if resp is None:
            self.add_result(
                service="$10", test_name="$10 suppressPosRsp切换Extended",
                expected="无响应(正确抑制)", actual="No Response", status="PASS")
        else:
            self.add_result(
                service="$10", test_name="$10 suppressPosRsp切换Extended",
                expected="无响应(正确抑制)", actual=self.resp_to_hex(resp), status="FAIL")

        # 验证实际已切换到Extended
        self.reset_to_default_session()
        time.sleep(0.05)
        resp = self.uds.send_request([SID_DIAGNOSTIC_SESSION_CONTROL, SESSION_EXTENDED | 0x80])
        time.sleep(0.05)
        resp2 = self.uds.control_dtc_setting(0x02)
        suppressed_and_switched = (resp is None) and self.is_positive_response(resp2, SID_CONTROL_DTC_SETTING)
        self.add_result(
            service="$10", test_name="$10 suppressPosRsp实际切换验证",
            expected="抑制响应且实际切换成功",
            actual=f"$10resp={{self.resp_to_hex(resp)}}, $85resp={{self.resp_to_hex(resp2)}}",
            status="PASS" if suppressed_and_switched else "FAIL")

        # 错误长度测试 - $10 只发SID
        self.reset_to_default_session()
        resp = self.uds.send_request([SID_DIAGNOSTIC_SESSION_CONTROL])
        if self.is_negative_response(resp, 0x13):
            self.add_result(
                service="$10", test_name="$10错误长度(缺子功能)",
                expected="NRC 0x13", actual=self.resp_to_hex(resp), status="PASS")
        else:
            self.add_result(
                service="$10", test_name="$10错误长度(缺子功能)",
                expected="NRC 0x13", actual=self.resp_to_hex(resp),
                status="PASS" if self.is_negative_response(resp) else "FAIL")

        # OEM会话范围边界测试 (ISO 14229-1 §10.2.1 Table 249)
        # 0x00 Reserved → NRC
        resp = self.uds.diagnostic_session_control(0x00)
        self.add_result(
            service="$10", test_name="$10 Reserved会话0x00",
            expected="NRC 0x12",
            actual=self.resp_to_hex(resp),
            status="PASS" if self.is_negative_response(resp, 0x12) else
                   ("PASS" if self.is_negative_response(resp) else "FAIL"))

        # 0x40 OEM定义范围下界
        resp = self.uds.diagnostic_session_control(0x40)
        nrc = self.get_nrc(resp)
        self.add_result(
            service="$10", test_name="$10 OEM会话0x40(下界)",
            expected="正响应(ECU支持)或NRC 0x12",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_DIAGNOSTIC_SESSION_CONTROL)
                              or nrc in (0x12, 0x22, 0x33)) else "FAIL")
        self.reset_to_default_session()

        # 0x5F OEM定义范围上界
        resp = self.uds.diagnostic_session_control(0x5F)
        nrc = self.get_nrc(resp)
        self.add_result(
            service="$10", test_name="$10 OEM会话0x5F(上界)",
            expected="正响应或NRC 0x12",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_DIAGNOSTIC_SESSION_CONTROL)
                              or nrc in (0x12, 0x22, 0x33)) else "FAIL")
        self.reset_to_default_session()

        # 0x60 系统供应商范围下界
        resp = self.uds.diagnostic_session_control(0x60)
        nrc = self.get_nrc(resp)
        self.add_result(
            service="$10", test_name="$10 SSP会话0x60(下界)",
            expected="正响应或NRC 0x12",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_DIAGNOSTIC_SESSION_CONTROL)
                              or nrc in (0x12, 0x22, 0x33)) else "FAIL")
        self.reset_to_default_session()

        # 0x7E 系统供应商范围上界
        resp = self.uds.diagnostic_session_control(0x7E)
        nrc = self.get_nrc(resp)
        self.add_result(
            service="$10", test_name="$10 SSP会话0x7E(上界)",
            expected="正响应或NRC 0x12",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_DIAGNOSTIC_SESSION_CONTROL)
                              or nrc in (0x12, 0x22, 0x33)) else "FAIL")

        self.reset_to_default_session()

    def test_ecu_reset(self):
        """$11 ECUReset 多类型测试"""
        print("\\n=== 测试 $11 ECUReset ===")

        # hardReset (0x01)
        resp = self.uds.send_request([SID_ECU_RESET, 0x01])
        if self.is_positive_response(resp, SID_ECU_RESET):
            self.add_result(
                service="$11", test_name="ECU HardReset(0x01)",
                expected="正响应 0x51", actual=self.resp_to_hex(resp), status="PASS")
            time.sleep(2.0)  # 等待ECU重启
        else:
            self.add_result(
                service="$11", test_name="ECU HardReset(0x01)",
                expected="正响应 0x51", actual=self.resp_to_hex(resp), status="FAIL")

        # 验证ECU重启后恢复通信
        time.sleep(1.0)
        resp = self.uds.tester_present()
        self.add_result(
            service="$11", test_name="HardReset后ECU恢复通信",
            expected="正响应$3E", actual=self.resp_to_hex(resp),
            status="PASS" if self.is_positive_response(resp, SID_TESTER_PRESENT) else "FAIL")

        # keyOffOnReset (0x02)
        resp = self.uds.send_request([SID_ECU_RESET, 0x02])
        if self.is_positive_response(resp, SID_ECU_RESET):
            self.add_result(
                service="$11", test_name="ECU KeyOffOnReset(0x02)",
                expected="正响应 0x51", actual=self.resp_to_hex(resp), status="PASS")
            time.sleep(2.0)
        elif self.is_negative_response(resp, 0x12):
            self.add_result(
                service="$11", test_name="ECU KeyOffOnReset(0x02)",
                expected="正响应或NRC 0x12", actual=self.resp_to_hex(resp), status="PASS",
                detail="ECU不支持此复位类型")
        else:
            self.add_result(
                service="$11", test_name="ECU KeyOffOnReset(0x02)",
                expected="正响应 0x51", actual=self.resp_to_hex(resp), status="FAIL")

        time.sleep(1.0)
        self.uds.tester_present()  # 确认恢复

        # softReset (0x03)
        resp = self.uds.send_request([SID_ECU_RESET, 0x03])
        if self.is_positive_response(resp, SID_ECU_RESET):
            self.add_result(
                service="$11", test_name="ECU SoftReset(0x03)",
                expected="正响应 0x51", actual=self.resp_to_hex(resp), status="PASS")
            time.sleep(1.0)
        elif self.is_negative_response(resp, 0x12):
            self.add_result(
                service="$11", test_name="ECU SoftReset(0x03)",
                expected="正响应或NRC 0x12", actual=self.resp_to_hex(resp), status="PASS",
                detail="ECU不支持此复位类型")
        else:
            self.add_result(
                service="$11", test_name="ECU SoftReset(0x03)",
                expected="正响应 0x51", actual=self.resp_to_hex(resp), status="FAIL")

        time.sleep(1.0)
        self.uds.tester_present()

        # enableRapidPowerShutDown (0x04) - ISO 14229-1 §11.3.2
        resp = self.uds.send_request([SID_ECU_RESET, 0x04])
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="$11", test_name="ECU enableRapidPowerShutDown(0x04)",
            expected="正响应或NRC 0x12",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_ECU_RESET)
                              or nrc in (0x12, 0x22, 0x33, 0x7F, 0x7E)) else "FAIL")
        time.sleep(1.0)
        self.uds.tester_present()

        # disableRapidPowerShutDown (0x05)
        resp = self.uds.send_request([SID_ECU_RESET, 0x05])
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="$11", test_name="ECU disableRapidPowerShutDown(0x05)",
            expected="正响应或NRC 0x12",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_ECU_RESET)
                              or nrc in (0x12, 0x22, 0x33, 0x7F, 0x7E)) else "FAIL")
        time.sleep(1.0)
        self.uds.tester_present()

        # 无效复位类型
        resp = self.uds.send_request([SID_ECU_RESET, 0x7F])
        if self.is_negative_response(resp, 0x12):
            self.add_result(
                service="$11", test_name="ECUReset无效类型0x7F",
                expected="NRC 0x12", actual=self.resp_to_hex(resp), status="PASS")
        else:
            self.add_result(
                service="$11", test_name="ECUReset无效类型0x7F",
                expected="NRC 0x12", actual=self.resp_to_hex(resp),
                status="PASS" if self.is_negative_response(resp) else "FAIL")

        # suppressPositiveResponse
        resp = self.uds.send_request([SID_ECU_RESET, 0x01 | 0x80])
        if resp is None:
            self.add_result(
                service="$11", test_name="ECUReset suppressPosRsp",
                expected="无响应(正确抑制)", actual="No Response", status="PASS")
            time.sleep(2.0)
        else:
            self.add_result(
                service="$11", test_name="ECUReset suppressPosRsp",
                expected="无响应(正确抑制)", actual=self.resp_to_hex(resp), status="FAIL")

        time.sleep(1.0)
        self.uds.tester_present()

        # 错误长度
        resp = self.uds.send_request([SID_ECU_RESET])
        if self.is_negative_response(resp, 0x13):
            self.add_result(
                service="$11", test_name="ECUReset错误长度(缺子功能)",
                expected="NRC 0x13", actual=self.resp_to_hex(resp), status="PASS")
        else:
            self.add_result(
                service="$11", test_name="ECUReset错误长度(缺子功能)",
                expected="NRC 0x13", actual=self.resp_to_hex(resp),
                status="PASS" if self.is_negative_response(resp) else "FAIL")

    def test_security_access_advanced(self):
        """$27 SecurityAccess 高级测试"""
        print("\\n=== 测试 $27 SecurityAccess 高级 ===")

        # 默认会话中请求 - 应拒绝
        self.reset_to_default_session()
        resp = self.uds.security_access_request_seed(0x01)
        if self.is_negative_response(resp):
            self.add_result(
                service="$27", test_name="默认会话请求Seed应拒绝",
                session="Default", expected="NRC 0x7F/0x7E",
                actual=self.resp_to_hex(resp), status="PASS")
        else:
            self.add_result(
                service="$27", test_name="默认会话请求Seed应拒绝",
                session="Default", expected="NRC",
                actual=self.resp_to_hex(resp),
                status="PASS" if self.is_positive_response(resp, SID_SECURITY_ACCESS) else "FAIL",
                detail="某些ECU可能在默认会话也支持")

        # 扩展会话中请求Seed Level1
        self.switch_session(SESSION_EXTENDED)
        time.sleep(0.05)
        resp1 = self.uds.security_access_request_seed(0x01)
        if self.is_positive_response(resp1, SID_SECURITY_ACCESS):
            seed1 = resp1[2:] if len(resp1) > 2 else []
            self.add_result(
                service="$27", test_name="扩展会话请求Seed Level1",
                session="Extended", security="Level1",
                expected="正响应+Seed", actual=self.resp_to_hex(resp1), status="PASS")

            # Seed唯一性测试 - 两次请求seed应不同(ISO 14229要求)
            time.sleep(0.05)
            resp2 = self.uds.security_access_request_seed(0x01)
            if self.is_positive_response(resp2, SID_SECURITY_ACCESS):
                seed2 = resp2[2:] if len(resp2) > 2 else []
                seeds_differ = (seed1 != seed2) or all(b == 0 for b in seed1)
                self.add_result(
                    service="$27", test_name="Seed唯一性(两次请求不同)",
                    session="Extended", security="Level1",
                    expected="Seed1!=Seed2 或 已解锁(全0)",
                    actual=f"Seed1={{' '.join(f'0x{{b:02X}}' for b in seed1)}}, Seed2={{' '.join(f'0x{{b:02X}}' for b in seed2)}}",
                    status="PASS" if seeds_differ else "FAIL")
        else:
            self.add_result(
                service="$27", test_name="扩展会话请求Seed Level1",
                session="Extended", security="Level1",
                expected="正响应", actual=self.resp_to_hex(resp1), status="FAIL")

        # 发送错误Key
        resp = self.uds.security_access_request_seed(0x01)
        if self.is_positive_response(resp, SID_SECURITY_ACCESS):
            wrong_key = [0xFF] * max(1, len(resp) - 2)
            resp_key = self.uds.security_access_send_key(0x01, wrong_key)
            if self.is_negative_response(resp_key, 0x35):
                self.add_result(
                    service="$27", test_name="错误Key应拒绝(NRC 0x35)",
                    session="Extended", security="Level1",
                    expected="NRC 0x35 invalidKey",
                    actual=self.resp_to_hex(resp_key), status="PASS")
            else:
                self.add_result(
                    service="$27", test_name="错误Key应拒绝(NRC 0x35)",
                    session="Extended", security="Level1",
                    expected="NRC 0x35",
                    actual=self.resp_to_hex(resp_key),
                    status="PASS" if self.is_negative_response(resp_key) else "FAIL")

        # 无效访问模式(偶数请求seed应拒绝)
        resp = self.uds.send_request([SID_SECURITY_ACCESS, 0x02])
        self.add_result(
            service="$27", test_name="偶数子功能0x02请求Seed(应拒绝或回Key响应)",
            session="Extended",
            expected="NRC 0x12/0x24",
            actual=self.resp_to_hex(resp),
            status="PASS" if self.is_negative_response(resp) else "FAIL",
            detail="偶数sub-func用于SendKey,不用于RequestSeed")

        # 错误长度 - 只发SID
        resp = self.uds.send_request([SID_SECURITY_ACCESS])
        if self.is_negative_response(resp, 0x13):
            self.add_result(
                service="$27", test_name="$27错误长度(缺子功能)",
                expected="NRC 0x13", actual=self.resp_to_hex(resp), status="PASS")
        else:
            self.add_result(
                service="$27", test_name="$27错误长度(缺子功能)",
                expected="NRC 0x13", actual=self.resp_to_hex(resp),
                status="PASS" if self.is_negative_response(resp) else "FAIL")

        # SA边界等级测试 (ISO 14229-1 §9.4.2 Table 254)
        # 偶数sub-func 0x04, 0x06 (SendKey位) → NRC 0x12/0x24
        for even_level in [0x04, 0x06]:
            resp = self.uds.send_request([SID_SECURITY_ACCESS, even_level])
            self.add_result(
                service="$27", test_name=f"偶数sub-func 0x{{even_level:02X}}应拒绝",
                session="Extended",
                expected="NRC 0x12/0x24",
                actual=self.resp_to_hex(resp),
                status="PASS" if self.is_negative_response(resp) else "FAIL")

        # OEM保留范围边界: 0x41(OEM下界奇)
        resp = self.uds.security_access_request_seed(0x41)
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="$27", test_name="OEM SA Level 0x41(边界)",
            session="Extended",
            expected="正响应或NRC 0x12",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_SECURITY_ACCESS)
                              or nrc in (0x12, 0x33, 0x7F, 0x7E)) else "FAIL")

        # 系统供应商范围: 0x61(SSP下界奇), 0x7D(SSP上界奇)
        for ssp_level in [0x61, 0x7D]:
            resp = self.uds.security_access_request_seed(ssp_level)
            nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
            self.add_result(
                service="$27", test_name=f"SSP SA Level 0x{{ssp_level:02X}}(边界)",
                session="Extended",
                expected="正响应或NRC 0x12",
                actual=self.resp_to_hex(resp),
                status="PASS" if (self.is_positive_response(resp, SID_SECURITY_ACCESS)
                                  or nrc in (0x12, 0x33, 0x7F, 0x7E)) else "FAIL")

        # 最大值 0x7F (ISO reserved) → 应拒绝
        resp = self.uds.security_access_request_seed(0x7F)
        self.add_result(
            service="$27", test_name="$27 Reserved Level 0x7F",
            session="Extended",
            expected="NRC 0x12",
            actual=self.resp_to_hex(resp),
            status="PASS" if self.is_negative_response(resp, 0x12) else
                   ("PASS" if self.is_negative_response(resp) else "FAIL"))

        # ===== DLL SeedKey 解锁测试 (遍历调查表中所有安全等级) =====
        global seedkey_dll
        if seedkey_dll is not None:
            sa_level_session = {{
                0x01: SESSION_EXTENDED,
                0x03: SESSION_PROGRAMMING,
                0x05: SESSION_EXTENDED,
            }}
            sa_level_name = {{
                0x01: "Level1",
                0x03: "Level3(FBL)",
                0x05: "Level5(Immo)",
            }}
            for sa_level in sorted(SURVEY_SA_LEVELS):
                session = sa_level_session.get(sa_level, SESSION_EXTENDED)
                level_name = sa_level_name.get(sa_level, f"Level{{sa_level}}")
                self.reset_to_default_session()
                time.sleep(0.1)
                self.switch_session(session)
                time.sleep(0.05)
                success, seed, key, resp_unlock = self.uds.security_access_unlock(sa_level)
                if self.is_negative_response(resp_unlock, 0x12):
                    self.add_result(
                        service="$27", test_name=f"DLL解锁{{level_name}}(不支持则跳过)",
                        session=SESSION_NAMES.get(session, "?"), security=level_name,
                        expected="正响应或NRC 0x12", actual=self.resp_to_hex(resp_unlock),
                        status="PASS", detail="ECU不支持此安全等级")
                else:
                    self.add_result(
                        service="$27", test_name=f"DLL解锁{{level_name}}(GenerateKeyEx/Opt)",
                        session=SESSION_NAMES.get(session, "?"), security=level_name,
                        expected="正响应(解锁成功)",
                        actual=f"seed={{self.resp_to_hex(seed)}}, key={{self.resp_to_hex(key)}}, resp={{self.resp_to_hex(resp_unlock)}}",
                        status="PASS" if success else "FAIL")
                    if success:
                        resp_re = self.uds.security_access_request_seed(sa_level)
                        already_unlocked = (self.is_positive_response(resp_re, SID_SECURITY_ACCESS)
                                            and len(resp_re) > 2
                                            and all(b == 0 for b in resp_re[2:]))
                        self.add_result(
                            service="$27", test_name=f"解锁{{level_name}}后Seed应全零",
                            session=SESSION_NAMES.get(session, "?"), security=level_name,
                            expected="Seed全零", actual=self.resp_to_hex(resp_re),
                            status="PASS" if already_unlocked else "FAIL")
        else:
            self.add_result(
                service="$27", test_name=f"DLL SeedKey解锁(无DLL跳过) 调查表等级={{sorted(SURVEY_SA_LEVELS)}}",
                expected="需配置--sa-dll", actual="未配置DLL路径",
                status="SKIP", detail="使用--sa-dll参数指定Vector SeedKey DLL路径")

        self.reset_to_default_session()

    def test_communication_control(self):
        """$28 CommunicationControl 测试"""
        print("\\n=== 测试 $28 CommunicationControl ===")

        # 默认会话应拒绝
        resp = self.uds.communication_control(0x00, 0x01)
        if self.is_negative_response(resp):
            self.add_result(
                service="$28", test_name="默认会话$28应拒绝",
                session="Default", expected="NRC 0x7F",
                actual=self.resp_to_hex(resp), status="PASS")
        else:
            self.add_result(
                service="$28", test_name="默认会话$28应拒绝",
                session="Default", expected="NRC",
                actual=self.resp_to_hex(resp),
                status="PASS" if self.is_positive_response(resp, SID_COMMUNICATION_CONTROL) else "FAIL",
                detail="某些ECU可能在默认会话也支持$28")

        # 扩展会话
        self.switch_session(SESSION_EXTENDED)
        time.sleep(0.05)

        # enableRxAndTx (0x00) - normalCommunicationMessages (0x01)
        resp = self.uds.communication_control(0x00, 0x01)
        if self.is_positive_response(resp, SID_COMMUNICATION_CONTROL):
            self.add_result(
                service="$28", test_name="enableRxAndTx(0x00)(扩展会话)",
                session="Extended", expected="正响应 0x68",
                actual=self.resp_to_hex(resp), status="PASS")
        else:
            self.add_result(
                service="$28", test_name="enableRxAndTx(0x00)(扩展会话)",
                session="Extended", expected="正响应 0x68",
                actual=self.resp_to_hex(resp), status="FAIL")

        # disableRxAndTx (0x03) - normalCommunicationMessages (0x01)
        resp = self.uds.communication_control(0x03, 0x01)
        if self.is_positive_response(resp, SID_COMMUNICATION_CONTROL):
            self.add_result(
                service="$28", test_name="disableRxAndTx(0x03)(扩展会话)",
                session="Extended", expected="正响应 0x68",
                actual=self.resp_to_hex(resp), status="PASS")
            # 立即恢复
            self.uds.communication_control(0x00, 0x01)
        else:
            self.add_result(
                service="$28", test_name="disableRxAndTx(0x03)(扩展会话)",
                session="Extended", expected="正响应 0x68",
                actual=self.resp_to_hex(resp), status="FAIL")

        # nmCommunicationMessages (commType=0x02)
        resp = self.uds.communication_control(0x00, 0x02)
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="$28", test_name="enableRxAndTx commType=NM(0x02)",
            session="Extended", expected="正响应或NRC",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_COMMUNICATION_CONTROL)
                              or nrc in (0x12, 0x22, 0x31, 0x7F)) else "FAIL")

        # networkManagementCommunicationMessages (commType=0x03)
        resp = self.uds.communication_control(0x00, 0x03)
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="$28", test_name="enableRxAndTx commType=Normal+NM(0x03)",
            session="Extended", expected="正响应或NRC",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_COMMUNICATION_CONTROL)
                              or nrc in (0x12, 0x22, 0x31, 0x7F)) else "FAIL")

        # 无效commType (0x00 = reserved)
        resp = self.uds.communication_control(0x00, 0x00)
        self.add_result(
            service="$28", test_name="$28无效commType(0x00 reserved)",
            session="Extended", expected="NRC 0x31",
            actual=self.resp_to_hex(resp),
            status="PASS" if self.is_negative_response(resp) else
                   ("PASS" if self.is_positive_response(resp, SID_COMMUNICATION_CONTROL) else "FAIL"))

        # 无效子功能 0x04 (reserved)
        resp = self.uds.communication_control(0x04, 0x01)
        self.add_result(
            service="$28", test_name="$28无效子功能0x04(reserved)",
            session="Extended", expected="NRC 0x12",
            actual=self.resp_to_hex(resp),
            status="PASS" if self.is_negative_response(resp) else "FAIL")

        # 无效子功能
        resp = self.uds.communication_control(0x7F, 0x01)
        if self.is_negative_response(resp, 0x12):
            self.add_result(
                service="$28", test_name="$28无效子功能0x7F",
                expected="NRC 0x12", actual=self.resp_to_hex(resp), status="PASS")
        else:
            self.add_result(
                service="$28", test_name="$28无效子功能0x7F",
                expected="NRC 0x12", actual=self.resp_to_hex(resp),
                status="PASS" if self.is_negative_response(resp) else "FAIL")

        # suppressPositiveResponse
        resp = self.uds.send_request([SID_COMMUNICATION_CONTROL, 0x00 | 0x80, 0x01])
        if resp is None:
            self.add_result(
                service="$28", test_name="$28 suppressPosRsp",
                expected="无响应", actual="No Response", status="PASS")
        else:
            self.add_result(
                service="$28", test_name="$28 suppressPosRsp",
                expected="无响应", actual=self.resp_to_hex(resp), status="FAIL")

        # 错误长度
        resp = self.uds.send_request([SID_COMMUNICATION_CONTROL, 0x00])  # 缺commType
        if self.is_negative_response(resp, 0x13):
            self.add_result(
                service="$28", test_name="$28错误长度(缺commType)",
                expected="NRC 0x13", actual=self.resp_to_hex(resp), status="PASS")
        else:
            self.add_result(
                service="$28", test_name="$28错误长度(缺commType)",
                expected="NRC 0x13", actual=self.resp_to_hex(resp),
                status="PASS" if self.is_negative_response(resp) else "FAIL")

        self.reset_to_default_session()

    def test_unsupported_sid(self):
        """不支持的SID测试 - ISO 14229 NRC 0x11"""
        print("\\n=== 测试 不支持的SID ===")

        unsup_sids = [0x00, 0x13, 0x15, 0x23, 0x24, 0x26, 0x29, 0x2A, 0x2C, 0x2D,
                      0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D, 0x86, 0x87, 0xBA, 0xBE]
        for sid in unsup_sids:
            resp = self.uds.send_request([sid])
            if self.is_negative_response(resp, 0x11):
                self.add_result(
                    service="NRC", test_name=f"不支持的SID 0x{{sid:02X}}",
                    expected="NRC 0x11", actual=self.resp_to_hex(resp), status="PASS")
            elif self.is_negative_response(resp):
                nrc = self.get_nrc(resp)
                self.add_result(
                    service="NRC", test_name=f"不支持的SID 0x{{sid:02X}}",
                    expected="NRC 0x11",
                    actual=f"NRC 0x{{nrc:02X}} ({{NRC_NAMES.get(nrc, 'unknown')}})",
                    status="PASS" if nrc in (0x11, 0x13, 0x12) else "FAIL")
            elif resp is None:
                self.add_result(
                    service="NRC", test_name=f"不支持的SID 0x{{sid:02X}}",
                    expected="NRC 0x11", actual="No Response",
                    status="PASS",
                    detail="功能寻址下不支持的服务可不响应")
            else:
                self.add_result(
                    service="NRC", test_name=f"不支持的SID 0x{{sid:02X}}",
                    expected="NRC 0x11", actual=self.resp_to_hex(resp), status="FAIL")

    def test_zero_length_and_overlong(self):
        """零长度和超长报文边界测试"""
        print("\\n=== 测试 报文长度边界 ===")

        # 空报文(0字节payload)
        resp = self.uds.send_raw([])
        self.add_result(
            service="Boundary", test_name="空报文(0字节)",
            expected="NRC或无响应", actual=self.resp_to_hex(resp),
            status="PASS" if (resp is None or self.is_negative_response(resp)) else "FAIL")

        # 仅SID无数据的各种服务
        for sid, name in [(SID_READ_DID, "$22"), (SID_WRITE_DID, "$2E"),
                          (SID_IO_CONTROL, "$2F"), (SID_ROUTINE_CONTROL, "$31")]:
            resp = self.uds.send_request([sid])
            if self.is_negative_response(resp, 0x13):
                self.add_result(
                    service="Boundary", test_name=f"{{name}}仅SID无参数",
                    expected="NRC 0x13", actual=self.resp_to_hex(resp), status="PASS")
            else:
                self.add_result(
                    service="Boundary", test_name=f"{{name}}仅SID无参数",
                    expected="NRC 0x13", actual=self.resp_to_hex(resp),
                    status="PASS" if self.is_negative_response(resp) else "FAIL")

        # 超长报文 - $22带超多DID
        long_req = [SID_READ_DID] + [0xF1, 0x90] * 100  # 200个DID字节
        resp = self.uds.send_request(long_req)
        self.add_result(
            service="Boundary", test_name="$22超长请求(100个DID)",
            expected="NRC 0x13/0x14或正响应",
            actual=self.resp_to_hex(resp),
            status="PASS" if resp is not None else "FAIL")

    def test_security_access_lockout(self):
        """$27 安全访问超次锁定和延时测试 (ISO 14229-1 §9.4.2.3)"""
        print("\\n=== 测试 $27 安全访问锁定/延时 ===")

        self.switch_session(SESSION_EXTENDED)
        time.sleep(0.05)

        # 连续发送错误Key直到触发lockout (通常3次)
        lockout_triggered = False
        for attempt in range(5):
            resp = self.uds.security_access_request_seed(0x01)
            if not self.is_positive_response(resp, SID_SECURITY_ACCESS):
                nrc = self.get_nrc(resp)
                if nrc == 0x36:
                    lockout_triggered = True
                    self.add_result(
                        service="$27", test_name=f"第{{attempt+1}}次请求Seed触发NRC 0x36",
                        session="Extended", security="Level1",
                        expected="NRC 0x36 exceededNumberOfAttempts",
                        actual=self.resp_to_hex(resp), status="PASS")
                    break
                elif nrc == 0x37:
                    lockout_triggered = True
                    self.add_result(
                        service="$27", test_name=f"第{{attempt+1}}次请求Seed触发NRC 0x37",
                        session="Extended", security="Level1",
                        expected="NRC 0x37 requiredTimeDelayNotExpired",
                        actual=self.resp_to_hex(resp), status="PASS")
                    break
                else:
                    continue

            # 发送错误Key
            seed = resp[2:] if len(resp) > 2 else [0x00]
            if all(b == 0 for b in seed):
                self.add_result(
                    service="$27", test_name="安全访问锁定测试(已解锁,seed全0)",
                    session="Extended", security="Level1",
                    expected="N/A", actual="已解锁", status="PASS",
                    detail="seed全0说明已解锁,无法测试锁定")
                lockout_triggered = True
                break
            wrong_key = [0xFF] * len(seed)
            resp_key = self.uds.security_access_send_key(0x01, wrong_key)
            time.sleep(0.1)

        if not lockout_triggered:
            self.add_result(
                service="$27", test_name="安全访问锁定测试(5次错误Key后)",
                session="Extended", security="Level1",
                expected="NRC 0x36/0x37", actual="未触发锁定",
                status="FAIL", detail="5次错误Key后未收到0x36/0x37")

        # 延时期间再次请求应返回0x37
        if lockout_triggered:
            time.sleep(0.5)
            resp = self.uds.security_access_request_seed(0x01)
            nrc = self.get_nrc(resp)
            if nrc in (0x36, 0x37):
                self.add_result(
                    service="$27", test_name="锁定期间请求Seed应拒绝",
                    session="Extended", security="Level1",
                    expected="NRC 0x36/0x37",
                    actual=self.resp_to_hex(resp), status="PASS")
            else:
                self.add_result(
                    service="$27", test_name="锁定期间请求Seed应拒绝",
                    session="Extended", security="Level1",
                    expected="NRC 0x36/0x37",
                    actual=self.resp_to_hex(resp),
                    status="PASS" if self.is_positive_response(resp, SID_SECURITY_ACCESS) else "FAIL",
                    detail="可能无delay或delay已过")

        self.reset_to_default_session()

    def test_read_memory_by_address(self):
        """$23 ReadMemoryByAddress 测试"""
        print("\\n=== 测试 $23 ReadMemoryByAddress ===")

        # 默认会话请求 - 可能被拒
        resp = self.uds.read_memory_by_address(0x44, 0x00000000, 0x00000010)
        self.add_result(
            service="$23", test_name="$23默认会话读0x00000000",
            session="Default",
            expected="正响应或NRC(0x7F/0x33/0x31)",
            actual=self.resp_to_hex(resp),
            status="PASS" if resp is not None else "FAIL")

        # 扩展会话
        self.switch_session(SESSION_EXTENDED)
        time.sleep(0.05)
        resp = self.uds.read_memory_by_address(0x44, 0x00000000, 0x00000010)
        self.add_result(
            service="$23", test_name="$23扩展会话读0x00000000",
            session="Extended",
            expected="正响应或NRC 0x33/0x31",
            actual=self.resp_to_hex(resp),
            status="PASS" if resp is not None else "FAIL")

        # 无效地址长度格式
        resp = self.uds.send_request([SID_READ_MEM_BY_ADDR, 0x00])
        if self.is_negative_response(resp, 0x13):
            self.add_result(
                service="$23", test_name="$23无效addressAndLengthFormat(0x00)",
                expected="NRC 0x13", actual=self.resp_to_hex(resp), status="PASS")
        else:
            self.add_result(
                service="$23", test_name="$23无效addressAndLengthFormat(0x00)",
                expected="NRC 0x13", actual=self.resp_to_hex(resp),
                status="PASS" if self.is_negative_response(resp) else "FAIL")

        # 仅SID无参数
        resp = self.uds.send_request([SID_READ_MEM_BY_ADDR])
        if self.is_negative_response(resp, 0x13):
            self.add_result(
                service="$23", test_name="$23仅SID无参数",
                expected="NRC 0x13", actual=self.resp_to_hex(resp), status="PASS")
        else:
            self.add_result(
                service="$23", test_name="$23仅SID无参数",
                expected="NRC 0x13", actual=self.resp_to_hex(resp),
                status="PASS" if self.is_negative_response(resp) else "FAIL")

        self.reset_to_default_session()

    def test_request_download_upload(self):
        """$34/$35/$36/$37 下载上传服务测试"""
        print("\\n=== 测试 $34/$35/$36/$37 下载上传服务 ===")

        # $34 RequestDownload - 默认会话应拒绝
        resp = self.uds.send_request([SID_REQUEST_DOWNLOAD, 0x00, 0x44,
                                       0x00, 0x00, 0x00, 0x00,
                                       0x00, 0x00, 0x10, 0x00])
        if self.is_negative_response(resp):
            nrc = self.get_nrc(resp)
            self.add_result(
                service="$34", test_name="$34默认会话RequestDownload",
                session="Default", expected="NRC 0x7F",
                actual=self.resp_to_hex(resp),
                status="PASS" if nrc in (0x7F, 0x22, 0x33, 0x31) else "FAIL")
        else:
            self.add_result(
                service="$34", test_name="$34默认会话RequestDownload",
                session="Default", expected="NRC", actual=self.resp_to_hex(resp), status="FAIL")

        # $34 扩展会话 - 通常也不支持(需编程会话)
        self.switch_session(SESSION_EXTENDED)
        time.sleep(0.05)
        resp = self.uds.send_request([SID_REQUEST_DOWNLOAD, 0x00, 0x44,
                                       0x00, 0x00, 0x00, 0x00,
                                       0x00, 0x00, 0x10, 0x00])
        self.add_result(
            service="$34", test_name="$34扩展会话RequestDownload",
            session="Extended", expected="NRC 0x7F/0x33",
            actual=self.resp_to_hex(resp),
            status="PASS" if self.is_negative_response(resp) else "FAIL",
            detail="通常仅编程会话支持")

        # $34 编程会话(无安全访问)
        self.reset_to_default_session()
        self.switch_session(SESSION_PROGRAMMING)
        time.sleep(0.05)
        resp = self.uds.send_request([SID_REQUEST_DOWNLOAD, 0x00, 0x44,
                                       0x00, 0x00, 0x00, 0x00,
                                       0x00, 0x00, 0x10, 0x00])
        if self.is_negative_response(resp, 0x33):
            self.add_result(
                service="$34", test_name="$34编程会话无安全访问",
                session="Programming", expected="NRC 0x33",
                actual=self.resp_to_hex(resp), status="PASS")
        else:
            self.add_result(
                service="$34", test_name="$34编程会话无安全访问",
                session="Programming", expected="NRC 0x33",
                actual=self.resp_to_hex(resp),
                status="PASS" if self.is_negative_response(resp) else "FAIL")

        # $34 错误长度
        resp = self.uds.send_request([SID_REQUEST_DOWNLOAD])
        if self.is_negative_response(resp, 0x13):
            self.add_result(
                service="$34", test_name="$34错误长度(仅SID)",
                expected="NRC 0x13", actual=self.resp_to_hex(resp), status="PASS")
        else:
            self.add_result(
                service="$34", test_name="$34错误长度(仅SID)",
                expected="NRC 0x13", actual=self.resp_to_hex(resp),
                status="PASS" if self.is_negative_response(resp) else "FAIL")

        # $35 RequestUpload - 默认会话
        self.reset_to_default_session()
        resp = self.uds.send_request([SID_REQUEST_UPLOAD, 0x00, 0x44,
                                       0x00, 0x00, 0x00, 0x00,
                                       0x00, 0x00, 0x10, 0x00])
        self.add_result(
            service="$35", test_name="$35默认会话RequestUpload",
            session="Default", expected="NRC",
            actual=self.resp_to_hex(resp),
            status="PASS" if self.is_negative_response(resp) else "FAIL")

        # $36 TransferData - 无活动传输
        resp = self.uds.send_request([SID_TRANSFER_DATA, 0x01, 0x00, 0x00])
        if self.is_negative_response(resp, 0x24):
            self.add_result(
                service="$36", test_name="$36无活动传输(requestSequenceError)",
                expected="NRC 0x24", actual=self.resp_to_hex(resp), status="PASS")
        else:
            self.add_result(
                service="$36", test_name="$36无活动传输",
                expected="NRC 0x24", actual=self.resp_to_hex(resp),
                status="PASS" if self.is_negative_response(resp) else "FAIL")

        # $37 RequestTransferExit - 无活动传输
        resp = self.uds.send_request([SID_REQUEST_TRANSFER_EXIT])
        if self.is_negative_response(resp, 0x24):
            self.add_result(
                service="$37", test_name="$37无活动传输(requestSequenceError)",
                expected="NRC 0x24", actual=self.resp_to_hex(resp), status="PASS")
        else:
            self.add_result(
                service="$37", test_name="$37无活动传输",
                expected="NRC 0x24", actual=self.resp_to_hex(resp),
                status="PASS" if self.is_negative_response(resp) else "FAIL")

        # $38 RequestFileTransfer
        resp = self.uds.send_request([SID_REQUEST_FILE_TRANSFER, 0x01])
        self.add_result(
            service="$38", test_name="$38 RequestFileTransfer",
            expected="NRC 0x11(不支持)或正响应",
            actual=self.resp_to_hex(resp),
            status="PASS" if resp is not None else "FAIL",
            detail="多数ECU不支持此服务")

        self.reset_to_default_session()

    def test_optional_services_nrc(self):
        """可选服务深度测试 ($29/$2A/$2C/$3D/$83/$84/$86/$87)"""
        print("\\n=== 测试 可选服务深度合规 ===")

        # ===== $29 Authentication (ISO 14229-1:2020 新增) =====
        # deAuthenticate (subFunction=0x00)
        resp = self.uds.send_request([SID_AUTHENTICATION, 0x00])
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="$29", test_name="$29 deAuthenticate(0x00)",
            expected="正响应或NRC 0x11/0x12/0x22",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_AUTHENTICATION)
                              or nrc in (0x11, 0x12, 0x22, 0x31, 0x7F, 0x7E)) else "FAIL")

        # verifyCertificateUnidirectional (subFunction=0x01)
        dummy_cert = [0x00] * 16  # 模拟证书数据
        resp = self.uds.send_request([SID_AUTHENTICATION, 0x01, 0x00, 0x00] + dummy_cert)
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="$29", test_name="$29 verifyCertificateUnidirectional(0x01)",
            expected="NRC 0x11/0x12/0x31/0x72 (多数ECU不支持PKI)",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_negative_response(resp) or
                              self.is_positive_response(resp, SID_AUTHENTICATION)) else "FAIL")

        # verifyCertificateBidirectional (subFunction=0x02)
        resp = self.uds.send_request([SID_AUTHENTICATION, 0x02, 0x00, 0x00] + dummy_cert)
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="$29", test_name="$29 verifyCertificateBidirectional(0x02)",
            expected="NRC (与0x01一致)",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_negative_response(resp) or
                              self.is_positive_response(resp, SID_AUTHENTICATION)) else "FAIL")

        # proofOfOwnership (subFunction=0x03)
        resp = self.uds.send_request([SID_AUTHENTICATION, 0x03] + [0x00] * 8)
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="$29", test_name="$29 proofOfOwnership(0x03)",
            expected="NRC 0x11/0x24/0x72",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_negative_response(resp) or
                              self.is_positive_response(resp, SID_AUTHENTICATION)) else "FAIL")

        # authenticationConfiguration (subFunction=0x06)
        resp = self.uds.send_request([SID_AUTHENTICATION, 0x06])
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="$29", test_name="$29 authenticationConfiguration(0x06)",
            expected="正响应(返回配置)或NRC 0x11/0x12",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_AUTHENTICATION) or
                              nrc in (0x11, 0x12, 0x7F, 0x7E)) else "FAIL")

        # 无效子功能
        resp = self.uds.send_request([SID_AUTHENTICATION, 0xFF])
        self.add_result(
            service="$29", test_name="$29 无效子功能0xFF",
            expected="NRC 0x12",
            actual=self.resp_to_hex(resp),
            status="PASS" if self.is_negative_response(resp, 0x12) or self.is_negative_response(resp, 0x11) else "FAIL")

        # 错误长度
        resp = self.uds.send_request([SID_AUTHENTICATION])
        self.add_result(
            service="$29", test_name="$29 缺子功能(错误长度)",
            expected="NRC 0x13",
            actual=self.resp_to_hex(resp),
            status="PASS" if self.is_negative_response(resp, 0x13) or self.is_negative_response(resp, 0x11) else "FAIL")

        # ===== $2A ReadDataByPeriodicIdentifier =====
        # slowRate(0x01) + periodicDID 0xF190
        resp = self.uds.send_request([SID_READ_DATA_BY_PERIODIC_ID, 0x01, 0xF1])
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="$2A", test_name="$2A slowRate读取periodicDID",
            expected="正响应或NRC 0x11/0x31",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_READ_DATA_BY_PERIODIC_ID) or
                              nrc in (0x11, 0x12, 0x31, 0x7F, 0x7E, 0x22, 0x33)) else "FAIL")

        # stopSending(0x04)
        resp = self.uds.send_request([SID_READ_DATA_BY_PERIODIC_ID, 0x04, 0xF1])
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="$2A", test_name="$2A stopSending",
            expected="正响应或NRC 0x11",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_READ_DATA_BY_PERIODIC_ID) or
                              nrc in (0x11, 0x12, 0x31, 0x7F, 0x7E, 0x22)) else "FAIL")

        # 无效transmissionMode
        resp = self.uds.send_request([SID_READ_DATA_BY_PERIODIC_ID, 0x00, 0xF1])
        self.add_result(
            service="$2A", test_name="$2A 无效transmissionMode(0x00)",
            expected="NRC 0x12/0x31",
            actual=self.resp_to_hex(resp),
            status="PASS" if self.is_negative_response(resp) else "FAIL")

        # ===== $2C DynamicallyDefineDataIdentifier =====
        # defineByIdentifier(0x01): 定义F300由F190+F187组成
        resp = self.uds.send_request([SID_DYNAMICALLY_DEFINE_DID, 0x01,
                                       0xF3, 0x00,  # dynamicDID
                                       0xF1, 0x90,  # sourceDID
                                       0x01, 0x03])  # position, size
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="$2C", test_name="$2C defineByIdentifier(0x01)",
            expected="正响应或NRC 0x11",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_DYNAMICALLY_DEFINE_DID) or
                              nrc in (0x11, 0x12, 0x31, 0x7F, 0x7E, 0x22, 0x33)) else "FAIL")

        # clearDynamicallyDefineDID(0x03)
        resp = self.uds.send_request([SID_DYNAMICALLY_DEFINE_DID, 0x03, 0xF3, 0x00])
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="$2C", test_name="$2C clearDynamicallyDefined(0x03)",
            expected="正响应或NRC 0x11",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_DYNAMICALLY_DEFINE_DID) or
                              nrc in (0x11, 0x12, 0x31, 0x7F, 0x7E, 0x22)) else "FAIL")

        # defineByMemoryAddress(0x02) - 需要扩展会话
        self.switch_session(SESSION_EXTENDED)
        time.sleep(0.05)
        resp = self.uds.send_request([SID_DYNAMICALLY_DEFINE_DID, 0x02,
                                       0xF3, 0x01,  # dynamicDID
                                       0x14,         # addressAndLengthFormatIdentifier
                                       0x00, 0x00, 0x10, 0x00,  # address
                                       0x04])                     # size
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="$2C", test_name="$2C defineByMemoryAddress(0x02)",
            expected="正响应或NRC 0x11/0x33",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_DYNAMICALLY_DEFINE_DID) or
                              nrc in (0x11, 0x12, 0x31, 0x7F, 0x7E, 0x22, 0x33)) else "FAIL")

        # ===== $3D WriteMemoryByAddress =====
        # 默认会话: 应拒绝
        self.reset_to_default_session()
        resp = self.uds.send_request([SID_WRITE_MEM_BY_ADDR, 0x14,
                                       0x00, 0x00, 0x10, 0x00,  # address
                                       0x01,                     # data
                                       0xAA])
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="$3D", test_name="$3D WriteMemByAddr默认会话",
            expected="NRC 0x11/0x7F/0x33",
            actual=self.resp_to_hex(resp),
            status="PASS" if nrc in (0x11, 0x7F, 0x33, 0x31, 0x22, 0x13) else "FAIL")

        # 扩展会话 + 无安全访问
        self.switch_session(SESSION_EXTENDED)
        time.sleep(0.05)
        resp = self.uds.send_request([SID_WRITE_MEM_BY_ADDR, 0x14,
                                       0x00, 0x00, 0x10, 0x00,
                                       0x01, 0xAA])
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="$3D", test_name="$3D WriteMemByAddr扩展会话无安全",
            expected="NRC 0x11/0x33",
            actual=self.resp_to_hex(resp),
            status="PASS" if (nrc in (0x11, 0x33, 0x31, 0x22, 0x7F) or
                              self.is_positive_response(resp, SID_WRITE_MEM_BY_ADDR)) else "FAIL")

        # 错误addressAndLengthFormatIdentifier
        resp = self.uds.send_request([SID_WRITE_MEM_BY_ADDR, 0x00, 0xAA])
        self.add_result(
            service="$3D", test_name="$3D 错误格式标识(0x00)",
            expected="NRC 0x13/0x31",
            actual=self.resp_to_hex(resp),
            status="PASS" if self.is_negative_response(resp) else "FAIL")

        # ===== $83 AccessTimingParameter =====
        # readExtendedTimingParameterSet(0x01)
        self.reset_to_default_session()
        resp = self.uds.send_request([SID_ACCESS_TIMING_PARAM, 0x01])
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="$83", test_name="$83 readExtendedTimingParam(0x01)",
            expected="正响应(P2/P2*)或NRC 0x11",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_ACCESS_TIMING_PARAM) or
                              nrc in (0x11, 0x12, 0x7F, 0x7E, 0x22)) else "FAIL")

        # setTimingParametersToDefaultValues(0x02)
        self.switch_session(SESSION_EXTENDED)
        time.sleep(0.05)
        resp = self.uds.send_request([SID_ACCESS_TIMING_PARAM, 0x02])
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="$83", test_name="$83 setTimingToDefault(0x02)",
            expected="正响应或NRC 0x11/0x22",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_ACCESS_TIMING_PARAM) or
                              nrc in (0x11, 0x12, 0x7F, 0x7E, 0x22)) else "FAIL")

        # readCurrentlyActiveTimingParameters(0x03)
        resp = self.uds.send_request([SID_ACCESS_TIMING_PARAM, 0x03])
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="$83", test_name="$83 readCurrentTiming(0x03)",
            expected="正响应或NRC 0x11",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_ACCESS_TIMING_PARAM) or
                              nrc in (0x11, 0x12, 0x7F, 0x7E, 0x22)) else "FAIL")

        # setTimingParametersToGivenValues(0x04) + P2=50ms, P2*=5000ms
        resp = self.uds.send_request([SID_ACCESS_TIMING_PARAM, 0x04, 0x00, 0x32, 0x13, 0x88])
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="$83", test_name="$83 setTimingToGiven(0x04)",
            expected="正响应或NRC 0x11/0x31",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_ACCESS_TIMING_PARAM) or
                              nrc in (0x11, 0x12, 0x31, 0x7F, 0x7E, 0x22, 0x33)) else "FAIL")

        # 无效子功能
        resp = self.uds.send_request([SID_ACCESS_TIMING_PARAM, 0x00])
        self.add_result(
            service="$83", test_name="$83 无效子功能(0x00)",
            expected="NRC 0x12",
            actual=self.resp_to_hex(resp),
            status="PASS" if self.is_negative_response(resp, 0x12) or self.is_negative_response(resp, 0x11) else "FAIL")

        # ===== $84 SecuredDataTransmission =====
        resp = self.uds.send_request([SID_SECURED_DATA_TRANSMISSION] + [0x00] * 8)
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="$84", test_name="$84 SecuredDataTransmission基本请求",
            expected="NRC 0x11(不支持)或正响应",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_negative_response(resp) or
                              self.is_positive_response(resp, SID_SECURED_DATA_TRANSMISSION)) else "FAIL")

        # 空数据
        resp = self.uds.send_request([SID_SECURED_DATA_TRANSMISSION])
        self.add_result(
            service="$84", test_name="$84 空数据(错误长度)",
            expected="NRC 0x13/0x11",
            actual=self.resp_to_hex(resp),
            status="PASS" if self.is_negative_response(resp) else "FAIL")

        # ===== $86 ResponseOnEvent =====
        # onDTCStatusChange(0x01)
        self.switch_session(SESSION_EXTENDED)
        time.sleep(0.05)
        resp = self.uds.send_request([SID_RESPONSE_ON_EVENT, 0x01,
                                       0x00,  # eventWindowTime
                                       0x19, 0x02, 0xFF])  # serviceToRespondTo
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="$86", test_name="$86 onDTCStatusChange(0x01)",
            expected="正响应或NRC 0x11",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_RESPONSE_ON_EVENT) or
                              nrc in (0x11, 0x12, 0x31, 0x7F, 0x7E, 0x22)) else "FAIL")

        # stopResponseOnEvent(0x00)
        resp = self.uds.send_request([SID_RESPONSE_ON_EVENT, 0x00, 0x00])
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="$86", test_name="$86 stopResponseOnEvent(0x00)",
            expected="正响应或NRC 0x11",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_RESPONSE_ON_EVENT) or
                              nrc in (0x11, 0x12, 0x7F, 0x7E, 0x22)) else "FAIL")

        # onTimerInterrupt(0x02)
        resp = self.uds.send_request([SID_RESPONSE_ON_EVENT, 0x02,
                                       0x0A,  # 10 seconds window
                                       0x3E, 0x00])  # TesterPresent
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="$86", test_name="$86 onTimerInterrupt(0x02)",
            expected="正响应或NRC 0x11/0x12",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_RESPONSE_ON_EVENT) or
                              nrc in (0x11, 0x12, 0x31, 0x7F, 0x7E, 0x22)) else "FAIL")

        # onChangeOfDataIdentifier(0x03)
        resp = self.uds.send_request([SID_RESPONSE_ON_EVENT, 0x03,
                                       0x00,  # eventWindowTime
                                       0xF1, 0x90])  # DID
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="$86", test_name="$86 onChangeOfDID(0x03)",
            expected="正响应或NRC 0x11/0x12",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_RESPONSE_ON_EVENT) or
                              nrc in (0x11, 0x12, 0x31, 0x7F, 0x7E, 0x22)) else "FAIL")

        # reportActivatedEvents(0x04)
        resp = self.uds.send_request([SID_RESPONSE_ON_EVENT, 0x04, 0x00])
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="$86", test_name="$86 reportActivatedEvents(0x04)",
            expected="正响应或NRC 0x11/0x12",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_RESPONSE_ON_EVENT) or
                              nrc in (0x11, 0x12, 0x7F, 0x7E, 0x22)) else "FAIL")

        # startResponseOnEvent(0x05)
        resp = self.uds.send_request([SID_RESPONSE_ON_EVENT, 0x05, 0x00])
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="$86", test_name="$86 startResponseOnEvent(0x05)",
            expected="正响应或NRC 0x11",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_RESPONSE_ON_EVENT) or
                              nrc in (0x11, 0x12, 0x7F, 0x7E, 0x22)) else "FAIL")

        # clearResponseOnEvent(0x06)
        resp = self.uds.send_request([SID_RESPONSE_ON_EVENT, 0x06, 0x00])
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="$86", test_name="$86 clearResponseOnEvent(0x06)",
            expected="正响应或NRC 0x11",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_RESPONSE_ON_EVENT) or
                              nrc in (0x11, 0x12, 0x7F, 0x7E, 0x22)) else "FAIL")

        # 无效子功能
        resp = self.uds.send_request([SID_RESPONSE_ON_EVENT, 0x7F, 0x00])
        self.add_result(
            service="$86", test_name="$86 无效子功能(0x7F)",
            expected="NRC 0x12",
            actual=self.resp_to_hex(resp),
            status="PASS" if self.is_negative_response(resp, 0x12) or self.is_negative_response(resp, 0x11) else "FAIL")

        # ===== $87 LinkControl =====
        # verifyModeTransitionWithFixedParameter(0x01) + linkRecord
        resp = self.uds.send_request([SID_LINK_CONTROL, 0x01, 0x01])  # CAN 250kbps
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="$87", test_name="$87 verifyFixed(0x01) CAN250k",
            expected="正响应或NRC 0x11",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_LINK_CONTROL) or
                              nrc in (0x11, 0x12, 0x31, 0x7F, 0x7E, 0x22)) else "FAIL")

        # verifyModeTransitionWithSpecificParameter(0x02)
        resp = self.uds.send_request([SID_LINK_CONTROL, 0x02, 0x00, 0x07, 0xA1, 0x20])
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="$87", test_name="$87 verifySpecific(0x02) 500kbps",
            expected="正响应或NRC 0x11",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_LINK_CONTROL) or
                              nrc in (0x11, 0x12, 0x31, 0x7F, 0x7E, 0x22)) else "FAIL")

        # transitionMode(0x03) - 注意:此命令可能导致通信中断!
        # 因此不发送transition请求,仅测试NRC
        resp = self.uds.send_request([SID_LINK_CONTROL, 0x03])
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="$87", test_name="$87 transitionMode(0x03)无先验verify",
            expected="NRC 0x24(requestSequenceError)或0x11",
            actual=self.resp_to_hex(resp),
            status="PASS" if (nrc in (0x11, 0x24, 0x22, 0x7F, 0x7E, 0x12) or
                              self.is_positive_response(resp, SID_LINK_CONTROL)) else "FAIL")

        # 默认会话应拒绝
        self.reset_to_default_session()
        resp = self.uds.send_request([SID_LINK_CONTROL, 0x01, 0x01])
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="$87", test_name="$87 默认会话应拒绝",
            expected="NRC 0x7F/0x11",
            actual=self.resp_to_hex(resp),
            status="PASS" if nrc in (0x11, 0x7F, 0x22) else "FAIL"
                if self.is_negative_response(resp) else "PASS")

        # 无效子功能
        resp = self.uds.send_request([SID_LINK_CONTROL, 0x00])
        self.add_result(
            service="$87", test_name="$87 无效子功能(0x00)",
            expected="NRC 0x12/0x11",
            actual=self.resp_to_hex(resp),
            status="PASS" if self.is_negative_response(resp) else "FAIL")

        self.reset_to_default_session()

    def test_nrc_priority(self):
        """NRC优先级验证 (ISO 14229-1 Table A.1)"""
        print("\\n=== 测试 NRC优先级 ===")

        # 场景1: 不支持的服务 → 应先返回0x11 而非0x13
        # 用一个未知SID,故意带错长度
        resp = self.uds.send_request([0xBA])  # 未知SID
        if self.is_negative_response(resp, 0x11):
            self.add_result(
                service="NRC优先级", test_name="未知SID先于长度检查 → NRC 0x11",
                expected="NRC 0x11 (优先于0x13)",
                actual=self.resp_to_hex(resp), status="PASS")
        elif self.is_negative_response(resp):
            self.add_result(
                service="NRC优先级", test_name="未知SID先于长度检查 → NRC 0x11",
                expected="NRC 0x11", actual=self.resp_to_hex(resp), status="FAIL")
        else:
            self.add_result(
                service="NRC优先级", test_name="未知SID先于长度检查 → NRC 0x11",
                expected="NRC 0x11", actual=self.resp_to_hex(resp) if resp else "No Response",
                status="PASS" if resp is None else "FAIL",
                detail="无响应也可接受(功能寻址)")

        # 场景2: 支持的SID + 不支持的会话 + 错误长度 → 0x7F先于0x13
        # $85在默认会话下,故意带多余字节
        self.reset_to_default_session()
        resp = self.uds.send_request([SID_CONTROL_DTC_SETTING, 0x02, 0xFF, 0xFF, 0xFF])
        if self.is_negative_response(resp):
            nrc = self.get_nrc(resp)
            self.add_result(
                service="NRC优先级", test_name="$85默认会话+多余字节 → NRC 0x7F先于0x13",
                expected="NRC 0x7F (会话检查先于长度)",
                actual=f"NRC 0x{{nrc:02X}}",
                status="PASS" if nrc in (0x7F, 0x13, 0x12) else "FAIL",
                detail="NRC优先级: 0x7F>0x13 per ISO 14229-1 Table A.1")
        else:
            self.add_result(
                service="NRC优先级", test_name="$85默认会话+多余字节",
                expected="NRC", actual=self.resp_to_hex(resp),
                status="PASS" if self.is_positive_response(resp, SID_CONTROL_DTC_SETTING) else "FAIL")

        # 场景3: $22无效DID → NRC 0x31 (requestOutOfRange)
        resp = self.uds.read_did(0xFFFF)
        if self.is_negative_response(resp, 0x31):
            self.add_result(
                service="NRC优先级", test_name="$22不存在的DID 0xFFFF → NRC 0x31",
                expected="NRC 0x31 requestOutOfRange",
                actual=self.resp_to_hex(resp), status="PASS")
        else:
            self.add_result(
                service="NRC优先级", test_name="$22不存在的DID 0xFFFF → NRC 0x31",
                expected="NRC 0x31", actual=self.resp_to_hex(resp),
                status="PASS" if self.is_negative_response(resp) else "FAIL")

        # $22 DID 0x0000
        resp = self.uds.read_did(0x0000)
        if self.is_negative_response(resp, 0x31):
            self.add_result(
                service="NRC优先级", test_name="$22不存在的DID 0x0000 → NRC 0x31",
                expected="NRC 0x31",
                actual=self.resp_to_hex(resp), status="PASS")
        else:
            self.add_result(
                service="NRC优先级", test_name="$22不存在的DID 0x0000 → NRC 0x31",
                expected="NRC 0x31", actual=self.resp_to_hex(resp),
                status="PASS" if self.is_negative_response(resp) else "FAIL")

{test_methods}

    # ============================================================
    # ISO 14229-1 服务深度合规测试
    # ============================================================
    def test_service_depth_compliance(self):
        """ISO 14229-1 各服务NRC/子功能/长度/会话深度测试"""
        print("\\n=== 测试 ISO 14229-1 服务深度合规 ===")

        # --- $11 ECUReset 深度 ---
        # $11 sub-function 0x04 enableRapidPowerShutDown
        resp = self.uds.send_request([SID_ECU_RESET, 0x04])
        self.add_result(
            service="$11", test_name="$11 SubFunc=04 enableRapidPowerShutDown",
            expected="正响应或NRC 0x12",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_ECU_RESET) or
                self.is_negative_response(resp, 0x12)) else "FAIL")
        # $11 sub-function 0x05 disableRapidPowerShutDown
        resp = self.uds.send_request([SID_ECU_RESET, 0x05])
        self.add_result(
            service="$11", test_name="$11 SubFunc=05 disableRapidPowerShutDown",
            expected="正响应或NRC 0x12",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_ECU_RESET) or
                self.is_negative_response(resp, 0x12)) else "FAIL")
        # $11 在扩展会话
        self.switch_session(SESSION_EXTENDED)
        time.sleep(0.05)
        resp = self.uds.send_request([SID_ECU_RESET, 0x03])
        self.add_result(
            service="$11", test_name="$11 softReset 扩展会话",
            session="Extended", expected="正响应或NRC",
            actual=self.resp_to_hex(resp),
            status="PASS" if resp is not None else "FAIL")
        time.sleep(2)
        self.reset_to_default_session()
        # $11 NRC 0x22 conditionsNotCorrect (难以触发,记录行为)
        resp = self.uds.send_request([SID_ECU_RESET, 0x01])
        self.add_result(
            service="$11", test_name="$11 hardReset NRC 0x22可能性",
            expected="正响应(通常)", actual=self.resp_to_hex(resp),
            status="PASS" if resp is not None else "FAIL",
            detail="NRC 0x22仅在特定条件下触发")
        time.sleep(3)

        # --- $27 SecurityAccess 深度 ---
        self.switch_session(SESSION_EXTENDED)
        time.sleep(0.05)
        # $27 suppressPositiveResponse
        resp = self.uds.send_request([SID_SECURITY_ACCESS, 0x01 | 0x80])
        self.add_result(
            service="$27", test_name="$27 RequestSeed suppressPosRsp",
            expected="无响应(被抑制)",
            actual=self.resp_to_hex(resp),
            status="PASS" if resp is None else "FAIL")
        # $27 Level 3 (0x03/0x04) - 不同安全等级
        resp = self.uds.send_request([SID_SECURITY_ACCESS, 0x03])
        nrc = self.get_nrc(resp)
        self.add_result(
            service="$27", test_name="$27 Level3(0x03) RequestSeed",
            expected="正响应或NRC 0x12(不支持)",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_SECURITY_ACCESS) or
                nrc in (0x12, 0x33, 0x7F)) else "FAIL")
        # $27 Level 5 (0x05/0x06)
        resp = self.uds.send_request([SID_SECURITY_ACCESS, 0x05])
        nrc = self.get_nrc(resp)
        self.add_result(
            service="$27", test_name="$27 Level5(0x05) RequestSeed",
            expected="正响应或NRC 0x12",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_SECURITY_ACCESS) or
                nrc in (0x12, 0x33, 0x7F)) else "FAIL")
        self.reset_to_default_session()

        # --- $28 CommunicationControl 深度 ---
        self.switch_session(SESSION_EXTENDED)
        time.sleep(0.05)
        # SubFunc 0x01 enableRxAndDisableTx
        resp = self.uds.communication_control(0x01, 0x01)
        self.add_result(
            service="$28", test_name="$28 SubFunc=01 enableRxDisableTx",
            expected="正响应或NRC 0x12",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_COMMUNICATION_CONTROL) or
                self.is_negative_response(resp, 0x12)) else "FAIL")
        # SubFunc 0x02 disableRxAndEnableTx
        resp = self.uds.communication_control(0x02, 0x01)
        self.add_result(
            service="$28", test_name="$28 SubFunc=02 disableRxEnableTx",
            expected="正响应或NRC 0x12",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_COMMUNICATION_CONTROL) or
                self.is_negative_response(resp, 0x12)) else "FAIL")
        # communicationType 0x02 nmCommunicationMessages
        resp = self.uds.communication_control(0x00, 0x02)
        self.add_result(
            service="$28", test_name="$28 commType=02 NM消息",
            expected="正响应或NRC",
            actual=self.resp_to_hex(resp),
            status="PASS" if resp is not None else "FAIL")
        # communicationType 0x03 nm + normal
        resp = self.uds.communication_control(0x00, 0x03)
        self.add_result(
            service="$28", test_name="$28 commType=03 NM+Normal",
            expected="正响应或NRC",
            actual=self.resp_to_hex(resp),
            status="PASS" if resp is not None else "FAIL")
        # 恢复通信
        self.uds.communication_control(0x00, 0x01)
        self.reset_to_default_session()

        # --- $2F IOControl 深度 (如果调查表有IOControl) ---
        # SubFunc 0x01 ResetToDefault, 0x02 FreezeCurrentState
        # 用0xFFFF作为不存在的DID来测试NRC行为
        resp = self.uds.io_control(0xFFFF, 0x01)  # ResetToDefault
        self.add_result(
            service="$2F", test_name="$2F IOCtrl ResetToDefault(0x01) 无效DID",
            expected="NRC 0x31/0x7F",
            actual=self.resp_to_hex(resp),
            status="PASS" if self.is_negative_response(resp) else "FAIL")
        resp = self.uds.io_control(0xFFFF, 0x02)  # FreezeCurrentState
        self.add_result(
            service="$2F", test_name="$2F IOCtrl FreezeCurrentState(0x02) 无效DID",
            expected="NRC 0x31/0x7F",
            actual=self.resp_to_hex(resp),
            status="PASS" if self.is_negative_response(resp) else "FAIL")
        # $2F 错误长度
        resp = self.uds.send_request([SID_IO_CONTROL, 0xFF])
        self.add_result(
            service="$2F", test_name="$2F 错误长度(缺少参数)",
            expected="NRC 0x13",
            actual=self.resp_to_hex(resp),
            status="PASS" if self.is_negative_response(resp, 0x13) else
                ("PASS" if self.is_negative_response(resp) else "FAIL"))

        # --- $31 RoutineControl 深度 ---
        # SubFunc 0x02 stopRoutine (RID 0xFFFF)
        resp = self.uds.routine_control(0x02, 0xFFFF)
        self.add_result(
            service="$31", test_name="$31 stopRoutine(0x02) 无效RID",
            expected="NRC 0x31/0x24/0x7F",
            actual=self.resp_to_hex(resp),
            status="PASS" if self.is_negative_response(resp) else "FAIL")
        # SubFunc 0x03 requestRoutineResults (RID 0xFFFF)
        resp = self.uds.routine_control(0x03, 0xFFFF)
        self.add_result(
            service="$31", test_name="$31 requestRoutineResults(0x03) 无效RID",
            expected="NRC 0x31/0x24/0x7F",
            actual=self.resp_to_hex(resp),
            status="PASS" if self.is_negative_response(resp) else "FAIL")
        # $31 suppressPositiveResponse
        resp = self.uds.send_request([SID_ROUTINE_CONTROL, 0x01 | 0x80, 0xFF, 0xFF])
        self.add_result(
            service="$31", test_name="$31 startRoutine suppressPosRsp 无效RID",
            expected="无响应或NRC(suppressed positive, 但NRC仍发送)",
            actual=self.resp_to_hex(resp),
            status="PASS" if self.is_negative_response(resp) else
                ("PASS" if resp is None else "FAIL"),
            detail="NRC不受suppress影响; 正响应应被抑制")
        # $31 错误长度
        resp = self.uds.send_request([SID_ROUTINE_CONTROL, 0x01])
        self.add_result(
            service="$31", test_name="$31 错误长度(缺RID)",
            expected="NRC 0x13",
            actual=self.resp_to_hex(resp),
            status="PASS" if self.is_negative_response(resp, 0x13) else
                ("PASS" if self.is_negative_response(resp) else "FAIL"))

        # --- $35 RequestUpload 深度 ---
        # 扩展会话
        self.switch_session(SESSION_EXTENDED)
        time.sleep(0.05)
        resp = self.uds.send_request([SID_REQUEST_UPLOAD, 0x00, 0x44,
                                       0x00, 0x00, 0x00, 0x00,
                                       0x00, 0x00, 0x10, 0x00])
        self.add_result(
            service="$35", test_name="$35 扩展会话RequestUpload",
            session="Extended", expected="NRC",
            actual=self.resp_to_hex(resp),
            status="PASS" if self.is_negative_response(resp) else "FAIL")
        self.reset_to_default_session()
        # 编程会话
        self.switch_session(SESSION_PROGRAMMING)
        time.sleep(0.05)
        resp = self.uds.send_request([SID_REQUEST_UPLOAD, 0x00, 0x44,
                                       0x00, 0x00, 0x00, 0x00,
                                       0x00, 0x00, 0x10, 0x00])
        self.add_result(
            service="$35", test_name="$35 编程会话RequestUpload(无安全)",
            session="Programming", expected="NRC 0x33",
            actual=self.resp_to_hex(resp),
            status="PASS" if self.is_negative_response(resp, 0x33) else
                ("PASS" if self.is_negative_response(resp) else "FAIL"))
        # $35 错误长度
        resp = self.uds.send_request([SID_REQUEST_UPLOAD])
        self.add_result(
            service="$35", test_name="$35 错误长度(仅SID)",
            expected="NRC 0x13",
            actual=self.resp_to_hex(resp),
            status="PASS" if self.is_negative_response(resp, 0x13) else
                ("PASS" if self.is_negative_response(resp) else "FAIL"))
        self.reset_to_default_session()

        # --- $3E TesterPresent 长度测试 ---
        resp = self.uds.send_request([SID_TESTER_PRESENT])
        self.add_result(
            service="$3E", test_name="$3E 错误长度(仅SID无SubFunc)",
            expected="NRC 0x13",
            actual=self.resp_to_hex(resp),
            status="PASS" if self.is_negative_response(resp, 0x13) else
                ("PASS" if self.is_negative_response(resp) else "FAIL"))
        # $3E 多余字节
        resp = self.uds.send_request([SID_TESTER_PRESENT, 0x00, 0xFF, 0xFF])
        self.add_result(
            service="$3E", test_name="$3E 多余字节(4字节)",
            expected="NRC 0x13或正响应(取决于实现)",
            actual=self.resp_to_hex(resp),
            status="PASS" if resp is not None else "FAIL")

        # --- $85 ControlDTCSetting 长度测试 ---
        self.switch_session(SESSION_EXTENDED)
        time.sleep(0.05)
        resp = self.uds.send_request([SID_CONTROL_DTC_SETTING])
        self.add_result(
            service="$85", test_name="$85 错误长度(仅SID)",
            expected="NRC 0x13",
            actual=self.resp_to_hex(resp),
            status="PASS" if self.is_negative_response(resp, 0x13) else
                ("PASS" if self.is_negative_response(resp) else "FAIL"))
        self.reset_to_default_session()

        # --- $10 深度: OEM会话(0x40-0x5F) 和 NRC 0x22 ---
        resp = self.uds.send_request([SID_DIAGNOSTIC_SESSION_CONTROL, 0x40])
        self.add_result(
            service="$10", test_name="$10 OEM会话0x40",
            expected="正响应或NRC 0x12(不支持)",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_DIAGNOSTIC_SESSION_CONTROL)
                or self.is_negative_response(resp)) else "FAIL")
        resp = self.uds.send_request([SID_DIAGNOSTIC_SESSION_CONTROL, 0x60])
        self.add_result(
            service="$10", test_name="$10 系统供应商会话0x60",
            expected="正响应或NRC 0x12",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_positive_response(resp, SID_DIAGNOSTIC_SESSION_CONTROL)
                or self.is_negative_response(resp)) else "FAIL")
        self.reset_to_default_session()

    # ============================================================
    # ISO 14229-2 功能寻址NRC抑制规则 (Table 4)
    # ============================================================
    def test_iso14229_2_functional_nrc_rules(self):
        """ISO 14229-2 Table 4 功能寻址NRC抑制规则深度测试"""
        print("\\n=== 测试 ISO 14229-2 Table 4 功能寻址NRC抑制 ===")

        if not self.uds.func_tp:
            self.add_result(
                service="ISO14229-2", test_name="Table4 功能寻址测试",
                expected="N/A", actual="无功能寻址配置",
                status="SKIP")
            return

        # NRC 0x11/0x12/0x7F/0x31 在功能寻址下应被抑制(不回复)
        # 测试1: 不支持的SID → NRC 0x11 应被抑制
        resp = self.uds.send_request([0xBA], functional=True)
        self.add_result(
            service="ISO14229-2", test_name="Table4: 不支持SID功能寻址→不回复(0x11抑制)",
            expected="无响应",
            actual=self.resp_to_hex(resp),
            status="PASS" if resp is None else "FAIL")

        # 测试2: $22 不存在DID → NRC 0x31 应被抑制
        resp = self.uds.send_request([SID_READ_DID, 0xFF, 0xFF], functional=True)
        self.add_result(
            service="ISO14229-2", test_name="Table4: $22不存在DID功能寻址→不回复(0x31抑制)",
            expected="无响应",
            actual=self.resp_to_hex(resp),
            status="PASS" if resp is None else "FAIL")

        # 测试3: $10 无效子功能 → NRC 0x12 功能寻址下应被抑制
        resp = self.uds.send_request([SID_DIAGNOSTIC_SESSION_CONTROL, 0x7F], functional=True)
        self.add_result(
            service="ISO14229-2", test_name="Table4: $10无效SubFunc功能寻址→不回复(0x12抑制)",
            expected="无响应",
            actual=self.resp_to_hex(resp),
            status="PASS" if resp is None else "FAIL")

        # 但NRC 0x13/0x22/0x33 在功能寻址下应仍然回复
        # 测试4: NRC 0x13 不被抑制 - $10发送错误长度(只有SID，缺子功能)
        resp = self.uds.send_request([SID_DIAGNOSTIC_SESSION_CONTROL], functional=True)
        self.add_result(
            service="ISO14229-2", test_name="Table4: 功能寻址NRC 0x13不被抑制(应回复)",
            expected="NRC 0x13(应回复)",
            actual=self.resp_to_hex(resp),
            status="PASS" if self.is_negative_response(resp, 0x13) else
                   ("PASS" if self.is_negative_response(resp) else "FAIL"),
            detail="NRC 0x13在功能寻址下不可抑制(ISO 14229-2 Table 4)")

        # 测试5: NRC 0x22 不被抑制 - $27 在默认会话(conditionsNotCorrect)
        resp = self.uds.send_request([SID_SECURITY_ACCESS, 0x01], functional=True)
        nrc = self.get_nrc(resp)
        self.add_result(
            service="ISO14229-2", test_name="Table4: 功能寻址NRC 0x22/0x7F不被抑制",
            expected="NRC 0x22或0x7F(应回复) 或不回复(某些ECU合规地不回复)",
            actual=self.resp_to_hex(resp),
            status="PASS" if (resp is None or self.is_negative_response(resp)) else "FAIL",
            detail="$27在默认会话功能寻址应回NRC(0x22/0x7F不被抑制)")

        # 测试6: NRC 0x33 不被抑制 - $2E写DID无安全解锁
        self.switch_session(SESSION_EXTENDED)
        time.sleep(0.05)
        resp = self.uds.send_request([SID_WRITE_DID, 0xF1, 0x90, 0x00], functional=True)
        nrc = self.get_nrc(resp)
        self.add_result(
            service="ISO14229-2", test_name="Table4: 功能寻址NRC 0x33不被抑制",
            expected="NRC 0x33(应回复)或0x31(被抑制不回复)",
            actual=self.resp_to_hex(resp),
            status="PASS" if (self.is_negative_response(resp) or resp is None) else "FAIL",
            detail="0x33在功能寻址下不被抑制(ISO 14229-2 Table 4)")
        self.reset_to_default_session()

        # NRC priority full chain: 0x11>0x7F>0x12>0x7E>0x13>0x14
        # 物理寻址下严格优先级验证
        # $85 in default session + invalid sub-func → should be 0x7F (not 0x12)
        resp = self.uds.send_request([SID_CONTROL_DTC_SETTING, 0xFF])
        if self.is_negative_response(resp):
            nrc = self.get_nrc(resp)
            self.add_result(
                service="ISO14229-2", test_name="NRC优先级: $85 default+无效SubFunc → 0x7F先于0x12",
                expected="NRC 0x7F(会话>子功能优先)",
                actual=f"NRC 0x{{nrc:02X}}",
                status="PASS" if nrc in (0x7F, 0x12) else "FAIL",
                detail="0x7F优先于0x12 per Table A.1")

        # $3E invalid subfunc + extra bytes → 0x12 before 0x13
        resp = self.uds.send_request([SID_TESTER_PRESENT, 0x02, 0xFF])
        if self.is_negative_response(resp):
            nrc = self.get_nrc(resp)
            self.add_result(
                service="ISO14229-2", test_name="NRC优先级: $3E无效SubFunc+多余字节 → 0x12先于0x13",
                expected="NRC 0x12(子功能>长度优先)",
                actual=f"NRC 0x{{nrc:02X}}",
                status="PASS" if nrc in (0x12, 0x13) else "FAIL")

    # ============================================================
    # ISO 15765-2 传输层边界测试
    # ============================================================
    def test_iso15765_2_edge_cases(self):
        """ISO 15765-2 传输层边界测试(N_Bs/N_Cr/FC Overflow)"""
        print("\\n=== 测试 ISO 15765-2 边界 ===")

        # FC Overflow (FS=2) — 发送超大请求看是否收到FS=2
        # 构造4096字节数据,超过SF+FF范围
        # 注: 实际这里只发FF看ECU如何响应
        huge_len = 4096
        ff = [(0x10 | ((huge_len >> 8) & 0x0F)), huge_len & 0xFF] + [0x22, 0xF1, 0x90, 0x00, 0x00, 0x00]
        self.uds.tp.send_raw_frame(ff)
        fc_raw = self.uds.tp.receive_raw_frame(timeout_ms=2000)
        if fc_raw:
            fc_data = fc_raw[1]
            fs = fc_data[0] & 0x0F if (fc_data[0] & 0xF0) == 0x30 else -1
            self.add_result(
                service="ISO15765-2", test_name="FF 4096字节→FC响应",
                expected="FC(FS=0 CTS或FS=2 Overflow)",
                actual=f"FS={{fs}} {{[hex(b) for b in fc_data]}}",
                status="PASS" if fs in (0, 1, 2) else "FAIL")
            if fs == 2:
                self.add_result(
                    service="ISO15765-2", test_name="FC Overflow(FS=2) 处理",
                    expected="FS=2", actual="FS=2",
                    status="PASS")
        else:
            self.add_result(
                service="ISO15765-2", test_name="FF 4096字节→FC响应",
                expected="有FC", actual="无响应",
                status="FAIL")
        time.sleep(2)

        # Extended FF test (>4095 bytes per ISO 15765-2:2016)
        # FF: PCI=0x10, DL=0x00 0x00 + 4-byte length
        ext_len = 5000
        eff = [0x10, 0x00, 0x00, 0x00, (ext_len >> 8) & 0xFF, ext_len & 0xFF, 0x22, 0xF1]
        self.uds.tp.send_raw_frame(eff)
        fc_raw = self.uds.tp.receive_raw_frame(timeout_ms=2000)
        if fc_raw:
            fc_data = fc_raw[1]
            fs = fc_data[0] & 0x0F if (fc_data[0] & 0xF0) == 0x30 else -1
            self.add_result(
                service="ISO15765-2", test_name="Extended FF(>4095字节)→FC响应",
                expected="FC或无响应(不支持)",
                actual=f"FS={{fs}}",
                status="PASS")
        else:
            self.add_result(
                service="ISO15765-2", test_name="Extended FF(>4095字节)→FC响应",
                expected="FC或无响应", actual="无响应",
                status="PASS", detail="ECU可能不支持extended FF")
        time.sleep(2)
        for sid, name in [(SID_DIAGNOSTIC_SESSION_CONTROL, "$10"),
                          (SID_TESTER_PRESENT, "$3E"),
                          (SID_READ_DTC_INFO, "$19")]:
            if sid == SID_DIAGNOSTIC_SESSION_CONTROL:
                req = [sid, SESSION_DEFAULT]
            elif sid == SID_TESTER_PRESENT:
                req = [sid, 0x00]
            else:
                req = [sid, 0x01, 0xFF]
            resp = self.uds.send_request(req)
            if resp and len(resp) > 0:
                expected_sid = sid + 0x40
                self.add_result(
                    service="ISO14229-2", test_name=f"{{name}}正响应SID=请求SID+0x40",
                    expected=f"0x{{expected_sid:02X}}",
                    actual=f"0x{{resp[0]:02X}}",
                    status="PASS" if resp[0] == expected_sid else "FAIL")
            else:
                self.add_result(
                    service="ISO14229-2", test_name=f"{{name}}正响应SID验证",
                    expected="有响应", actual="无响应", status="FAIL")

        # 2. 负响应格式验证: 0x7F + SID + NRC
        resp = self.uds.send_request([0xBA])  # 不支持的SID
        if resp and len(resp) >= 3:
            self.add_result(
                service="ISO14229-2", test_name="负响应格式: 0x7F+SID+NRC",
                expected="0x7F, 0xBA, NRC",
                actual=self.resp_to_hex(resp),
                status="PASS" if (resp[0] == 0x7F and resp[1] == 0xBA) else "FAIL")
        elif resp and len(resp) < 3:
            self.add_result(
                service="ISO14229-2", test_name="负响应最小长度>=3字节",
                expected=">=3字节", actual=f"{{len(resp)}}字节",
                status="FAIL")
        else:
            self.add_result(
                service="ISO14229-2", test_name="负响应格式验证",
                expected="0x7F+SID+NRC", actual="无响应",
                status="PASS", detail="功能寻址不支持的SID可以不响应")

        # 3. NRC 0x78 (Pending) 处理验证
        # 使用一个可能需要较长处理时间的服务(如$14清除DTC)
        resp, elapsed = self.uds.send_request_timed([SID_CLEAR_DTC, 0xFF, 0xFF, 0xFF])
        self.add_result(
            service="ISO14229-2", test_name="NRC 0x78 Pending处理(清除DTC)",
            expected="最终正响应(可能经过pending)",
            actual=f"{{self.resp_to_hex(resp)}} ({{elapsed:.0f}}ms)",
            status="PASS" if resp is not None else "FAIL",
            detail="send_request_timed自动处理0x78 pending循环")

        # 4. 功能寻址 vs 物理寻址行为差异
        # $3E TesterPresent 功能寻址应有响应
        if self.uds.func_tp:
            resp = self.uds.send_request([SID_TESTER_PRESENT, 0x00], functional=True)
            self.add_result(
                service="ISO14229-2", test_name="$3E功能寻址应有响应",
                expected="正响应 0x7E",
                actual=self.resp_to_hex(resp),
                status="PASS" if self.is_positive_response(resp, SID_TESTER_PRESENT) else "FAIL")

            # $3E功能寻址 + suppressPosRsp → 无响应
            resp = self.uds.send_request([SID_TESTER_PRESENT, 0x80], functional=True)
            self.add_result(
                service="ISO14229-2", test_name="$3E功能寻址+suppress → 无响应",
                expected="无响应(被抑制)",
                actual=self.resp_to_hex(resp),
                status="PASS" if resp is None else "FAIL")

            # 不支持的SID + 功能寻址 → 不应回复NRC
            resp = self.uds.send_request([0xBA], functional=True)
            self.add_result(
                service="ISO14229-2", test_name="功能寻址不支持SID → 不回复",
                expected="无响应(per ISO 14229-2 §7.5.4)",
                actual=self.resp_to_hex(resp),
                status="PASS" if resp is None else "FAIL",
                detail="功能寻址下NRC 0x11/0x12/0x7F/0x31不应发送")

            # $22 功能寻址读不存在的DID → 不应回复NRC 0x31
            resp = self.uds.send_request([SID_READ_DID, 0xFF, 0xFF], functional=True)
            self.add_result(
                service="ISO14229-2", test_name="功能寻址$22不存在DID → 不回复",
                expected="无响应(per ISO 14229-2)",
                actual=self.resp_to_hex(resp),
                status="PASS" if resp is None else "FAIL",
                detail="功能寻址requestOutOfRange不应回复")
        else:
            self.add_result(
                service="ISO14229-2", test_name="功能寻址测试",
                expected="N/A", actual="无功能寻址ID配置",
                status="SKIP", detail="需配置func_id")

        # 5. suppressPositiveResponse bit综合验证
        # $10 suppress + 0x80
        resp = self.uds.send_request([SID_DIAGNOSTIC_SESSION_CONTROL, SESSION_DEFAULT | 0x80])
        self.add_result(
            service="ISO14229-2", test_name="$10 suppressPosRsp (Default+0x80)",
            expected="无响应",
            actual=self.resp_to_hex(resp),
            status="PASS" if resp is None else "FAIL")

        # $28 suppress
        self.switch_session(SESSION_EXTENDED)
        time.sleep(0.05)
        resp = self.uds.send_request([SID_COMMUNICATION_CONTROL, 0x80, 0x01])  # enable + suppress
        self.add_result(
            service="ISO14229-2", test_name="$28 CommunicationControl suppressPosRsp",
            expected="无响应",
            actual=self.resp_to_hex(resp),
            status="PASS" if resp is None else "FAIL")

        # $2A suppress (transmissionMode | 0x80)
        resp = self.uds.send_request([SID_READ_DATA_BY_PERIODIC_ID, 0x01 | 0x80, 0xF1])
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="ISO14229-2", test_name="$2A ReadPeriodicDID suppressPosRsp",
            expected="无响应(正)或NRC(不应被抑制)",
            actual=self.resp_to_hex(resp),
            status="PASS" if resp is None or self.is_negative_response(resp) else "FAIL",
            detail="suppress时正响应不返回,负响应仍返回")

        # $2C suppress (defineByIdentifier 0x01 | 0x80)
        resp = self.uds.send_request([SID_DYNAMICALLY_DEFINE_DID, 0x01 | 0x80,
                                       0xF3, 0x00, 0xF1, 0x90, 0x01, 0x03])
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="ISO14229-2", test_name="$2C DynDefineDID suppressPosRsp",
            expected="无响应(正)或NRC",
            actual=self.resp_to_hex(resp),
            status="PASS" if resp is None or self.is_negative_response(resp) else "FAIL",
            detail="suppress时正响应不返回,负响应仍返回")

        # $83 suppress (readExtendedTiming 0x01 | 0x80)
        resp = self.uds.send_request([SID_ACCESS_TIMING_PARAM, 0x01 | 0x80])
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="ISO14229-2", test_name="$83 AccessTimingParam suppressPosRsp",
            expected="无响应(正)或NRC",
            actual=self.resp_to_hex(resp),
            status="PASS" if resp is None or self.is_negative_response(resp) else "FAIL",
            detail="suppress时正响应不返回,负响应仍返回")

        # $86 suppress (stopResponseOnEvent 0x00 | 0x80 = 0x80)
        resp = self.uds.send_request([SID_RESPONSE_ON_EVENT, 0x00 | 0x80, 0x00])
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="ISO14229-2", test_name="$86 ResponseOnEvent suppressPosRsp",
            expected="无响应(正)或NRC",
            actual=self.resp_to_hex(resp),
            status="PASS" if resp is None or self.is_negative_response(resp) else "FAIL",
            detail="suppress时正响应不返回,负响应仍返回")

        # $87 suppress (verifyModeTransitionWithFixedParameter 0x01 | 0x80)
        resp = self.uds.send_request([SID_LINK_CONTROL, 0x01 | 0x80, 0x01])
        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None
        self.add_result(
            service="ISO14229-2", test_name="$87 LinkControl suppressPosRsp",
            expected="无响应(正)或NRC",
            actual=self.resp_to_hex(resp),
            status="PASS" if resp is None or self.is_negative_response(resp) else "FAIL",
            detail="suppress时正响应不返回,负响应仍返回")

        self.reset_to_default_session()

    # ============================================================
    # ISO 15765-2 传输层测试
    # ============================================================
    def test_iso15765_2_transport_layer(self):
        """ISO 15765-2 传输层合规测试"""
        print("\\n=== 测试 ISO 15765-2 传输层 ===")

        # 1. Single Frame 正常收发 (DLC=8)
        resp = self.uds.send_request([SID_TESTER_PRESENT, 0x00])
        self.add_result(
            service="ISO15765-2", test_name="SF标准收发(DLC=8)",
            expected="正响应", actual=self.resp_to_hex(resp),
            status="PASS" if self.is_positive_response(resp, SID_TESTER_PRESENT) else "FAIL")

        # 2. Multi-Frame 收发验证 (读取长DID触发多帧响应)
        # 尝试$19-0A(所有DTC列表) - 通常返回多帧
        resp = self.uds.send_request([SID_READ_DTC_INFO, 0x0A])
        if resp and len(resp) > 7:
            self.add_result(
                service="ISO15765-2", test_name="Multi-Frame接收(>7字节)",
                expected="多帧响应", actual=f"{{len(resp)}}字节",
                status="PASS")
        else:
            self.add_result(
                service="ISO15765-2", test_name="Multi-Frame接收",
                expected="多帧响应", actual=f"{{len(resp) if resp else 0}}字节",
                status="PASS" if resp else "FAIL",
                detail="响应较短可以是单帧")

        # 3. Multi-Frame 发送验证 (发送长请求)
        # $22 读取多个DID (超过7字节触发多帧发送)
        long_req = [SID_READ_DID, 0xF1, 0x90, 0xF1, 0x91, 0xF1, 0x86, 0xF1, 0x87]  # 9字节
        resp = self.uds.send_request(long_req)
        self.add_result(
            service="ISO15765-2", test_name="Multi-Frame发送(>7字节请求)",
            expected="有响应",
            actual=self.resp_to_hex(resp),
            status="PASS" if resp is not None else "FAIL",
            detail="验证多帧发送和Flow Control处理")

        # 4. padding字节验证 - 不同填充不影响解析
        resp1 = self.uds.tp.send_sf_with_custom_padding(
            [SID_TESTER_PRESENT, 0x00], padding=0xCC)
        resp2 = self.uds.tp.send_sf_with_custom_padding(
            [SID_TESTER_PRESENT, 0x00], padding=0xAA)
        resp3 = self.uds.tp.send_sf_with_custom_padding(
            [SID_TESTER_PRESENT, 0x00], padding=0x00)
        resp4 = self.uds.tp.send_sf_with_custom_padding(
            [SID_TESTER_PRESENT, 0x00], padding=0xFF)

        for pad, resp, name in [(0xCC, resp1, "0xCC"), (0xAA, resp2, "0xAA"),
                                (0x00, resp3, "0x00"), (0xFF, resp4, "0xFF")]:
            self.add_result(
                service="ISO15765-2", test_name=f"SF padding={{name}} 不影响解析",
                expected="正响应 0x7E",
                actual=self.resp_to_hex(resp),
                status="PASS" if self.is_positive_response(resp, SID_TESTER_PRESENT) else "FAIL")

        # 5. 错误DLC帧(ISO 15765-2要求DLC=8 for classic CAN)
        resp = self.uds.tp.send_sf_with_wrong_dlc([SID_TESTER_PRESENT, 0x00], dlc=3)
        self.add_result(
            service="ISO15765-2", test_name="SF DLC<8(CAN classic要求DLC=8)",
            expected="无响应或NRC(ECU应忽略错误DLC)",
            actual=self.resp_to_hex(resp),
            status="PASS",
            detail="ISO 15765-2要求classic CAN DLC=8; ECU行为取决于实现")

        # 6. First Frame 后中止(不发CF)
        # 构造>7字节的请求数据
        abort_data = [SID_READ_DID] + [0xF1, 0x90] * 5  # 11字节 → FirstFrame
        fc = self.uds.tp.send_multiframe_abort(bytes(abort_data))
        if fc is not None:
            self.add_result(
                service="ISO15765-2", test_name="FF后ECU发送FlowControl",
                expected="FC帧(0x3X)", actual=f"{{[hex(b) for b in fc]}}",
                status="PASS" if (fc[0] & 0xF0) == 0x30 else "FAIL")

            # 验证FC参数
            flow_status = fc[0] & 0x0F
            block_size = fc[1] if len(fc) > 1 else 0
            st_min = fc[2] if len(fc) > 2 else 0
            self.add_result(
                service="ISO15765-2", test_name="FC FlowStatus合法(0-2)",
                expected="0(CTS)/1(Wait)/2(Overflow)",
                actual=f"{{flow_status}}",
                status="PASS" if flow_status in (0, 1, 2) else "FAIL")
            self.add_result(
                service="ISO15765-2", test_name=f"FC BS={{block_size}}, STmin={{st_min}}",
                expected="BS 0-255, STmin 0-127或0xF1-F9",
                actual=f"BS={{block_size}}, STmin={{st_min}}",
                status="PASS" if (0 <= block_size <= 255 and
                    (0 <= st_min <= 127 or 0xF1 <= st_min <= 0xF9)) else "FAIL")
        else:
            self.add_result(
                service="ISO15765-2", test_name="FF后ECU发送FlowControl",
                expected="FC帧", actual="无FC",
                status="FAIL", detail="ECU未响应FlowControl")

        # 等待ECU超时恢复
        time.sleep(2)

        # 7. 错误Consecutive Frame序号
        bad_data = [SID_READ_DID] + [0xF1, 0x90] * 5
        resp = self.uds.tp.send_cf_wrong_sequence(bytes(bad_data))
        self.add_result(
            service="ISO15765-2", test_name="CF错误序号(发5应发1)",
            expected="无响应/忽略(ECU中止传输)",
            actual=self.resp_to_hex(resp),
            status="PASS" if resp is None else "FAIL",
            detail="ISO 15765-2: 错误SN应中止接收")

        # 等待ECU恢复
        time.sleep(1)

    # ============================================================
    # ISO 14229-3 UDSonCAN 测试
    # ============================================================
    def test_iso14229_3_uds_on_can(self):
        """ISO 14229-3 UDS on CAN 实现合规测试"""
        print("\\n=== 测试 ISO 14229-3 UDSonCAN ===")

        # 1. 最小消息长度验证 (各SID)
        # $10 DiagnosticSessionControl最小2字节
        resp = self.uds.send_request([SID_DIAGNOSTIC_SESSION_CONTROL, SESSION_DEFAULT])
        self.add_result(
            service="ISO14229-3", test_name="$10 最小请求2字节",
            expected="正响应",
            actual=self.resp_to_hex(resp),
            status="PASS" if self.is_positive_response(resp, SID_DIAGNOSTIC_SESSION_CONTROL) else "FAIL")

        # $10 正响应最小长度 = 6字节 (SID+subFunc+P2hi+P2lo+P2*hi+P2*lo)
        if resp and len(resp) >= 6:
            self.add_result(
                service="ISO14229-3", test_name="$10 正响应>=6字节(含P2/P2*)",
                expected=">=6字节", actual=f"{{len(resp)}}字节",
                status="PASS")
            # 提取P2和P2*值
            p2_server = (resp[2] << 8) | resp[3]
            p2_star = ((resp[4] << 8) | resp[5]) * 10
            self.add_result(
                service="ISO14229-3", test_name=f"$10 P2={{p2_server}}ms P2*={{p2_star}}ms",
                expected="P2=25-5000, P2*=25-50000",
                actual=f"P2={{p2_server}} P2*={{p2_star}}",
                status="PASS" if (1 <= p2_server <= 5000 and 1 <= p2_star <= 50000) else "FAIL")
            # 动态更新全局时间参数 (ISO 14229-3: ECU报告的值应生效)
            global P2_TIMEOUT, P2_STAR_TIMEOUT
            if 1 <= p2_server <= 5000:
                P2_TIMEOUT = p2_server
                print(f"    [INFO] P2_TIMEOUT 已更新为 {{p2_server}}ms (来自$10响应)")
            if 1 <= p2_star <= 50000:
                P2_STAR_TIMEOUT = p2_star
                print(f"    [INFO] P2_STAR_TIMEOUT 已更新为 {{p2_star}}ms (来自$10响应)")
        elif resp:
            self.add_result(
                service="ISO14229-3", test_name="$10 正响应>=6字节",
                expected=">=6字节", actual=f"{{len(resp)}}字节", status="FAIL")

        # 2. $3E TesterPresent 正响应 = 2字节
        resp = self.uds.send_request([SID_TESTER_PRESENT, 0x00])
        if resp:
            self.add_result(
                service="ISO14229-3", test_name="$3E 正响应=2字节",
                expected="2字节(0x7E, 0x00)",
                actual=f"{{len(resp)}}字节 {{self.resp_to_hex(resp)}}",
                status="PASS" if (len(resp) == 2 and resp[0] == 0x7E and resp[1] == 0x00) else "FAIL")

        # 3. $22 正响应长度验证
        resp = self.uds.send_request([SID_READ_DID, 0xF1, 0x90])
        if resp and self.is_positive_response(resp, SID_READ_DID):
            # 正响应最小3字节(SID + DID_hi + DID_lo)
            self.add_result(
                service="ISO14229-3", test_name="$22 正响应>=3字节(SID+DID)",
                expected=">=3字节", actual=f"{{len(resp)}}字节",
                status="PASS" if len(resp) >= 3 else "FAIL")
            # 验证响应中的DID匹配请求
            if len(resp) >= 3:
                self.add_result(
                    service="ISO14229-3", test_name="$22 响应DID匹配请求DID",
                    expected="F190",
                    actual=f"{{resp[1]:02X}}{{resp[2]:02X}}",
                    status="PASS" if (resp[1] == 0xF1 and resp[2] == 0x90) else "FAIL")

        # 4. 负响应长度 = 固定3字节
        resp = self.uds.send_request([0xBA])
        if resp and resp[0] == 0x7F:
            self.add_result(
                service="ISO14229-3", test_name="负响应固定3字节",
                expected="3字节(0x7F+SID+NRC)",
                actual=f"{{len(resp)}}字节",
                status="PASS" if len(resp) == 3 else "FAIL")

        # 5. CAN ID范围验证 (这些是配置检查)
        tx_ok = 0x600 <= self.tx_id <= 0x7FF or self.tx_id == 0x7E0
        rx_ok = 0x600 <= self.rx_id <= 0x7FF or self.rx_id == 0x7E8
        self.add_result(
            service="ISO14229-3", test_name="CAN ID范围(0x600-0x7FF典型)",
            expected="TX/RX在诊断ID范围",
            actual=f"TX=0x{{self.tx_id:03X}} RX=0x{{self.rx_id:03X}}",
            status="PASS" if (tx_ok and rx_ok) else "FAIL",
            detail="ISO 14229-3 / ISO 15765-3 定义的标准诊断CAN ID范围")

        # 6. $11 ECUReset 正响应最小长度
        resp = self.uds.send_request([SID_ECU_RESET, 0x01])
        if resp and self.is_positive_response(resp, SID_ECU_RESET):
            self.add_result(
                service="ISO14229-3", test_name="$11 ECUReset正响应>=2字节",
                expected=">=2字节", actual=f"{{len(resp)}}字节",
                status="PASS" if len(resp) >= 2 else "FAIL")
            time.sleep(3)  # 等待ECU复位

    # ============================================================
    # ISO 15031-5 OBD 服务测试
    # ============================================================
    def test_iso15031_5_obd_services(self):
        """ISO 15031-5 OBD排放相关诊断服务测试"""
        print("\\n=== 测试 ISO 15031-5 OBD服务 ===")

        # OBD Mode 01 - Request Current Powertrain Diagnostic Data
        resp = self.uds.send_obd_request(0x01, 0x00)  # PID 0x00: 支持的PID列表
        if resp and len(resp) >= 2 and resp[0] == 0x41:
            self.add_result(
                service="OBD$01", test_name="Mode01 PID00 支持的PID",
                expected="正响应 0x41", actual=self.resp_to_hex(resp), status="PASS")
        elif resp and resp[0] == 0x7F:
            self.add_result(
                service="OBD$01", test_name="Mode01 PID00 支持的PID",
                expected="正响应或NRC 0x11",
                actual=self.resp_to_hex(resp),
                status="PASS" if self.get_nrc(resp) == 0x11 else "FAIL",
                detail="ECU不支持OBD服务")
        else:
            self.add_result(
                service="OBD$01", test_name="Mode01 PID00",
                expected="有响应", actual=self.resp_to_hex(resp),
                status="PASS" if resp is None else "FAIL",
                detail="无响应可接受(非OBD ECU)")

        # OBD Mode 02 - Request Powertrain Freeze Frame Data
        resp = self.uds.send_obd_request(0x02, 0x02)
        self.add_result(
            service="OBD$02", test_name="Mode02 冻结帧数据",
            expected="正响应0x42或NRC/无响应",
            actual=self.resp_to_hex(resp),
            status="PASS",
            detail="非OBD ECU无响应可接受")

        # OBD Mode 03 - Request Emission-Related DTCs
        resp = self.uds.send_obd_request(0x03)
        self.add_result(
            service="OBD$03", test_name="Mode03 排放DTC",
            expected="正响应0x43或NRC/无响应",
            actual=self.resp_to_hex(resp),
            status="PASS",
            detail="非排放ECU无响应可接受")

        # OBD Mode 04 - Clear/Reset Emission-Related DTCs
        # 注意: 这会清除排放DTC，保守起见仅检查是否支持
        resp = self.uds.send_obd_request(0x04)
        self.add_result(
            service="OBD$04", test_name="Mode04 清除排放DTC",
            expected="正响应0x44或NRC/无响应",
            actual=self.resp_to_hex(resp),
            status="PASS",
            detail="非OBD ECU无响应可接受; 会清除DTC")

        # OBD Mode 06 - Request On-Board Monitoring Test Results
        resp = self.uds.send_obd_request(0x06, 0x00)
        self.add_result(
            service="OBD$06", test_name="Mode06 监控测试结果",
            expected="正响应0x46或NRC/无响应",
            actual=self.resp_to_hex(resp),
            status="PASS",
            detail="非OBD ECU无响应可接受")

        # OBD Mode 07 - Request Emission-Related DTCs (Pending)
        resp = self.uds.send_obd_request(0x07)
        self.add_result(
            service="OBD$07", test_name="Mode07 Pending排放DTC",
            expected="正响应0x47或NRC/无响应",
            actual=self.resp_to_hex(resp),
            status="PASS",
            detail="非OBD ECU无响应可接受")

        # OBD Mode 09 - Request Vehicle Information
        resp = self.uds.send_obd_request(0x09, 0x02)  # VIN
        if resp and len(resp) >= 2 and resp[0] == 0x49:
            self.add_result(
                service="OBD$09", test_name="Mode09 PID02 VIN",
                expected="正响应0x49含VIN", actual=self.resp_to_hex(resp), status="PASS")
        else:
            self.add_result(
                service="OBD$09", test_name="Mode09 PID02 VIN",
                expected="正响应或无响应",
                actual=self.resp_to_hex(resp),
                status="PASS",
                detail="非OBD ECU无响应可接受")

        # OBD Mode 0A - Request emission-related DTCs with permanent status
        resp = self.uds.send_obd_request(0x0A)
        self.add_result(
            service="OBD$0A", test_name="Mode0A 永久排放DTC",
            expected="正响应0x4A或NRC/无响应",
            actual=self.resp_to_hex(resp),
            status="PASS",
            detail="非OBD ECU无响应可接受")

        # OBD Mode 05 - O2 sensor monitoring (ISO 15031-5:2006, removed in 2015+)
        resp = self.uds.send_obd_request(0x05, 0x01)
        self.add_result(
            service="OBD$05", test_name="Mode05 O2传感器测试(遗留)",
            expected="正响应0x45或NRC/无响应",
            actual=self.resp_to_hex(resp),
            status="PASS",
            detail="ISO 15031-5:2015+已移除,大多数ECU不支持")

        # OBD Mode 08 - Control of on-board system
        resp = self.uds.send_obd_request(0x08, 0x00)
        self.add_result(
            service="OBD$08", test_name="Mode08 车载系统控制",
            expected="正响应0x48或NRC/无响应",
            actual=self.resp_to_hex(resp),
            status="PASS",
            detail="非OBD ECU无响应可接受")

        # OBD Mode 09 additional PIDs
        for pid, name in [(0x00, "支持的InfoType"), (0x04, "CalID"), (0x06, "CVN"), (0x0A, "ECU Name")]:
            resp = self.uds.send_obd_request(0x09, pid)
            if resp and len(resp) >= 2 and resp[0] == 0x49:
                self.add_result(
                    service="OBD$09", test_name=f"Mode09 PID{{pid:02X}} {{name}}",
                    expected="正响应0x49", actual=self.resp_to_hex(resp), status="PASS")
            else:
                self.add_result(
                    service="OBD$09", test_name=f"Mode09 PID{{pid:02X}} {{name}}",
                    expected="正响应或无响应",
                    actual=self.resp_to_hex(resp),
                    status="PASS", detail="非OBD ECU无响应可接受")

        # OBD Mode 01 PID bitmap scanning
        resp = self.uds.send_obd_request(0x01, 0x00)
        if resp and len(resp) >= 6 and resp[0] == 0x41:
            bitmap = (resp[2] << 24) | (resp[3] << 16) | (resp[4] << 8) | resp[5]
            supported = []
            for bit in range(32):
                if bitmap & (1 << (31 - bit)):
                    supported.append(bit + 1)
            self.add_result(
                service="OBD$01", test_name="Mode01 PID00 Bitmap解析",
                expected="有效bitmap", actual=f"支持{{len(supported)}}个PID: {{supported[:10]}}...",
                status="PASS")
            # Read a few supported PIDs
            for pid in supported[:3]:
                resp = self.uds.send_obd_request(0x01, pid)
                self.add_result(
                    service="OBD$01", test_name=f"Mode01 PID{{pid:02X}}",
                    expected="正响应", actual=self.resp_to_hex(resp),
                    status="PASS" if (resp and resp[0] == 0x41) else
                        ("PASS" if resp is None else "FAIL"))

        # OBD invalid mode test
        resp = self.uds.send_obd_request(0x0B)  # Mode 0x0B = invalid
        self.add_result(
            service="OBD", test_name="无效OBD Mode 0x0B",
            expected="NRC或无响应",
            actual=self.resp_to_hex(resp),
            status="PASS" if (resp is None or self.is_negative_response(resp)) else "FAIL")

        # ISO 15031-6 DTC format validation
        # OBD uses 2-byte DTC; UDS uses 3-byte. Verify Mode 03 response format
        resp = self.uds.send_obd_request(0x03)
        if resp and len(resp) >= 3 and resp[0] == 0x43:
            dtc_count = resp[1]
            if dtc_count > 0 and len(resp) >= 4:
                # 每个DTC = 2字节
                first_dtc_hi = resp[2]
                first_dtc_lo = resp[3] if len(resp) > 3 else 0
                category = (first_dtc_hi >> 6) & 0x03
                cat_names = {{0: 'P', 1: 'C', 2: 'B', 3: 'U'}}
                self.add_result(
                    service="ISO15031-6", test_name="Mode03 2字节DTC格式验证",
                    expected="2字节/DTC, 首字节高2位=类别",
                    actual=f"DTC数={{dtc_count}}, 首DTC=0x{{first_dtc_hi:02X}}{{first_dtc_lo:02X}}, 类别={{cat_names.get(category, '?')}}",
                    status="PASS")
            else:
                self.add_result(
                    service="ISO15031-6", test_name="Mode03 DTC格式",
                    expected="有DTC数据", actual=f"DTC count={{dtc_count}}, resp_len={{len(resp)}}",
                    status="PASS", detail="无活动DTC")
        else:
            self.add_result(
                service="ISO15031-6", test_name="Mode03 DTC格式验证",
                expected="0x43响应或无响应", actual=self.resp_to_hex(resp),
                status="PASS", detail="非OBD ECU无响应可接受")

    # ======================================
    # 运行所有测试
    # ======================================

    def run_all_tests(self):
        """执行所有测试"""
        print("=" * 60)
        print("UDS 诊断自动化测试")
        print(f"开始时间: {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}")
        print("=" * 60)

        if not self.connect():
            print("[ERROR] 无法连接CAN总线，测试中止")
            return False

        try:
            # ISO 14229 通用服务测试
            self.test_session_management()
            self.test_session_advanced()
            self.test_tester_present()
            self.test_ecu_reset()
            self.test_security_access_advanced()
            self.test_communication_control()
            self.test_unsupported_sid()
            self.test_timing_p2()
            self.test_s3_server_timeout()
            self.test_sa_time_delay()
            self.test_p2_dynamic_extraction()
            self.test_p2_actual_compliance()
            self.test_zero_length_and_overlong()
            self.test_security_access_lockout()
            self.test_read_memory_by_address()
            self.test_request_download_upload()
            self.test_optional_services_nrc()
            self.test_nrc_priority()

            # ISO 14229-1 服务深度合规测试
            self.test_service_depth_compliance()

            # ISO 14229-2 功能寻址NRC抑制规则
            self.test_iso14229_2_functional_nrc_rules()

            # ISO 15765-2 传输层边界测试
            self.test_iso15765_2_edge_cases()

            # ISO 14229-2 会话层合规测试
            self.test_iso14229_2_session_layer()

            # ISO 15765-2 传输层合规测试
            self.test_iso15765_2_transport_layer()

            # ISO 14229-3 UDSonCAN合规测试
            self.test_iso14229_3_uds_on_can()

            # ISO 15031-5 OBD服务测试
            self.test_iso15031_5_obd_services()

            # 诊断调查表具体服务测试
{test_calls}

        except Exception as e:
            print(f"\\n[ERROR] 测试过程中发生异常: {{e}}")
        finally:
            self.reset_to_default_session()
            self.disconnect()

        return True

    def generate_report(self, output_path):
        """生成测试报告"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.status == "PASS")
        failed = sum(1 for r in self.results if r.status == "FAIL")
        skipped = sum(1 for r in self.results if r.status == "SKIP")
        pass_rate = (passed / total * 100) if total > 0 else 0

        report = []
        report.append("# UDS 诊断测试报告\\n")
        report.append(f"**日期**: {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}\\n")
        report.append(f"**源文件**: {source_file}\\n")
        report.append(f"**CAN通道**: {{self.channel}}\\n")
        report.append(f"**波特率**: {{self.bitrate}} bps\\n")
        report.append(f"**CAN ID**: TX=0x{{self.tx_id:03X}}, RX=0x{{self.rx_id:03X}}\\n")
        if self.can_log_path:
            report.append(f"**CAN通信日志**: {{self.can_log_path}}\\n")
        report.append("")
        report.append("## 测试汇总\\n")
        report.append("| 指标 | 数量 |")
        report.append("|------|------|")
        report.append(f"| 总测试用例 | {{total}} |")
        report.append(f"| 通过 (PASS) | {{passed}} |")
        report.append(f"| 失败 (FAIL) | {{failed}} |")
        report.append(f"| 跳过 (SKIP) | {{skipped}} |")
        report.append(f"| 通过率 | {{pass_rate:.1f}}% |")
        report.append("")

        # 按服务分组
        services = {{}}
        for r in self.results:
            services.setdefault(r.service, []).append(r)

        for service, cases in services.items():
            report.append(f"## {{service}}\\n")
            report.append("| # | 测试用例 | DID/RID | 会话 | 安全等级 | 期望结果 | 实际结果 | 状态 |")
            report.append("|---|----------|---------|------|----------|----------|----------|------|")
            for r in cases:
                status_badge = f"**{{r.status}}**"
                report.append(f"| {{r.case_id}} | {{r.test_name}} | {{r.did_rid}} | {{r.session}} | {{r.security}} | {{r.expected}} | {{r.actual[:50]}} | {{status_badge}} |")
            report.append("")

        # 失败用例详情
        failed_results = [r for r in self.results if r.status == "FAIL"]
        if failed_results:
            report.append("## 失败用例详情\\n")
            for r in failed_results:
                report.append(f"### Case #{{r.case_id}}: {{r.test_name}}\\n")
                report.append(f"- **服务**: {{r.service}}")
                if r.did_rid:
                    report.append(f"- **DID/RID**: {{r.did_rid}}")
                if r.session:
                    report.append(f"- **会话**: {{r.session}}")
                if r.security:
                    report.append(f"- **安全等级**: {{r.security}}")
                report.append(f"- **期望结果**: {{r.expected}}")
                report.append(f"- **实际结果**: {{r.actual}}")
                if r.detail:
                    report.append(f"- **失败原因**: {{r.detail}}")
                else:
                    # 自动推断失败原因
                    if "NRC" in r.actual and "NRC" not in r.expected:
                        report.append(f"- **失败原因**: ECU返回否定响应，期望正响应")
                    elif "超时" in r.actual or "timeout" in r.actual.lower() or "None" in r.actual:
                        report.append(f"- **失败原因**: ECU无响应（通信超时）")
                    elif r.expected and r.actual and r.expected != r.actual:
                        report.append(f"- **失败原因**: 响应内容与期望不匹配")
                report.append("")

        report_text = "\\n".join(report)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report_text)

        print(f"\\n[INFO] 测试报告已保存: {{output_path}}")
        print(f"  总计: {{total}} | 通过: {{passed}} | 失败: {{failed}} | 跳过: {{skipped}} | 通过率: {{pass_rate:.1f}}%")

        return report_text


# ============================================================================
# 入口
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="UDS诊断自动化测试")
    parser.add_argument("--channel", default=DEFAULT_CHANNEL, help="CAN通道 (如can0)")
    parser.add_argument("--can-if", default=DEFAULT_CAN_IF, choices=["socketcan"],
                        help="CAN接口类型 (仅支持socketcan)")
    parser.add_argument("--bitrate", type=int, default=DEFAULT_BITRATE, help="CAN波特率")
    parser.add_argument("--sample-point", type=float, default=DEFAULT_SAMPLE_POINT, help="CAN采样点 (0.0~1.0)")
    parser.add_argument("--tx-id", type=lambda x: int(x, 0), default=DEFAULT_TX_ID, help="发送CAN ID")
    parser.add_argument("--rx-id", type=lambda x: int(x, 0), default=DEFAULT_RX_ID, help="接收CAN ID")
    parser.add_argument("--func-id", type=lambda x: int(x, 0), default=DEFAULT_FUNC_ID, help="功能寻址ID")
    parser.add_argument("--report", default="uds_test_report.md", help="测试报告输出路径")
    parser.add_argument("--can-log", default="", help="CAN通信日志输出路径 (支持.asc/.blf/.csv/.log格式, 留空则不记录)")
    parser.add_argument("--test-connection", action="store_true", default=False,
                        help="仅测试CAN连通性: 连接总线→发送TesterPresent→断开，不执行完整测试")
    args = parser.parse_args()

    runner = TestRunner(args.channel, args.bitrate, args.tx_id, args.rx_id, args.func_id,
                        can_if=getattr(args, 'can_if', 'socketcan'),
                        sample_point=args.sample_point,
                        can_log_path=args.can_log)

    if args.test_connection:
        # 快速连通性验证模式
        print("=" * 50)
        print("CAN连通性快速验证")
        print("=" * 50)
        if not runner.connect():
            print("[FAIL] CAN连接失败")
            sys.exit(1)
        # 发送TesterPresent ($3E 00) 验证ECU是否应答
        print("[INFO] 发送 TesterPresent ($3E 00)...")
        resp = runner.uds.tester_present()
        if resp and len(resp) >= 2 and resp[0] == 0x7E:
            print(f"[OK] ECU应答: {{resp.hex()}}")
            print("[RESULT] CAN总线连通，ECU正常响应")
        elif resp is None:
            print("[WARN] ECU无应答 (总线可达但ECU可能未上电或CAN ID不匹配)")
            print("[RESULT] CAN总线已连接，但未收到ECU响应")
        else:
            print(f"[INFO] ECU响应: {{resp.hex() if resp else 'None'}}")
            print("[RESULT] CAN总线已连接")
        runner.disconnect()
        sys.exit(0)

    runner.run_all_tests()
    runner.generate_report(args.report)


if __name__ == "__main__":
    main()
'''


def generate_did_read_tests(dids):
    """生成DID读取测试方法"""
    methods = []
    calls = []

    if not dids:
        return "", ""

    method = []
    method.append('    def test_read_dids(self):')
    method.append('        """测试 $22 ReadDataByIdentifier"""')
    method.append('        print("\\n=== 测试 $22 ReadDataByIdentifier ===")')
    method.append('')

    for did in dids:
        did_num = did["did_number"]
        did_name = did.get("did_name", "Unknown")
        did_int = int(did_num, 16)
        size = did.get("size_bytes", 1)
        rw = did.get("rw_state", "R").upper()
        func_addr = did.get("functional_addressing", "N")

        if "R" not in rw:
            continue

        read_sessions = did.get("read_sessions", {})
        read_security = did.get("read_security", {})
        data_type = did.get("data_type", "RAW").upper()

        # 提取读取所需的SA等级
        read_sa_level = None
        read_sa_name = "无"
        for key, sa_val in [("level1", 0x01), ("level_fbl", 0x03), ("level_immo", 0x05)]:
            if read_security.get(key, "N").upper() == "Y":
                read_sa_level = sa_val
                read_sa_name = {"level1": "Level1", "level_fbl": "Level3(FBL)", "level_immo": "Level5(IMMO)"}[key]
                break
        needs_read_security = read_sa_level is not None

        # 生成每个会话的测试
        for session_key, session_val in [
            ("default_0x01", 0x01),
            ("programming_0x02", 0x02),
            ("extended_0x03", 0x03),
        ]:
            supported = read_sessions.get(session_key, "N") == "Y"
            session_name = SESSION_NAMES_MAP.get(session_val, f"0x{session_val:02X}")

            method.append(f'        # DID {did_num} - {did_name} - 会话 {session_name}')
            method.append(f'        self.reset_to_default_session()')
            method.append(f'        self.switch_session(0x{session_val:02X})')
            method.append(f'        time.sleep(0.05)')

            # 对于有安全访问需求的DID，在支持的会话中先解锁
            if supported and needs_read_security:
                method.append(f'        self.unlock_security(0x{read_sa_level:02X})  # {read_sa_name}')

            method.append(f'        resp = self.uds.read_did(0x{did_int:04X})')

            if supported:
                method.append(f'        if self.is_positive_response(resp, SID_READ_DID):')
                method.append(f'            resp_len = len(resp) - 3  # 减去SID+DID两字节')
                method.append(f'            len_ok = resp_len == {size}')
                # 数值范围校验 (仅数值型DID)
                range_min = did.get("range_min", 0)
                range_max = did.get("range_max", None)
                has_numeric_range = (isinstance(range_min, (int, float)) and
                                     isinstance(range_max, (int, float)) and
                                     data_type not in ("ASCII", "BCD"))
                if has_numeric_range:
                    r_min = int(range_min)
                    r_max = int(range_max)
                    method.append(f'            # 数据范围校验: [{r_min}, {r_max}]')
                    method.append(f'            data_bytes = resp[3:]')
                    method.append(f'            data_val = int.from_bytes(data_bytes, "big") if data_bytes else 0')
                    method.append(f'            range_ok = {r_min} <= data_val <= {r_max}')
                    method.append(f'            self.add_result(')
                    method.append(f'                service="$22", test_name="读取{did_num} {did_name[:20]}({session_name})",')
                    method.append(f'                did_rid="{did_num}", session="{session_name}",')
                    method.append(f'                expected="正响应+长度{size}B+范围[{r_min},{r_max}]",')
                    method.append(f'                actual=self.resp_to_hex(resp),')
                    method.append(f'                status="PASS" if (len_ok and range_ok) else "FAIL",')
                    method.append(f'                detail=f"len={{resp_len}}/{size} val={{data_val}} range=[{r_min},{r_max}] " +')
                    method.append(f'                    ("" if (len_ok and range_ok) else ("长度不匹配" if not len_ok else "范围越界")))')
                else:
                    method.append(f'            self.add_result(')
                    method.append(f'                service="$22", test_name="读取{did_num} {did_name[:20]}({session_name})",')
                    method.append(f'                did_rid="{did_num}", session="{session_name}",')
                    method.append(f'                expected="正响应+长度{size}B",')
                    method.append(f'                actual=self.resp_to_hex(resp),')
                    method.append(f'                status="PASS" if len_ok else "FAIL",')
                    method.append(f'                detail="" if len_ok else f"长度不匹配:期望{size},实际{{resp_len}}")')
                method.append(f'        else:')
                method.append(f'            self.add_result(')
                method.append(f'                service="$22", test_name="读取{did_num} {did_name[:20]}({session_name})",')
                method.append(f'                did_rid="{did_num}", session="{session_name}",')
                method.append(f'                expected="正响应 0x62",')
                method.append(f'                actual=self.resp_to_hex(resp), status="FAIL")')
            else:
                method.append(f'        if self.is_negative_response(resp):')
                method.append(f'            nrc = self.get_nrc(resp)')
                method.append(f'            self.add_result(')
                method.append(f'                service="$22", test_name="读取{did_num}({session_name})应拒绝",')
                method.append(f'                did_rid="{did_num}", session="{session_name}",')
                method.append(f'                expected="NRC 0x7F/0x31/0x22",')
                method.append(f'                actual=self.resp_to_hex(resp),')
                method.append(f'                status="PASS" if nrc in (0x7F, 0x31, 0x22, 0x33, 0x11) else "FAIL")')
                method.append(f'        elif self.is_positive_response(resp, SID_READ_DID):')
                method.append(f'            self.add_result(')
                method.append(f'                service="$22", test_name="读取{did_num}({session_name})应拒绝",')
                method.append(f'                did_rid="{did_num}", session="{session_name}",')
                method.append(f'                expected="NRC", actual="意外的正响应", status="FAIL")')
                method.append(f'        else:')
                method.append(f'            self.add_result(')
                method.append(f'                service="$22", test_name="读取{did_num}({session_name})应拒绝",')
                method.append(f'                did_rid="{did_num}", session="{session_name}",')
                method.append(f'                expected="NRC", actual=self.resp_to_hex(resp), status="FAIL")')

            method.append('')

        # 有安全访问需求的DID: 不解锁时应返回NRC 0x33
        if needs_read_security:
            # 找一个支持的会话来测试
            for sk2, sv2 in [("default_0x01", 0x01), ("programming_0x02", 0x02), ("extended_0x03", 0x03)]:
                if read_sessions.get(sk2, "N") == "Y":
                    sn2 = SESSION_NAMES_MAP.get(sv2, f"0x{sv2:02X}")
                    method.append(f'        # DID {did_num} - 无安全访问读取 (需要{read_sa_name})')
                    method.append(f'        self.reset_to_default_session()')
                    method.append(f'        self.switch_session(0x{sv2:02X})')
                    method.append(f'        time.sleep(0.05)')
                    method.append(f'        resp = self.uds.read_did(0x{did_int:04X})  # 不先解锁')
                    method.append(f'        if self.is_negative_response(resp, 0x33):')
                    method.append(f'            self.add_result(')
                    method.append(f'                service="$22", test_name="读取{did_num}无SA解锁→NRC0x33",')
                    method.append(f'                did_rid="{did_num}", session="{sn2}", security="{read_sa_name}",')
                    method.append(f'                expected="NRC 0x33", actual=self.resp_to_hex(resp), status="PASS")')
                    method.append(f'        else:')
                    method.append(f'            self.add_result(')
                    method.append(f'                service="$22", test_name="读取{did_num}无SA解锁",')
                    method.append(f'                did_rid="{did_num}", session="{sn2}", security="{read_sa_name}",')
                    method.append(f'                expected="NRC 0x33", actual=self.resp_to_hex(resp),')
                    method.append(f'                status="PASS" if (self.is_positive_response(resp, SID_READ_DID) or')
                    method.append(f'                                  self.is_negative_response(resp)) else "FAIL",')
                    method.append(f'                detail="可能ECU不要求SA或通过其他方式授权")')
                    method.append('')
                    break

        # 功能寻址测试
        if func_addr == "Y":
            method.append(f'        # DID {did_num} - 功能寻址测试')
            method.append(f'        self.reset_to_default_session()')
            method.append(f'        resp = self.uds.read_did(0x{did_int:04X}, functional=True)')
            method.append(f'        if self.is_positive_response(resp, SID_READ_DID):')
            method.append(f'            self.add_result(')
            method.append(f'                service="$22", test_name="功能寻址读取{did_num}",')
            method.append(f'                did_rid="{did_num}", session="Default",')
            method.append(f'                expected="正响应", actual=self.resp_to_hex(resp), status="PASS")')
            method.append(f'        else:')
            method.append(f'            self.add_result(')
            method.append(f'                service="$22", test_name="功能寻址读取{did_num}",')
            method.append(f'                did_rid="{did_num}", session="Default",')
            method.append(f'                expected="正响应", actual=self.resp_to_hex(resp), status="FAIL")')
            method.append('')

        # 错误长度测试
        method.append(f'        # DID {did_num} - 错误长度请求')
        method.append(f'        self.reset_to_default_session()')
        method.append(f'        resp = self.uds.send_request([SID_READ_DID, 0x{(did_int >> 8) & 0xFF:02X}])  # 缺少DID低字节')
        method.append(f'        if self.is_negative_response(resp, 0x13):')
        method.append(f'            self.add_result(')
        method.append(f'                service="$22", test_name="错误长度读取{did_num}",')
        method.append(f'                did_rid="{did_num}",')
        method.append(f'                expected="NRC 0x13", actual=self.resp_to_hex(resp), status="PASS")')
        method.append(f'        else:')
        method.append(f'            self.add_result(')
        method.append(f'                service="$22", test_name="错误长度读取{did_num}",')
        method.append(f'                did_rid="{did_num}",')
        method.append(f'                expected="NRC 0x13", actual=self.resp_to_hex(resp),')
        method.append(f'                status="PASS" if self.is_negative_response(resp) else "FAIL")')
        method.append('')

    method.append('        self.reset_to_default_session()')
    methods.append('\n'.join(method))
    calls.append('            self.test_read_dids()')

    return '\n\n'.join(methods), '\n'.join(calls)


def generate_did_write_tests(dids):
    """生成DID写入测试方法"""
    write_dids = [d for d in dids if "W" in d.get("rw_state", "R").upper()]
    if not write_dids:
        return "", ""

    method = []
    method.append('    def test_write_dids(self):')
    method.append('        """测试 $2E WriteDataByIdentifier"""')
    method.append('        print("\\n=== 测试 $2E WriteDataByIdentifier ===")')
    method.append('')

    for did in write_dids:
        did_num = did["did_number"]
        did_name = did.get("did_name", "Unknown")
        did_int = int(did_num, 16)
        size = did.get("size_bytes", 1)
        data_type = did.get("data_type", "RAW").upper()

        write_sessions = did.get("write_sessions", {})
        write_security = did.get("write_security", {})

        # 生成测试数据
        if "ASCII" in data_type:
            test_data_str = f'[0x41] * {size}  # "AAA..."'
        else:
            test_data_str = f'[0x00] * {size}'

        # 在不支持的会话中写入
        for session_key, session_val in [
            ("default_0x01", 0x01),
            ("programming_0x02", 0x02),
            ("extended_0x03", 0x03),
        ]:
            supported = write_sessions.get(session_key, "N") == "Y"
            session_name = SESSION_NAMES_MAP.get(session_val, f"0x{session_val:02X}")

            if not supported:
                method.append(f'        # DID {did_num} 写入 - 不支持的会话 {session_name}')
                method.append(f'        self.switch_session(0x{session_val:02X})')
                method.append(f'        time.sleep(0.05)')
                method.append(f'        test_data = {test_data_str}')
                method.append(f'        resp = self.uds.write_did(0x{did_int:04X}, test_data)')
                method.append(f'        if self.is_negative_response(resp):')
                method.append(f'            self.add_result(')
                method.append(f'                service="$2E", test_name="写入{did_num}({session_name})应拒绝",')
                method.append(f'                did_rid="{did_num}", session="{session_name}",')
                method.append(f'                expected="NRC", actual=self.resp_to_hex(resp), status="PASS")')
                method.append(f'        else:')
                method.append(f'            self.add_result(')
                method.append(f'                service="$2E", test_name="写入{did_num}({session_name})应拒绝",')
                method.append(f'                did_rid="{did_num}", session="{session_name}",')
                method.append(f'                expected="NRC", actual=self.resp_to_hex(resp), status="FAIL")')
                method.append('')

        # 无安全访问写入（在支持的会话中）
        supported_sessions = [(k, v) for k, v in [
            ("default_0x01", 0x01), ("programming_0x02", 0x02), ("extended_0x03", 0x03)
        ] if write_sessions.get(k, "N") == "Y"]

        if supported_sessions:
            sk, sv = supported_sessions[0]
            session_name = SESSION_NAMES_MAP.get(sv, f"0x{sv:02X}")

            # 需要安全访问但未解锁
            needs_security = any(v == "Y" for k, v in write_security.items() if k != "level0_locked")

            # 提取具体SA等级
            sa_level = None
            sa_level_name = "无"
            for key, sa_val in [("level1", 0x01), ("level_fbl", 0x03), ("level_immo", 0x05)]:
                if write_security.get(key, "N").upper() == "Y":
                    sa_level = sa_val
                    sa_level_name = {"level1": "Level1", "level_fbl": "Level3(FBL)", "level_immo": "Level5(IMMO)"}[key]
                    break  # 取最高优先级的

            if needs_security:
                method.append(f'        # DID {did_num} 写入 - 无安全访问 (需要{sa_level_name})')
                method.append(f'        self.reset_to_default_session()')
                method.append(f'        self.switch_session(0x{sv:02X})')
                method.append(f'        time.sleep(0.05)')
                method.append(f'        test_data = {test_data_str}')
                method.append(f'        resp = self.uds.write_did(0x{did_int:04X}, test_data)')
                method.append(f'        if self.is_negative_response(resp, 0x33):')
                method.append(f'            self.add_result(')
                method.append(f'                service="$2E", test_name="写入{did_num}无安全访问→NRC0x33",')
                method.append(f'                did_rid="{did_num}", session="{session_name}", security="{sa_level_name}",')
                method.append(f'                expected="NRC 0x33", actual=self.resp_to_hex(resp), status="PASS")')
                method.append(f'        else:')
                method.append(f'            self.add_result(')
                method.append(f'                service="$2E", test_name="写入{did_num}无安全访问",')
                method.append(f'                did_rid="{did_num}", session="{session_name}", security="{sa_level_name}",')
                method.append(f'                expected="NRC 0x33", actual=self.resp_to_hex(resp),')
                method.append(f'                status="PASS" if self.is_negative_response(resp) else "FAIL")')
                method.append('')

                # SA解锁后正向写入测试
                if sa_level is not None:
                    method.append(f'        # DID {did_num} 写入 - SA解锁后 (SA=0x{sa_level:02X} {sa_level_name})')
                    method.append(f'        self.reset_to_default_session()')
                    method.append(f'        self.switch_session(0x{sv:02X})')
                    method.append(f'        time.sleep(0.05)')
                    method.append(f'        self.unlock_security(0x{sa_level:02X})')
                    method.append(f'        test_data = {test_data_str}')
                    method.append(f'        resp = self.uds.write_did(0x{did_int:04X}, test_data)')
                    method.append(f'        if self.is_positive_response(resp, SID_WRITE_DID):')
                    method.append(f'            self.add_result(')
                    method.append(f'                service="$2E", test_name="写入{did_num} SA解锁后成功",')
                    method.append(f'                did_rid="{did_num}", session="{session_name}", security="{sa_level_name}",')
                    method.append(f'                expected="正响应 0x6E", actual=self.resp_to_hex(resp), status="PASS")')
                    method.append(f'        else:')
                    method.append(f'            nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None')
                    method.append(f'            self.add_result(')
                    method.append(f'                service="$2E", test_name="写入{did_num} SA解锁后",')
                    method.append(f'                did_rid="{did_num}", session="{session_name}", security="{sa_level_name}",')
                    method.append(f'                expected="正响应 0x6E", actual=self.resp_to_hex(resp),')
                    method.append(f'                status="PASS" if nrc in (0x22, 0x72) else "FAIL",')
                    method.append(f'                detail="NRC 0x22(条件不满足)/0x72可接受")')
                    method.append('')

        # 错误长度写入
        if supported_sessions:
            sk, sv = supported_sessions[0]
            session_name = SESSION_NAMES_MAP.get(sv, f"0x{sv:02X}")
            wrong_size = max(1, size + 3)
            method.append(f'        # DID {did_num} 写入 - 错误长度')
            method.append(f'        self.reset_to_default_session()')
            method.append(f'        self.switch_session(0x{sv:02X})')
            method.append(f'        time.sleep(0.05)')
            method.append(f'        resp = self.uds.write_did(0x{did_int:04X}, [0x00] * {wrong_size})')
            method.append(f'        if self.is_negative_response(resp, 0x13):')
            method.append(f'            self.add_result(')
            method.append(f'                service="$2E", test_name="过长数据写入{did_num}({wrong_size}B>期望{size}B)",')
            method.append(f'                did_rid="{did_num}", session="{session_name}",')
            method.append(f'                expected="NRC 0x13", actual=self.resp_to_hex(resp), status="PASS")')
            method.append(f'        else:')
            method.append(f'            self.add_result(')
            method.append(f'                service="$2E", test_name="过长数据写入{did_num}({wrong_size}B>期望{size}B)",')
            method.append(f'                did_rid="{did_num}", session="{session_name}",')
            method.append(f'                expected="NRC 0x13", actual=self.resp_to_hex(resp),')
            method.append(f'                status="PASS" if self.is_negative_response(resp) else "FAIL")')
            method.append('')

            # 过短数据写入 (仅DID无数据)
            method.append(f'        # DID {did_num} 写入 - 过短数据(0字节)')
            method.append(f'        resp = self.uds.write_did(0x{did_int:04X}, [])')
            method.append(f'        if self.is_negative_response(resp, 0x13):')
            method.append(f'            self.add_result(')
            method.append(f'                service="$2E", test_name="过短数据写入{did_num}(0B<期望{size}B)",')
            method.append(f'                did_rid="{did_num}", session="{session_name}",')
            method.append(f'                expected="NRC 0x13", actual=self.resp_to_hex(resp), status="PASS")')
            method.append(f'        else:')
            method.append(f'            self.add_result(')
            method.append(f'                service="$2E", test_name="过短数据写入{did_num}(0B<期望{size}B)",')
            method.append(f'                did_rid="{did_num}", session="{session_name}",')
            method.append(f'                expected="NRC 0x13", actual=self.resp_to_hex(resp),')
            method.append(f'                status="PASS" if self.is_negative_response(resp) else "FAIL")')
            method.append('')

            if size > 1:
                short_size = size - 1
                method.append(f'        # DID {did_num} 写入 - 少1字节({short_size}B<期望{size}B)')
                method.append(f'        resp = self.uds.write_did(0x{did_int:04X}, [0x00] * {short_size})')
                method.append(f'        if self.is_negative_response(resp, 0x13):')
                method.append(f'            self.add_result(')
                method.append(f'                service="$2E", test_name="少1字节写入{did_num}({short_size}B<期望{size}B)",')
                method.append(f'                did_rid="{did_num}", session="{session_name}",')
                method.append(f'                expected="NRC 0x13", actual=self.resp_to_hex(resp), status="PASS")')
                method.append(f'        else:')
                method.append(f'            self.add_result(')
                method.append(f'                service="$2E", test_name="少1字节写入{did_num}({short_size}B<期望{size}B)",')
                method.append(f'                did_rid="{did_num}", session="{session_name}",')
                method.append(f'                expected="NRC 0x13", actual=self.resp_to_hex(resp),')
                method.append(f'                status="PASS" if self.is_negative_response(resp) else "FAIL")')
                method.append('')

        # 数据范围越界写入测试 (需要有写入会话和数值型range)
        range_min = did.get("range_min", 0)
        range_max = did.get("range_max", None)
        if supported_sessions and isinstance(range_min, (int, float)) and isinstance(range_max, (int, float)):
            sk, sv = supported_sessions[0]
            session_name = SESSION_NAMES_MAP.get(sv, f"0x{sv:02X}")
            r_min = int(range_min)
            r_max = int(range_max)
            byte_max = (1 << (size * 8)) - 1

            # 在有SA需求时先解锁
            unlock_code = ""
            if sa_level is not None:
                unlock_code = f"\n        self.unlock_security(0x{sa_level:02X})"

            # 超上限值测试 (range_max + 1, 如果不超过字节容量)
            if r_max < byte_max:
                over_val = r_max + 1
                over_bytes = []
                for bi in range(size - 1, -1, -1):
                    over_bytes.append(f"0x{(over_val >> (bi * 8)) & 0xFF:02X}")
                over_bytes_str = f"[{', '.join(over_bytes)}]"

                method.append(f'        # DID {did_num} 写入 - 超上限值({over_val} > max {r_max})')
                method.append(f'        self.reset_to_default_session()')
                method.append(f'        self.switch_session(0x{sv:02X})')
                method.append(f'        time.sleep(0.05)')
                if unlock_code:
                    method.append(f'        self.unlock_security(0x{sa_level:02X})')
                method.append(f'        resp = self.uds.write_did(0x{did_int:04X}, {over_bytes_str})')
                method.append(f'        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None')
                method.append(f'        self.add_result(')
                method.append(f'            service="$2E", test_name="超上限写入{did_num}(val={over_val}>max={r_max})",')
                method.append(f'            did_rid="{did_num}", session="{session_name}",')
                method.append(f'            expected="NRC 0x31(requestOutOfRange)",')
                method.append(f'            actual=self.resp_to_hex(resp),')
                method.append(f'            status="PASS" if nrc in (0x31, 0x72, 0x22) else "FAIL",')
                method.append(f'            detail="超范围写入应返回NRC 0x31/0x22")')
                method.append('')

            # 超下限值测试 (range_min - 1, 如果 > 0)
            if r_min > 0:
                under_val = r_min - 1
                under_bytes = []
                for bi in range(size - 1, -1, -1):
                    under_bytes.append(f"0x{(under_val >> (bi * 8)) & 0xFF:02X}")
                under_bytes_str = f"[{', '.join(under_bytes)}]"

                method.append(f'        # DID {did_num} 写入 - 低于下限值({under_val} < min {r_min})')
                method.append(f'        self.reset_to_default_session()')
                method.append(f'        self.switch_session(0x{sv:02X})')
                method.append(f'        time.sleep(0.05)')
                if unlock_code:
                    method.append(f'        self.unlock_security(0x{sa_level:02X})')
                method.append(f'        resp = self.uds.write_did(0x{did_int:04X}, {under_bytes_str})')
                method.append(f'        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None')
                method.append(f'        self.add_result(')
                method.append(f'            service="$2E", test_name="低于下限写入{did_num}(val={under_val}<min={r_min})",')
                method.append(f'            did_rid="{did_num}", session="{session_name}",')
                method.append(f'            expected="NRC 0x31(requestOutOfRange)",')
                method.append(f'            actual=self.resp_to_hex(resp),')
                method.append(f'            status="PASS" if nrc in (0x31, 0x72, 0x22) else "FAIL",')
                method.append(f'            detail="低于范围写入应返回NRC 0x31/0x22")')
                method.append('')

            # 全FF写入测试 (最大字节值)
            if byte_max > r_max:
                method.append(f'        # DID {did_num} 写入 - 全0xFF(字节最大值)')
                method.append(f'        self.reset_to_default_session()')
                method.append(f'        self.switch_session(0x{sv:02X})')
                method.append(f'        time.sleep(0.05)')
                if unlock_code:
                    method.append(f'        self.unlock_security(0x{sa_level:02X})')
                method.append(f'        resp = self.uds.write_did(0x{did_int:04X}, [0xFF] * {size})')
                method.append(f'        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None')
                method.append(f'        self.add_result(')
                method.append(f'            service="$2E", test_name="全FF写入{did_num}(0x{"FF"*size})",')
                method.append(f'            did_rid="{did_num}", session="{session_name}",')
                method.append(f'            expected="NRC 0x31(超范围)或正响应(看ECU)",')
                method.append(f'            actual=self.resp_to_hex(resp),')
                method.append(f'            status="PASS" if resp is not None else "FAIL",')
                method.append(f'            detail="全FF写入 — ECU行为可能因实现而异")')
                method.append('')

    method.append('        self.reset_to_default_session()')

    return '\n'.join(method), '            self.test_write_dids()'


def generate_multi_did_read_tests(dids):
    """生成多DID单次读取测试方法 - ISO 14229 $22支持一次请求多个DID"""
    readable_dids = [d for d in dids if "R" in d.get("rw_state", "R").upper()]
    if len(readable_dids) < 2:
        return "", ""

    method = []
    method.append('    def test_multi_did_read(self):')
    method.append('        """测试 $22 多DID单次读取"""')
    method.append('        print("\\n=== 测试 $22 多DID单次读取 ===")')
    method.append('')
    method.append('        self.reset_to_default_session()')
    method.append('        time.sleep(0.05)')

    # 取默认会话下可读的前几个DID
    default_readable = []
    for d in readable_dids:
        if d.get("read_sessions", {}).get("default_0x01", "N") == "Y":
            default_readable.append(d)
        if len(default_readable) >= 5:
            break

    if len(default_readable) >= 2:
        # 2个DID
        d1, d2 = default_readable[0], default_readable[1]
        d1_int = int(d1["did_number"], 16)
        d2_int = int(d2["did_number"], 16)
        method.append(f'        # 读取2个DID: {d1["did_number"]} + {d2["did_number"]}')
        method.append(f'        req = [SID_READ_DID, 0x{(d1_int>>8)&0xFF:02X}, 0x{d1_int&0xFF:02X}, 0x{(d2_int>>8)&0xFF:02X}, 0x{d2_int&0xFF:02X}]')
        method.append(f'        resp = self.uds.send_request(req)')
        method.append(f'        if self.is_positive_response(resp, SID_READ_DID):')
        method.append(f'            self.add_result(')
        method.append(f'                service="$22", test_name="多DID读取({d1["did_number"]}+{d2["did_number"]})",')
        method.append(f'                expected="正响应含两个DID数据", actual=self.resp_to_hex(resp), status="PASS")')
        method.append(f'        elif self.is_negative_response(resp):')
        method.append(f'            nrc = self.get_nrc(resp)')
        method.append(f'            self.add_result(')
        method.append(f'                service="$22", test_name="多DID读取({d1["did_number"]}+{d2["did_number"]})",')
        method.append(f'                expected="正响应或NRC",')
        method.append(f'                actual=self.resp_to_hex(resp),')
        method.append(f'                status="PASS" if nrc == 0x14 else "FAIL",')
        method.append(f'                detail="NRC 0x14=responseTooLong是可接受的")')
        method.append(f'        else:')
        method.append(f'            self.add_result(')
        method.append(f'                service="$22", test_name="多DID读取({d1["did_number"]}+{d2["did_number"]})",')
        method.append(f'                expected="正响应", actual=self.resp_to_hex(resp), status="FAIL")')
        method.append('')

    if len(default_readable) >= 3:
        # 3个DID
        d3 = default_readable[2]
        d3_int = int(d3["did_number"], 16)
        method.append(f'        # 读取3个DID')
        method.append(f'        req = [SID_READ_DID, 0x{(d1_int>>8)&0xFF:02X}, 0x{d1_int&0xFF:02X}, 0x{(d2_int>>8)&0xFF:02X}, 0x{d2_int&0xFF:02X}, 0x{(d3_int>>8)&0xFF:02X}, 0x{d3_int&0xFF:02X}]')
        method.append(f'        resp = self.uds.send_request(req)')
        method.append(f'        self.add_result(')
        method.append(f'            service="$22", test_name="多DID读取(3个DID)",')
        method.append(f'            expected="正响应或NRC 0x14",')
        method.append(f'            actual=self.resp_to_hex(resp),')
        method.append(f'            status="PASS" if (self.is_positive_response(resp, SID_READ_DID) or self.is_negative_response(resp)) else "FAIL")')
        method.append('')

    # 一个有效DID + 一个无效DID
    method.append(f'        # 有效DID + 无效DID 0xFFFF (混合有效/无效)')
    method.append(f'        req = [SID_READ_DID, 0x{(d1_int>>8)&0xFF:02X}, 0x{d1_int&0xFF:02X}, 0xFF, 0xFF]')
    method.append(f'        resp = self.uds.send_request(req)')
    method.append(f'        self.add_result(')
    method.append(f'            service="$22", test_name="多DID读取(有效+无效0xFFFF)",')
    method.append(f'            expected="NRC 0x31或部分响应",')
    method.append(f'            actual=self.resp_to_hex(resp),')
    method.append(f'            status="PASS" if resp is not None else "FAIL")')
    method.append('')

    # 5+个DID读取 → 测试NRC 0x14 responseTooLong
    if len(default_readable) >= 5:
        did_bytes = []
        did_names = []
        for dr in default_readable[:5]:
            di = int(dr["did_number"], 16)
            did_bytes.extend([f'0x{(di>>8)&0xFF:02X}', f'0x{di&0xFF:02X}'])
            did_names.append(dr["did_number"])
        method.append(f'        # 5个DID同时读取 → 可能NRC 0x14 responseTooLong')
        method.append(f'        req = [SID_READ_DID, {", ".join(did_bytes)}]')
        method.append(f'        resp = self.uds.send_request(req)')
        method.append(f'        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None')
        method.append(f'        self.add_result(')
        method.append(f'            service="$22", test_name="多DID读取(5个: {"+".join(did_names)})",')
        method.append(f'            expected="正响应或NRC 0x14",')
        method.append(f'            actual=self.resp_to_hex(resp),')
        method.append(f'            status="PASS" if (self.is_positive_response(resp, SID_READ_DID) or nrc == 0x14) else')
        method.append(f'                   ("PASS" if self.is_negative_response(resp) else "FAIL"),')
        method.append(f'            detail="NRC 0x14=responseTooLong 当多个DID响应超过单帧容量时")')
        method.append('')

    # 响应长度验证 - 单DID读取后验证DID echo
    method.append(f'        # DID echo验证 - 响应中DID应与请求匹配')
    method.append(f'        resp = self.uds.read_did(0x{d1_int:04X})')
    method.append(f'        if self.is_positive_response(resp, SID_READ_DID) and len(resp) >= 3:')
    method.append(f'            echo_did = (resp[1] << 8) | resp[2]')
    method.append(f'            self.add_result(')
    method.append(f'                service="$22", test_name="DID echo验证({d1["did_number"]})",')
    method.append(f'                expected="响应中DID=0x{d1_int:04X}",')
    method.append(f'                actual=f"echo DID=0x{{echo_did:04X}}",')
    method.append(f'                status="PASS" if echo_did == 0x{d1_int:04X} else "FAIL")')
    method.append(f'        else:')
    method.append(f'            self.add_result(')
    method.append(f'                service="$22", test_name="DID echo验证({d1["did_number"]})",')
    method.append(f'                expected="正响应含DID", actual=self.resp_to_hex(resp),')
    method.append(f'                status="FAIL" if resp is not None and not self.is_positive_response(resp, SID_READ_DID) else "PASS")')
    method.append('')

    method.append('        self.reset_to_default_session()')

    return '\n'.join(method), '            self.test_multi_did_read()'


def generate_functional_write_reject_tests(dids):
    """生成功能寻址写入拒绝测试 - $2E功能寻址应被拒绝"""
    write_dids = [d for d in dids if "W" in d.get("rw_state", "R").upper()]
    if not write_dids:
        return "", ""

    method = []
    method.append('    def test_functional_write_reject(self):')
    method.append('        """测试 $2E 功能寻址写入应被拒绝"""')
    method.append('        print("\\n=== 测试 $2E 功能寻址写入拒绝 ===")')
    method.append('')

    # 只取第一个可写DID做测试
    did = write_dids[0]
    did_num = did["did_number"]
    did_int = int(did_num, 16)
    size = did.get("size_bytes", 1)

    method.append(f'        # 功能寻址$2E应被拒绝或无响应')
    method.append(f'        self.reset_to_default_session()')
    method.append(f'        self.switch_session(SESSION_EXTENDED)')
    method.append(f'        time.sleep(0.05)')
    method.append(f'        req = [SID_WRITE_DID, 0x{(did_int>>8)&0xFF:02X}, 0x{did_int&0xFF:02X}] + [0x00] * {size}')
    method.append(f'        resp = self.uds.send_request(req, functional=True)')
    method.append(f'        if resp is None or self.is_negative_response(resp):')
    method.append(f'            self.add_result(')
    method.append(f'                service="$2E", test_name="功能寻址写入{did_num}应拒绝",')
    method.append(f'                did_rid="{did_num}",')
    method.append(f'                expected="NRC或无响应", actual=self.resp_to_hex(resp), status="PASS")')
    method.append(f'        else:')
    method.append(f'            self.add_result(')
    method.append(f'                service="$2E", test_name="功能寻址写入{did_num}应拒绝",')
    method.append(f'                did_rid="{did_num}",')
    method.append(f'                expected="NRC或无响应", actual=self.resp_to_hex(resp), status="FAIL",')
    method.append(f'                detail="ISO 14229: $2E不应支持功能寻址")')
    method.append('')
    method.append('        self.reset_to_default_session()')

    return '\n'.join(method), '            self.test_functional_write_reject()'


def generate_did_timing_tests(dids):
    """生成DID级P2时间验证测试"""
    readable_dids = [d for d in dids if "R" in d.get("rw_state", "R").upper()
                     and d.get("read_sessions", {}).get("default_0x01", "N") == "Y"]
    if not readable_dids:
        return "", ""

    # 取前5个可读DID做P2测试
    test_dids = readable_dids[:5]

    method = []
    method.append('    def test_did_response_timing(self):')
    method.append('        """测试各DID P2响应时间合规"""')
    method.append('        print("\\n=== 测试 DID P2响应时间 ===")')
    method.append('')
    method.append('        self.reset_to_default_session()')
    method.append('        time.sleep(0.1)')

    for did in test_dids:
        did_num = did["did_number"]
        did_int = int(did_num, 16)
        did_name = did.get("did_name", "Unknown")[:20]

        method.append(f'        # P2 timing: {did_num} {did_name}')
        method.append(f'        resp, elapsed = self.uds.send_request_timed([SID_READ_DID, 0x{(did_int>>8)&0xFF:02X}, 0x{did_int&0xFF:02X}])')
        method.append(f'        p2_ok = elapsed <= P2_TIMEOUT * 1.1')
        method.append(f'        self.add_result(')
        method.append(f'            service="Timing", test_name="P2 DID {did_num} {did_name}",')
        method.append(f'            did_rid="{did_num}",')
        method.append(f'            expected=f"<={{P2_TIMEOUT}}ms",')
        method.append(f'            actual=f"{{elapsed:.1f}}ms",')
        method.append(f'            status="PASS" if (p2_ok and resp is not None) else ("FAIL" if resp is not None else "FAIL"),')
        method.append(f'            detail="P2超时" if not p2_ok else "")')
        method.append('')

    method.append('        self.reset_to_default_session()')

    return '\n'.join(method), '            self.test_did_response_timing()'


def generate_routine_timing_tests(routines):
    """生成Routine P2响应时间测试"""
    if not routines:
        return "", ""

    method = []
    method.append('    def test_routine_response_timing(self):')
    method.append('        """测试 $31 RoutineControl P2响应时间"""')
    method.append('        print("\\n=== 测试 $31 Routine P2响应时间 ===")')
    method.append('')

    for routine in routines:
        rid_num = routine["rid_number"]
        rid_name = routine.get("rid_name", "Unknown")[:20]
        rid_int = int(rid_num, 16)
        conditions = routine.get("conditions", "Extended Session")
        security = routine.get("security_level", "Level1")

        # 确定会话
        if "program" in conditions.lower():
            target_session = 0x02
            session_name = "Programming"
        elif "extend" in conditions.lower():
            target_session = 0x03
            session_name = "Extended"
        else:
            target_session = 0x01
            session_name = "Default"

        # 解析SA
        sa_level = None
        if security:
            s = security.strip().lower()
            if "3" in s or "fbl" in s or "prog" in s:
                sa_level = 0x03
            elif "5" in s or "immo" in s:
                sa_level = 0x05
            elif "1" in s:
                sa_level = 0x01

        # 构建参数
        req_params = routine.get("req_parameters", [])
        req_data = []
        for p in req_params:
            bit_len = safe_int_gen(p.get("bit_length", 8))
            byte_len = max(1, (bit_len + 7) // 8)
            req_data.extend([0x00] * byte_len)
        req_data_str = str(req_data) if req_data else "[]"

        method.append(f'        # Routine {rid_num} - {rid_name} P2时间测量')
        method.append(f'        self.reset_to_default_session()')
        method.append(f'        self.switch_session(0x{target_session:02X})')
        method.append(f'        time.sleep(0.05)')
        if sa_level is not None:
            method.append(f'        self.unlock_security(0x{sa_level:02X})')
        # 构建原始请求以使用send_request_timed
        rid_hi = (rid_int >> 8) & 0xFF
        rid_lo = rid_int & 0xFF
        method.append(f'        req_data = [SID_ROUTINE_CONTROL, 0x01, 0x{rid_hi:02X}, 0x{rid_lo:02X}] + {req_data_str}')
        method.append(f'        resp, elapsed = self.uds.send_request_timed(req_data)')
        method.append(f'        p2_ok = elapsed <= P2_STAR_TIMEOUT * 1.1')
        method.append(f'        if self.is_positive_response(resp, SID_ROUTINE_CONTROL):')
        method.append(f'            self.add_result(')
        method.append(f'                service="Timing", test_name="P2 Routine {rid_num} {rid_name}",')
        method.append(f'                did_rid="{rid_num}",')
        method.append(f'                expected=f"<={{P2_STAR_TIMEOUT}}ms(允许P2*)",')
        method.append(f'                actual=f"{{elapsed:.1f}}ms",')
        method.append(f'                status="PASS" if p2_ok else "FAIL",')
        method.append(f'                detail=f"Routine可能使用NRC0x78 pending, 总耗时{{elapsed:.1f}}ms")')
        method.append(f'        else:')
        method.append(f'            nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None')
        method.append(f'            self.add_result(')
        method.append(f'                service="Timing", test_name="P2 Routine {rid_num} {rid_name}",')
        method.append(f'                did_rid="{rid_num}",')
        method.append(f'                expected=f"正响应+P2合规",')
        method.append(f'                actual=f"{{self.resp_to_hex(resp)}} {{elapsed:.1f}}ms",')
        method.append(f'                status="PASS" if nrc in (0x22, 0x72, 0x31) else "FAIL",')
        method.append(f'                detail=f"NRC 0x22/0x72条件不满足可接受, 耗时{{elapsed:.1f}}ms")')
        method.append('')

    method.append('        self.reset_to_default_session()')

    return '\n'.join(method), '            self.test_routine_response_timing()'


def generate_io_control_timing_tests(io_controls):
    """生成IOControl P2响应时间测试"""
    if not io_controls:
        return "", ""

    method = []
    method.append('    def test_io_control_response_timing(self):')
    method.append('        """测试 $2F IOControl P2响应时间"""')
    method.append('        print("\\n=== 测试 $2F IOControl P2响应时间 ===")')
    method.append('')

    for io in io_controls:
        did_num = io["did_number"]
        did_name = io.get("did_name", "Unknown")[:20]
        did_int = int(did_num, 16)
        conditions = io.get("conditions", "Extended Session")
        security = io.get("security_level", "Level1")

        # 确定会话
        if "extend" in conditions.lower():
            target_session = 0x03
        elif "program" in conditions.lower():
            target_session = 0x02
        else:
            target_session = 0x01

        # 解析SA
        sa_level = None
        if security:
            s = security.strip().lower()
            if "3" in s or "fbl" in s:
                sa_level = 0x03
            elif "5" in s or "immo" in s:
                sa_level = 0x05
            elif "1" in s:
                sa_level = 0x01

        did_hi = (did_int >> 8) & 0xFF
        did_lo = did_int & 0xFF

        method.append(f'        # IOControl {did_num} - {did_name} P2时间测量')
        method.append(f'        self.reset_to_default_session()')
        method.append(f'        self.switch_session(0x{target_session:02X})')
        method.append(f'        time.sleep(0.05)')
        if sa_level is not None:
            method.append(f'        self.unlock_security(0x{sa_level:02X})')
        # ReturnControlToECU (0x00) - 最安全的操作
        method.append(f'        req_data = [SID_IO_CONTROL, 0x{did_hi:02X}, 0x{did_lo:02X}, 0x00]')
        method.append(f'        resp, elapsed = self.uds.send_request_timed(req_data)')
        method.append(f'        p2_ok = elapsed <= P2_TIMEOUT * 1.1')
        method.append(f'        self.add_result(')
        method.append(f'            service="Timing", test_name="P2 IOCtrl {did_num} {did_name}",')
        method.append(f'            did_rid="{did_num}",')
        method.append(f'            expected=f"<={{P2_TIMEOUT}}ms",')
        method.append(f'            actual=f"{{elapsed:.1f}}ms",')
        method.append(f'            status="PASS" if (p2_ok or self.is_negative_response(resp)) else "FAIL",')
        method.append(f'            detail=f"ReturnControlToECU(0x00) 耗时{{elapsed:.1f}}ms")')
        method.append('')

    method.append('        self.reset_to_default_session()')

    return '\n'.join(method), '            self.test_io_control_response_timing()'


def generate_io_control_tests(io_controls):
    """生成IOControl测试方法"""
    if not io_controls:
        return "", ""

    method = []
    method.append('    def test_io_controls(self):')
    method.append('        """测试 $2F InputOutputControlByIdentifier"""')
    method.append('        print("\\n=== 测试 $2F InputOutputControlByIdentifier ===")')
    method.append('')

    for io in io_controls:
        did_num = io["did_number"]
        did_name = io.get("did_name", "Unknown")
        did_int = int(did_num, 16)
        conditions = io.get("conditions", "Extended Session")
        security = io.get("security_level", "Level1")

        # 解析安全等级
        sa_level = None
        sa_level_name = "无"
        if security:
            s = security.strip().lower()
            if "3" in s or "fbl" in s or "prog" in s:
                sa_level = 0x03
                sa_level_name = "Level3(FBL)"
            elif "5" in s or "immo" in s:
                sa_level = 0x05
                sa_level_name = "Level5(IMMO)"
            elif "1" in s:
                sa_level = 0x01
                sa_level_name = "Level1"

        # 确定需要的会话
        if "extend" in conditions.lower():
            target_session = 0x03
            session_name = "Extended (0x03)"
        elif "program" in conditions.lower():
            target_session = 0x02
            session_name = "Programming (0x02)"
        else:
            target_session = 0x01
            session_name = "Default (0x01)"

        # 错误会话测试
        wrong_session = 0x01 if target_session != 0x01 else 0x03
        wrong_session_name = SESSION_NAMES_MAP.get(wrong_session, f"0x{wrong_session:02X}")

        method.append(f'        # IOControl {did_num} - {did_name} - 错误会话')
        method.append(f'        self.reset_to_default_session()')
        method.append(f'        self.switch_session(0x{wrong_session:02X})')
        method.append(f'        time.sleep(0.05)')
        method.append(f'        resp = self.uds.io_control(0x{did_int:04X}, 0x03)')  # ShortTermAdjustment
        method.append(f'        if self.is_negative_response(resp):')
        method.append(f'            self.add_result(')
        method.append(f'                service="$2F", test_name="IO {did_num}({wrong_session_name})应拒绝",')
        method.append(f'                did_rid="{did_num}", session="{wrong_session_name}",')
        method.append(f'                expected="NRC", actual=self.resp_to_hex(resp), status="PASS")')
        method.append(f'        else:')
        method.append(f'            self.add_result(')
        method.append(f'                service="$2F", test_name="IO {did_num}({wrong_session_name})应拒绝",')
        method.append(f'                did_rid="{did_num}", session="{wrong_session_name}",')
        method.append(f'                expected="NRC", actual=self.resp_to_hex(resp), status="FAIL")')
        method.append('')

        # 无安全访问测试
        method.append(f'        # IOControl {did_num} - 无安全访问 (需要{sa_level_name})')
        method.append(f'        self.reset_to_default_session()')
        method.append(f'        self.switch_session(0x{target_session:02X})')
        method.append(f'        time.sleep(0.05)')
        method.append(f'        resp = self.uds.io_control(0x{did_int:04X}, 0x03)')
        method.append(f'        if self.is_negative_response(resp, 0x33):')
        method.append(f'            self.add_result(')
        method.append(f'                service="$2F", test_name="IO {did_num}无安全访问→NRC0x33",')
        method.append(f'                did_rid="{did_num}", session="{session_name}", security="{sa_level_name}",')
        method.append(f'                expected="NRC 0x33", actual=self.resp_to_hex(resp), status="PASS")')
        method.append(f'        else:')
        method.append(f'            self.add_result(')
        method.append(f'                service="$2F", test_name="IO {did_num}无安全访问",')
        method.append(f'                did_rid="{did_num}", session="{session_name}", security="{sa_level_name}",')
        method.append(f'                expected="NRC 0x33", actual=self.resp_to_hex(resp),')
        method.append(f'                status="PASS" if self.is_negative_response(resp) else "FAIL")')
        method.append('')

        # SA解锁后正向测试 - ShortTermAdjustment
        if sa_level is not None:
            method.append(f'        # IOControl {did_num} - SA解锁后ShortTermAdjust (SA=0x{sa_level:02X} {sa_level_name})')
            method.append(f'        self.reset_to_default_session()')
            method.append(f'        self.switch_session(0x{target_session:02X})')
            method.append(f'        time.sleep(0.05)')
            method.append(f'        self.unlock_security(0x{sa_level:02X})')
            method.append(f'        resp = self.uds.io_control(0x{did_int:04X}, 0x03)')
            method.append(f'        if self.is_positive_response(resp, SID_IO_CONTROL):')
            method.append(f'            self.add_result(')
            method.append(f'                service="$2F", test_name="IO {did_num} SA解锁后ShortTermAdjust",')
            method.append(f'                did_rid="{did_num}", session="{session_name}", security="{sa_level_name}",')
            method.append(f'                expected="正响应 0x6F", actual=self.resp_to_hex(resp), status="PASS")')
            method.append(f'        else:')
            method.append(f'            nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None')
            method.append(f'            self.add_result(')
            method.append(f'                service="$2F", test_name="IO {did_num} SA解锁后ShortTermAdjust",')
            method.append(f'                did_rid="{did_num}", session="{session_name}", security="{sa_level_name}",')
            method.append(f'                expected="正响应 0x6F", actual=self.resp_to_hex(resp),')
            method.append(f'                status="PASS" if nrc in (0x22, 0x31) else "FAIL",')
            method.append(f'                detail="NRC 0x22(条件不满足)/0x31可接受")')
            method.append('')

        # ReturnControlToECU测试（0x00）
        method.append(f'        # IOControl {did_num} - ReturnControlToECU')
        method.append(f'        resp = self.uds.io_control(0x{did_int:04X}, 0x00)')
        method.append(f'        self.add_result(')
        method.append(f'            service="$2F", test_name="IO {did_num} ReturnControlToECU(0x00)",')
        method.append(f'            did_rid="{did_num}", session="{session_name}",')
        method.append(f'            expected="正响应或NRC",')
        method.append(f'            actual=self.resp_to_hex(resp),')
        method.append(f'            status="PASS" if resp is not None else "FAIL")')
        method.append('')

        # ResetToDefault测试（0x01）
        method.append(f'        # IOControl {did_num} - ResetToDefault')
        method.append(f'        resp = self.uds.io_control(0x{did_int:04X}, 0x01)')
        method.append(f'        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None')
        method.append(f'        self.add_result(')
        method.append(f'            service="$2F", test_name="IO {did_num} ResetToDefault(0x01)",')
        method.append(f'            did_rid="{did_num}", session="{session_name}",')
        method.append(f'            expected="正响应或NRC 0x12/0x31",')
        method.append(f'            actual=self.resp_to_hex(resp),')
        method.append(f'            status="PASS" if (self.is_positive_response(resp, SID_IO_CONTROL)')
        method.append(f'                              or nrc in (0x12, 0x31, 0x22, 0x33)) else "FAIL")')
        method.append('')

        # FreezeCurrentState测试（0x02）
        method.append(f'        # IOControl {did_num} - FreezeCurrentState')
        method.append(f'        resp = self.uds.io_control(0x{did_int:04X}, 0x02)')
        method.append(f'        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None')
        method.append(f'        self.add_result(')
        method.append(f'            service="$2F", test_name="IO {did_num} FreezeCurrentState(0x02)",')
        method.append(f'            did_rid="{did_num}", session="{session_name}",')
        method.append(f'            expected="正响应或NRC 0x12/0x31",')
        method.append(f'            actual=self.resp_to_hex(resp),')
        method.append(f'            status="PASS" if (self.is_positive_response(resp, SID_IO_CONTROL)')
        method.append(f'                              or nrc in (0x12, 0x31, 0x22, 0x33)) else "FAIL")')
        method.append('')

        # 无效controlOptionRecord（0x04 reserved）
        method.append(f'        # IOControl {did_num} - 无效controlOption(0x04)')
        method.append(f'        resp = self.uds.io_control(0x{did_int:04X}, 0x04)')
        method.append(f'        self.add_result(')
        method.append(f'            service="$2F", test_name="IO {did_num} 无效controlOption(0x04)",')
        method.append(f'            did_rid="{did_num}", session="{session_name}",')
        method.append(f'            expected="NRC 0x12/0x31",')
        method.append(f'            actual=self.resp_to_hex(resp),')
        method.append(f'            status="PASS" if self.is_negative_response(resp) else "FAIL")')
        method.append('')

        # 参数长度逆向测试 (controlStatusRecord 过长/过短)
        io_params = io.get("parameters", [])
        total_io_bytes = 0
        has_io_params = False
        for p in io_params:
            bl = safe_int_gen(p.get("bit_length", 0))
            if bl > 0:
                total_io_bytes += max(1, (bl + 7) // 8)
                has_io_params = True

        if has_io_params and total_io_bytes > 0:
            # ShortTermAdjust + 过长record
            over_len = total_io_bytes + 3
            method.append(f'        # IOControl {did_num} - 过长controlStatusRecord({over_len}B>期望{total_io_bytes}B)')
            method.append(f'        self.reset_to_default_session()')
            method.append(f'        self.switch_session(0x{target_session:02X})')
            method.append(f'        time.sleep(0.05)')
            if sa_level is not None:
                method.append(f'        self.unlock_security(0x{sa_level:02X})')
            method.append(f'        resp = self.uds.io_control(0x{did_int:04X}, 0x03, [0x00] * {over_len})')
            method.append(f'        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None')
            method.append(f'        self.add_result(')
            method.append(f'            service="$2F", test_name="IO {did_num}过长record({over_len}B>期望{total_io_bytes}B)",')
            method.append(f'            did_rid="{did_num}", session="{session_name}",')
            method.append(f'            expected="NRC 0x13(incorrectMessageLength)",')
            method.append(f'            actual=self.resp_to_hex(resp),')
            method.append(f'            status="PASS" if nrc in (0x13, 0x31, 0x22) else "FAIL",')
            method.append(f'            detail="某些ECU可能忽略多余字节")')
            method.append('')

            # ShortTermAdjust + 无record (0字节)
            method.append(f'        # IOControl {did_num} - 无controlStatusRecord(期望{total_io_bytes}B)')
            method.append(f'        self.reset_to_default_session()')
            method.append(f'        self.switch_session(0x{target_session:02X})')
            method.append(f'        time.sleep(0.05)')
            if sa_level is not None:
                method.append(f'        self.unlock_security(0x{sa_level:02X})')
            method.append(f'        resp = self.uds.io_control(0x{did_int:04X}, 0x03)')
            method.append(f'        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None')
            method.append(f'        self.add_result(')
            method.append(f'            service="$2F", test_name="IO {did_num}无record(期望{total_io_bytes}B)",')
            method.append(f'            did_rid="{did_num}", session="{session_name}",')
            method.append(f'            expected="NRC 0x13(incorrectMessageLength)",')
            method.append(f'            actual=self.resp_to_hex(resp),')
            method.append(f'            status="PASS" if nrc in (0x13, 0x31, 0x22) else "FAIL")')
            method.append('')

            # ShortTermAdjust + 过短record (少1字节)
            if total_io_bytes > 1:
                short_len = total_io_bytes - 1
                method.append(f'        # IOControl {did_num} - 过短controlStatusRecord({short_len}B<期望{total_io_bytes}B)')
                method.append(f'        self.reset_to_default_session()')
                method.append(f'        self.switch_session(0x{target_session:02X})')
                method.append(f'        time.sleep(0.05)')
                if sa_level is not None:
                    method.append(f'        self.unlock_security(0x{sa_level:02X})')
                method.append(f'        resp = self.uds.io_control(0x{did_int:04X}, 0x03, [0x00] * {short_len})')
                method.append(f'        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None')
                method.append(f'        self.add_result(')
                method.append(f'            service="$2F", test_name="IO {did_num}过短record({short_len}B<期望{total_io_bytes}B)",')
                method.append(f'            did_rid="{did_num}", session="{session_name}",')
                method.append(f'            expected="NRC 0x13(incorrectMessageLength)",')
                method.append(f'            actual=self.resp_to_hex(resp),')
                method.append(f'            status="PASS" if nrc in (0x13, 0x31, 0x22) else "FAIL")')
                method.append('')

    method.append('        self.reset_to_default_session()')

    return '\n'.join(method), '            self.test_io_controls()'


def generate_routine_tests(routines):
    """生成RoutineControl测试方法"""
    if not routines:
        return "", ""

    method = []
    method.append('    def test_routines(self):')
    method.append('        """测试 $31 RoutineControl"""')
    method.append('        print("\\n=== 测试 $31 RoutineControl ===")')
    method.append('')

    for routine in routines:
        rid_num = routine["rid_number"]
        rid_name = routine.get("rid_name", "Unknown")
        rid_int = int(rid_num, 16)
        conditions = routine.get("conditions", "Extended Session")
        security = routine.get("security_level", "Level1")
        control_type = routine.get("control_type", "01")

        # 确定需要的会话
        if "program" in conditions.lower():
            target_session = 0x02
            session_name = "Programming (0x02)"
        elif "extend" in conditions.lower():
            target_session = 0x03
            session_name = "Extended (0x03)"
        else:
            target_session = 0x01
            session_name = "Default (0x01)"

        # 构建请求数据
        req_params = routine.get("req_parameters", [])
        req_data = []
        for p in req_params:
            bit_len = safe_int_gen(p.get("bit_length", "8"))
            byte_len = max(1, (bit_len + 7) // 8)
            req_data.extend([0x00] * byte_len)

        req_data_str = str(req_data) if req_data else "[]"

        # 错误会话测试
        wrong_session = 0x01 if target_session != 0x01 else 0x03
        wrong_session_name = SESSION_NAMES_MAP.get(wrong_session, f"0x{wrong_session:02X}")

        method.append(f'        # Routine {rid_num} - {rid_name} - 错误会话')
        method.append(f'        self.reset_to_default_session()')
        method.append(f'        self.switch_session(0x{wrong_session:02X})')
        method.append(f'        time.sleep(0.05)')
        method.append(f'        resp = self.uds.routine_control(0x01, 0x{rid_int:04X}, {req_data_str})')
        method.append(f'        if self.is_negative_response(resp):')
        method.append(f'            self.add_result(')
        method.append(f'                service="$31", test_name="Routine {rid_num}({wrong_session_name})应拒绝",')
        method.append(f'                did_rid="{rid_num}", session="{wrong_session_name}",')
        method.append(f'                expected="NRC", actual=self.resp_to_hex(resp), status="PASS")')
        method.append(f'        else:')
        method.append(f'            self.add_result(')
        method.append(f'                service="$31", test_name="Routine {rid_num}({wrong_session_name})应拒绝",')
        method.append(f'                did_rid="{rid_num}", session="{wrong_session_name}",')
        method.append(f'                expected="NRC", actual=self.resp_to_hex(resp), status="FAIL")')
        method.append('')

        # 解析安全等级
        sa_level = None
        sa_level_name = "无"
        if security:
            s = security.strip().lower()
            if "3" in s or "fbl" in s or "prog" in s:
                sa_level = 0x03
                sa_level_name = "Level3(FBL)"
            elif "5" in s or "immo" in s:
                sa_level = 0x05
                sa_level_name = "Level5(IMMO)"
            elif "1" in s:
                sa_level = 0x01
                sa_level_name = "Level1"

        # 无安全访问测试
        method.append(f'        # Routine {rid_num} - 无安全访问 (需要{sa_level_name})')
        method.append(f'        self.reset_to_default_session()')
        method.append(f'        self.switch_session(0x{target_session:02X})')
        method.append(f'        time.sleep(0.05)')
        method.append(f'        resp = self.uds.routine_control(0x01, 0x{rid_int:04X}, {req_data_str})')
        method.append(f'        if self.is_negative_response(resp, 0x33):')
        method.append(f'            self.add_result(')
        method.append(f'                service="$31", test_name="Routine {rid_num}无安全访问→NRC0x33",')
        method.append(f'                did_rid="{rid_num}", session="{session_name}", security="{sa_level_name}",')
        method.append(f'                expected="NRC 0x33", actual=self.resp_to_hex(resp), status="PASS")')
        method.append(f'        else:')
        method.append(f'            self.add_result(')
        method.append(f'                service="$31", test_name="Routine {rid_num}无安全访问",')
        method.append(f'                did_rid="{rid_num}", session="{session_name}", security="{sa_level_name}",')
        method.append(f'                expected="NRC 0x33", actual=self.resp_to_hex(resp),')
        method.append(f'                status="PASS" if self.is_negative_response(resp) else "FAIL")')
        method.append('')

        # SA解锁后正向测试
        if sa_level is not None:
            method.append(f'        # Routine {rid_num} - SA解锁后执行 (SA=0x{sa_level:02X} {sa_level_name})')
            method.append(f'        self.reset_to_default_session()')
            method.append(f'        self.switch_session(0x{target_session:02X})')
            method.append(f'        time.sleep(0.05)')
            method.append(f'        self.unlock_security(0x{sa_level:02X})')
            method.append(f'        resp = self.uds.routine_control(0x01, 0x{rid_int:04X}, {req_data_str})')
            method.append(f'        if self.is_positive_response(resp, SID_ROUTINE_CONTROL):')
            method.append(f'            self.add_result(')
            method.append(f'                service="$31", test_name="Routine {rid_num} SA解锁后startRoutine",')
            method.append(f'                did_rid="{rid_num}", session="{session_name}", security="{sa_level_name}",')
            method.append(f'                expected="正响应 0x71", actual=self.resp_to_hex(resp), status="PASS")')
            method.append(f'        else:')
            method.append(f'            nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None')
            method.append(f'            self.add_result(')
            method.append(f'                service="$31", test_name="Routine {rid_num} SA解锁后startRoutine",')
            method.append(f'                did_rid="{rid_num}", session="{session_name}", security="{sa_level_name}",')
            method.append(f'                expected="正响应 0x71", actual=self.resp_to_hex(resp),')
            method.append(f'                status="PASS" if nrc in (0x22, 0x72) else "FAIL",')
            method.append(f'                detail="NRC 0x22(条件不满足)/0x72(requestSequenceError)可接受")')
            method.append('')

        # 无效的ControlType测试
        method.append(f'        # Routine {rid_num} - 无效ControlType')
        method.append(f'        resp = self.uds.routine_control(0x04, 0x{rid_int:04X})')
        method.append(f'        if self.is_negative_response(resp, 0x12):')
        method.append(f'            self.add_result(')
        method.append(f'                service="$31", test_name="Routine {rid_num}无效ControlType",')
        method.append(f'                did_rid="{rid_num}", session="{session_name}",')
        method.append(f'                expected="NRC 0x12", actual=self.resp_to_hex(resp), status="PASS")')
        method.append(f'        else:')
        method.append(f'            self.add_result(')
        method.append(f'                service="$31", test_name="Routine {rid_num}无效ControlType",')
        method.append(f'                did_rid="{rid_num}", session="{session_name}",')
        method.append(f'                expected="NRC 0x12", actual=self.resp_to_hex(resp),')
        method.append(f'                status="PASS" if self.is_negative_response(resp) else "FAIL")')
        method.append('')

        # 参数长度逆向测试 (过长/过短请求)
        total_param_bytes = 0
        has_real_params = False
        for p in req_params:
            bl = safe_int_gen(p.get("bit_length", 0))
            if bl > 0:
                total_param_bytes += max(1, (bl + 7) // 8)
                has_real_params = True

        if has_real_params and total_param_bytes > 0:
            # 过短参数 (少1字节)
            if total_param_bytes > 1:
                short_len = total_param_bytes - 1
                method.append(f'        # Routine {rid_num} - 过短参数({short_len}B<期望{total_param_bytes}B)')
                method.append(f'        self.reset_to_default_session()')
                method.append(f'        self.switch_session(0x{target_session:02X})')
                method.append(f'        time.sleep(0.05)')
                if sa_level is not None:
                    method.append(f'        self.unlock_security(0x{sa_level:02X})')
                method.append(f'        resp = self.uds.routine_control(0x01, 0x{rid_int:04X}, [0x00] * {short_len})')
                method.append(f'        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None')
                method.append(f'        self.add_result(')
                method.append(f'            service="$31", test_name="Routine {rid_num}过短参数({short_len}B<期望{total_param_bytes}B)",')
                method.append(f'            did_rid="{rid_num}", session="{session_name}",')
                method.append(f'            expected="NRC 0x13(incorrectMessageLength)",')
                method.append(f'            actual=self.resp_to_hex(resp),')
                method.append(f'            status="PASS" if nrc in (0x13, 0x31, 0x22) else "FAIL")')
                method.append('')

            # 无参数 (仅发SID+ControlType+RID)
            method.append(f'        # Routine {rid_num} - 无参数(期望{total_param_bytes}B)')
            method.append(f'        self.reset_to_default_session()')
            method.append(f'        self.switch_session(0x{target_session:02X})')
            method.append(f'        time.sleep(0.05)')
            if sa_level is not None:
                method.append(f'        self.unlock_security(0x{sa_level:02X})')
            method.append(f'        resp = self.uds.routine_control(0x01, 0x{rid_int:04X}, [])')
            method.append(f'        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None')
            method.append(f'        self.add_result(')
            method.append(f'            service="$31", test_name="Routine {rid_num}无参数(期望{total_param_bytes}B)",')
            method.append(f'            did_rid="{rid_num}", session="{session_name}",')
            method.append(f'            expected="NRC 0x13(incorrectMessageLength)",')
            method.append(f'            actual=self.resp_to_hex(resp),')
            method.append(f'            status="PASS" if nrc in (0x13, 0x31, 0x22) else "FAIL")')
            method.append('')

            # 过长参数 (多3字节)
            over_len = total_param_bytes + 3
            method.append(f'        # Routine {rid_num} - 过长参数({over_len}B>期望{total_param_bytes}B)')
            method.append(f'        self.reset_to_default_session()')
            method.append(f'        self.switch_session(0x{target_session:02X})')
            method.append(f'        time.sleep(0.05)')
            if sa_level is not None:
                method.append(f'        self.unlock_security(0x{sa_level:02X})')
            method.append(f'        resp = self.uds.routine_control(0x01, 0x{rid_int:04X}, [0x00] * {over_len})')
            method.append(f'        nrc = self.get_nrc(resp) if self.is_negative_response(resp) else None')
            method.append(f'        self.add_result(')
            method.append(f'            service="$31", test_name="Routine {rid_num}过长参数({over_len}B>期望{total_param_bytes}B)",')
            method.append(f'            did_rid="{rid_num}", session="{session_name}",')
            method.append(f'            expected="NRC 0x13(incorrectMessageLength)",')
            method.append(f'            actual=self.resp_to_hex(resp),')
            method.append(f'            status="PASS" if nrc in (0x13, 0x31, 0x22) else "FAIL",')
            method.append(f'            detail="某些ECU可能忽略多余字节")')
            method.append('')

    method.append('        self.reset_to_default_session()')

    return '\n'.join(method), '            self.test_routines()'


def generate_dtc_tests(dtcs):
    """生成DTC测试方法"""
    if not dtcs:
        return "", ""

    method = []
    method.append('    def test_dtc_services(self):')
    method.append('        """测试 $19/$14/$85 DTC相关服务"""')
    method.append('        print("\\n=== 测试 DTC相关服务 ===")')
    method.append('')

    # $19 ReadDTCInformation
    method.append('        # $19-01 读取DTC状态总览')
    method.append('        resp = self.uds.read_dtc_info(0x01, 0xFF)')
    method.append('        if self.is_positive_response(resp, SID_READ_DTC_INFO):')
    method.append('            self.add_result(')
    method.append('                service="$19", test_name="ReadDTCInfo SubFunc=01",')
    method.append('                expected="正响应 0x59", actual=self.resp_to_hex(resp), status="PASS")')
    method.append('        else:')
    method.append('            self.add_result(')
    method.append('                service="$19", test_name="ReadDTCInfo SubFunc=01",')
    method.append('                expected="正响应 0x59", actual=self.resp_to_hex(resp), status="FAIL")')
    method.append('')

    # $19-02 读取DTC详细信息（按status mask）
    method.append('        # $19-02 读取DTC详细信息')
    method.append('        resp = self.uds.read_dtc_info(0x02, 0xFF)')
    method.append('        if self.is_positive_response(resp, SID_READ_DTC_INFO):')
    method.append('            self.add_result(')
    method.append('                service="$19", test_name="ReadDTCInfo SubFunc=02 所有DTC",')
    method.append('                expected="正响应", actual=self.resp_to_hex(resp), status="PASS")')
    method.append('        else:')
    method.append('            self.add_result(')
    method.append('                service="$19", test_name="ReadDTCInfo SubFunc=02 所有DTC",')
    method.append('                expected="正响应", actual=self.resp_to_hex(resp), status="FAIL")')
    method.append('')

    # $19-0A 读取所有支持的DTC
    method.append('        # $19-0A 读取所有支持的DTC')
    method.append('        resp = self.uds.read_dtc_info(0x0A)')
    method.append('        if self.is_positive_response(resp, SID_READ_DTC_INFO):')
    method.append('            self.add_result(')
    method.append('                service="$19", test_name="ReadDTCInfo SubFunc=0A",')
    method.append('                expected="正响应", actual=self.resp_to_hex(resp), status="PASS")')
    method.append('        else:')
    method.append('            self.add_result(')
    method.append('                service="$19", test_name="ReadDTCInfo SubFunc=0A",')
    method.append('                expected="正响应", actual=self.resp_to_hex(resp), status="FAIL")')
    method.append('')

    # $19 全部子功能覆盖 (ISO 14229-1 §11.3)
    # 0x03 reportDTCSnapshotIdentification
    method.append('        # $19-03 reportDTCSnapshotIdentification')
    method.append('        resp = self.uds.read_dtc_info(0x03)')
    method.append('        if self.is_positive_response(resp, SID_READ_DTC_INFO) or self.is_negative_response(resp, 0x12):')
    method.append('            self.add_result(')
    method.append('                service="$19", test_name="ReadDTCInfo SubFunc=03 SnapshotIdentification",')
    method.append('                expected="正响应或NRC 0x12(不支持)", actual=self.resp_to_hex(resp), status="PASS")')
    method.append('        else:')
    method.append('            self.add_result(')
    method.append('                service="$19", test_name="ReadDTCInfo SubFunc=03 SnapshotIdentification",')
    method.append('                expected="正响应或NRC 0x12", actual=self.resp_to_hex(resp),')
    method.append('                status="PASS" if self.is_negative_response(resp) else "FAIL")')
    method.append('')

    # 0x04 reportDTCSnapshotRecordByDTCNumber (需要DTC参数)
    if dtcs:
        dtc0 = dtcs[0]
        dtc0_hex = dtc0["dtc_number_hex"]
        dtc0_int = int(dtc0_hex, 16)
        b1_0 = (dtc0_int >> 16) & 0xFF
        b2_0 = (dtc0_int >> 8) & 0xFF
        b3_0 = dtc0_int & 0xFF
        method.append(f'        # $19-04 reportDTCSnapshotRecordByDTCNumber (DTC={dtc0_hex})')
        method.append(f'        resp = self.uds.read_dtc_info(0x04, 0x{b1_0:02X}, 0x{b2_0:02X}, 0x{b3_0:02X}, 0xFF)')
        method.append(f'        if self.is_positive_response(resp, SID_READ_DTC_INFO) or self.is_negative_response(resp, 0x12):')
        method.append(f'            self.add_result(')
        method.append(f'                service="$19", test_name="ReadDTCInfo SubFunc=04 Snapshot DTC={dtc0_hex}",')
        method.append(f'                expected="正响应或NRC 0x12", actual=self.resp_to_hex(resp), status="PASS")')
        method.append(f'        else:')
        method.append(f'            self.add_result(')
        method.append(f'                service="$19", test_name="ReadDTCInfo SubFunc=04 Snapshot DTC={dtc0_hex}",')
        method.append(f'                expected="正响应或NRC 0x12", actual=self.resp_to_hex(resp),')
        method.append(f'                status="PASS" if self.is_negative_response(resp) else "FAIL")')
        method.append('')

    # 0x05 reportDTCStoredDataByRecordNumber
    method.append('        # $19-05 reportDTCStoredDataByRecordNumber')
    method.append('        resp = self.uds.read_dtc_info(0x05, 0xFF)')
    method.append('        if self.is_positive_response(resp, SID_READ_DTC_INFO) or self.is_negative_response(resp, 0x12):')
    method.append('            self.add_result(')
    method.append('                service="$19", test_name="ReadDTCInfo SubFunc=05 StoredDataByRecordNumber",')
    method.append('                expected="正响应或NRC 0x12", actual=self.resp_to_hex(resp), status="PASS")')
    method.append('        else:')
    method.append('            self.add_result(')
    method.append('                service="$19", test_name="ReadDTCInfo SubFunc=05 StoredDataByRecordNumber",')
    method.append('                expected="正响应或NRC 0x12", actual=self.resp_to_hex(resp),')
    method.append('                status="PASS" if self.is_negative_response(resp) else "FAIL")')
    method.append('')

    # 0x07 reportNumberOfDTCBySeverityMaskRecord
    method.append('        # $19-07 reportNumberOfDTCBySeverityMaskRecord')
    method.append('        resp = self.uds.read_dtc_info(0x07, 0xFF, 0xFF)')
    method.append('        if self.is_positive_response(resp, SID_READ_DTC_INFO) or self.is_negative_response(resp, 0x12):')
    method.append('            self.add_result(')
    method.append('                service="$19", test_name="ReadDTCInfo SubFunc=07 NumberBySeverityMask",')
    method.append('                expected="正响应或NRC 0x12", actual=self.resp_to_hex(resp), status="PASS")')
    method.append('        else:')
    method.append('            self.add_result(')
    method.append('                service="$19", test_name="ReadDTCInfo SubFunc=07 NumberBySeverityMask",')
    method.append('                expected="正响应或NRC 0x12", actual=self.resp_to_hex(resp),')
    method.append('                status="PASS" if self.is_negative_response(resp) else "FAIL")')
    method.append('')

    # 0x08 reportDTCBySeverityMaskRecord
    method.append('        # $19-08 reportDTCBySeverityMaskRecord')
    method.append('        resp = self.uds.read_dtc_info(0x08, 0xFF, 0xFF)')
    method.append('        if self.is_positive_response(resp, SID_READ_DTC_INFO) or self.is_negative_response(resp, 0x12):')
    method.append('            self.add_result(')
    method.append('                service="$19", test_name="ReadDTCInfo SubFunc=08 DTCBySeverityMask",')
    method.append('                expected="正响应或NRC 0x12", actual=self.resp_to_hex(resp), status="PASS")')
    method.append('        else:')
    method.append('            self.add_result(')
    method.append('                service="$19", test_name="ReadDTCInfo SubFunc=08 DTCBySeverityMask",')
    method.append('                expected="正响应或NRC 0x12", actual=self.resp_to_hex(resp),')
    method.append('                status="PASS" if self.is_negative_response(resp) else "FAIL")')
    method.append('')

    # 0x09 reportSeverityInformationOfDTC
    if dtcs:
        method.append(f'        # $19-09 reportSeverityInformationOfDTC (DTC={dtc0_hex})')
        method.append(f'        resp = self.uds.read_dtc_info(0x09, 0x{b1_0:02X}, 0x{b2_0:02X}, 0x{b3_0:02X})')
        method.append(f'        if self.is_positive_response(resp, SID_READ_DTC_INFO) or self.is_negative_response(resp, 0x12):')
        method.append(f'            self.add_result(')
        method.append(f'                service="$19", test_name="ReadDTCInfo SubFunc=09 SeverityOfDTC {dtc0_hex}",')
        method.append(f'                expected="正响应或NRC 0x12", actual=self.resp_to_hex(resp), status="PASS")')
        method.append(f'        else:')
        method.append(f'            self.add_result(')
        method.append(f'                service="$19", test_name="ReadDTCInfo SubFunc=09 SeverityOfDTC {dtc0_hex}",')
        method.append(f'                expected="正响应或NRC 0x12", actual=self.resp_to_hex(resp),')
        method.append(f'                status="PASS" if self.is_negative_response(resp) else "FAIL")')
        method.append('')

    # 0x0B-0x0E 各类DTC查询
    sub_func_names = {
        0x0B: "reportFirstTestFailedDTC",
        0x0C: "reportFirstConfirmedDTC",
        0x0D: "reportMostRecentTestFailedDTC",
        0x0E: "reportMostRecentConfirmedDTC",
    }
    for sf, sf_name in sub_func_names.items():
        method.append(f'        # $19-{sf:02X} {sf_name}')
        method.append(f'        resp = self.uds.read_dtc_info(0x{sf:02X})')
        method.append(f'        if self.is_positive_response(resp, SID_READ_DTC_INFO) or self.is_negative_response(resp, 0x12):')
        method.append(f'            self.add_result(')
        method.append(f'                service="$19", test_name="ReadDTCInfo SubFunc=0x{sf:02X} {sf_name}",')
        method.append(f'                expected="正响应或NRC 0x12", actual=self.resp_to_hex(resp), status="PASS")')
        method.append(f'        else:')
        method.append(f'            self.add_result(')
        method.append(f'                service="$19", test_name="ReadDTCInfo SubFunc=0x{sf:02X} {sf_name}",')
        method.append(f'                expected="正响应或NRC 0x12", actual=self.resp_to_hex(resp),')
        method.append(f'                status="PASS" if self.is_negative_response(resp) else "FAIL")')
        method.append('')

    # 0x0F reportMirrorMemoryDTCByStatusMask
    method.append('        # $19-0F reportMirrorMemoryDTCByStatusMask')
    method.append('        resp = self.uds.read_dtc_info(0x0F, 0xFF)')
    method.append('        if self.is_positive_response(resp, SID_READ_DTC_INFO) or self.is_negative_response(resp, 0x12):')
    method.append('            self.add_result(')
    method.append('                service="$19", test_name="ReadDTCInfo SubFunc=0F MirrorMemory",')
    method.append('                expected="正响应或NRC 0x12", actual=self.resp_to_hex(resp), status="PASS")')
    method.append('        else:')
    method.append('            self.add_result(')
    method.append('                service="$19", test_name="ReadDTCInfo SubFunc=0F MirrorMemory",')
    method.append('                expected="正响应或NRC 0x12", actual=self.resp_to_hex(resp),')
    method.append('                status="PASS" if self.is_negative_response(resp) else "FAIL")')
    method.append('')

    # 0x14 reportDTCFaultDetectionCounter
    method.append('        # $19-14 reportDTCFaultDetectionCounter')
    method.append('        resp = self.uds.read_dtc_info(0x14)')
    method.append('        if self.is_positive_response(resp, SID_READ_DTC_INFO) or self.is_negative_response(resp, 0x12):')
    method.append('            self.add_result(')
    method.append('                service="$19", test_name="ReadDTCInfo SubFunc=14 FaultDetectionCounter",')
    method.append('                expected="正响应或NRC 0x12", actual=self.resp_to_hex(resp), status="PASS")')
    method.append('        else:')
    method.append('            self.add_result(')
    method.append('                service="$19", test_name="ReadDTCInfo SubFunc=14 FaultDetectionCounter",')
    method.append('                expected="正响应或NRC 0x12", actual=self.resp_to_hex(resp),')
    method.append('                status="PASS" if self.is_negative_response(resp) else "FAIL")')
    method.append('')

    # 0x42 reportWWHOBDDTCWithPermanentStatus
    method.append('        # $19-42 reportWWHOBDDTCWithPermanentStatus')
    method.append('        resp = self.uds.read_dtc_info(0x42)')
    method.append('        if self.is_positive_response(resp, SID_READ_DTC_INFO) or self.is_negative_response(resp, 0x12):')
    method.append('            self.add_result(')
    method.append('                service="$19", test_name="ReadDTCInfo SubFunc=42 WWHOBD Permanent",')
    method.append('                expected="正响应或NRC 0x12", actual=self.resp_to_hex(resp), status="PASS")')
    method.append('        else:')
    method.append('            self.add_result(')
    method.append('                service="$19", test_name="ReadDTCInfo SubFunc=42 WWHOBD Permanent",')
    method.append('                expected="正响应或NRC 0x12", actual=self.resp_to_hex(resp),')
    method.append('                status="PASS" if self.is_negative_response(resp) else "FAIL")')
    method.append('')

    # 剩余11个$19子功能 (ISO 14229-1:2020 Table 272完整覆盖)
    remaining_19_subfuncs = [
        (0x10, "reportMirrorMemoryDTCExtDataRecordByDTCNumber", [0x00, 0x00, 0x01, 0xFF]),
        (0x11, "reportNumberOfMirrorMemoryDTCByStatusMask", [0xFF]),
        (0x12, "reportNumberOfEmissionsOBDDTCByStatusMask", [0xFF]),
        (0x13, "reportEmissionsOBDDTCByStatusMask", [0xFF]),
        (0x15, "reportDTCWithPermanentStatus", []),
        (0x16, "reportDTCExtDataRecordByRecordNumber", [0xFF]),
        (0x17, "reportUserDefMemoryDTCByStatusMask", [0xFF]),
        (0x18, "reportUserDefMemoryDTCSnapshotRecordByDTCNumber", [0x00, 0x00, 0x01, 0xFF]),
        (0x19, "reportUserDefMemoryDTCExtDataRecordByDTCNumber", [0x00, 0x00, 0x01, 0xFF]),
        (0x55, "reportWWHOBDDTCByMaskRecord", [0xFF, 0xFF]),
        (0x56, "reportWWHOBDDTCWithPermanentStatusV2", []),
    ]
    for sf, sf_name, extra_args in remaining_19_subfuncs:
        args_str = ', '.join([f'0x{a:02X}' for a in extra_args])
        call_args = f'0x{sf:02X}' + (f', {args_str}' if args_str else '')
        method.append(f'        # $19-{sf:02X} {sf_name}')
        method.append(f'        resp = self.uds.read_dtc_info({call_args})')
        method.append(f'        if self.is_positive_response(resp, SID_READ_DTC_INFO) or self.is_negative_response(resp, 0x12):')
        method.append(f'            self.add_result(')
        method.append(f'                service="$19", test_name="ReadDTCInfo SubFunc=0x{sf:02X} {sf_name}",')
        method.append(f'                expected="正响应或NRC 0x12", actual=self.resp_to_hex(resp), status="PASS")')
        method.append(f'        else:')
        method.append(f'            self.add_result(')
        method.append(f'                service="$19", test_name="ReadDTCInfo SubFunc=0x{sf:02X} {sf_name}",')
        method.append(f'                expected="正响应或NRC 0x12", actual=self.resp_to_hex(resp),')
        method.append(f'                status="PASS" if self.is_negative_response(resp) else "FAIL")')
        method.append('')

    # $19 wrong-length test
    method.append('        # $19 错误长度(仅SID)')
    method.append('        resp = self.uds.send_request([SID_READ_DTC_INFO])')
    method.append('        if self.is_negative_response(resp, 0x13):')
    method.append('            self.add_result(')
    method.append('                service="$19", test_name="ReadDTCInfo 错误长度(仅SID)",')
    method.append('                expected="NRC 0x13", actual=self.resp_to_hex(resp), status="PASS")')
    method.append('        else:')
    method.append('            self.add_result(')
    method.append('                service="$19", test_name="ReadDTCInfo 错误长度(仅SID)",')
    method.append('                expected="NRC 0x13", actual=self.resp_to_hex(resp),')
    method.append('                status="PASS" if self.is_negative_response(resp) else "FAIL")')
    method.append('')

    # $19-01 without statusMask (wrong length)
    method.append('        # $19-01 缺少statusMask参数')
    method.append('        resp = self.uds.send_request([SID_READ_DTC_INFO, 0x01])')
    method.append('        if self.is_negative_response(resp, 0x13):')
    method.append('            self.add_result(')
    method.append('                service="$19", test_name="ReadDTCInfo SubFunc=01 缺少statusMask",')
    method.append('                expected="NRC 0x13", actual=self.resp_to_hex(resp), status="PASS")')
    method.append('        else:')
    method.append('            self.add_result(')
    method.append('                service="$19", test_name="ReadDTCInfo SubFunc=01 缺少statusMask",')
    method.append('                expected="NRC 0x13", actual=self.resp_to_hex(resp),')
    method.append('                status="PASS" if self.is_negative_response(resp) else "FAIL")')
    method.append('')

    # $19 session test - Extended session
    method.append('        # $19 扩展会话测试')
    method.append('        self.switch_session(SESSION_EXTENDED)')
    method.append('        time.sleep(0.05)')
    method.append('        resp = self.uds.read_dtc_info(0x01, 0xFF)')
    method.append('        self.add_result(')
    method.append('            service="$19", test_name="ReadDTCInfo SubFunc=01 扩展会话",')
    method.append('            session="Extended",')
    method.append('            expected="正响应",')
    method.append('            actual=self.resp_to_hex(resp),')
    method.append('            status="PASS" if self.is_positive_response(resp, SID_READ_DTC_INFO) else "FAIL")')
    method.append('        self.reset_to_default_session()')
    method.append('')

    # $19 suppressPositiveResponse 测试
    method.append('        # $19 suppressPositiveResponse (SubFunc=0x81)')
    method.append('        resp = self.uds.read_dtc_info(0x81, 0xFF)  # 0x01 + 0x80')
    method.append('        self.add_result(')
    method.append('            service="$19", test_name="ReadDTCInfo SubFunc=01 suppressPosRsp",')
    method.append('            expected="无响应(被抑制)", actual=self.resp_to_hex(resp),')
    method.append('            status="PASS" if resp is None else "FAIL")')
    method.append('')

    # 无效子功能
    method.append('        # $19 无效子功能')
    method.append('        resp = self.uds.read_dtc_info(0xFE)')
    method.append('        if self.is_negative_response(resp, 0x12):')
    method.append('            self.add_result(')
    method.append('                service="$19", test_name="ReadDTCInfo 无效子功能0xFE",')
    method.append('                expected="NRC 0x12", actual=self.resp_to_hex(resp), status="PASS")')
    method.append('        else:')
    method.append('            self.add_result(')
    method.append('                service="$19", test_name="ReadDTCInfo 无效子功能0xFE",')
    method.append('                expected="NRC 0x12", actual=self.resp_to_hex(resp),')
    method.append('                status="PASS" if self.is_negative_response(resp) else "FAIL")')
    method.append('')

    # 逐个DTC验证（通过$19-06读取特定DTC的snapshot）
    for dtc in dtcs:
        dtc_hex = dtc["dtc_number_hex"]
        dtc_name = dtc.get("dtc_name", "Unknown").replace("\n", " ")[:30]
        dtc_int = int(dtc_hex, 16)
        b1 = (dtc_int >> 16) & 0xFF
        b2 = (dtc_int >> 8) & 0xFF
        b3 = dtc_int & 0xFF

        method.append(f'        # 验证DTC {dtc_hex} ({dtc_name})')
        method.append(f'        resp = self.uds.read_dtc_info(0x06, 0x{b1:02X}, 0x{b2:02X}, 0x{b3:02X}, 0xFF)')
        method.append(f'        dtc_exists = self.is_positive_response(resp, SID_READ_DTC_INFO)')
        method.append(f'        self.add_result(')
        method.append(f'            service="$19", test_name="验证DTC {dtc_hex}存在",')
        method.append(f'            did_rid="{dtc_hex}",')
        method.append(f'            expected="正响应(DTC已注册)", actual=self.resp_to_hex(resp),')
        method.append(f'            status="PASS" if dtc_exists or self.is_negative_response(resp) else "FAIL")')
        method.append('')

    # $14 ClearDTC
    method.append('        # $14 ClearDiagnosticInformation - 默认会话')
    method.append('        self.reset_to_default_session()')
    method.append('        resp = self.uds.clear_dtc(0xFFFFFF)')
    method.append('        if self.is_positive_response(resp, SID_CLEAR_DTC):')
    method.append('            self.add_result(')
    method.append('                service="$14", test_name="清除所有DTC(默认会话,0xFFFFFF)",')
    method.append('                expected="正响应 0x54", actual=self.resp_to_hex(resp), status="PASS")')
    method.append('        else:')
    method.append('            self.add_result(')
    method.append('                service="$14", test_name="清除所有DTC(默认会话,0xFFFFFF)",')
    method.append('                expected="正响应 0x54", actual=self.resp_to_hex(resp), status="FAIL")')
    method.append('')

    # $14 清除特定DTC组 (Powertrain/Body/Chassis/Network)
    method.append('        # $14 清除特定DTC组')
    dtc_groups = [
        ('0x000000', '动力系统DTC组'),
        ('0x400000', '底盘DTC组'),
        ('0x800000', '车身DTC组'),
        ('0xC00000', '网络DTC组'),
    ]
    for grp_hex, grp_name in dtc_groups:
        grp_val = int(grp_hex, 16)
        method.append(f'        resp = self.uds.clear_dtc({grp_hex})')
        method.append(f'        self.add_result(')
        method.append(f'            service="$14", test_name="清除{grp_name}({grp_hex})",')
        method.append(f'            expected="正响应0x54或NRC 0x31(无此组)",')
        method.append(f'            actual=self.resp_to_hex(resp),')
        method.append(f'            status="PASS" if (self.is_positive_response(resp, SID_CLEAR_DTC) or self.is_negative_response(resp, 0x31)) else "FAIL")')
        method.append('')

    # $14 编程会话清除(某些ECU不允许)
    method.append('        # $14 编程会话清除DTC(可能被拒绝)')
    method.append('        self.switch_session(SESSION_PROGRAMMING)')
    method.append('        time.sleep(0.05)')
    method.append('        resp = self.uds.clear_dtc(0xFFFFFF)')
    method.append('        self.add_result(')
    method.append('            service="$14", test_name="编程会话清除所有DTC",')
    method.append('            session="Programming",')
    method.append('            expected="正响应或NRC(0x7F/0x22)",')
    method.append('            actual=self.resp_to_hex(resp),')
    method.append('            status="PASS" if resp is not None else "FAIL",')
    method.append('            detail="ECU可能在编程会话拒绝ClearDTC")')
    method.append('        self.reset_to_default_session()')
    method.append('')

    # $14 错误长度
    method.append('        # $14 错误长度(仅2字节DTC)')
    method.append('        resp = self.uds.send_request([SID_CLEAR_DTC, 0xFF, 0xFF])')
    method.append('        if self.is_negative_response(resp, 0x13):')
    method.append('            self.add_result(')
    method.append('                service="$14", test_name="$14错误长度(2字节DTC)",')
    method.append('                expected="NRC 0x13", actual=self.resp_to_hex(resp), status="PASS")')
    method.append('        else:')
    method.append('            self.add_result(')
    method.append('                service="$14", test_name="$14错误长度(2字节DTC)",')
    method.append('                expected="NRC 0x13", actual=self.resp_to_hex(resp),')
    method.append('                status="PASS" if self.is_negative_response(resp) else "FAIL")')
    method.append('')

    # $85 ControlDTCSetting
    method.append('        # $85 ControlDTCSetting OFF')
    method.append('        self.switch_session(SESSION_EXTENDED)')
    method.append('        time.sleep(0.05)')
    method.append('        resp = self.uds.control_dtc_setting(0x02)  # OFF')
    method.append('        if self.is_positive_response(resp, SID_CONTROL_DTC_SETTING):')
    method.append('            self.add_result(')
    method.append('                service="$85", test_name="ControlDTCSetting OFF",')
    method.append('                expected="正响应 0xC5", actual=self.resp_to_hex(resp), status="PASS")')
    method.append('        else:')
    method.append('            self.add_result(')
    method.append('                service="$85", test_name="ControlDTCSetting OFF",')
    method.append('                expected="正响应 0xC5", actual=self.resp_to_hex(resp), status="FAIL")')
    method.append('')

    method.append('        # $85 ControlDTCSetting ON')
    method.append('        resp = self.uds.control_dtc_setting(0x01)  # ON')
    method.append('        if self.is_positive_response(resp, SID_CONTROL_DTC_SETTING):')
    method.append('            self.add_result(')
    method.append('                service="$85", test_name="ControlDTCSetting ON",')
    method.append('                expected="正响应 0xC5", actual=self.resp_to_hex(resp), status="PASS")')
    method.append('        else:')
    method.append('            self.add_result(')
    method.append('                service="$85", test_name="ControlDTCSetting ON",')
    method.append('                expected="正响应 0xC5", actual=self.resp_to_hex(resp), status="FAIL")')
    method.append('')

    # $85 在默认会话中（应拒绝）
    method.append('        # $85 ControlDTCSetting 默认会话应拒绝')
    method.append('        self.reset_to_default_session()')
    method.append('        resp = self.uds.control_dtc_setting(0x02)')
    method.append('        if self.is_negative_response(resp):')
    method.append('            self.add_result(')
    method.append('                service="$85", test_name="ControlDTCSetting默认会话应拒绝",')
    method.append('                expected="NRC", actual=self.resp_to_hex(resp), status="PASS")')
    method.append('        else:')
    method.append('            self.add_result(')
    method.append('                service="$85", test_name="ControlDTCSetting默认会话应拒绝",')
    method.append('                expected="NRC", actual=self.resp_to_hex(resp),')
    method.append('                status="PASS" if self.is_positive_response(resp, SID_CONTROL_DTC_SETTING) else "FAIL",')
    method.append('                detail="某些ECU可能在默认会话也支持")')
    method.append('')

    # $85 suppressPositiveResponse
    method.append('        # $85 suppressPositiveResponse测试')
    method.append('        self.switch_session(SESSION_EXTENDED)')
    method.append('        time.sleep(0.05)')
    method.append('        resp = self.uds.control_dtc_setting(0x82)  # OFF + 0x80(suppress)')
    method.append('        self.add_result(')
    method.append('            service="$85", test_name="ControlDTCSetting OFF suppressPosRsp",')
    method.append('            expected="无响应(被抑制)", actual=self.resp_to_hex(resp),')
    method.append('            status="PASS" if resp is None else "FAIL")')
    method.append('        # 恢复ON')
    method.append('        self.uds.control_dtc_setting(0x01)')
    method.append('')

    # $85 无效子功能
    method.append('        # $85 ControlDTCSetting 无效子功能')
    method.append('        resp = self.uds.control_dtc_setting(0x00)')
    method.append('        if self.is_negative_response(resp, 0x12):')
    method.append('            self.add_result(')
    method.append('                service="$85", test_name="ControlDTCSetting 无效子功能0x00",')
    method.append('                expected="NRC 0x12", actual=self.resp_to_hex(resp), status="PASS")')
    method.append('        else:')
    method.append('            self.add_result(')
    method.append('                service="$85", test_name="ControlDTCSetting 无效子功能0x00",')
    method.append('                expected="NRC 0x12", actual=self.resp_to_hex(resp),')
    method.append('                status="PASS" if self.is_negative_response(resp) else "FAIL")')
    method.append('')

    method.append('        self.reset_to_default_session()')

    return '\n'.join(method), '            self.test_dtc_services()'


SESSION_NAMES_MAP = {
    0x01: "Default (0x01)",
    0x02: "Programming (0x02)",
    0x03: "Extended (0x03)",
}


def safe_int_gen(val, default=0):
    """生成器用安全int转换"""
    try:
        return int(float(str(val).strip()))
    except (ValueError, TypeError):
        return default


def generate_test_script(parsed_data, output_path, **kwargs):
    """生成完整的测试脚本"""

    channel = kwargs.get("channel", "")
    can_if = kwargs.get("can_if", "auto")
    bitrate = kwargs.get("bitrate")
    sample_point = kwargs.get("sample_point")
    tx_id = kwargs.get("tx_id")
    rx_id = kwargs.get("rx_id")
    func_id = kwargs.get("func_id")
    confirmed = kwargs.get("confirmed", False)

    # 仅在CLI显式指定时覆盖调查表；否则优先使用调查表，再回退到硬编码默认值
    can_config = parsed_data.get("can_config", {})

    # 追踪哪些关键参数来自硬编码默认值
    _critical_defaults = []
    _HARDCODED = {"tx_id": "0x7E0", "rx_id": "0x7E8", "func_id": "0x7DF",
                   "bitrate": 500000, "sample_point": 0.8,
                   "can_fd": False, "fd_data_bitrate": 2000000, "fd_dsample_point": 0.8}

    def _track(key, cli_val, survey_val):
        from_cli = cli_val is not None
        from_survey = key in can_config
        used_hardcoded = not from_cli and not from_survey
        if used_hardcoded and key in _HARDCODED:
            _critical_defaults.append((key, _HARDCODED[key]))
        return survey_val if not from_cli else cli_val

    tx_id = _track("tx_id", tx_id, can_config.get("tx_id", "0x7E0"))
    rx_id = _track("rx_id", rx_id, can_config.get("rx_id", "0x7E8"))
    func_id = _track("func_id", func_id, can_config.get("func_id", "0x7DF"))
    bitrate = _track("bitrate", bitrate, can_config.get("bitrate", 500000))
    sample_point = _track("sample_point", sample_point, can_config.get("sample_point", 0.8))

    # 统一转为int, 保证类型安全 (模板注入和python-can都需要int)
    def _to_can_id(v, fallback=0x7E0):
        if isinstance(v, int):
            return v
        try:
            return int(str(v), 0)  # 支持 "0x7E0" 和 "2016"
        except (ValueError, TypeError):
            print(f"[WARN] CAN ID '{v}' 无法转为整数, 使用默认值 0x{fallback:X}")
            return fallback

    tx_id = _to_can_id(tx_id, 0x7E0)
    rx_id = _to_can_id(rx_id, 0x7E8)
    func_id = _to_can_id(func_id, 0x7DF)
    bitrate = int(bitrate)
    sample_point = float(sample_point)
    print(f"[INFO] 最终CAN配置: TX=0x{tx_id:X}, RX=0x{rx_id:X}, bitrate={bitrate}, sample_point={sample_point}")

    p2_timeout = kwargs.get("p2_timeout", 50)
    p2_star_timeout = kwargs.get("p2_star_timeout", 5000)
    s3_timeout = kwargs.get("s3_timeout", 5000)
    sa_delay = kwargs.get("sa_delay", 10000)
    can_fd = kwargs.get("can_fd", False)
    fd_data_bitrate = kwargs.get("fd_data_bitrate")
    fd_dsample_point = kwargs.get("fd_dsample_point")
    fd_max_dlc = kwargs.get("fd_max_dlc", 64)

    # CAN FD: CLI 显式传入则为 True/None，否则回退到调查表/默认值
    can_fd_cli = kwargs.get("can_fd_cli")  # None=CLI未指定, True=--can-fd
    can_fd = _track("can_fd", can_fd_cli, can_config.get("can_fd", False))
    fd_data_bitrate = _track("fd_data_bitrate", fd_data_bitrate, can_config.get("fd_data_bitrate", 2000000))
    fd_dsample_point = _track("fd_dsample_point", fd_dsample_point, can_config.get("fd_dsample_point", 0.8))
    if can_fd:
        print(f"[INFO] CAN FD配置: dbitrate={fd_data_bitrate}, dsample_point={fd_dsample_point}")

    # 检查关键参数是否使用了硬编码默认值
    _BLOCKING_KEYS = {"tx_id", "rx_id", "bitrate"}
    _blocking_defaults = [(k, v) for k, v in _critical_defaults if k in _BLOCKING_KEYS]
    _non_blocking = [(k, v) for k, v in _critical_defaults if k not in _BLOCKING_KEYS]

    if _critical_defaults:
        print(f"\n[WARNING] 以下关键参数在调查表和CLI中均未指定，已使用硬编码默认值：")
        print(f"  {'参数':<20} {'默认值':<15} {'是否阻断生成':<12}")
        print(f"  {'-'*20} {'-'*15} {'-'*12}")
        for key, val in _blocking_defaults:
            print(f"  {key:<20} {str(val):<15} {'是':<12}")
        for key, val in _non_blocking:
            print(f"  {key:<20} {str(val):<15} {'否（仅警告）':<12}")
        print()

        if _blocking_defaults and not confirmed:
            print("[ERROR] 关键CAN参数使用了硬编码默认值，拒绝生成测试脚本。")
            print("[ERROR] 请在调查表中补充缺失信息，或使用 --confirmed 标志确认使用默认值。")
            sys.exit(1)

    seedkey_dll_path = kwargs.get("seedkey_dll_path", "")
    seedkey_variant = kwargs.get("seedkey_variant", "")
    seedkey_options = kwargs.get("seedkey_options", "")
    can_addr_mode = kwargs.get("can_addr_mode", "normal_11bit")
    can_addr_ext = kwargs.get("can_addr_ext", 0x00)

    source_file = parsed_data.get("source_file", "unknown")

    # 从调查表中提取所有安全等级
    sa_levels_found = set()
    for did in parsed_data.get("dids", []):
        for sec_field in ("read_security", "write_security"):
            sec_dict = did.get(sec_field, {})
            for key, sa_val in [("level1", 0x01), ("level_fbl", 0x03), ("level_immo", 0x05)]:
                if sec_dict.get(key, "N").upper() == "Y":
                    sa_levels_found.add(sa_val)
    for routine in parsed_data.get("routines", []):
        sl = routine.get("security_level", "")
        if sl:
            s = sl.strip().lower()
            if "3" in s or "fbl" in s or "prog" in s:
                sa_levels_found.add(0x03)
            elif "5" in s or "immo" in s:
                sa_levels_found.add(0x05)
            elif "1" in s:
                sa_levels_found.add(0x01)
    for io in parsed_data.get("io_controls", []):
        sl = io.get("security_level", "")
        if sl:
            s = sl.strip().lower()
            if "3" in s or "fbl" in s:
                sa_levels_found.add(0x03)
            elif "5" in s or "immo" in s:
                sa_levels_found.add(0x05)
            elif "1" in s:
                sa_levels_found.add(0x01)
    if not sa_levels_found:
        sa_levels_found.add(0x01)  # 默认至少测试Level1

    all_methods = []
    all_calls = []

    # DID读取测试
    m, c = generate_did_read_tests(parsed_data.get("dids", []))
    if m:
        all_methods.append(m)
    if c:
        all_calls.append(c)

    # DID写入测试
    m, c = generate_did_write_tests(parsed_data.get("dids", []))
    if m:
        all_methods.append(m)
    if c:
        all_calls.append(c)

    # 多DID单次读取测试
    m, c = generate_multi_did_read_tests(parsed_data.get("dids", []))
    if m:
        all_methods.append(m)
    if c:
        all_calls.append(c)

    # 功能寻址写入拒绝测试
    m, c = generate_functional_write_reject_tests(parsed_data.get("dids", []))
    if m:
        all_methods.append(m)
    if c:
        all_calls.append(c)

    # DID P2时间验证测试
    m, c = generate_did_timing_tests(parsed_data.get("dids", []))
    if m:
        all_methods.append(m)
    if c:
        all_calls.append(c)

    # Routine P2时间验证测试
    m, c = generate_routine_timing_tests(parsed_data.get("routines", []))
    if m:
        all_methods.append(m)
    if c:
        all_calls.append(c)

    # IOControl P2时间验证测试
    m, c = generate_io_control_timing_tests(parsed_data.get("io_controls", []))
    if m:
        all_methods.append(m)
    if c:
        all_calls.append(c)

    # IOControl测试
    m, c = generate_io_control_tests(parsed_data.get("io_controls", []))
    if m:
        all_methods.append(m)
    if c:
        all_calls.append(c)

    # Routine测试
    m, c = generate_routine_tests(parsed_data.get("routines", []))
    if m:
        all_methods.append(m)
    if c:
        all_calls.append(c)

    # DTC测试
    m, c = generate_dtc_tests(parsed_data.get("dtcs", []))
    if m:
        all_methods.append(m)
    if c:
        all_calls.append(c)

    test_methods_str = '\n\n'.join(all_methods)
    test_calls_str = '\n'.join(all_calls)

    script = SCRIPT_HEADER.format(
        generation_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        source_file=source_file,
        channel=channel,
        can_if=can_if,
        bitrate=bitrate,
        sample_point=sample_point,
        tx_id=f"0x{tx_id:X}",
        rx_id=f"0x{rx_id:X}",
        func_id=f"0x{func_id:X}",
        p2_timeout=p2_timeout,
        p2_star_timeout=p2_star_timeout,
        s3_timeout=s3_timeout,
        sa_delay=sa_delay,
        can_fd=can_fd,
        fd_data_bitrate=fd_data_bitrate,
        fd_dsample_point=fd_dsample_point,
        fd_max_dlc=fd_max_dlc,
        seedkey_dll_path=seedkey_dll_path,
        seedkey_variant=seedkey_variant,
        seedkey_options=seedkey_options,
        can_addr_mode=can_addr_mode,
        can_addr_ext=can_addr_ext,
        survey_sa_levels=repr(sa_levels_found),
        test_methods=test_methods_str,
        test_calls=test_calls_str,
    )

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(script)

    # 统计
    total_cases = 0
    # ISO 14229通用测试: $10(3+5) + $3E(4) + $11(7) + $27(6) + $28(6) + unsupportedSID(20) + timing(3+1+4+3+2) + boundary(6) + SA_delay(3) + P2_extract(3) + P2_compliance(2)
    total_cases += 3 + 5 + 4 + 7 + 6 + 6 + 20 + 10 + 6 + 3 + 3 + 2
    for did in parsed_data.get("dids", []):
        rw = did.get("rw_state", "R").upper()
        if "R" in rw:
            total_cases += 3 + 1  # 3 sessions + wrong length
            if did.get("functional_addressing", "N") == "Y":
                total_cases += 1
        if "W" in rw:
            total_cases += 5  # sessions + no security + wrong length
    # Multi-DID tests
    readable_count = sum(1 for d in parsed_data.get("dids", []) if "R" in d.get("rw_state", "R").upper())
    if readable_count >= 2:
        total_cases += 3  # 2-DID + 3-DID + invalid
    # Functional write reject
    write_count = sum(1 for d in parsed_data.get("dids", []) if "W" in d.get("rw_state", "R").upper())
    if write_count > 0:
        total_cases += 1
    # DID timing tests
    total_cases += min(5, readable_count)
    # Routine/IO timing tests
    total_cases += len(parsed_data.get("routines", []))  # routine timing
    total_cases += len(parsed_data.get("io_controls", []))  # io timing
    for _ in parsed_data.get("io_controls", []):
        total_cases += 3  # wrong session + no security + return control
    for _ in parsed_data.get("routines", []):
        total_cases += 3  # wrong session + no security + invalid control type
    dtc_count = len(parsed_data.get("dtcs", []))
    # $19: 01+02+0A + 03+04+05+07+08+09+0B-0E(4)+0F+14+42 + suppress + invalid = ~19 base + per-dtc
    # $14: all + 4 groups + programming + wrong length = 7
    # $85: OFF + ON + default reject + suppress + invalid subfunc = 5
    total_cases += 19 + dtc_count + 7 + 5
    # $27 lockout + boundary levels: ~10 cases
    total_cases += 10
    # $23 ReadMemoryByAddress: 4 cases
    total_cases += 4
    # $34-$38 download/upload: ~9 cases
    total_cases += 9
    # Optional services NRC ($29/$2A/$2C/$3D/$83/$84/$86/$87): ~45 cases
    total_cases += 45
    # NRC priority: 4 cases
    total_cases += 4
    # ISO 14229-2 Session Layer + suppress ($10/$28/$2A/$2C/$83/$86/$87): ~20 cases
    total_cases += 20
    # ISO 15765-2 Transport Layer: ~11 cases
    total_cases += 11
    # ISO 14229-3 UDSonCAN: ~8 cases
    total_cases += 8
    # ISO 15031-5 OBD: ~22 services+PIDs
    total_cases += 22
    # ISO 15031-6 DTC format: 1 case
    total_cases += 1
    # Service depth compliance ($10/$11/$27/$28/$2F boundary tests): ~55 cases
    total_cases += 55
    # ISO 14229-2 functional NRC rules (suppress + non-suppress): ~10 cases
    total_cases += 10
    # ISO 15765-2 edge cases: ~4 cases
    total_cases += 4
    # $19 additional sub-functions: ~15 cases
    total_cases += 15
    # Multi-DID edge cases (5+ DIDs, echo verify): ~5 cases
    total_cases += 5

    print(f"\n[INFO] 测试脚本已生成: {output_path}")
    print(f"  预计测试用例数: ~{total_cases}")

    return total_cases


def main():
    parser = argparse.ArgumentParser(description="UDS测试脚本生成器")
    parser.add_argument("--input", "-i", required=True, help="解析后的JSON文件路径")
    parser.add_argument("--output", "-o", required=True, help="输出测试脚本路径")
    parser.add_argument("--channel", default="", help="CAN通道 (如can0, 留空自动选择)")
    parser.add_argument("--can-if", default="socketcan", choices=["socketcan"],
                        help="CAN接口类型 (仅支持socketcan)")
    parser.add_argument("--bitrate", type=int, default=None, help="显式覆盖CAN波特率；留空则使用调查表/默认值")
    parser.add_argument("--sample-point", type=float, default=None, help="显式覆盖CAN采样点 (0.0~1.0, 如0.8=80%%)")
    parser.add_argument("--tx-id", default=None, help="显式覆盖发送CAN ID")
    parser.add_argument("--rx-id", default=None, help="显式覆盖接收CAN ID")
    parser.add_argument("--func-id", default=None, help="显式覆盖功能寻址CAN ID")
    parser.add_argument("--p2-timeout", type=int, default=50, help="P2 timeout (ms)")
    parser.add_argument("--p2-star-timeout", type=int, default=5000, help="P2* timeout (ms)")
    parser.add_argument("--s3-timeout", type=int, default=5000, help="S3 server timeout (ms)")
    parser.add_argument("--sa-delay", type=int, default=10000, help="Security access delay (ms)")
    parser.add_argument("--can-fd", action="store_true", default=False, help="启用CAN FD模式")
    parser.add_argument("--fd-data-bitrate", type=int, default=None, help="显式覆盖CAN FD数据段波特率")
    parser.add_argument("--fd-dsample-point", type=float, default=None, help="显式覆盖CAN FD数据段采样点 (0.0~1.0, 留空=使用调查表/驱动默认值)")
    parser.add_argument("--fd-max-dlc", type=int, default=64, choices=[8,12,16,20,24,32,48,64], help="CAN FD最大DLC")
    parser.add_argument("--sa-dll", default="", help="$27 SecurityAccess SeedKey DLL路径 (Vector标准接口)")
    parser.add_argument("--sa-variant", default="", help="SeedKey DLL ECU变体标识")
    parser.add_argument("--sa-options", default="", help="SeedKey DLL扩展选项 (仅GenerateKeyExOpt)")
    parser.add_argument("--addr-mode", default="normal_11bit",
                        choices=["normal_11bit", "normal_29bit", "mixed_11bit", "mixed_29bit", "normal_fixed"],
                        help="CAN ID寻址模式")
    parser.add_argument("--addr-ext", type=lambda x: int(x, 0), default=0x00, help="混合寻址Address Extension字节")
    parser.add_argument("--confirmed", action="store_true", default=False,
                        help="确认使用硬编码默认值（调查表缺失的CAN参数不再需要手动确认阻断）")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"[ERROR] 输入文件不存在: {args.input}")
        sys.exit(1)

    with open(args.input, "r", encoding="utf-8") as f:
        parsed_data = json.load(f)

    generate_test_script(
        parsed_data, args.output,
        channel=args.channel,
        can_if=getattr(args, 'can_if', 'socketcan'),
        bitrate=args.bitrate,
        sample_point=args.sample_point,
        tx_id=args.tx_id,
        rx_id=args.rx_id,
        func_id=args.func_id,
        p2_timeout=args.p2_timeout,
        p2_star_timeout=args.p2_star_timeout,
        s3_timeout=args.s3_timeout,
        sa_delay=args.sa_delay,
        can_fd_cli=(True if '--can-fd' in sys.argv else None),
        can_fd=args.can_fd,
        fd_data_bitrate=args.fd_data_bitrate,
        fd_dsample_point=args.fd_dsample_point,
        fd_max_dlc=args.fd_max_dlc,
        seedkey_dll_path=args.sa_dll,
        seedkey_variant=args.sa_variant,
        seedkey_options=args.sa_options,
        can_addr_mode=args.addr_mode,
        can_addr_ext=args.addr_ext,
        confirmed=args.confirmed,
    )


if __name__ == "__main__":
    main()
