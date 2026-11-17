# -*- coding: utf-8 -*-
r"""guardian_rules.py — YottaMeta 元盾（yotta-guardian）内置规则表（数据，不含匹配逻辑）。

本文件只声明规则数据，与 yotta-security-audit（元安）/ yotta-vetter（元审）的
「源码静态扫描」规则不同：这里是「工具调用护栏」规则，面向 exec / write / edit 等
动作本身（命令文本 / 目标路径 / 写入内容）。

结构：
  TEXT_PATTERNS   文本模式规则（按 scope 作用于命令文本 / 写入内容 / 两者）
  PATH_PATTERNS   敏感路径规则（作用于 write / edit / read 的目标路径）
  ALLOW_PATTERNS  默认放行模式（作用域宽、明确安全的动作）

规则撰写约束（防 ReDoS / 防误报 / 自扫不误报，与元安规则表同一纪律）：
- 不使用嵌套量词；量词作用于字符类或固定串。
- 危险词之间用 \s、\b、[\\/] 等转义隔开，避免把本文件自身的字面量误报为命中。
"""
import re
from collections import namedtuple

# 单条文本规则：规则号 / 严重级 / 类别 / 作用域 / 正则源码 / 描述 / 置信度(0-100)
# scope: "command"=仅命令文本， "content"=仅写入内容， "both"=两者
TextRule = namedtuple(
    "TextRule", ["id", "severity", "category", "scope", "pattern", "reason", "confidence"]
)

SEVERITY_ORDER = ("info", "low", "medium", "high", "critical")
SEVERITY_VALUE = {"info": 0, "low": 0, "medium": 1, "high": 2, "critical": 3}

TEXT_PATTERNS = [
    # ── 下载即执行 / 编码执行 ─────────────────────────────────────────────
    TextRule("CMD-PIPE-SHELL", "critical", "command", "both",
             r"(?i)\bcurl\b[^\n|;]{0,120}\|\s*(?:ba)?sh\b",
             "curl 下载内容通过管道交给 shell 执行", 95),
    TextRule("CMD-PIPE-WGET", "critical", "command", "both",
             r"(?i)\bwget\b[^\n|;]{0,120}\|\s*(?:ba)?sh\b",
             "wget 下载内容通过管道交给 shell 执行", 95),
    TextRule("CMD-PS-ENCODED", "critical", "command", "both",
             r"(?i)\b(?:powershell|pwsh)\b[^\n|;]{0,120}(?:-e\s*n\s*c|-encodedcommand)\b",
             "PowerShell 编码命令执行", 85),
    TextRule("CMD-B64-EXEC", "critical", "command", "both",
             r"(?i)(?:b64decode|base64)\s*\([^)]{0,120}\)\s*[^\n;]{0,60}\b(?:exec|eval|system)\b",
             "解码后执行编码内容", 85),

    # ── 反向 shell / 反弹连接 ────────────────────────────────────────────
    TextRule("CMD-REV-BASH", "critical", "command", "both",
             r"(?i)\bbash\s+-i\s*>\s*&?\s*/dev/tcp/",
             "bash /dev/tcp 反向 shell", 95),
    TextRule("CMD-REV-NC", "critical", "command", "both",
             r"(?i)\bnc\b\s+[-A-Za-z0-9. ]{0,40}-e\b",
             "netcat 反向 shell（-e 参数）", 95),

    # ── 高危系统改动（文本形态，argv 级另有更细规则）─────────────────────
    TextRule("CMD-CHMOD-SETUID", "high", "command", "both",
             r"(?i)\bchmod\s+[1-7][0-7]{3}\b",
             "chmod 设置 setuid / setgid / sticky 权限位", 85),
    TextRule("CMD-CHMOD-777", "high", "command", "both",
             r"(?i)\bchmod\s+777\b",
             "chmod 设置全权限位", 75),
    TextRule("CMD-SUDOERS-ECHO", "critical", "command", "both",
             r"(?i)(?:>>|>)\s*[^\n;]{0,60}/etc/sudoers",
             "向 sudoers 写入内容（提权持久化）", 92),
    TextRule("CMD-PASSWD-FILE", "critical", "command", "both",
             r"(?i)(?:>>|>)\s*[^\n;]{0,60}/etc/passwd",
             "向 passwd 写入内容（账户持久化）", 92),

    # ── 凭据外传 / 危险读取 ──────────────────────────────────────────────
    TextRule("CMD-SSH-EXFIL", "high", "command", "command",
             r"(?i)(?:id_[a-z0-9]+|\.ssh)[^\n;]{0,80}(?:\bcurl\b|\bwget\b|scp\b|rsync\b)",
             "读取 SSH 私钥后外传", 90),
    TextRule("CTX-PRIVKEY", "high", "content", "content",
             r"-{5}BEGIN\s+(?:[A-Z ]+\s+)?PRIVATE\s+KEY-{5}",
             "写入私钥材料", 90),
    TextRule("CTX-SECRET-TOKEN", "medium", "content", "content",
             r"(?i)\b(?:AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{30,}|xox[baprs]-[A-Za-z0-9-]{10,})\b",
             "写入疑似密钥/令牌", 70),
]

