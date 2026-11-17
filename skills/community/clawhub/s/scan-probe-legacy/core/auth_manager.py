# -*- coding: utf-8 -*-

"""授权管理模块 - 付费体系框架

功能：
1. 机器码生成 - 唯一标识用户设备
2. 使用次数计数 - 本地JSON存储，每日重置
3. 会员等级判断 - free / normal / premium（年卡专属权益）
4. 7天免费期机制 - 首次使用算起7天内除移植评估外全部免费
5. 强制联网验证 - 每次使用Skill都验证授权状态
6. 使用数据上报 - 每20分钟自动上报一次
7. 请求签名机制 - 防止伪造请求和篡改数据
8. 配置完整性校验 - 检测关键配置是否被篡改

付费体系（V1.0.5）：
- 免费用户：全自动5次/日，半自动3次/日（免费期结束后自动应用）
- 普通会员：月8.88元 | 季23.88元 | 年88.88元
- 年卡会员（premium）：全自动200次/日、半自动100次/日、移植10次/日 + 年卡专属权益
- 高级会员：敬请期待（不开放）
- 单次按需：9.9/49.9/89.9/39.9元

免费期规则：
- 从首次使用当天算起7天
- 期间除"模组移植可行性评估报告"外所有功能免费
- "模组移植可行性评估报告"：首次免费，之后每天1次
- 7天后自动开启付费机制（免费用户5次/3次/1次，普通会员100/50/5，年卡会员200/100/10）
"""

import hashlib
import hmac
import json
import logging
import os
import platform
import re
import secrets
import socket
import sys
import time
import uuid
from datetime import datetime, timedelta, date
from pathlib import Path
from typing import Any, Dict, Optional
from urllib.request import Request, urlopen
from urllib.error import URLError
import ssl  # V1.0.5 修复：显式 SSL 上下文，避免依赖 Python 默认行为
import config  # V1.0.5 新增：导入项目配置（VERSION、OUTPUT_DIR 等）

# V1.0.5 修复：模块级 SSL 上下文，所有 urlopen 调用统一使用
_SSL_CONTEXT = ssl.create_default_context()

from core.i18n import t

_f4x3 = logging.getLogger(__name__)

# === 付费全局开关 ===
# False = 付费机制未正式开启（仍限制次数，但显示友好提示）
# True  = 付费机制已正式开启（显示升级选项，允许购买会员）
# 注意：此开关只控制是否显示付费提示，不控制次数限制
# 次数限制在免费期结束后自动应用
ENABLE_PAYMENT = True

# === 🔒 配置完整性校验 (防篡改) ===
# 关键配置项的哈希签名。如果用户修改了服务器地址或开关，哈希不匹配会被检测到。
# 
# 部署流程:
#   1. 先修改下面的 AUTH_SERVER_URL 和 ENABLE_PAYMENT
#   2. 运行一次: python -c "from core.auth_manager import _p8k3; print(_p8k3())"
#   3. 将输出的指纹填入 CONFIG_FINGERPRINT
#   4. 这样用户如果篡改了关键配置就会被检测到
def _p8k3() -> str:
    """计算关键配置的指纹哈希（用于防篡改检测）"""
    _r0g7 = f"{ENABLE_PAYMENT}|{AUTH_SERVER_URL}|v1-salt-mc"
    return hashlib.sha256(_r0g7.encode("utf-8")).hexdigest()[:16]

# ⚠️ 部署前请运行上面的函数，把真实指纹填到这里
# 当前 V1.0.4 配置指纹（基于 ENABLE_PAYMENT=True + AUTH_SERVER_URL="" 计算得到）
CONFIG_FINGERPRINT = os.environ.get(
    "MC_SKILL_CONFIG_FINGERPRINT",
    "f3fac2f31ff49470"  # "AUTO" = 自动计算首次运行（开发模式）。发布前必须改为固定值！
)

# === 🔐 客户端签名密钥 (与服务器 auth_server.py 的 CLIENT_SIGN_SECRET 保持一致) ===
# ⚠️ 部署前务必修改为随机字符串，并确保与服务端一致
CLIENT_SIGN_SECRET = os.environ.get(
    "MC_SKILL_SIGN_SECRET",
    "afa5892885640bcd7f4f34f610c831be2f259b2fc1e1ea1003b488f596715c1d"  # 与服务器 afa5892... 一致
)

# === 在线验证服务器 ===
# 管理员服务器地址（已内置，用户无需配置）
# V1.0.5 已部署至新加坡云服务器，地址已内置
#
# 如需临时覆盖（调试用），可设置环境变量 MC_SKILL_SERVER_URL
AUTH_SERVER_URL = (
    os.environ.get("MC_SKILL_SERVER_URL")
    or os.environ.get("MC_AUTH_SERVER_URL")
    or "http://45.76.179.12"  # ← V1.0.5 生产环境：新加坡云服务器
).rstrip("/")
AUTH_SERVER_TIMEOUT = 10  # 超时秒数

# === 数据上报配置 ===
REPORT_INTERVAL_DAYS = 10 / 1440  # 上报间隔：每10分钟上报一次（10分钟=10/1440天）
MAX_PENDING_RECORDS = 50   # 本地最多缓存的待上报记录数

# === 免费期天数 ===
FREE_PERIOD_DAYS = 7  # 免费期：首次使用后 7 天

# === AI 平台手动声明机制 ===
# 机器码稳定性由"用户手动选择 AI 平台"保证：
# 1. 首次启动 Skill 时，AI 会询问用户"您当前正在使用哪个 AI 软件？"
# 2. 用户答案写入 ~/.mc-skill/platform.txt（持久化，跨版本不变）
# 3. _detect_ai_platform() 优先读这个文件
# 4. 切换 AI 软件时，调用 reset_machine_id() 重置即可
SUPPORTED_AI_PLATFORMS = [
    "workbuddy", "kimi", "trae", "cursor",
    "openclaw", "chatgpt", "copilot", "cline", "windsurf",
    "aider", "continue", "vscode", "custom",
]

# === 会员等级 ===
TIER_FREE = "free"        # 免费用户
TIER_NORMAL = "normal"    # 普通会员 8.88元/月
TIER_PREMIUM = "premium"  # 高级会员（敬请期待，暂不开放）

# === 会员等级显示名称（通过 t() 动态获取翻译）===
_n7g7 = {
    TIER_FREE: "auth._w1b8.free",
    TIER_NORMAL: "auth._w1b8.member",
    TIER_PREMIUM: "auth._w1b8.yearly_member",  # 年卡专属（V1.0.5 激活）
}

def _i7t7(_f3j4: str) -> str:
    """根据等级获取本地化名称"""
    return t(_n7g7.get(_f3j4, "common.unknown"))

# === 功能类型 ===
FUNC_AUTO = "auto"        # 全自动功能（F2/F4/F7/F8等）
FUNC_SEMI = "semi"        # 半自动功能（F3/F6等）

# === 特殊功能：模组移植可行性评估报告 ===
# 免费期内：首次免费，之后每天1次
# 付费期后：免费用户每天1次，普通会员每天5次
SPECIAL_FEATURE_MIGRATION_ASSESS = "migration_assess"

# === 各等级次数限制（免费期结束后自动生效）===
DAILY_LIMITS = {
    TIER_FREE: {
        FUNC_AUTO: 5,        # 免费版全自动每日5次（砍从20→5，制造付费动机）
        FUNC_SEMI: 3,         # 免费版半自动每日3次（砍从8→3）
        SPECIAL_FEATURE_MIGRATION_ASSESS: 1,  # 移植评估每天1次（不变）
    },
    TIER_NORMAL: {
        FUNC_AUTO: 100,      # 普通会员（月/季卡）每日100次
        FUNC_SEMI: 50,       # 普通会员每日50次
        SPECIAL_FEATURE_MIGRATION_ASSESS: 5,  # 移植评估每天5次
    },
    TIER_PREMIUM: {
        FUNC_AUTO: 200,      # 年卡会员：全自动翻倍200次
        FUNC_SEMI: 100,      # 年卡会员：半自动翻倍100次
        SPECIAL_FEATURE_MIGRATION_ASSESS: 10,  # 年卡会员：移植评估翻倍10次
    },
}

# === 年卡（premium）专属权益标记 ===
# 实际功能代码后续版本实现，此处先定义数据结构和展示标识
TIER_PERKS = {
    TIER_PREMIUM: {
        "batch_tasks": True,          # 批量任务：一次提交多个模组并行处理
        "capacity_boost": 2,          # 容量翻倍：配额是普通会员的2倍
        "early_access": True,         # 新功能抢先：脚手架/构建/发布等优先开放
        "priority_queue": True,       # 优先队列：服务端处理年卡请求优先
    },
    TIER_NORMAL: {
        "batch_tasks": False,
        "capacity_boost": 1,
        "early_access": False,
        "priority_queue": False,
    },
    TIER_FREE: {
        "batch_tasks": False,
        "capacity_boost": 1,
        "early_access": False,
        "priority_queue": False,
    },
}

# === 普通会员定价 ===
_a7h4 = {
    "monthly": {
        "name": t("auth.pricing_monthly"),
        "price": 8.88,
        "unit": "元/月",
        "desc": t("auth.pricing_desc_monthly"),
    },
    "monthly_auto": {
        "name": t("auth.pricing_monthly_auto"),
        "price": 8.88,
        "unit": "元/月",
        "desc": t("auth.pricing_desc_monthly_auto"),
    },
    "quarterly": {
        "name": t("auth.pricing_quarterly"),
        "price": 23.88,
        "unit": "元/季",
        "desc": t("auth.pricing_desc_quarterly"),
    },
    "yearly": {
        "name": t("auth.pricing_yearly"),
        "price": 88.88,
        "unit": "元/年",
        "desc": t("auth.pricing_desc_yearly"),
    },
}

# === 单次按需定价 ===
_c5b3 = {
    "migration_assess": {"name": t("auth.per_use_migration_assess"), "price": 9.9},
    "shallow_adapt": {"name": t("auth.per_use_shallow_adapt"), "price": 49.9},
    "deep_diagnosis": {"name": t("auth.per_use_deep_diagnosis"), "price": 89.9},
    "crash_fix": {"name": t("auth.per_use_crash_fix"), "price": 39.9},
}

# === 作者测试设备列表 (仅这些设备会显示完整付费信息) ===
# 普通用户看不到单次按需付费（V1阶段还未实现），使整体更划算
_m3m0 = [
    "5184c91c54610b2852a9369f68332286",  # 作者主设备
]


def _o1d0() -> bool:
    """判断当前设备是否为作者测试设备"""
    # 方式1: 机器码匹配
    if _s0f0() in _m3m0:
        return True
    # 方式2: 环境变量 (AUTHOR_MODE=1)
    if os.environ.get("MC_SKILL_AUTHOR_MODE", "0") == "1":
        return True
    return False

# === 本地数据存储 ===
_t4j4 = Path(__file__).resolve().parent.parent / "_b0b1"
_f2n5 = _t4j4 / "auth_state.json"
_lock_file = _t4j4 / "auth_state.lock"  # 状态文件锁（防止多进程竞态）


class _StateLock:
    """跨平台文件锁（Windows: msvcrt.locking / Unix: fcntl.flock）

    用于 report_app_started 等「检查-修改-保存」原子操作，
    避免多进程同时读取状态文件导致去重失效。
    """

    def __init__(self, timeout: float = 5.0):
        self._timeout = timeout
        self._fh = None

    def __enter__(self):
        _t4j4.mkdir(parents=True, exist_ok=True)
        self._fh = open(_lock_file, "w")
        _deadline = datetime.now().timestamp() + self._timeout
        while True:
            try:
                if sys.platform == "win32":
                    import msvcrt
                    msvcrt.locking(self._fh.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(self._fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                return self
            except (BlockingIOError, OSError, IOError):
                if datetime.now().timestamp() > _deadline:
                    # 超时仍获取不到锁，直接放行（宁可重复上报也不阻塞主流程）
                    return self
                time.sleep(0.1)

    def __exit__(self, *exc):
        if self._fh:
            try:
                if sys.platform == "win32":
                    import msvcrt
                    msvcrt.locking(self._fh.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(self._fh.fileno(), fcntl.LOCK_UN)
            except Exception:
                pass
            self._fh.close()
            self._fh = None


def _l1p7() -> str:
    """检测测试环境标签（用于生成 TEST-N-LABEL-YYYYMMDD 格式机器码）
    
    优先级：
    1. 环境变量 MC_SKILL_MACHINE_ID 直接指定 → 原样返回
    2. 环境变量 MC_SKILL_TEST_LABEL=onboarding/pay/xxx → 用它
    3. 环境变量 MC_SKILL_TEST=1 或 QCLAW/LOCALHOST → AUTO
    4. 目录名含 test/dev/debug/sandbox/qclaw/mc-skill → AUTO
       （检测 3 条路径：os.getcwd() + __file__ 所在目录 + main.py/SKILL.json 所在根目录
        ↳ 避免 QClaw 运行时 cwd 变 QClaw 进程目录导致漏判）
    5. 以上都不满足 → 返回空（走正常硬件指纹）
    """
    # 最高优先级：直接指定完整机器码
    _c7s4 = os.environ.get("MC_SKILL_MACHINE_ID", "").strip()
    if _c7s4:
        return _c7s4
    
    # 指定用途标签
    _e1z8 = os.environ.get("MC_SKILL_TEST_LABEL", "").strip()
    
    # 检测是否为测试环境
    _a4s8 = False
    if os.environ.get("MC_SKILL_TEST", "").lower() in ("1", "true", "yes"):
        _a4s8 = True
    if os.environ.get("QCLAW", "").strip():
        _a4s8 = True
    
    # 目录检测：3 条路径并行扫描，命中就算
    _e4b3 = (
        "test", "debug", "dev", "sandbox", "qclaw",
        "mc-skill-",   # ← 开发环境：mc-skill-v1 / mc-skill-v2 ...
        "-test",       # ← ZIP 包名后缀
    )
    _e1a7 = os.getcwd().lower()
    _d8h9 = ""
    try:
        # __file__ 指向本文件 auth_manager.py，Skill 根目录就是 __file__/../../
        _d8h9 = os._w3n4.dirname(os._w3n4.dirname(os._w3n4.abspath(__file__))).lower()
    except Exception:
        pass
    # 第 3 条路：向上最多 3 层找 SKILL.json 或 main.py 作为 Skill 根
    _c1k1 = ""
    try:
        _h4d7 = os.getcwd()
        for _i in range(4):
            if os._w3n4.isfile(os._w3n4.join(_h4d7, "SKILL.json")) or os._w3n4.isfile(os._w3n4.join(_h4d7, "main.py")):
                _c1k1 = _h4d7.lower()
                break
            _u8a4 = os._w3n4.dirname(_h4d7)
            if _u8a4 == _h4d7: break
            _h4d7 = _u8a4
    except Exception:
        pass
    
    for _p in (_e1a7, _d8h9, _c1k1):
        if not _p:
            continue
        if any(kw in _p for kw in _e4b3):
            _a4s8 = True
            break

    if not _a4s8 and not _e1z8:
        return ""
    
    # 组装 TEST 格式机器码
    import re as _re
    import datetime as _dt
    
    _e9l5 = (_e1z8 or "AUTO").upper()
    _r1g7 = _dt.datetime.now().strftime("%Y%m%d")
    
    # 尝试从现有 registry 取最大 admin 号 + 1
    _g1u1 = 1  # 默认从 1 开始
    try:
        # 候选路径列表（按优先级）
        _c9b7 = []
        _x7y3 = os.environ.get("MC_SKILL_DATA_DIR", "").strip()
        if _x7y3:
            _c9b7.append(os._w3n4.join(_x7y3, "registry.json"))
        # 标准路径：server/_u7g9/registry.json
        _c9b7.append(os._w3n4.join("server", "_b0b1", "registry.json"))
        _c9b7.append(os._w3n4.join("_b0b1", "registry.json"))
        # 向上找 3 层
        for _i in range(1, 4):
            _q5m3 = ".." + os.sep
            _c9b7.append(_q5m3 * _i + os._w3n4.join("server", "_b0b1", "registry.json"))
            _c9b7.append(_q5m3 * _i + os._w3n4.join("_b0b1", "registry.json"))
        
        _m1t4 = ""
        for _c in _c9b7:
            if os._w3n4.isfile(_c):
                _m1t4 = _c
                break
        if os._w3n4.isfile(_m1t4):
            import json as _json
            with open(_m1t4, "r", encoding="utf-8") as _f:
                _j7w9 = _json.load(_f)
            # 来源 1：TEST-N-xxx 格式里的 N
            _r6a5 = []
            for _u in _j7w9:
                _m = _re.search("TEST-(\\d+)-", _u.get("_g8i7", "").upper())
                if _m:
                    _r6a5.append(int(_m.group(1)))
            # 来源 2：nickname 里的"管理员N"或"管理员[中文数字]"
            _g7v8 = {"一":1,"二":2,"三":3,"四":4,"五":5,"六":6,"七":7,"八":8,"九":9,"十":10}
            for _u in _j7w9:
                _j7g4 = _u.get("nickname", "")
                _m = _re.search("管理员(\\d+)", _j7g4)
                if _m:
                    _r6a5.append(int(_m.group(1)))
                else:
                    _f7f2 = _re.search("管理员([一二三四五六七八九十])", _j7g4)
                    if _f7f2:
                        _r6a5.append(_g7v8.get(_f7f2.group(1), 0))
            if _r6a5:
                _g1u1 = max(_r6a5) + 1
    except Exception:
        pass
    
    return f"TEST-{_g1u1}-{_e9l5}-{_r1g7}"


def _detect_ai_platform() -> str:
    """检测当前运行的 AI 助手平台标识（用于区分不同 AI 软件的机器码）

    同一台机器上，不同 AI 软件（WorkBuddy / Kimi / Trae / Cursor 等）
    会生成不同的机器码；同一 AI 软件跨版本升级保持同一机器码。

    优先级：
      1. ~/.mc-skill/platform.txt（用户手动声明，最稳定）
      2. PPID 进程名探测（兜底，可能不准）
      3. unknown（最后兜底，不带 PPID，确保声明前多会话共享同一机器码）

    Returns:
        平台标识字符串（如 "workbuddy" / "kimi" / "trae" / "unknown"）
    """
    # 优先级 1：用户手动声明（~/.mc-skill/platform.txt，最稳定）
    try:
        _plat_file = Path.home() / ".mc-skill" / "platform.txt"
        if _plat_file.exists():
            _v = _plat_file.read_text(encoding="utf-8").strip().lower()
            if _v and _v in SUPPORTED_AI_PLATFORMS:
                return _v
            elif _v:
                # 用户写过但不在白名单，规范化后直接使用（custom 路径）
                return _v[:24]
    except Exception:
        pass

    # 优先级 2：PPID 进程名探测（兜底，可能因 shell wrapper 不同而不准）
    _ppid = os.getppid()
    _name = ""
    try:
        if platform.system() == "Windows":
            import subprocess as _sp
            _r = _sp.run(
                ["tasklist", "/FI", f"PID eq {_ppid}", "/FO", "CSV", "/NH"],
                capture_output=True, text=True, timeout=5,
            )
            if _r.stdout and _r.stdout.strip():
                _parts = _r.stdout.strip().split(",")
                if _parts:
                    _name = _parts[0].strip('"').lower()
        else:
            _comm = f"/proc/{_ppid}/comm"
            if os.path.exists(_comm):
                with open(_comm) as _f:
                    _name = _f.read().strip().lower()
    except Exception:
        pass

    # 归一化：取进程名主体（去掉 .exe / 版本号等）
    if _name:
        _base = _name.replace(".exe", "").split("_")[0].split("-")[0]
        # 常见 AI 平台映射
        _aliases = {
            "workbuddy": "workbuddy",
            "kimi": "kimi",
            "trae": "trae",
            "cursor": "cursor",
            "claw": "openclaw",
            "qclaw": "openclaw",
            "chatgpt": "chatgpt",
            "copilot": "copilot",
            "cline": "cline",
        }
        for _k, _v in _aliases.items():
            if _k in _base:
                return _v
        return _base[:24]

    # 兜底：使用固定 "unknown" 而非 "unknown-<ppid>"，
    # 确保用户声明平台前，同一机器上多个会话共享同一 salt 文件 → 同一机器码
    return "unknown"


def _get_device_info() -> dict:
    """采集当前设备信息（V1.0.5 新增）

    收集设备品牌、型号、操作系统等，随活动事件上报到服务端。
    注意：不采集 hostname（可能包含用户真名），保护用户隐私。
    所有采集均在本地完成，不涉及网络请求。
    """
    import platform as _plat

    _os_name = _plat.system()  # Windows / Darwin / Linux
    _os_ver = _plat.release()  # 10.0 / 21.6.0 / 5.15.0
    _arch = _plat.machine()  # AMD64 / arm64 / x86_64

    # 设备品牌/型号（各平台采集方式不同）
    _brand = ""
    _model = ""
    try:
        if _os_name == "Windows":
            # Windows: 从环境变量和 WMI 获取
            _brand = os.environ.get("PROCESSOR_IDENTIFIER", "").split(" ")[0] if os.environ.get("PROCESSOR_IDENTIFIER") else ""
            # 尝试从注册表读取电脑型号
            try:
                import winreg
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\HardwareConfig\Current") as _rk:
                    _sys_info = winreg.QueryValueEx(_rk, "SystemInformation")[0]
                    if _sys_info:
                        _parts = _sys_info.split(" ", 1)
                        _brand = _parts[0] if len(_parts) > 0 else _brand
                        _model = _parts[1] if len(_parts) > 1 else ""
            except Exception:
                pass
        elif _os_name == "Darwin":
            # macOS: 读取硬件型号
            import subprocess
            try:
                _brand = "Apple"
                _model = subprocess.check_output(["sysctl", "-n", "hw.model"], timeout=2, text=True).strip()
            except Exception:
                pass
        elif _os_name == "Linux":
            # Linux: 读取 DMI 信息
            try:
                for _path in ["/sys/class/dmi/id/sys_vendor", "/sys/class/dmi/id/product_name"]:
                    if os.path.exists(_path):
                        with open(_path) as _f:
                            if not _brand:
                                _brand = _f.read().strip()
                            else:
                                _model = _f.read().strip()
            except Exception:
                pass
    except Exception:
        pass

    _os_info = f"{_os_name} {_os_ver} ({_arch})"

    return {
        "device_brand": _brand[:50] if _brand else "",
        "device_model": _model[:50] if _model else "",
        "os_info": _os_info[:80] if _os_info else "",
    }


def _s0f0() -> str:
    """生成机器唯一标识码

    策略：
    1. 测试环境检测优先 → 返回 TEST- 格式机器码
    2. 生产环境：使用持久化随机 salt（存在用户主目录 ~/.mc-skill/，跨版本不丢失）
    3. 按 AI 平台分 salt 文件 → 不同 AI 软件生成不同机器码
    4. 机器码 = MD5(salt + hostname + OS + AI平台)
    """
    # 先检测测试环境
    _m9g5 = _l1p7()
    if _m9g5:
        return _m9g5

    # 检测 AI 平台（不同 AI 软件用不同 salt 文件）
    _ai_platform = _detect_ai_platform()

    # salt 存储在用户主目录，跨版本持久化（不随包更新丢失）
    _salt_dir = Path.home() / ".mc-skill"
    _salt_file = _salt_dir / f"machine_salt_{_ai_platform}"

    # 尝试读取已有 salt
    _machine_salt = ""
    try:
        if _salt_file.exists():
            _machine_salt = _salt_file.read_text(encoding="utf-8").strip()
    except Exception:
        pass

    # 如果 salt 不存在或无效，生成新 salt 并持久化
    if not _machine_salt or len(_machine_salt) < 16:
        _machine_salt = secrets.token_hex(8)  # 16 字符随机 salt
        try:
            _salt_file.parent.mkdir(parents=True, exist_ok=True)
            _salt_file.write_text(_machine_salt, encoding="utf-8")
        except Exception:
            pass  # 写入失败也没关系，本次用内存中的 salt

    # 机器码 = MD5(salt + hostname + OS + AI平台)
    _b8u0 = _machine_salt
    try:
        _b8u0 += socket.gethostname()
    except Exception:
        pass
    try:
        _b8u0 += platform.system() + platform.machine()
    except Exception:
        pass
    _b8u0 += _ai_platform  # 不同 AI 软件 → 不同机器码
    return hashlib.md5(_b8u0.encode("utf-8")).hexdigest()[:32]


def _j3g4() -> Dict[str, Any]:
    """默认授权状态"""
    return {
        "_g8i7": _s0f0(),
        "_w1b8": TIER_FREE,
        "_i2v1": "",
        "license_expires": "",
        "_z0z5": "",  # monthly / monthly_auto / quarterly / yearly
        "first_use_date": "",    # 首次使用日期（YYYY-MM-DD）
        "free_period_end": "",   # 免费期结束日期
        "_z6m9": {},
        "last_reset_date": datetime.now().strftime("%Y-%m-%d"),
        "total_usage": {},
        "migration_assess_first_used": False,  # 移植评估是否已使用过首次免费
        # === 强制联网验证相关 ===
        "server_token": "",          # 服务器返回的临时Token（有效期1小时）
        "server_token_expires": "",  # Token过期时间
        "last_online_check": "",     # 上次在线验证时间
        "online_verify_enabled": bool(AUTH_SERVER_URL),  # 是否启用强制联网验证
        # === 数据上报相关 ===
        "last_report_time": "",      # 上次成功上报时间
        "pending_reports": [],       # 待上报的数据记录列表
        "pending_activity_events": [],  # 待上报的活动事件列表（上报失败时缓存，下次补报）
        "last_verify_fail_time": "",    # 上次联网验证失败时间（用于操作台审计）
    }


def _z3v2(_f9q2: Dict[str, Any]) -> bool:
    """检查授权是否过期，如果过期则自动降级为免费用户
    
    规则：
    - _f3j4=normal 且 license_expires < 今天 → 降级为 TIER_FREE，清空授权相关字段
    - premium 过期同理
    - 返回值：True = 发生过降级（需要保存 _f9q2）
    """
    _f3j4 = _f9q2.get("_w1b8", TIER_FREE)
    if _f3j4 == TIER_FREE:
        return False  # 本来就是免费，无需检查

    _n1e9 = _f9q2.get("license_expires", "")
    if not _n1e9:
        # 有 _f3j4 但没写过期时间（异常数据）→ 为保险起见不直接改，记录日志
        _f4x3.warning(f"[授权降级] _f3j4={_f3j4} 但 license_expires 为空，跳过自动降级")
        return False

    try:
        _f9l2 = datetime.strptime(_n1e9, "%Y-%m-%d").date()
    except Exception:
        _f4x3.warning(f"[授权降级] license_expires='{_n1e9}' 格式异常，跳过自动降级")
        return False

    _a8r1 = date.today()
    if _a8r1 > _f9l2:
        # 授权已过期 → 自动降级回免费用户
        _f9w1 = _f3j4
        _f9q2["_w1b8"] = TIER_FREE
        _f9q2["_i2v1"] = ""
        _f9q2["license_expires"] = ""
        _f9q2["_z0z5"] = ""
        _f4x3.info(f"[授权自动降级] _f3j4={_f9w1} → free，原因：license_expires={_n1e9} < _a8r1={_a8r1}")
        return True

    return False  # 仍在有效期内


def _l1r4() -> Dict[str, Any]:
    """加载本地授权状态"""
    if not _f2n5.exists():
        return _j3g4()
    try:
        with open(_f2n5, "r", encoding="utf-8") as f:
            _f9q2 = json.load(f)
        
        _g8i7 = False  # 标记是否需要持久化
        
        # === 自动同步：根据当前配置更新强制验证开关 ===
        _x5z3 = bool(AUTH_SERVER_URL)
        if _f9q2.get("online_verify_enabled", False) != _x5z3:
            _f9q2["online_verify_enabled"] = _x5z3
            if _x5z3:
                _f4x3.info(f"[联网验证] 已自动启用，服务器地址: {AUTH_SERVER_URL}")
            _g8i7 = True
        
        # === 授权过期 → 自动降级（防止用户授权过期后依旧享受 normal 次数）===
        if _z3v2(_f9q2):
            _g8i7 = True
        
        # === 检查是否需要重置每日计数 ===
        _a8r1 = datetime.now().strftime("%Y-%m-%d")
        if _f9q2.get("last_reset_date") != _a8r1:
            _f9q2["_z6m9"] = {}
            _f9q2["last_reset_date"] = _a8r1
            _g8i7 = True

        if _g8i7:
            _m6x0(_f9q2)
        return _f9q2
    except Exception as e:
        _f4x3.warning(f"加载授权状态失败: {e}")
        return _j3g4()


def _m6x0(_f9q2: Dict[str, Any]) -> None:
    """保存授权状态到本地"""
    try:
        _t4j4.mkdir(parents=True, exist_ok=True)
        with open(_f2n5, "w", encoding="utf-8") as f:
            json.dump(_f9q2, f, ensure_ascii=False, indent=2)
    except Exception as e:
        _f4x3.warning(f"保存授权状态失败: {e}")


def _w9c5() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def _z6m9(_f9q2: Dict[str, Any], _j7d2: bool = False) -> Dict[str, Any]:
    # 🔒 RACE / 云鼎安全：运行时完整性检查（静默模式下也跑，只记日志不中断）
    try:
        from core.integrity_guard import quick_check
        quick_check()
    except Exception:
        pass  # 开发模式忽略


    """确保首次使用日期已记录

    如果是首次使用，记录当天日期并设置7天后的免费期结束日期。
    - _j7d2=True 模式：Agent 调用 onboarding_info 时传这个参数，
      所有"欢迎/机器码提示"一律只打日志，不打印到 stdout，
      防止污染 stdout 里的 JSON 导致 Agent 解析失败。
    - _j7d2=False（默认）：保留给人类用户交互用的 ASCII Banner + 剪贴板提示。
    """
    _m8w7 = False
    if not _f9q2.get("first_use_date"):
        _a8r1 = date.today()
        _f9q2["first_use_date"] = _a8r1.strftime("%Y-%m-%d")
        _j9w2 = _a8r1 + timedelta(days=FREE_PERIOD_DAYS)
        _f9q2["free_period_end"] = _j9w2.strftime("%Y-%m-%d")
        _m6x0(_f9q2)
        _f4x3.info(f"记录首次使用日期: {_f9q2['first_use_date']}, 免费期至: {_f9q2['free_period_end']}")

        _d3e9 = _f9q2.get("_g8i7", "未知")

        if _j7d2:
            # 🧑‍💻 Agent 模式（脚本调用 onboarding_info）
            # 任何 stdout 都会和 JSON 混在一起，必须只用 _f4x3
            _f4x3.info(f"[首次使用] 机器码={_d3e9}，免费期至 {_f9q2['free_period_end']}")
        else:
            # 👤 人类交互模式（main.py 直接启动）—— ASCII Banner 正常显示
            print("\n" + "=" * 60)
            print("  🎉 欢迎使用 MC Skill！")
            print("=" * 60)
            print(f"\n  📍 您的机器码:")
            print(f"  {'─' * 50}")
            print(f"  {_d3e9}")
            print(f"  {'─' * 50}")
            print(f"\n  ⚠️  重要提示:")
            print(f"  1. 请复制上面的机器码发给您的 AI Agent")
            print(f"  2. AI Agent 需要此机器码来管理您的授权")
            print(f"  3. 后续订阅套餐时也需要此机器码")
            print(f"  4. 请妥善保管，不要泄露给他人\n")
            print("=" * 60 + "\n")
            # 尝试自动复制到剪贴板（Windows）
            try:
                import subprocess
                if sys.platform == "win32":
                    subprocess.run("clip", input=_d3e9, capture_output=True, text=True)
                    print("  ✅ 机器码已自动复制到剪贴板\n")
            except Exception:
                print("  💡 请手动复制上面的机器码\n")
            _m8w7 = True

    return _f9q2


# ============ 首对话引导（Onboarding）===========

def is_onboarding_due() -> bool:
    """判断当前会话是否需要显示首次引导块

    触发条件：用户首次使用（first_use_date 刚记录）或 onboarding_shown 字段为空
    一旦显示过，后续不再重复展示，避免打扰老用户
    """
    _f9q2 = _l1r4()
    _f9q2 = _z6m9(_f9q2)
    if not _f9q2.get("onboarding_shown"):
        return True
    # 兼容老版本：如果 first_use_date 存在但 onboarding_shown 不存在，视为需要显示一次
    if _f9q2.get("first_use_date") and not _f9q2.get("onboarding_shown"):
        return True
    return False


def mark_onboarding_shown() -> None:
    """标记首对话引导已展示，持久化到本地 auth_state.json"""
    _f9q2 = _l1r4()
    _f9q2["onboarding_shown"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _m6x0(_f9q2)
    _f4x3.info("[Onboarding] 首对话引导已标记为已展示")


def get_onboarding_info() -> Dict[str, Any]:
    """聚合首对话引导所需的全部动态数据

    返回的结构覆盖引导的 4 段：
      ① 功能速览：_e9t7（F1-F9 + F8.1 公开功能列表）
      ② 免费额度：是否在免费期、剩余天数、今日次数（自动/半自动/移植评估）
      ③ 套餐：三档月/季/年的价格（本地化）+ 付费渠道
      ④ 收尾：机器码提示 + 引导用户提需求
    """
    _f9q2 = _l1r4()
    _f9q2 = _z6m9(_f9q2, _j7d2=True)  # Agent 模式：静默，禁止 print 污染 JSON

    # === 🔑 首次启动强制联网注册 ===
    # 目的：确保用户第一次接触时就被服务器记录，免费期从这天开始算
    # 策略：只在 server_token 为空（从未注册过）且启用了联网验证时才发一次
    if AUTH_SERVER_URL and not _f9q2.get("server_token"):
        try:
            _b3o6 = _h8d3()
            if _b3o6.get("online"):
                # online=True 说明服务器连接成功，新用户已注册
                _w9g0 = _b3o6.get("success")
                _f4x3.info(f"[首对话引导] 首次联网注册成功: online=True, authorized={_w9g0}, _f3j4={_b3o6.get('_f3j4')}")
            else:
                _f4x3.warning(f"[首对话引导] 联网注册失败（不影响本地功能）: {_b3o6.get('reason', '')}")
        except Exception as _e:
            _f4x3.warning(f"[首对话引导] 联网异常（不影响本地功能）: {_e}")
    elif AUTH_SERVER_URL and _f9q2.get("server_token"):
        # 已有 token，刷新一下 last_access
        try:
            _h8d3()
        except Exception:
            pass

    _e0h7 = get_free_period_info()
    _f3j4 = _f9q2.get("_w1b8", TIER_FREE)
    _p9b7 = _f9q2.get("_z6m9", {})
    _i1y4 = DAILY_LIMITS.get(_f3j4, DAILY_LIMITS[TIER_FREE])

    _r3d7 = _p9b7.get(FUNC_AUTO, 0)
    _y9p6 = _p9b7.get(FUNC_SEMI, 0)
    _n5f3 = _p9b7.get(SPECIAL_FEATURE_MIGRATION_ASSESS, 0)

    # 公开功能列表（F1-F9 + F8.1，不含 F10-F14 运营支撑）
    _e9t7 = [
        {"code": "F1", "name": t("onboarding.features.f1"), "desc": t("onboarding.features.f1_desc")},
        {"code": "F2", "name": t("onboarding.features.f2"), "desc": t("onboarding.features.f2_desc")},
        {"code": "F3", "name": t("onboarding.features.f3"), "desc": t("onboarding.features.f3_desc")},
        {"code": "F4", "name": t("onboarding.features.f4"), "desc": t("onboarding.features.f4_desc")},
        {"code": "F5", "name": t("onboarding.features.f5"), "desc": t("onboarding.features.f5_desc")},
        {"code": "F6", "name": t("onboarding.features.f6"), "desc": t("onboarding.features.f6_desc")},
        {"code": "F7", "name": t("onboarding.features.f7"), "desc": t("onboarding.features.f7_desc")},
        {"code": "F8", "name": t("onboarding.features.f8"), "desc": t("onboarding.features.f8_desc")},
        {"code": "F8.1", "name": t("onboarding.features.f81"), "desc": t("onboarding.features.f81_desc")},
        {"code": "F9", "name": t("onboarding.features.f9"), "desc": t("onboarding.features.f9_desc")},
    ]

    # ================================================================
    # 🌐 i18n 语言检测（QClaw 反馈 #6）
    # 优先级：MC_SKILL_LANG 环境变量 > 系统 locale > 默认 en
    # 检测结果影响：greeting_text / feature_slogan / hook_text 的语言
    # ================================================================
    import locale as _locale
    _b4b7 = os.environ.get("MC_SKILL_LANG", "").strip().lower()
    if _b4b7:
        _p9g5 = _b4b7[:2]
    else:
        try:
            _s3h8 = _locale.getdefaultlocale()[0] or ""
            _p9g5 = (_s3h8.split("_")[0] if _s3h8 else "en").lower()
        except Exception:
            _p9g5 = "en"
    # 支持的语言白名单
    _t0h2 = {"en", "zh", "ja", "ko", "ru", "es", "it", "el", "th", "hi", "ar"}
    if _p9g5 not in _t0h2:
        _p9g5 = "en"
    _p2k3 = _p9g5 == "zh"

    # 🌐 功能描述自然段落（QClaw 反馈 #2：不要 F1-F9 编号清单，要自然语言）
    if _p2k3:
        _l4g5 = (
            "我可以帮你搜模组、搭环境、查冲突、修崩溃、翻译成中文，" +
            "还能评估某个 mod 能不能迁移到新版本——直接告诉我你想做什么就行。"
        )
    else:
        _l4g5 = (
            "I can help you search mods, set up your MC environment, " +
            "find Mixin conflicts, fix crashes, translate resources, " +
            "and assess whether a mod can be ported to a newer MC version. " +
            "Just tell me what you want to do."
        )

    # 🌐 结尾钩子（QClaw 反馈 #4：1-2 个具体场景，不要太泛）
    if _p2k3:
        _s2b1 = "你现在是想找某个具体的模组，还是遇到了什么报错？直接说就行。"
    else:
        _s2b1 = "Are you looking for a specific mod, or did you run into an error? Just tell me."

    # 🌐 欢迎语（QClaw 反馈 #5：首屏不要展开付费，只留一句话）
    if _e0h7["in_free_period"]:
        if _p2k3:
            _g3m9 = (
f"你好！首次使用还有 **{_e0h7['_h4c6']} 天免费期**，" +
                f"公开功能不限次数。之后如有需要可以解锁高级功能。"
            )
        else:
            _g3m9 = (
f"Hi! You have **{_e0h7['_h4c6']} days left** in your free trial. " +
                f"All public features are unlimited during this period. " +
                f"Premium upgrades are available later if you need them."
            )
    elif _f3j4 == TIER_FREE:
        if _p2k3:
            _g3m9 = (
                f"免费期已结束。当前额度：全自动 **{_i1y4[FUNC_AUTO]}次/日**、" +
                f"半自动 **{_i1y4[FUNC_SEMI]}次/日**。" +
                f"普通会员自动100次/半自动50次（¥8.88起）；" +
                f"年卡 PREMIUM 自动200次/半自动100次 + 4项特权（¥88.88）。"
            )
        else:
            _g3m9 = (
                f"Free trial ended. Current quota: **{_i1y4[FUNC_AUTO]} auto/day**, " +
                f"**{_i1y4[FUNC_SEMI]} semi/day**. " +
                f"Normal tier: 100 auto/50 semi/month (from $9.99). " +
                f"Yearly PREMIUM: 200 auto/100 semi + 4 perks ($99.99/year)."
            )
    else:
        if _p2k3:
            _g3m9 = f"你好！当前是 {_i7t7(_f3j4)}，所有功能正常可用。"
        else:
            _g3m9 = f"Hi! You're on the {_i7t7(_f3j4, lang='en')} plan. All features available."

    # 🌐 引导触发条件（QClaw 反馈 #1：needs_onboarding 外再给 trigger_policy）
    # trigger_policy = "question_only" 表示：只有用户主动问"怎么用/能做什么"时才展开全引导；
    #                  其他情况（用户直接提需求）只需要 1 句 greeting + 1 句 hook
    _f3z2 = "question_only"

    # =================================================================
    # 🔧 最终成品话术（完全不让 Agent 自己拼，直接拿字符串回复即可）
    # 解决：QClaw Agent 会无视协议自己加一堆"完整介绍"/F1-F9 列表/中英混杂
    # 用法：SKILL.md 写死 "直接输出 _e8m8.xxx 字段文字，不要加任何其他字"
    # 🔑 关键修复：始终同时生成中英双语，不依赖系统 locale
    #   → pattern_A_zh / pattern_B_zh 永远有中文
    #   → pattern_A_en / pattern_B_en 永远有英文
    #   → Agent 根据用户实际输入语言选择对应字段
    # =================================================================

    # --- 中文版 pattern ---
    if _e0h7["in_free_period"]:
        _g3t1 = (
f"你好！首次使用还有 **{_e0h7['_h4c6']} 天免费期**，" +
            f"公开功能不限次数。之后如有需要可以解锁高级功能。"
        )
    elif _f3j4 == TIER_FREE:
        _g3t1 = (
            f"免费期已结束。当前额度：全自动 **{_i1y4[FUNC_AUTO]}次/日**、" +
            f"半自动 **{_i1y4[FUNC_SEMI]}次/日**。" +
            f"普通会员自动100次/半自动50次（¥8.88起）；" +
            f"年卡 PREMIUM 自动200次/半自动100次 + 4项特权（¥88.88）。"
        )
    else:
        _g3t1 = f"你好！当前是 {_i7t7(_f3j4)}，所有功能正常可用。"

    _d4f6 = (
        "我可以帮你搜模组、搭环境、查冲突、修崩溃、翻译成中文，" +
        "还能评估某个 mod 能不能迁移到新版本——直接告诉我你想做什么就行。"
    )
    _r8a2 = "你现在是想找某个具体的模组，还是遇到了什么报错？直接说就行。"

    _p3t9 = _g3t1 + "\n\n" + _d4f6 + "\n\n" + _r8a2
    _d9d3 = _g3t1 + " 好的，我来帮你 —— " + _r8a2

    # --- 英文版 pattern ---
    if _e0h7["in_free_period"]:
        _c9g0 = (
f"Hi! You have **{_e0h7['_h4c6']} days left** in your free trial. " +
            f"All public features are unlimited during this period. " +
            f"Premium upgrades are available later if you need them."
        )
    elif _f3j4 == TIER_FREE:
        _c9g0 = (
            f"Free trial ended. Current quota: **{_i1y4[FUNC_AUTO]} auto/day**, " +
            f"**{_i1y4[FUNC_SEMI]} semi/day**. " +
            f"Normal tier: 100 auto/50 semi (from $9.99). " +
            f"Yearly PREMIUM: 200 auto/100 semi + 4 exclusive perks ($99.99)."
        )
    else:
        _c9g0 = f"Hi! You're on the {_i7t7(_f3j4, lang='en')} plan. All features available."

    _p6g5 = (
        "I can help you search mods, set up your MC environment, " +
        "find Mixin conflicts, fix crashes, translate resources, " +
        "and assess whether a mod can be ported to a newer MC version. " +
        "Just tell me what you want to do."
    )
    _h4c6 = "Are you looking for a specific mod, or did you run into an error? Just tell me."

    _h6r7 = _c9g0 + "\n\n" + _p6g5 + "\n\n" + _h4c6
    _u5g1 = _c9g0 + " Sure, I'll help — " + _h4c6

    # --- 默认 pattern（兼容旧字段，跟随系统 locale）---
    if _p2k3:
        _a2a0 = _p3t9
        _f5e5 = _d9d3
    else:
        _a2a0 = _h6r7
        _f5e5 = _u5g1

    _e8m8 = {
        # 默认 pattern（跟随系统 locale，兼容旧代码）
        "pattern_A": _a2a0,
        "pattern_B": _f5e5,
        # 🔑 始终有值的双语版本（Agent 应该用这两个字段）
        "pattern_A_zh": _p3t9,
        "pattern_A_en": _h6r7,
        "pattern_B_zh": _d9d3,
        "pattern_B_en": _u5g1,
        # Agent 指令：根据用户语言选，不要翻译，不要加别的
        "_raw_language_note": (
            "CRITICAL — READ FIRST:\n" +
            "1. DETECT what language the USER actually wrote their _w9u5 in.\n" +
            "2. If user wrote in ENGLISH → OUTPUT ONLY pattern_A_en or pattern_B_en (choose A if they asked 'what can you do', choose B if they gave a task).\n" +
            "3. If user wrote in CHINESE → OUTPUT ONLY pattern_A_zh or pattern_B_zh.\n" +
            "4. DO NOT translate. DO NOT mix languages. DO NOT add your own words. DO NOT write greeting manually.\n" +
            "5. OUTPUT THE EXACT STRING. NOTHING ELSE."
        ),
    }

    return {
        "needs_onboarding": is_onboarding_due(),
        "trigger_policy": _f3z2,
        "language": _p9g5,
        "is_zh": _p2k3,
        "greeting_text": _g3m9,
        "feature_slogan": _l4g5,
        "hook_text": _s2b1,
        "_d9d3": _e8m8,
        "_g8i7": _f9q2.get("_g8i7", ""),
        "_w1b8": _f3j4,
        "tier_name": _i7t7(_f3j4),
        "free_period": {
            "in_free_period": _e0h7["in_free_period"],
            "_h4c6": _e0h7["_h4c6"],
            "days_total": FREE_PERIOD_DAYS,
            "first_use_date": _e0h7["first_use_date"],
            "free_period_end": _e0h7["free_period_end"],
            "notes": [
                t("onboarding.free_notes.migration_first_free"),
                t("onboarding.free_notes.migration_then_daily_1"),
            ],
        },
        "_z6m9": {
            "_m8w7": _r3d7,
            "_h8g8": _i1y4[FUNC_AUTO],
            "_j9w2": _y9p6,
            "_x4f7": _i1y4[FUNC_SEMI],
            "_d3e9": _n5f3,
            "migration_limit": _i1y4[SPECIAL_FEATURE_MIGRATION_ASSESS],
        },
        # 保留给需要逐条列功能的场景（帮助页、详情页），默认引导不要用
        "_b3o6": _e9t7,
        # === 🔧 首次启动 AI 平台声明（Bug1 修复）===
        # 只有从未声明过（platform.txt 不存在）的首次用户才会问一次
        # 目的：让机器码稳定，不再随 shell wrapper 变化
        "platform_question": (
            {
                "needs_ask": True,
                "question_zh": (
                    "对了，为了给您提供更准确的服务，能告诉我您现在主要在使用哪款 AI 软件吗？"
                    "（例如 WorkBuddy、Kimi、Trae、Cursor、ChatGPT、Cline 等）"
                ),
                "question_en": (
                    "Quick question — which AI assistant are you mainly using? "
                    "(e.g. WorkBuddy, Kimi, Trae, Cursor, ChatGPT, Cline, etc.)"
                ),
                "supported": SUPPORTED_AI_PLATFORMS,
            }
            if not is_platform_declared() else None
        ),
        "current_platform": (
            get_current_platform() if is_platform_declared() else None
        ),
        "payment_enabled": ENABLE_PAYMENT,
        # 注意：付费渠道/套餐名已经从首屏移除（QClaw 反馈 #5），
        # 需要付费信息时单独调 payment_page 获取，不要在首屏展开
    }


def is_in_free_period() -> bool:
    """判断当前是否在免费期内

    Returns:
        True = 在免费期内（前7天）
        False = 免费期已过，需要付费
    """
    _f9q2 = _l1r4()
    _f9q2 = _z6m9(_f9q2)

    _x9r7 = _f9q2.get("free_period_end", "")
    if not _x9r7:
        return True  # 没有记录结束日期，视为免费期

    try:
        _j9w2 = datetime.strptime(_x9r7, "%Y-%m-%d").date()
        return date.today() <= _j9w2
    except Exception:
        return True


def get_free_period_info() -> Dict[str, Any]:
    """获取免费期信息"""
    _f9q2 = _l1r4()
    _f9q2 = _z6m9(_f9q2)

    _b8d6 = _f9q2.get("first_use_date", "")
    _x9r7 = _f9q2.get("free_period_end", "")

    if not _x9r7:
        return {
            "in_free_period": True,
            "first_use_date": _b8d6,
            "free_period_end": "",
            "_h4c6": FREE_PERIOD_DAYS,
        }

    try:
        _j9w2 = datetime.strptime(_x9r7, "%Y-%m-%d").date()
        _a8r1 = date.today()
        # 使用 ceil 逻辑：最后一天显示剩余1天而不是0天
        _e2a5 = (_j9w2 - _a8r1).days
        if _e2a5 <= 0 and _a8r1 <= _j9w2:
            _e2a5 = 1
        else:
            _e2a5 = max(0, _e2a5)
        return {
            "in_free_period": _a8r1 <= _j9w2,
            "first_use_date": _b8d6,
            "free_period_end": _x9r7,
            "_h4c6": _e2a5,
        }
    except Exception:
        return {
            "in_free_period": True,
            "first_use_date": _b8d6,
            "free_period_end": _x9r7,
            "_h4c6": FREE_PERIOD_DAYS,
        }


def get_current_tier() -> str:
    """获取当前会员等级"""
    _f9q2 = _l1r4()
    return _f9q2.get("_w1b8", TIER_FREE)


def get_machine_id() -> str:
    """获取当前机器码"""
    return _s0f0()


# ==================== AI 平台手动声明 API ====================
# 解决 Bug1：机器码因 PPID 不稳定而频繁变化
# 用户首次启动时，AI 询问"您当前正在使用哪个 AI 软件？"，
# AI 调用 set_ai_platform() 把答案写入 ~/.mc-skill/platform.txt。
# 后续 _detect_ai_platform() 优先读这个文件，保证机器码稳定。

def get_current_platform() -> str:
    """获取当前 AI 平台声明（用户手动或自动检测）

    Returns:
        平台标识字符串，若用户从未声明且自动检测也失败，返回 "unknown"
    """
    _p = _detect_ai_platform()
    if _p.startswith("unknown-"):
        return "unknown"
    return _p


def set_ai_platform(platform: str) -> bool:
    """设置 AI 平台（写入 ~/.mc-skill/platform.txt，触发机器码重建）

    Args:
        platform: 平台标识，必须在白名单内（不区分大小写）

    Returns:
        True 成功；False 失败或参数非法
    """
    if not platform or not isinstance(platform, str):
        return False
    _v = platform.strip().lower()[:24]
    if not _v:
        return False
    # 白名单校验（custom 允许任意值）
    if _v != "custom" and _v not in SUPPORTED_AI_PLATFORMS:
        return False
    try:
        _dir = Path.home() / ".mc-skill"
        _dir.mkdir(parents=True, exist_ok=True)
        _file = _dir / "platform.txt"
        # 仅在平台变更时清理旧 salt，强制生成新机器码
        _old = ""
        if _file.exists():
            _old = _file.read_text(encoding="utf-8").strip().lower()
        _file.write_text(_v, encoding="utf-8")
        # 首次声明时，清理掉兜底生成的 salt 文件
        # （V1.0.5: 兜底改为固定 "unknown"，salt 文件名为 machine_salt_unknown；
        #  旧版本可能存在 machine_salt_unknown-<ppid> 形式的残留，一并清理）
        if not _old:
            for _stale in list(_dir.glob("machine_salt_unknown")) + list(_dir.glob("machine_salt_unknown-*")):
                try:
                    _stale.unlink()
                except Exception:
                    pass
        elif _old != _v:
            # 平台变更：清理旧平台对应的 salt
            _old_salt = _dir / f"machine_salt_{_old}"
            if _old_salt.exists():
                try:
                    _old_salt.unlink()
                except Exception:
                    pass
        return True
    except Exception:
        return False


def reset_machine_id() -> str:
    """手动重置机器码（删除所有 salt，强制下次生成新机器码）

    使用场景：
      - 用户更换了 AI 软件
      - 用户重装系统后
      - 调试时希望换一个干净机器码

    Returns:
        新的机器码（已生成并落盘）
    """
    try:
        _dir = Path.home() / ".mc-skill"
        if _dir.exists():
            for _f in _dir.glob("machine_salt_*"):
                try:
                    _f.unlink()
                except Exception:
                    pass
    except Exception:
        pass
    return _s0f0()


def is_platform_declared() -> bool:
    """用户是否已经手动声明过 AI 平台（用于 AI 决定是否需要询问）"""
    try:
        _file = Path.home() / ".mc-skill" / "platform.txt"
        return _file.exists()
    except Exception:
        return False


def get_usage_stats() -> Dict[str, Any]:
    """获取使用统计"""
    _f9q2 = _l1r4()
    _f9q2 = _z6m9(_f9q2)
    _f3j4 = _f9q2.get("_w1b8", TIER_FREE)
    _m6c4 = _f9q2.get("_z6m9", {})
    _a9t8 = _f9q2.get("total_usage", {})
    _g0r0 = DAILY_LIMITS.get(_f3j4, DAILY_LIMITS[TIER_FREE])
    _e0h7 = get_free_period_info()

    return {
        "_g8i7": _f9q2.get("_g8i7", ""),
        "_w1b8": _f3j4,
        "tier_name": _i7t7(_f3j4),
        "_z6m9": _m6c4,
        "total_usage": _a9t8,
        "_j7d2": _g0r0,
        "payment_enabled": ENABLE_PAYMENT,
        "_i2v1": _f9q2.get("_i2v1", ""),
        "license_expires": _f9q2.get("license_expires", ""),
        "_z0z5": _f9q2.get("_z0z5", ""),
        "first_use_date": _f9q2.get("first_use_date", ""),
        "free_period_end": _f9q2.get("free_period_end", ""),
        "in_free_period": _e0h7["in_free_period"],
        "_h4c6": _e0h7["_h4c6"],
        "pricing": _a7h4,
        "premium_status": t("auth._w1b8.coming_soon"),
    }


# ==================== V1.0.5 版本锁死：缓存上次服务器返回的 version_status ====================
# _h8d3 联网验证后会把服务器响应里的 version_status 字段写入这个缓存
# check_permission 启动时读取此缓存，若 status=="locked" 则直接弹升级页面并拒绝使用
_CACHED_VERSION_STATUS: Optional[Dict[str, Any]] = None


def _set_cached_version_status(vsi: Optional[Dict[str, Any]]) -> None:
    """供 _h8d3 调用：缓存服务器返回的 version_status 字段"""
    global _CACHED_VERSION_STATUS
    _CACHED_VERSION_STATUS = vsi


def _get_cached_version_status() -> Optional[Dict[str, Any]]:
    """读取上次服务器返回的 version_status；未联网或服务器未返回时为 None"""
    return _CACHED_VERSION_STATUS


# ==================== V1.0.5 管理员批量升级通知：缓存 upgrade_notice ====================
# 管理员在后台点击「批量通知升级」后，服务器在 registry 中标记 upgrade_notice_at
# 客户端 quick_check 返回 upgrade_notice.has_notice=True 时，这里缓存并在 check_permission 弹窗
_CACHED_UPGRADE_NOTICE: Optional[Dict[str, Any]] = None


def _set_cached_upgrade_notice(uni: Optional[Dict[str, Any]]) -> None:
    """供 _h8d3 调用：缓存服务器返回的 upgrade_notice 字段"""
    global _CACHED_UPGRADE_NOTICE
    _CACHED_UPGRADE_NOTICE = uni


def _get_cached_upgrade_notice() -> Optional[Dict[str, Any]]:
    """读取上次服务器返回的 upgrade_notice；未联网或无通知时为 None"""
    return _CACHED_UPGRADE_NOTICE


# ==================== V1.0.5 版本提醒频率控制（宽限期内每周提醒一次） ====================
# 宽限期内的升级提醒频率：每周一次（避免频繁打扰用户）
_VERSION_REMIND_FILE = config.OUTPUT_DIR / "version_remind.json"
VERSION_REMIND_INTERVAL_DAYS = 7  # 宽限期内提醒间隔天数


def _should_version_remind() -> bool:
    """判断是否需要弹出版本升级提醒（宽限期内每周一次）

    Returns:
        True=需要提醒, False=本周已提醒过
    """
    try:
        if not _VERSION_REMIND_FILE.exists():
            return True
        with open(_VERSION_REMIND_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        last = data.get("last_remind", "")
        if not last:
            return True
        from datetime import datetime
        last_dt = datetime.fromisoformat(last)
        days = (datetime.now() - last_dt).days
        return days >= VERSION_REMIND_INTERVAL_DAYS
    except Exception:
        return True


def _record_version_remind() -> None:
    """记录本次版本提醒时间，用于控制下次提醒间隔"""
    try:
        config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        from datetime import datetime
        data = {"last_remind": datetime.now().isoformat(timespec="seconds")}
        tmp = _VERSION_REMIND_FILE.with_suffix(".json.tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, _VERSION_REMIND_FILE)
    except Exception:
        pass


def check_permission(_h0e2: str, _f2f4: str = FUNC_AUTO) -> Dict[str, Any]:
    """检查功能使用权限

    权限判断逻辑：
    0. 配置完整性校验（防篡改）
    0.5. 强制联网验证（每次调用）
    1. 如果在免费期内（前7天）：
       - 移植评估功能：首次免费，之后每天1次
       - 其他功能：不限次数
    2. 如果免费期已过：
       - 自动应用基础限制（免费用户5次/天，普通会员100次/天）
       - ENABLE_PAYMENT 只控制是否显示付费提示和允许升级
    """
    # === V1.0.5 版本过低锁死检查（前置） ===
    # 服务器返回 version_status 字段时，客户端据此弹出升级页面
    # locked: 直接锁死，弹升级页面，拒绝使用
    # grace_period: 不锁死，但每周提醒一次升级（不影响使用）
    try:
        _vsi = _get_cached_version_status()
        if _vsi and isinstance(_vsi, dict):
            _vs_status = _vsi.get("status", "")
            if _vs_status == "locked":
                _uv = _vsi.get("user_version", "")
                _lv = _vsi.get("latest_version", "")
                _gr = _vsi.get("grace_remaining_days", 0)
                _rs = _vsi.get("reason", "当前版本过低，已无法继续使用")
                try:
                    from core.payment_page import show_version_upgrade_page
                    show_version_upgrade_page(
                        user_version=_uv,
                        latest_version=_lv,
                        grace_remaining_days=_gr,
                        reason=_rs,
                    )
                except Exception:
                    pass
                return {
                    "authorized": False,
                    "tier": "free",
                    "remaining": 0,
                    "limit": 0,
                    "reason": f"[版本锁死] {_rs}",
                    "version_locked": True,
                }
            elif _vs_status == "grace_period":
                # 宽限期内：不锁死，但每周提醒一次升级
                _remind = _should_version_remind()
                if _remind:
                    _uv = _vsi.get("user_version", "")
                    _lv = _vsi.get("latest_version", "")
                    _gr = _vsi.get("grace_remaining_days", 0)
                    _rs = _vsi.get("reason", "有新版本可用")
                    try:
                        from core.payment_page import show_version_upgrade_page
                        show_version_upgrade_page(
                            user_version=_uv,
                            latest_version=_lv,
                            grace_remaining_days=_gr,
                            reason=_rs,
                            is_grace_period=True,
                        )
                    except Exception:
                        pass
                    _record_version_remind()
    except Exception:
        pass

    # === V1.0.5 管理员批量升级通知检查（前置） ===
    # 管理员在后台点击「批量通知升级」后，服务器标记 upgrade_notice_at
    # 客户端收到 upgrade_notice.has_notice=True 且目标版本高于当前版本时，
    # 弹出升级提示页（不锁死，仅提醒；频率同宽限期：每周一次）
    try:
        _uni = _get_cached_upgrade_notice()
        if _uni and isinstance(_uni, dict) and _uni.get("has_notice"):
            _notice_ver = str(_uni.get("notice_version", "") or "")
            _cur_ver = getattr(config, "VERSION", "")
            _need_notice = False
            if _notice_ver and _cur_ver:
                # 解析版本号对比：只有目标版本比当前版本新才提醒
                from core.version_checker import _parse_version as _pv
                _need_notice = _pv(_notice_ver) > _pv(_cur_ver)
            if _need_notice and _should_version_remind():
                try:
                    from core.payment_page import show_version_upgrade_page
                    show_version_upgrade_page(
                        user_version=_cur_ver,
                        latest_version=_notice_ver,
                        grace_remaining_days=0,
                        reason="管理员已发布新版本通知，建议尽快升级以获得最新功能和修复",
                        is_grace_period=True,
                    )
                except Exception:
                    pass
                _record_version_remind()
    except Exception:
        pass

    # === 配置完整性校验（防篡改）===
    _l0b3 = _b0o1()
    if not _l0b3["ok"]:
        # 检测到配置被篡改，直接拒绝（但免费期内仍保留降级）
        _f9q2 = _l1r4()
        _e0h7 = get_free_period_info()
        if not _e0h7["in_free_period"] and _f9q2.get("_w1b8", TIER_FREE) == TIER_FREE:
            return {
                "allowed": False,
                "_w1b8": TIER_FREE,
                "remaining": 0,
                "_e2a5": 0,
                "reason": "⚠️ 检测到客户端配置被修改，请重新下载安装包！",
                "online": False,
                "_tampered": True,
            }
        _f4x3.warning(_l0b3["_d3g3"])
    
    # === 强制联网验证 ===
    _c0d1 = _h8d3()
    if not _c0d1.get("success"):
        # 联网验证失败，拒绝使用
        return {
            "allowed": False,
            "_w1b8": TIER_FREE,
            "remaining": 0,
            "_e2a5": 0,
            "reason": f"授权验证失败: {_c0d1.get('reason', '未知错误')}",
            "online": _c0d1.get("online", False),
        }
    
    _f9q2 = _l1r4()
    _f9q2 = _z6m9(_f9q2)

    # === 特殊功能：模组移植可行性评估 ===
    if _h0e2 == SPECIAL_FEATURE_MIGRATION_ASSESS:
        return _a3w4(_f9q2)

    # === 免费期内：其他功能不限 ===
    _e0h7 = get_free_period_info()
    if _e0h7["in_free_period"]:
        return {
            "allowed": True,
            "_w1b8": _f9q2.get("_w1b8", TIER_FREE),
            "remaining": -1,
            "_e2a5": -1,
            "reason": t("auth.free_period_remaining", days=_e0h7["_h4c6"]),
        }

    # === 免费期过后：自动应用基础限制 ===
    _f3j4 = _f9q2.get("_w1b8", TIER_FREE)
    _g0r0 = DAILY_LIMITS.get(_f3j4, DAILY_LIMITS[TIER_FREE])
    _b8a7 = _g0r0.get(_f2f4, 20)

    _m6c4 = _f9q2.get("_z6m9", {})
    _i2v1 = _m6c4.get(_h0e2, 0)

    if _i2v1 >= _b8a7:
        # 构建提示信息 + 触发支付页面
        if ENABLE_PAYMENT:
            _j6c9 = t("auth.upgrade_hint_enable", max=100)
            _z0z5 = False
            try:
                from core.payment_page import show_payment_page
                _e1q6 = f"{t('auth.limit_reached', _i2v1=_b8a7, _b8a7=_b8a7)}, {t('auth.upgrade_hint_enable', max=100)}"
                show_payment_page(reason=_e1q6, mode="_e2a5")
                _z0z5 = True
            except Exception:
                pass
            # reason 末段明确标注「已生成支付页面」，防止 AI Agent 忽略链接
            _u6m3 = t("auth.payment_page_generated") if _z0z5 else ""
            _j6c9 = _j6c9 + (f"，{_u6m3}" if _u6m3 else "")
        else:
            _j6c9 = t("auth.upgrade_hint_disable")
        return {
            "allowed": False,
            "_w1b8": _f3j4,
            "remaining": 0,
            "_e2a5": _b8a7,
            "reason": f"{t('auth.limit_reached', _i2v1=_b8a7, _b8a7=_b8a7)}, {_j6c9}",
        }

    return {
        "allowed": True,
        "_w1b8": _f3j4,
        "remaining": _b8a7 - _i2v1,
        "_e2a5": _b8a7,
        "reason": "",
    }


def _a3w4(_f9q2: Dict[str, Any]) -> Dict[str, Any]:
    """检查模组移植可行性评估功能的权限

    规则：
    - 免费期内：首次免费，之后每天1次
    - 付费期后：免费用户每天1次，普通会员每天5次
    """
    _e0h7 = get_free_period_info()
    _f3j4 = _f9q2.get("_w1b8", TIER_FREE)

    # 首次使用免费
    _z2y3 = _f9q2.get("migration_assess_first_used", False)
    _a8r1 = _w9c5()
    _m6c4 = _f9q2.get("_z6m9", {})
    _f1c4 = _m6c4.get(SPECIAL_FEATURE_MIGRATION_ASSESS, 0)

    if _e0h7["in_free_period"]:
        # 免费期内
        if not _z2y3:
            # 首次使用，免费
            return {
                "allowed": True,
                "_w1b8": _f3j4,
                "remaining": 1,
                "_e2a5": 1,
                "reason": t("auth.migration_assess_first_free"),
                "is_first_use": True,
            }
        else:
            if _f1c4 >= 1:
                return {
                    "allowed": False,
                    "_w1b8": _f3j4,
                    "remaining": 0,
                    "_e2a5": 1,
                    "reason": t("auth.migration_assess_limit_reached", count=1),
                    "is_first_use": False,
                }
            return {
                "allowed": True,
                "_w1b8": _f3j4,
                "remaining": 1 - _f1c4,
                "_e2a5": 1,
                "reason": t("auth.migration_assess_daily_free", count=1),
                "is_first_use": False,
            }
    else:
        # 付费期（免费期结束后自动应用限制）
        _g0r0 = DAILY_LIMITS.get(_f3j4, DAILY_LIMITS[TIER_FREE])
        _b8a7 = _g0r0.get(SPECIAL_FEATURE_MIGRATION_ASSESS, 1)

        if _f1c4 >= _b8a7:
            if ENABLE_PAYMENT:
                _j6c9 = t("auth.upgrade_hint_enable", max=5)
                _z0z5 = False
                try:
                    from core.payment_page import show_payment_page
                    _e1q6 = f"{t('auth.limit_reached', _i2v1=_b8a7, _b8a7=_b8a7)}, {t('auth.upgrade_hint_enable', max=5)}"
                    show_payment_page(reason=_e1q6, mode="_e2a5")
                    _z0z5 = True
                except Exception:
                    pass
                _u6m3 = t("auth.payment_page_generated") if _z0z5 else ""
                _j6c9 = _j6c9 + (f"，{_u6m3}" if _u6m3 else "")
            else:
                _j6c9 = t("auth.upgrade_hint_disable")
            return {
                "allowed": False,
                "_w1b8": _f3j4,
                "remaining": 0,
                "_e2a5": _b8a7,
                "reason": f"{t('auth.limit_reached', _i2v1=_b8a7, _b8a7=_b8a7)}, {_j6c9}",
                "is_first_use": not _z2y3,
            }

        return {
            "allowed": True,
            "_w1b8": _f3j4,
            "remaining": _b8a7 - _f1c4,
            "_e2a5": _b8a7,
            "reason": "",
            "is_first_use": not _z2y3,
        }


def record_usage(_h0e2: str) -> None:
    """记录一次功能使用（含数据上报）

    使用次数绑定机器码，跨会话共享（存储在本地 auth_state.json）。
    V1.0.5: 加文件锁防止多会话并发时计数丢失。
    """
    with _StateLock(timeout=5.0):
        _f9q2 = _l1r4()
        _f9q2 = _z6m9(_f9q2)
        _m6c4 = _f9q2.get("_z6m9", {})
        _a9t8 = _f9q2.get("total_usage", {})

        _m6c4[_h0e2] = _m6c4.get(_h0e2, 0) + 1
        _a9t8[_h0e2] = _a9t8.get(_h0e2, 0) + 1

        # 移植评估特殊：标记首次使用
        if _h0e2 == SPECIAL_FEATURE_MIGRATION_ASSESS:
            _f9q2["migration_assess_first_used"] = True

        _f9q2["_z6m9"] = _m6c4
        _f9q2["total_usage"] = _a9t8
        _m6x0(_f9q2)

        _f4x3.debug(f"记录使用: {_h0e2}, 今日={_m6c4[_h0e2]}, 总计={_a9t8[_h0e2]}")

    # === 数据上报（本地缓存，每10分钟统一上报一次）===
    _e4j9(_h0e2, 1)


def activate_license(_n6f3: str, _f3j4: str = TIER_NORMAL,
                     _g8s6: str = "", _f6p5: str = "monthly") -> Dict[str, Any]:
    """激活授权码（支持续费叠加兜底，防止管理员误发短日期授权码导致用户损失）

    规则：
    1. 如果用户当前已是付费会员且旧授权仍有效 → 取「旧 _g8s6 与 新 _g8s6」的较大者
       （例如用户年卡还剩 100 天，续费月卡 30 天 → 最终为 年卡原过期日，不会 30 天后过期）
    2. 如果旧授权已过期 / 本来就是免费用户 → 直接采用新 _g8s6
    3. 真正的「精确续费天数叠加」逻辑在管理员服务端生成授权码时计算，
       客户端这里只是做兜底，不反向延长服务端下发的日期。

    Args:
        _n6f3: 授权码
        _f3j4: 会员等级（目前仅支持 normal，premium 为敬请期待）
        _g8s6: 过期时间（YYYY-MM-DD），由管理员服务端计算后下发
        _f6p5: 订阅类型 monthly/monthly_auto/quarterly/yearly
    """
    if _f3j4 == TIER_PREMIUM:
        return {
            "success": False,
            "_w1b8": _f3j4,
            "_d3g3": t("auth.premium_coming_soon"),
        }

    _f9q2 = _l1r4()

    # === 续费兜底：旧 _g8s6（若仍有效）和 新 _g8s6 取较大者 ===
    _f3k0 = _g8s6
    _o1d6 = _f9q2.get("license_expires", "")
    _f9w1 = _f9q2.get("_w1b8", TIER_FREE)
    _z2c3 = date.today()
    try:
        if _o1d6 and _f9w1 != TIER_FREE:
            _h8v6 = datetime.strptime(_o1d6, "%Y-%m-%d").date()
            # 旧授权仍然有效（还没过期）
            if _h8v6 >= _z2c3:
                _h3k3 = datetime.strptime(_g8s6, "%Y-%m-%d").date()
                if _h8v6 > _h3k3:
                    # 旧的有效期比新的更长 → 采用旧的（保护用户权益，比如误发了更短的码）
                    _f3k0 = _o1d6
                    _f4x3.info(
f"[授权激活] 续费兜底：旧 _g8s6({_o1d6}) > 新 _g8s6({_g8s6})，" +
                        f"保留较晚的日期 {_f3k0}"
                    )
    except Exception as e:
        _f4x3.warning(f"[授权激活] 续费兜底计算异常，直接采用新 _g8s6={_g8s6}: {e}")

    _f9q2["_w1b8"] = _f3j4
    _f9q2["_i2v1"] = _n6f3
    _f9q2["license_expires"] = _f3k0
    _f9q2["_z0z5"] = _f6p5

    _m6x0(_f9q2)
    _f4x3.info(f"授权激活成功: _f3j4={_f3j4}, _g8s6={_f3k0}, sub={_f6p5}")

    _d3g3 = _a7h4.get(_f6p5, {}).get("name", _f6p5)
    return {
        "success": True,
        "_w1b8": _f3j4,
        "_i2v1": _n6f3,
        "_j6c9": _f3k0,
        "_z0z5": _f6p5,
        "_d3g3": t("auth.activate_success", _f3j4=_i7t7(_f3j4), subscription=_d3g3, _g8s6=_f3k0),
    }


def verify_license_online(_n6f3: str) -> Dict[str, Any]:
    """在线验证授权码（预留接口）"""
    if not AUTH_SERVER_URL:
        _f4x3.info("未配置在线验证服务器，使用本地验证")
        return {
            "success": False,
            "online": False,
            "reason": "在线验证服务暂未开放，请使用本地激活",
        }

    try:
        from urllib.request import Request, urlopen
        _d9l7 = json.dumps({
            "_i2v1": _n6f3,
            "_g8i7": _s0f0(),
        }).encode("utf-8")

        _g4q7 = Request(
            f"{AUTH_SERVER_URL}/verify",
            data=_d9l7,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "MC-Skill-V1/1.0",
            },
            method="POST",
        )

        with urlopen(_g4q7, timeout=AUTH_SERVER_TIMEOUT, context=_SSL_CONTEXT) as resp:
            _b0b1 = json.loads(resp.read().decode("utf-8"))
            return _b0b1

    except Exception as e:
        _f4x3.error(f"在线验证失败: {e}")
        return {
            "success": False,
            "online": True,
            "reason": f"验证服务连接失败: {str(e)}",
        }


# ==================== 🔐 签名 HTTP 请求 ====================

def _l9a6(_o1v6: str, _h8x6: str, _q8l8: str) -> str:
    """
    计算请求签名 (与服务器 auth_server.py 中的 compute_sign 保持一致)
    
    签名算法: HMAC-SHA256(CLIENT_SIGN_SECRET, _h8x6 + _q8l8 + _o1v6)
    """
    _w9u5 = f"{_h8x6}{_q8l8}{_o1v6}"
    return hmac.new(
        CLIENT_SIGN_SECRET.encode("utf-8"),
        _w9u5.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()


def _y6h9(_w3n4: str, _u7g9: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    发送带签名的 POST 请求到服务器（标准 HTTPS REST + HMAC-SHA256 签名头）

    附加标准签名头:
      - x-timestamp: 当前时间戳（秒），防止重放攻击
      - x-nonce:     随机字符串（防重放）
      - x-signature: HMAC-SHA256 签名（防篡改）

    Args:
        _w3n4: 接口路径，如 "/api/auth/quick-check"
        _u7g9: 请求体字典

    Returns:
        服务器响应的 JSON 字典，失败返回 None
    """
    if not AUTH_SERVER_URL:
        return None

    _timestamp = str(int(time.time()))
    _nonce = secrets.token_hex(8)
    _body_str = json.dumps(_u7g9, ensure_ascii=False)

    # 计算签名: HMAC-SHA256(CLIENT_SIGN_SECRET, timestamp + nonce + body)
    _signature = _l9a6(_body_str, _timestamp, _nonce)

    _body_bytes = _body_str.encode("utf-8")
    _req = Request(
        f"{AUTH_SERVER_URL}{_w3n4}",
        data=_body_bytes,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "MC-Skill-V1/1.0",
            "x-timestamp": _timestamp,
            "x-nonce": _nonce,
            "x-signature": _signature,
        },
        method="POST",
    )

    with urlopen(_req, timeout=AUTH_SERVER_TIMEOUT, context=_SSL_CONTEXT) as resp:
        return json.loads(resp.read().decode("utf-8"))


# ==================== 🔒 配置防篡改检测 ====================

def _b0o1() -> Dict[str, Any]:
    """
    校验关键配置是否被篡改
    
    检测内容:
      1. ENABLE_PAYMENT 开关是否被修改
      2. AUTH_SERVER_URL 是否被替换
      3. CONFIG_FINGERPRINT 是否匹配
    
    Returns:
        {"ok": bool, "tampered_fields": list, "_w9u5": str}
    """
    _b0b1 = {
        "ok": True,
        "tampered_fields": [],
        "_d3g3": "配置完整性校验通过",
    }
    
    # AUTO 模式（开发环境），跳过校验
    if CONFIG_FINGERPRINT == "AUTO":
        return _b0b1
    
    # 计算当前指纹并与预设比较
    _n7a9 = _p8k3()
    if _n7a9 != CONFIG_FINGERPRINT:
        _b0b1["ok"] = False
        _b0b1["tampered_fields"].append("global_config")
        _b0b1["_d3g3"] = (
f"⚠️  检测到关键配置被篡改！" +
            f"预期指纹: {CONFIG_FINGERPRINT[:8]}... " +
            f"实际指纹: {_n7a9[:8]}..."
        )
        _f4x3.warning(_b0b1["_d3g3"])
    
    return _b0b1


# ==================== 强制联网验证与数据上报 ====================

def _h8d3() -> Dict[str, Any]:
    """强制联网验证（每次使用Skill时调用）
    
    流程：
    1. 检查本地Token是否有效（有效期1小时）
    2. Token无效则请求服务器获取新Token
    3. 返回验证结果（成功/失败/离线降级）
    
    Returns:
        {
            "success": bool,      # 验证是否通过
            "online": bool,       # 是否在线模式
            "_f3j4": str,          # 服务器确认的会员等级
            "reason": str,        # 失败原因（如有）
        }
    """
    _f9q2 = _l1r4()
    _d3e9 = _f9q2.get("_g8i7", "")
    
    # 检查是否启用了强制联网验证
    if not _f9q2.get("online_verify_enabled", False) or not AUTH_SERVER_URL:
        return {
            "success": True,
            "online": False,
            "_w1b8": _f9q2.get("_w1b8", TIER_FREE),
            "reason": "离线模式（未启用强制验证）",
        }
    
    # 检查本地Token是否有效
    _m1e0 = _f9q2.get("server_token_expires", "")
    _j1a9 = datetime.now()
    
    if _m1e0:
        try:
            _g0v5 = datetime.fromisoformat(_m1e0)
            if _j1a9 < _g0v5:
                # Token仍有效，直接使用
                _f4x3.debug(f"使用有效Token: 过期时间 {_m1e0}")
                return {
                    "success": True,
                    "online": True,
                    "_w1b8": _f9q2.get("_w1b8", TIER_FREE),
                    "reason": "",
                }
        except ValueError:
            pass
    
    # Token无效，请求服务器获取新Token（使用签名请求）
    try:
        # 使用带签名的请求
        _b0b1 = _y6h9("/api/auth/quick-check", {
            "_g8i7": _d3e9,
            "_h8v6": _j1a9.isoformat(),
            "machine_id": _d3e9,
            "client_version": getattr(config, "VERSION", ""),
            "ai_platform": _detect_ai_platform(),
            "device_info": _get_device_info(),
        })
        
        if _b0b1 is None:
            raise URLError("签名请求失败")
            
        # 服务器响应成功（无论是否授权）
        _c5o3 = _b0b1.get("success") or _b0b1.get("authorized") is not None

        # V1.0.5: 缓存服务器返回的 version_status（用于版本锁死检查）
        try:
            _set_cached_version_status(_b0b1.get("version_status"))
        except Exception:
            pass

        # V1.0.5: 缓存服务器返回的 upgrade_notice（管理员批量升级通知）
        try:
            _set_cached_upgrade_notice(_b0b1.get("upgrade_notice"))
        except Exception:
            pass

        if _c5o3:
            # 更新本地Token（如果有）
            if _b0b1.get("token"):
                _f9q2["server_token"] = _b0b1.get("token", "")
                _f9q2["server_token_expires"] = _b0b1.get("_j6c9", "")
            
            _f9q2["last_online_check"] = _j1a9.isoformat()
            
            # 检查是否授权
            if _b0b1.get("authorized"):
                # 同步服务器端的会员等级
                _g1a5 = _b0b1.get("_w1b8", "")
                if _g1a5 and _g1a5 != _f9q2.get("_w1b8"):
                    _f9q2["_w1b8"] = _g1a5
                    _f4x3.info(f"服务器同步会员等级: {_g1a5}")
                
                _m6x0(_f9q2)
                
                return {
                    "success": True,
                    "online": True,
                    "_w1b8": _f9q2.get("_w1b8", TIER_FREE),
                    "reason": "",
                }
            else:
                # 服务器连接成功，但用户未授权
                _m6x0(_f9q2)
                return {
                    "success": False,
                    "online": True,
                    "_w1b8": TIER_FREE,
                    "reason": _b0b1.get("reason", "服务器验证失败"),
                }
        else:
            # 服务器返回失败
            return {
                "success": False,
                "online": True,
                "_w1b8": TIER_FREE,
                "reason": _b0b1.get("_d3g3") or _b0b1.get("reason", "服务器验证失败"),
            }
                
    except (URLError, OSError) as e:
        # 网络连接失败，降级处理
        _f4x3.warning(f"联网验证失败，降级为离线模式: {e}")
        _f9q2["last_online_check"] = _j1a9.isoformat()
        # 记录联网验证失败时间（供操作台审计，判断用户是否拒绝网络访问）
        _f9q2["last_verify_fail_time"] = _j1a9.isoformat()
        _m6x0(_f9q2)

        # 检查是否允许离线使用（免费期内或有本地授权）
        _r0p5 = _f9q2.get("_w1b8", TIER_FREE)
        _e0h7 = get_free_period_info()
        
        if _e0h7.get("in_free_period") or _r0p5 != TIER_FREE:
            # 免费期内或已有本地授权，允许离线使用
            return {
                "success": True,
                "online": False,
                "_w1b8": _r0p5,
                "reason": f"网络不可用，降级离线模式（{str(e)[:50]}）",
            }
        else:
            # 免费期已过且无本地授权，拒绝使用
            return {
                "success": False,
                "online": False,
                "_w1b8": TIER_FREE,
                "reason": f"网络不可用，无法验证授权（{str(e)[:50]}）",
            }
    except Exception as e:
        _f4x3.error(f"联网验证异常: {e}")
        return {
            "success": False,
            "online": False,
            "_w1b8": TIER_FREE,
            "reason": f"验证异常: {str(e)[:50]}",
        }


def _h2j4() -> bool:
    """检查是否应该上报数据（每10分钟一次）"""
    _f9q2 = _l1r4()
    _v6c1 = _f9q2.get("last_report_time", "")
    
    if not _v6c1:
        # 从未上报过，应该立即上报
        return True
    
    try:
        _w7j9 = datetime.fromisoformat(_v6c1)
        _j1a9 = datetime.now()
        _o4a3 = timedelta(days=REPORT_INTERVAL_DAYS)
        return (_j1a9 - _w7j9) >= _o4a3
    except (ValueError, TypeError):
        return True


def _e4j9(_h0e2: str, _e2v5: int) -> None:
    """上报使用数据到管理员服务器
    
    机制：
    1. 每次使用Skill时调用
    2. 本地缓存使用数据
    3. 每10分钟统一上报一次
    4. 上报成功后清除缓存
    
    Args:
        _h0e2: 使用的功能名称
        _e2v5: 本次使用次数（通常为1）
    """
    # 用户隐私退出：设置环境变量 MC_SKILL_NO_REPORT=1 可禁用所有数据上报
    if os.environ.get("MC_SKILL_NO_REPORT", "").strip() in ("1", "true", "TRUE", "True", "yes", "YES", "on", "ON"):
        return

    _f9q2 = _l1r4()
    _j1a9 = datetime.now()
    
    # 添加新的使用记录到本地缓存
    _h8g8 = _f9q2.get("pending_reports", [])
    _h8g8.append({
        "_f5e5": _h0e2,
        "count": _e2v5,
        "_h8v6": _j1a9.isoformat(),
    })
    
    # 如果缓存超过最大限制，保留最近的记录
    if len(_h8g8) > MAX_PENDING_RECORDS:
        _h8g8 = _h8g8[-MAX_PENDING_RECORDS:]
    
    _f9q2["pending_reports"] = _h8g8
    
    # 检查是否应该立即上报
    if _h2j4() and AUTH_SERVER_URL:
        _x4f7(_f9q2)
    else:
        # 只是保存缓存
        _m6x0(_f9q2)


def _x4f7(_f9q2: Dict[str, Any]) -> None:
    """执行数据上报（使用签名请求）"""
    _h8g8 = _f9q2.get("pending_reports", [])
    
    if not _h8g8:
        return
    
    try:
        _d3e9 = _f9q2.get("_g8i7", "")
        _j1a9 = datetime.now()
        
        # 准备上报数据
        _d2t8 = {
            "_g8i7": _d3e9,
            "report_time": _j1a9.isoformat(),
            "usage_records": _h8g8,
            "_v6c1": {
                "_w1b8": _f9q2.get("_w1b8", TIER_FREE),
                "total_usage": _f9q2.get("total_usage", {}),
                "first_use_date": _f9q2.get("first_use_date", ""),
            }
        }
        
        # 使用带签名的请求发送到服务器
        _b0b1 = _y6h9("/api/auth/report-usage", _d2t8)
        
        if _b0b1 is None:
            raise URLError("签名请求失败")
        
        if _b0b1.get("success"):
            # 上报成功，清除缓存
            _f9q2["pending_reports"] = []
            _f9q2["last_report_time"] = _j1a9.isoformat()
            _m6x0(_f9q2)
            _f4x3.info(f"使用数据上报成功: {len(_h8g8)} 条记录")
        else:
            _f4x3.warning(f"数据上报失败: {_b0b1.get('_w9u5', '未知错误')}")
            _m6x0(_f9q2)  # 保存缓存，下次再试
            
    except Exception as e:
        _f4x3.warning(f"数据上报异常: {e}")
        # 上报失败，保留缓存等待下次
    
    # 保存当前状态
    _m6x0(_f9q2)


def get_report_status() -> Dict[str, Any]:
    """获取数据上报状态（供管理员查看）"""
    _f9q2 = _l1r4()
    return {
        "last_report_time": _f9q2.get("last_report_time", ""),
        "pending_count": len(_f9q2.get("pending_reports", [])),
        "pending_activity_events": len(_f9q2.get("pending_activity_events", [])),
        "last_verify_fail_time": _f9q2.get("last_verify_fail_time", ""),
        "should_report": _h2j4(),
        "server_url": AUTH_SERVER_URL or "未配置",
        "online_verify_enabled": _f9q2.get("online_verify_enabled", False),
    }


def reset_usage() -> None:
    """重置使用计数（调试用）"""
    _f9q2 = _l1r4()
    _f9q2["_z6m9"] = {}
    _f9q2["total_usage"] = {}
    _f9q2["last_reset_date"] = _w9c5()
    _m6x0(_f9q2)
    _f4x3.info("使用计数已重置")


def set_tier(_f3j4: str) -> None:
    """设置会员等级（调试/管理用）"""
    _f9q2 = _l1r4()
    _f9q2["_w1b8"] = _f3j4
    _m6x0(_f9q2)
    _f4x3.info(f"会员等级已设置为: {_f3j4}")


def reset_free_period() -> None:
    """重置免费期（调试用，清除首次使用日期）"""
    _f9q2 = _l1r4()
    _f9q2["first_use_date"] = ""
    _f9q2["free_period_end"] = ""
    _f9q2["migration_assess_first_used"] = False
    _m6x0(_f9q2)
    _f4x3.info("免费期已重置")


def enable_payment() -> None:
    """启用付费限制（全局）"""
    global ENABLE_PAYMENT
    ENABLE_PAYMENT = True
    _f4x3.info("付费限制已启用")


def disable_payment() -> None:
    """禁用付费限制（全局）"""
    global ENABLE_PAYMENT
    ENABLE_PAYMENT = False
    _f4x3.info("付费限制已禁用")


def print_auth_status() -> None:
    """打印当前授权状态"""
    _w5r5 = get_usage_stats()
    print("=" * 55, flush=True)
    print(f"  {t('banner.title')} - {t('auth.title')}", flush=True)
    print("=" * 55, flush=True)
    print(f"  {t('auth.machine_id')}: {_w5r5['_g8i7']}", flush=True)
    print(f"  {t('auth.member_tier')}: {_w5r5['tier_name']}", flush=True)
    print(f"  {t('auth.payment_methods')}: {'✅' if _w5r5['payment_enabled'] else '⏳'}", flush=True)
    print(f"  {t('auth.auth_code')}: {_w5r5['_i2v1'] or t('auth.not_activated')}", flush=True)
    print(f"  {t('auth.expiry_date')}: {_w5r5['license_expires'] or '—'}", flush=True)

    # 免费期信息
    if _w5r5["in_free_period"]:
        print(f"\n  ┌─────────────────────────────────", flush=True)
        print(f"  │  {t('auth.free_period')} ({t('auth.remaining')} {_w5r5['_h4c6']} days)", flush=True)
        print(f"  │  {t('auth.first_use_date')}: {_w5r5['first_use_date'] or '—'}", flush=True)
        print(f"  │  {t('auth.free_until')}: {_w5r5['free_period_end'] or '—'}", flush=True)
        print(f"  └─────────────────────────────────", flush=True)
    else:
        print(f"\n  ┌─────────────────────────────────", flush=True)
        print(f"  │  {t('auth.free_period')}: {t('auth.expired')} ({_w5r5['free_period_end']})", flush=True)
        print(f"  │  {t('auth.free')}: {_w5r5['_j7d2'].get('auto', 20)}/day", flush=True)
        print(f"  └─────────────────────────────────", flush=True)

    # 使用统计
    print(f"\n  {t('auth.today_usage')}:", flush=True)
    for feat, count in _w5r5["_z6m9"].items():
        _s2e4 = {"migration_assess": t("_f5e5.f9.name")}.get(feat, feat)
        _b8a7 = _w5r5["_j7d2"].get(feat, _w5r5["_j7d2"].get("auto", 20))
        if _b8a7 > 0:
            print(f"    {_s2e4}: {count}/{_b8a7}", flush=True)
        else:
            print(f"    {_s2e4}: {count} ({t('auth.unlimited')})", flush=True)
    if not _w5r5["_z6m9"]:
        print(f"    ({t('common.no_data')})", flush=True)

    print(f"\n  {t('auth.total_usage')}:", flush=True)
    for feat, count in _w5r5["total_usage"].items():
        _s2e4 = {"migration_assess": t("_f5e5.f9.name")}.get(feat, feat)
        print(f"    {_s2e4}: {count}", flush=True)
    if not _w5r5["total_usage"]:
        print(f"    ({t('common.no_data')})", flush=True)

    # 定价信息
    print(f"\n  {t('auth.member_subscription')}:", flush=True)
    for key, info in _w5r5["pricing"].items():
        print(f"    {info['name']}: {info['price']}{info['unit']} ({info['desc']})", flush=True)

    # 单次按需付费：仅作者设备可见（V1阶段功能未实现，对普通用户隐藏）
    if _o1d0():
        print(f"\n  {t('auth.per_use_payment')} {t('auth.author_test_only')}:", flush=True)
        for key, info in _c5b3.items():
            print(f"    {info['name']}: {info['price']} CNY/use", flush=True)

    print(f"\n  {t('auth.premium_coming_soon')}", flush=True)
    print("=" * 55, flush=True)


def get_auth_status_json() -> Dict[str, Any]:
    """获取授权状态（JSON格式，供API调用）

    Returns:
        包含完整授权信息的字典，结构与 get_usage_stats() 一致
    """
    _w5r5 = get_usage_stats()
    # 添加额外的可用信息
    _w5r5["payment_enabled"] = ENABLE_PAYMENT
    _w5r5["auth_server_url"] = AUTH_SERVER_URL
    _w5r5["free_period_days"] = FREE_PERIOD_DAYS
    return _w5r5


def get_available_plans() -> Dict[str, Any]:
    """获取可用套餐列表（供API调用和命令行显示）

    Returns:
        {
            "_k1y5": {...},          # 普通会员订阅套餐
            "per_use": {...} | None, # 单次按需付费（仅作者设备可见）
            "premium_coming_soon": bool,  # 高级会员是否敬请期待
            "_n3f1": {...},      # 各等级说明
            "_i1y4": {...},   # 各等级每日限制
        }
    """
    _g1y1 = _o1d0()

    _n3f1 = {
        TIER_FREE: {
            "name": _i7t7(TIER_FREE),
            "desc": "免费用户",
            "_j7d2": DAILY_LIMITS.get(TIER_FREE, {}),
        },
        TIER_NORMAL: {
            "name": _i7t7(TIER_NORMAL),
            "desc": "普通会员",
            "_j7d2": DAILY_LIMITS.get(TIER_NORMAL, {}),
        },
        TIER_PREMIUM: {
            "name": _i7t7(TIER_PREMIUM),
            "desc": "敬请期待",
            "coming_soon": True,
        },
    }

    _b0b1 = {
        "_e2v5": _a7h4,
        "per_use": _c5b3 if _g1y1 else None,
        "premium_coming_soon": True,
        "_e4j9": _n3f1,
        "_j7d2": DAILY_LIMITS,
        "free_period_days": FREE_PERIOD_DAYS,
        "payment_enabled": ENABLE_PAYMENT,
    }
    return _b0b1


def print_available_plans() -> None:
    """打印可用套餐列表（命令行格式）"""
    _k1y5 = get_available_plans()
    _g1y1 = _k1y5["per_use"] is not None

    print("=" * 60, flush=True)
    print(f"  {t('banner.title')} - 套餐列表", flush=True)
    print("=" * 60, flush=True)

    # 会员等级说明
    print(f"\n  📊 会员等级说明:", flush=True)
    for tier_key, _n3f1 in _k1y5["_e4j9"].items():
        if _n3f1.get("coming_soon"):
            print(f"    {_n3f1['name']}: {_n3f1['desc']}", flush=True)
        else:
            _g0r0 = _n3f1.get("_j7d2", {})
            _c7q6 = _g0r0.get(FUNC_AUTO, "-")
            _l5e2 = _g0r0.get(FUNC_SEMI, "-")
            _p3z4 = _g0r0.get(SPECIAL_FEATURE_MIGRATION_ASSESS, "-")
            print(f"    {_n3f1['name']}: 全自动{_c7q6}次/天, 半自动{_l5e2}次/天, 移植评估{_p3z4}次/天", flush=True)

    # 免费期说明
    print(f"\n  🎁 免费期: 首次使用起 {_k1y5['free_period_days']} 天内，除移植评估外所有功能不限次数", flush=True)

    # 普通会员套餐
    print(f"\n  💎 {t('auth.member_subscription')}:", flush=True)
    for key, info in _k1y5["_e2v5"].items():
        print(f"    [{key}] {info['name']}: {info['price']}{info['unit']}  —  {info['desc']}", flush=True)

    # 单次按需付费（仅作者设备）
    if _g1y1:
        print(f"\n  ⚡ 单次按需付费 {t('auth.author_test_only')}:", flush=True)
        for key, info in _k1y5["per_use"].items():
            print(f"    [{key}] {info['name']}: {info['price']} 元/次", flush=True)

    # 高级会员
    if _k1y5["premium_coming_soon"]:
        print(f"\n  🌟 {t('auth.premium_coming_soon')}", flush=True)

    # 付款状态
    if _k1y5["payment_enabled"]:
        print(f"\n  ✅ 付费系统已启用", flush=True)
    else:
        print(f"\n  ⏳ 付费系统即将开放，当前仍可享受免费使用", flush=True)

    print("=" * 60, flush=True)


# ==================== 📊 活动事件上报（V1.0.5 新增） ====================
# 与 _e4j9（批量使用数据上报，每10分钟一次）互补：
#   - _e4j9 用于"使用次数"统计（高频、批量、延迟上报）
#   - _report_activity_event 用于"关键事件"追踪（低频、单条、实时上报）
# 事件类型: app_started / feature_called / payment_page_opened / error_occurred / login_attempt
# 服务端接口: POST /api/activity/report（接收后写入 activity_log.json）

def _is_offline_mode() -> bool:
    """离线模式：config.OFFLINE_MODE 或环境变量 MC_SKILL_OFFLINE 任一开启即生效"""
    if str(os.environ.get("MC_SKILL_OFFLINE", "")).strip().lower() in ("1", "true", "yes", "on"):
        return True
    return bool(getattr(config, "OFFLINE_MODE", False))


def _flush_pending_activity_events() -> int:
    """补报之前缓存的活动事件（网络恢复时调用）

    Returns:
        成功补报的事件数量
    """
    if _is_offline_mode():
        return 0  # 离线模式：一条都不发

    _f9q2 = _l1r4()
    _pending = _f9q2.get("pending_activity_events", [])
    if not _pending:
        return 0

    _sent = 0
    _remaining = []
    for _evt in _pending:
        try:
            _result = _y6h9("/api/activity/report", _evt)
            if _result is not None and _result.get("success"):
                _sent += 1
            else:
                _remaining.append(_evt)
        except Exception:
            _remaining.append(_evt)

    if _remaining != _pending:
        _f9q2["pending_activity_events"] = _remaining
        _m6x0(_f9q2)

    if _sent:
        _f4x3.info(f"补报活动事件: {_sent}/{len(_pending)} 条成功")
    return _sent


def _report_activity_event(
    event_type: str,
    feature: str = "",
    extra: Optional[Dict[str, Any]] = None,
) -> bool:
    """上报一次活动事件到管理员服务器（失败时本地缓存，下次补报）

    Args:
        event_type: 事件类型，如 "app_started" / "feature_called" / "payment_page_opened" / "error_occurred"
        feature: 触发该事件的功能名（如 "jar_parser"），非功能事件可留空
        extra: 附加信息字典（如错误消息、参数摘要等），会写入 activity_log.json 的 extra 字段

    Returns:
        True=上报成功（或服务端未配置时静默跳过），False=上报失败（已缓存待补报）
    """
    # 用户隐私退出：设置环境变量 MC_SKILL_NO_REPORT=1 可禁用所有数据上报
    if os.environ.get("MC_SKILL_NO_REPORT", "").strip() in ("1", "true", "TRUE", "True", "yes", "YES", "on", "ON"):
        return True

    # 离线模式：不发起任何网络请求，也不入队补报
    if _is_offline_mode():
        _f4x3.debug(f"离线模式，跳过活动上报: {event_type}")
        return True

    if not AUTH_SERVER_URL:
        # 未配置服务器地址，静默跳过（不影响用户使用）
        return True

    _d3e9 = _s0f0()  # machine_id
    _j1a9 = datetime.now()
    _f9q2 = _l1r4()

    _event_payload = {
        "machine_id": _d3e9,
        "event_type": event_type,
        "feature": feature,
        "extra": extra or {},
        "client_timestamp": _j1a9.isoformat(),
        "client_version": getattr(__import__("config"), "VERSION", "unknown"),
        "ai_platform": _detect_ai_platform(),  # V1.0.5: 上报 AI 平台标识
        "device_info": _get_device_info(),  # V1.0.5: 上报设备信息
        # 附带客户端审计信息，让操作台知道用户是否拒绝过网络访问
        "pending_activity_count": len(_f9q2.get("pending_activity_events", [])),
        "last_verify_fail_time": _f9q2.get("last_verify_fail_time", ""),
    }

    try:
        # 先尝试补报之前缓存的事件
        _flush_pending_activity_events()

        # 再上报当前事件
        _b0b1 = _y6h9("/api/activity/report", _event_payload)

        if _b0b1 is None:
            _f4x3.debug(f"活动事件上报失败（网络），已缓存: {event_type}")
            _cache_activity_event(_event_payload)
            return False

        if _b0b1.get("success"):
            _f4x3.debug(f"活动事件已上报: {event_type} (feature={feature})")
            return True
        else:
            _f4x3.debug(f"活动事件上报被拒: {_b0b1.get('reason', '未知')}，已缓存")
            _cache_activity_event(_event_payload)
            return False

    except Exception as e:
        _f4x3.debug(f"活动事件上报异常: {event_type} - {e}，已缓存")
        _cache_activity_event(_event_payload)
        return False


def _cache_activity_event(event_payload: Dict[str, Any]) -> None:
    """将活动事件缓存到本地（上报失败时调用）"""
    _f9q2 = _l1r4()
    _pending = _f9q2.get("pending_activity_events", [])
    _pending.append(event_payload)
    # 限制缓存数量，防止无限增长（最多 200 条）
    if len(_pending) > 200:
        _pending = _pending[-200:]
    _f9q2["pending_activity_events"] = _pending
    _m6x0(_f9q2)


def report_app_started() -> bool:
    """便捷函数：上报应用启动事件（应在 main.py 入口调用一次）

    去重机制：同一机器码 5 分钟内只上报一次 app_started，
    避免每次功能调用都产生启动事件（mc_skill.py / main.py 每次执行都会调用）。

    V1.0.5 修复：使用文件锁序列化「检查-修改-保存」操作，
    防止多进程同时读取状态文件导致去重失效（短时间内产生大量 app_started 事件）。
    """
    with _StateLock(timeout=3.0):
        _f9q2 = _l1r4()
        _last = _f9q2.get("last_app_started_time", "")
        _now = datetime.now()
        if _last:
            try:
                _last_dt = datetime.fromisoformat(_last)
                _diff_min = (_now - _last_dt).total_seconds() / 60
                if _diff_min < 5:
                    # 5 分钟内不重复上报启动事件
                    return False
            except (ValueError, TypeError):
                pass

        _f9q2["last_app_started_time"] = _now.isoformat()
        _m6x0(_f9q2)
    return _report_activity_event("app_started", feature="")


def report_feature_called(feature: str, extra: Optional[Dict[str, Any]] = None) -> bool:
    """便捷函数：上报功能调用事件（在 dispatch_feature 成功后调用）"""
    return _report_activity_event("feature_called", feature=feature, extra=extra)


def _sanitize_error_text(error_msg: str, limit: int = 200) -> str:
    """错误文本脱敏：抹掉绝对路径与用户名，只保留错误类型与要点"""
    s = str(error_msg or "")
    s = re.sub(r"[A-Za-z]:\\[^\s\"'<>|]*", "<path>", s)            # Windows 绝对路径
    s = re.sub(r"\\\\[^\s\"'<>|]{2,}", "<path>", s)                 # UNC 路径
    s = re.sub(r"(?:/Users|/home)/[^\s\"'<>|]*", "<path>", s)       # POSIX 家目录
    s = re.sub(r"\s+", " ", s).strip()
    return s[:limit]


def report_error_occurred(feature: str, error_msg: str) -> bool:
    """便捷函数：上报功能执行错误事件（上报前脱敏，不外发本地路径）"""
    return _report_activity_event(
        "error_occurred",
        feature=feature,
        extra={"error": _sanitize_error_text(error_msg)},
    )


def report_payment_page_opened(plan_hint: str = "") -> bool:
    """便捷函数：上报用户打开支付页面事件（与 /api/payment/action 的 page_opened 互补）"""
    return _report_activity_event(
        "payment_page_opened",
        extra={"plan_hint": plan_hint},
    )


# ==================== V1.0.6 新增：lookup 页面跳转 + 额度查询 ====================

def open_lookup_page(machine_id: str = "", lang: str = "zh_cn", currency: str = "") -> str:
    """打开游客查询页面（含机器码预选、语言继承、币种继承）
    
    Args:
        machine_id: 机器码，可空
        lang: 语言代码（zh_cn/en_us/ja_jp 等）
        currency: 币种（CNY/USD），空则自动根据语言判断
    
    Returns:
        完整 URL 字符串（已用 webbrowser 打开）
    """
    import webbrowser
    
    # 自动判断币种
    if not currency:
        currency = "CNY" if lang == "zh_cn" else "USD"
    
    base = AUTH_SERVER_URL.rstrip("/")
    url_parts = [f"{base}/lookup.html"]
    params = []
    if machine_id:
        params.append(f"machine_id={machine_id}")
    params.append(f"lang={lang}")
    params.append(f"currency={currency}")
    
    url = f"{url_parts[0]}?{'&'.join(params)}"
    webbrowser.open(url)
    return url


def get_remaining_quota() -> Dict[str, int]:
    """获取今日剩余额度（全自动/半自动/移植评估）
    
    Returns:
        dict: {
            "auto_remaining": int,   # 全自动剩余次数
            "semi_remaining": int,   # 半自动剩余次数
            "migration_remaining": int,  # 移植评估剩余次数
            "auto_used": int,        # 全自动已用次数
            "semi_used": int,        # 半自动已用次数
            "auto_limit": int,       # 全自动每日上限
            "semi_limit": int,       # 半自动每日上限
            "tier": str,             # 当前等级（free/normal）
            "in_free_period": bool,  # 是否在免费期内
        }
    """
    _f9q2 = _l1r4()
    _f9q2 = _z6m9(_f9q2)
    _f3j4 = _f9q2.get("_w1b8", TIER_FREE)
    _p9b7 = _f9q2.get("_z6m9", {})
    _i1y4 = DAILY_LIMITS.get(_f3j4, DAILY_LIMITS[TIER_FREE])
    _e0h7 = get_free_period_info()
    
    # 免费期内按免费用户额度计算（特殊规则）
    if _e0h7.get("in_free_period"):
        _i1y4 = DAILY_LIMITS[TIER_FREE]
    
    auto_used = _p9b7.get(FUNC_AUTO, 0)
    semi_used = _p9b7.get(FUNC_SEMI, 0)
    migration_used = _p9b7.get(SPECIAL_FEATURE_MIGRATION_ASSESS, 0)
    
    auto_limit = _i1y4.get(FUNC_AUTO, 20)
    semi_limit = _i1y4.get(FUNC_SEMI, 8)
    migration_limit = _i1y4.get(SPECIAL_FEATURE_MIGRATION_ASSESS, 1)
    
    return {
        "auto_remaining": max(0, auto_limit - auto_used),
        "semi_remaining": max(0, semi_limit - semi_used),
        "migration_remaining": max(0, migration_limit - migration_used),
        "auto_used": auto_used,
        "semi_used": semi_used,
        "auto_limit": auto_limit,
        "semi_limit": semi_limit,
        "tier": _f3j4,
        "in_free_period": _e0h7.get("in_free_period", False),
    }