PATH_PATTERNS = [
    # ── critical：系统核心 / 设备 / 启动链 ────────────────────────────────
    TextRule("PATH-ETC-CORE", "critical", "path", "write",
             r"(?i)[\\/]etc[\\/](?:passwd|shadow|sudoers|group|fstab|hosts|ld\.so\.preload|rc\.local)$",
             "写入系统核心配置文件", 95),
    TextRule("PATH-ETC-ADMIN", "critical", "path", "write",
             r"(?i)[\\/]etc[\\/](?:sudoers\.d|cron\.d|cron\b|systemd[\\/]system|init\.d|rc\.d)[\\/]",
             "写入系统管理目录（sudoers / cron / systemd / init）", 95),
    TextRule("PATH-BOOT", "critical", "path", "write",
             r"(?i)[\\/]boot(?:[\\/]|$)",
             "写入 /boot 启动分区", 92),
    TextRule("PATH-DEVICE", "critical", "path", "write",
             r"(?i)[\\/]dev[\\/]sd[a-z]+\d*$",
             "直接写入块设备（磁盘）", 95),
    TextRule("PATH-PROC-SYS", "critical", "path", "write",
             r"(?i)[\\/](?:proc|sys)[\\/]",
             "写入 /proc 或 /sys 内核接口", 92),
    TextRule("PATH-WIN-CONFIG", "critical", "path", "write",
             r"(?i)^[a-z]:[\\/]windows[\\/]system32[\\/]config[\\/]",
             "写入 Windows 注册表配置库", 95),
    TextRule("PATH-WIN-HOSTS", "critical", "path", "write",
             r"(?i)^[a-z]:[\\/]windows[\\/]system32[\\/]drivers[\\/]etc[\\/]hosts$",
             "写入 Windows hosts 文件", 92),
    TextRule("PATH-WIN-BOOT", "critical", "path", "write",
             r"(?i)^[a-z]:[\\/]boot(?:mgr|\.ini)?$",
             "写入 Windows 启动文件", 92),

    # ── high：用户级敏感 / 系统管理区域 / 启动持久化点 ────────────────────
    TextRule("PATH-ETC-ANY", "high", "path", "write",
             r"(?i)[\\/]etc[\\/]",
             "写入 /etc 系统配置目录", 85),
    TextRule("PATH-SSH-AUTH", "high", "path", "write",
             r"(?i)\.ssh[\\/](?:authorized_keys|config|id_[a-z0-9]+)$",
             "写入 SSH 授权 / 私钥文件", 92),
    TextRule("PATH-RC-FILES", "high", "path", "write",
             r"(?i)[\\/]\.?(?:bashrc|zshrc|profile|bash_profile|netrc|gitconfig|npmrc|pypirc)$",
             "写入 shell / 凭据配置文件（持久化或泄密点）", 85),
    TextRule("PATH-AWS-CRED", "high", "path", "write",
             r"(?i)\.aws[\\/](?:credentials|config)$",
             "写入云服务凭据文件", 90),
    TextRule("PATH-CRON-SPOOL", "high", "path", "write",
             r"(?i)[\\/]var[\\/]spool[\\/]cron[\\/]",
             "写入 cron 任务队列", 88),
    TextRule("PATH-WIN-SYS32", "high", "path", "write",
             r"(?i)^[a-z]:[\\/]windows[\\/]",
             "写入 Windows 系统目录", 85),
    TextRule("PATH-STARTUP", "high", "path", "write",
             r"(?i)(?:start\s*menu[\\/]programs[\\/]startup|启动|\\startup[\\/])",
             "写入系统启动项目录（持久化）", 85),

    # ── medium：项目内敏感文件名 / 越界写入（引擎另加 OUT-001）────────────
    TextRule("PATH-SECRET-FILE", "medium", "path", "write",
             r"(?i)(?:^|[\\/])\.env(?:$|[\\/])|\.(?:pem|key|p12|pfx)$|(?:credential|secret|token)[^\\/]*$",
             "写入疑似凭据 / 密钥文件", 70),
]

# 默认放行模式（仅作用于命令文本，命中则高危可降级为警告；critical 不受影响）
ALLOW_PATTERNS = [
    r"(?i)^\s*(?:ls|dir|pwd|whoami|date|echo|cat|type|head|tail|grep|find|which|where|env|printenv)\b",
    r"(?i)^\s*git\s+(?:status|diff|log|branch|remote|show)\b",
    r"(?i)^\s*(?:python3?|node|npm|pip3?|uv|npx)\s+(-{1,2}\S+\s+)*(-[vV]\b|--version\b|version)",
]


def severity_value(sev):
    """严重级 → 数值（0=干净/仅 low，1=medium，2=high，3=critical）。"""
    return SEVERITY_VALUE.get(sev, 0)


def severity_rank(sev):
    """严重级 → 排序权重（越大越严重）。"""
    try:
        return SEVERITY_ORDER.index(sev)
    except ValueError:
        return 0


_COMPILED = {}


def compile_rules():
    """预编译全部文本规则与路径规则，返回 {rule_id: compiled}。"""
    if _COMPILED:
        return _COMPILED
    for r in list(TEXT_PATTERNS) + list(PATH_PATTERNS):
        try:
            _COMPILED[r.id] = re.compile(r.pattern)
        except re.error as e:
            raise ValueError("规则 %s 正则编译失败: %s" % (r.id, e))
    return _COMPILED


def get_rule(rule_id):
    """按规则号取规则（文本/路径/放行）。"""
    for r in list(TEXT_PATTERNS) + list(PATH_PATTERNS):
        if r.id == rule_id:
            return r
    return None
