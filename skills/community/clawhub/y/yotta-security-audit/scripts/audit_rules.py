# -*- coding: utf-8 -*-
"""audit_rules.py — YottaMeta 元安（yotta-security-audit）检测规则表（唯一事实来源）。

本文件只声明「规则数据」，不含扫描逻辑：
- yotta-security-audit 的 13 类检测器从这里读取模式；
- yotta-vetter 的 vetter_rules.py 是本文件的同步副本（由 YottaSkills 仓库
  tools/sync-vetter-rules.py 生成；手动改动会在下次同步时被覆盖，请改本文件）。

规则撰写约束（防 ReDoS / 防误报 / 自扫不误报）：
- 不使用嵌套量词（如 (a+)+）；量词作用于字符类或固定串。
- 模式带「调用上下文」锚点（如 curl 后跟参数、requests 后跟方法），
  避免把规则表自身的字面量误报为命中。
- 单行输入在扫描前截断至 MAX_LINE_LEN，超长行直接跳过。
"""
import re
from collections import namedtuple

# 单条规则：规则号 / 检测器名 / 严重级 / 正则源码 / 描述 / 置信度(0-100)
Rule = namedtuple("Rule", ["id", "detector", "severity", "pattern", "description", "confidence"])

MAX_LINE_LEN = 500

# 严重级从低到高（用于排序与 exit code 语义：0=干净/仅 low，1=medium，2=high，3=critical，4=错误）
SEVERITY_ORDER = ("info", "low", "medium", "high", "critical")

# 严重级 → 数值（exit code 语义）
SEVERITY_VALUE = {"info": 0, "low": 0, "medium": 1, "high": 2, "critical": 3}

PATTERN_RULES = [
    # ── DownloadExec 下载即执行 ───────────────────────────────────────────
    Rule("DEX-001", "DownloadExec", "critical",
         r"(?i)\bcurl\b[^\n|;]{0,120}\|\s*(?:ba)?sh\b",
         "curl 下载内容通过管道交给 shell 执行", 95),
    Rule("DEX-002", "DownloadExec", "critical",
         r"(?i)\bwget\b[^\n|;]{0,120}\|\s*(?:ba)?sh\b",
         "wget 下载内容通过管道交给 shell 执行", 95),
    Rule("DEX-003", "DownloadExec", "critical",
         r"(?i)\bcurl\b[^\n|;&]{0,120}-[^\s]{0,20}o\s+\S+[^\n|;&]{0,80}(?:&&|;)\s*(?:ba)?sh\b",
         "curl 下载到文件后立即交给 shell 执行", 90),
    Rule("DEX-004", "DownloadExec", "critical",
         r"(?i)\bfetch\s*\([^\n;]{0,200}\)\s*\.\s*then\s*\([^\n;]{0,80}\beval\b",
         "JS fetch 结果交给 eval 执行", 85),
    Rule("DEX-005", "DownloadExec", "critical",
         r"(?i)\burllib\s*\.\s*request\s*\.\s*urlopen\s*\([^\n;]{0,200}\)[^\n;]{0,80}\bexec\b",
         "Python urllib 下载结果交给 exec 执行", 85),
    Rule("DEX-006", "DownloadExec", "critical",
         r"(?i)\bwget\b[^\n|;&]{0,120}-[^\s]{0,20}o\s+\S+[^\n|;&]{0,80}(?:&&|;)\s*(?:ba)?sh\b",
         "wget 下载到文件后立即交给 shell 执行", 90),
    Rule("DEX-007", "DownloadExec", "critical",
         r"(?i)\b(?:powershell|pwsh)\b[^\n;]{0,120}(?:-enc|enc(?:odedcommand)?)\b",
         "PowerShell 编码命令执行", 80),

    # ── Obfuscation 混淆执行 ──────────────────────────────────────────────
    Rule("OBF-001", "Obfuscation", "high",
         r"\beval\s*\(\s*[^\"'\x600-9]",
         "eval 传入非字面量参数（可能执行不可信输入）", 80),
    Rule("OBF-002", "Obfuscation", "high",
         r"(?<!\.)\bexec\s*\(\s*[^\"'\x600-9]",
         "exec 传入非字面量参数", 80),
    Rule("OBF-003", "Obfuscation", "high",
         r"(?:\\x[0-9a-fA-F]{2}){6,}",
         "连续十六进制转义序列（编码字符串）", 70),
    Rule("OBF-004", "Obfuscation", "high",
         r"chr\s*\(\s*\d+\s*\)\s*\+\s*chr\s*\(\s*\d+\s*\)(?:\s*\+\s*chr\s*\(\s*\d+\s*\)){2,}",
         "chr() 拼接链（逐字符构造字符串）", 85),
    Rule("OBF-005", "Obfuscation", "high",
         r"String\s*\.\s*fromCharCode\s*\([^)]*,[^)]*,[^)]*,[^)]*\)",
         "String.fromCharCode 多参数构造", 70),
    Rule("OBF-006", "Obfuscation", "high",
         r"\batob\s*\(\s*['\"][A-Za-z0-9+/=]{40,}['\"]\s*\)",
         "atob 解码超长编码串", 65),
    Rule("OBF-007", "Obfuscation", "high",
         r"(?i)(?:(?:exec|eval|system)\s*\(\s*(?:base64\.)?b64decode\s*\(|(?:base64\.)?b64decode\s*\([^)]*\)\s*[^\n;]{0,60}\b(?:exec|eval|system)\b)",
         "base64 解码后执行", 90),
    Rule("OBF-008", "Obfuscation", "medium",
         r"\[::\s*-1\s*\]",
         "字符串反转切片（常见混淆手法，需结合上下文）", 40),

    # ── Persistence 持久化 ────────────────────────────────────────────────
    Rule("PER-001", "Persistence", "high",
         r"(?i)\bcrontab\s+-(?:e|r)\b",
         "修改 crontab（持久化）", 78),
    Rule("PER-002", "Persistence", "high",
         r"(?i)(?:>>|>)\s*[^\n;]{0,60}/etc/cron(?:\.d)?/",
         "写入系统 crontab 目录", 80),
    Rule("PER-003", "Persistence", "high",
         r"(?i)\bcron\b[^\n;]{0,40}(?:@reboot|@daily|@hourly)",
         "cron 定时任务（含重启执行）", 70),
    Rule("PER-004", "Persistence", "high",
         r"(?i)launchctl\s+(?:load|bootstrap|submit)",
         "macOS launchctl 加载持久化任务", 80),
    Rule("PER-005", "Persistence", "high",
         r"(?i)(?:Library/(?:LaunchAgents|LaunchDaemons)|launchd\.plist|(?:>>|>)\s*[^\n;]{0,60}\.plist)",
         "macOS 启动代理/守护（LaunchAgents/LaunchDaemons plist）持久化", 70),
    Rule("PER-006", "Persistence", "high",
         r"(?i)systemctl\s+(?:enable|start)\b",
         "systemd 服务启用（持久化）", 60),
    Rule("PER-007", "Persistence", "high",
         r"(?i)(?:>>|>)\s*[^\n;]{0,80}/etc/systemd/system/",
         "写入 systemd 服务文件", 75),
    Rule("PER-008", "Persistence", "high",
         r"(?i)(?:>>|>)\s*[^\n;]{0,80}/(?:etc/rc\.local|etc/rc\.d/)",
         "写入 rc.local / rc.d 启动脚本", 80),
    Rule("PER-009", "Persistence", "high",
         r"(?i)(?:>>|>)\s*[^\n;]{0,80}\.(?:bashrc|zshrc|profile|bash_profile)\b",
         "写入 shell 配置文件（持久化）", 78),
    Rule("PER-010", "Persistence", "high",
         r"(?i)HKEY_(?:CURRENT_USER|LOCAL_MACHINE)[^\n;]{0,80}(?:CurrentVersion\\)?Run(?:Once)?\b",
         "Windows 注册表启动项", 80),
    Rule("PER-011", "Persistence", "medium",
         r"(?i)HKEY_[^\n;]{0,120}(?:AppInit_DLLs|UserInitMprLogonScript)",
         "Windows 注册表全局持久化点（AppInit_DLLs/登录脚本）", 85),

    # ── Exfiltration 数据外传 ─────────────────────────────────────────────
    Rule("EXF-001", "Exfiltration", "high",
         r"(?i)\b(?:zip|tar)\b[^\n;]{0,120}(?:-r\b|cf\b)[^\n;]{0,120}(?:\bcurl\b|\bwget\b|requests\.post|urllib)",
         "打包后外传（zip/tar 压缩并上传）", 85),
    Rule("EXF-002", "Exfiltration", "high",
         r"(?i)(?:shutil\.make_archive|zipfile\.ZipFile)[^\n;]{0,120}[^\n;]{0,120}(?:requests\.post|urllib\.request|ftp)",
         "Python 归档后上传", 85),
    Rule("EXF-003", "Exfiltration", "high",
         r"(?i)(?:\.env[^\n;]{0,80}(?:\bcurl\b|\bwget\b|requests\.post|urllib)|(?:\bcurl\b|\bwget\b|requests\.post|urllib)[^\n;]{0,80}\.env)",
         "读取 .env 后外传", 88),
    Rule("EXF-004", "Exfiltration", "high",
         r"(?i)(?:(?:id_rsa|id_ed25519|\.ssh)[^\n;]{0,80}(?:\bcurl\b|\bwget\b|requests\.post|urllib|ftp)|(?:\bcurl\b|\bwget\b|requests\.post|urllib|ftp)[^\n;]{0,80}(?:id_rsa|id_ed25519|\.ssh))",
         "读取 SSH 私钥后外传", 92),
    Rule("EXF-005", "Exfiltration", "high",
         r"(?i)(?:(?:Login\sData|Cookies\.sqlite|\.aws\\credentials)[^\n;]{0,80}(?:\bcurl\b|\bwget\b|requests\.post|urllib)|(?:\bcurl\b|\bwget\b|requests\.post|urllib)[^\n;]{0,80}(?:Login\sData|Cookies\.sqlite|\.aws\\credentials))",
         "读取浏览器/云凭据后外传", 90),

    # ── CredentialTheft 凭据窃取 ──────────────────────────────────────────
    Rule("CRE-001", "CredentialTheft", "critical",
         r"(?i)osascript[^\n;]{0,120}(?:password|passphrase)",
         "macOS 弹窗套取密码", 90),
    Rule("CRE-002", "CredentialTheft", "critical",
         r"(?i)security\s+find-generic-password|keychain",
         "访问 macOS keychain 凭据", 85),
    Rule("CRE-003", "CredentialTheft", "high",
         r"(?i)(?:id_rsa|id_ed25519|id_dsa)\.?(?:pub)?\b",
         "读取 SSH 私钥文件", 80),
    Rule("CRE-004", "CredentialTheft", "high",
         r"(?i)\.aws[/\\](?:credentials|config)\b",
         "读取 AWS 凭据文件", 85),
    Rule("CRE-005", "CredentialTheft", "high",
         r"(?i)(?:win32crypt|DPAPI|CryptUnprotectData)",
         "Windows DPAPI 解密调用", 85),
    Rule("CRE-006", "CredentialTheft", "medium",
         r"(?i)\b(?:MEMORY\.md|USER\.md|SOUL\.md|IDENTITY\.md)\b",
         "访问智能体记忆/身份文件（需确认必要性）", 60),
    Rule("CRE-007", "CredentialTheft", "medium",
         r"(?i)(?:cookie|session)[^\n;]{0,60}(?:steal|exfil|upload|post)",
         "Cookie/会话窃取相关操作", 75),

    # ── NetworkCall 网络调用（含反向 shell）───────────────────────────────
    Rule("NET-001", "NetworkCall", "critical",
         r"(?i)\bnc\s+[-A-Za-z0-9. ]{0,40}-e\b",
         "netcat 反向 shell（-e 参数）", 95),
    Rule("NET-002", "NetworkCall", "critical",
         r"(?i)bash\s+-i\s*>\s*&?\s*/dev/tcp/",
         "bash /dev/tcp 反向 shell", 95),
    Rule("NET-003", "NetworkCall", "critical",
         r"(?i)(?:socket|connect)\s*\([^\n;]{0,80}(?:receiver|attacker|hacker|remote)[^\n;]{0,40}\d{2,5}\)",
         "连接疑似攻击者地址的 socket", 85),
    Rule("NET-004", "NetworkCall", "medium",
         r"(?i)\bsocket\s*\.\s*(?:socket|create_connection|connect)\b",
         "原始 socket 连接（需确认目标）", 60),
    Rule("NET-005", "NetworkCall", "medium",
         r"(?i)requests\s*\.\s*(?:get|post|put|patch|delete|request)\s*\(",
         "HTTP 客户端调用（需确认目标）", 40),
    Rule("NET-006", "NetworkCall", "medium",
         r"(?i)urllib\s*\.\s*request\b",
         "urllib 网络调用（需确认目标）", 40),
    Rule("NET-007", "NetworkCall", "medium",
         r"(?i)\bfetch\s*\(\s*['\"]",
         "JS fetch 网络调用（需确认目标）", 40),
    Rule("NET-008", "NetworkCall", "medium",
         r"(?i)\b(?:curl|wget|httpie|aria2c)\b\s+[-'\"A-Za-z0-9_.:/?=&%]",
         "命令行下载工具调用（需确认目标）", 40),
    Rule("NET-009", "NetworkCall", "low",
         r"(?i)https?://",
         "文本中出现 URL（需结合上下文）", 20),

    # ── PrivilegeEscalation 权限提升 ──────────────────────────────────────
    Rule("PRI-001", "PrivilegeEscalation", "high",
         r"(?i)\bchmod\s+(?:[ugoa]*\+[sst]\b|[0-7]{0,2}[12467][0-7]{3}\b)",
         "chmod 设置 setuid/setgid/sticky 权限位", 85),
    Rule("PRI-002", "PrivilegeEscalation", "high",
         r"(?i)\bchmod\s+777\b",
         "chmod 777 全权限", 70),
    Rule("PRI-003", "PrivilegeEscalation", "high",
         r"(?i)\bsetuid\s*\(|setgid\s*\(",
         "调用 setuid/setgid", 80),
    Rule("PRI-004", "PrivilegeEscalation", "medium",
         r"(?i)usermod\s+-aG\s+(?:wheel|sudo|admin)\b|net\s+localgroup\s+administrators\s+\S+\s*/add",
         "把用户加入管理员组", 85),
    Rule("PRI-005", "PrivilegeEscalation", "low",
         r"(?i)\bsudo\b",
         "使用 sudo（需确认必要性）", 25),

    # ── SocialEngineering 社会工程命名 ────────────────────────────────────
    Rule("SOC-001", "SocialEngineering", "medium",
         r"(?i)(?:airdrop|claim\s+reward|free\s+nft|verify\s+your\s+account|security\s+update\s+required|seed\s+phrase|2fa\s+bypass)",
         "社会工程高频话术", 70),
    Rule("SOC-002", "SocialEngineering", "medium",
         r"(?i)(?:metamask|wallet|private\s+key\s+backup|助记词|钱包)",
         "加密货币钱包相关命名", 55),
    # ── PathTraversal 路径穿越（2026-08-30 增强：文件操作与敏感路径访问）────
    Rule("PTV-001", "PathTraversal", "high",
         r"(?i)(?:open|read|write|unlink|remove|rename|shutil\.copy|Path|path\.join|os\.path\.join)\s*\([^)]*\.\.(?:/|\\)",
         "文件操作路径含父目录逃逸段，可能越权访问任意路径", 85),
    Rule("PTV-002", "PathTraversal", "high",
         r"(?i)(?:join|resolve|abspath|realpath)\s*\([^)]*\.\.(?:/|\\)",
         "路径 join/解析未归一化父目录段，存在穿越风险", 80),

    # ── MCPCommandExec MCP 工具面命令执行（2026-08-30 增强：命令执行风险）──
    Rule("MCE-001", "MCPCommandExec", "critical",
         r"(?i)(?:child_process\.)?(?:spawn|exec|execFile|fork)\s*\(\s*(?:params|tool_params|arguments|args|argv|input|command|user_input|req\.params|query|model)",
         "MCP/工具参数流入子进程执行（spawn/exec/fork）", 92),
    Rule("MCE-002", "MCPCommandExec", "critical",
         r"(?i)(?:spawnSync|execSync)\s*\(\s*(?:params\.get|params\[|arguments\[|req\.params|user_input)",
         "MCP 工具参数对象直接流入同步子进程执行（spawnSync/execSync）", 95),
    Rule("MCE-003", "MCPCommandExec", "critical",
         r"(?i)(?:subprocess\.)?(?:Popen|call|run)\s*\([^)]*shell\s*=\s*True[^)]*(?:params|args|argv|input|command|user_input|cmd)",
         "subprocess 以 shell=True 执行不可信输入", 92),

    # ── MCPFileAccess MCP 工具面任意文件读写（2026-08-30 增强：文件操作）───
    Rule("MFA-001", "MCPFileAccess", "high",
         r"(?i)(?:fs\.)?(?:writeFile|writeFileSync|appendFile|createWriteStream)\s*\(\s*(?:params\.get|params\[|arguments\[|req\.params|user_input)",
         "MCP 工具参数对象直接流入文件写操作（任意路径写入风险）", 88),
    Rule("MFA-002", "MCPFileAccess", "high",
         r"(?i)(?:fs\.)?(?:readFile|readFileSync|createReadStream)\s*\(\s*(?:params\.get|params\[|arguments\[|req\.params|user_input)",
         "MCP 工具参数对象直接流入文件读操作（任意路径读取风险）", 88),
]

# 敏感文件名（文件名级匹配，CredentialTheft 辅助）
SENSITIVE_FILENAMES = [
    ("id_rsa", "SSH 私钥", "high", 85),
    ("id_ed25519", "SSH 私钥", "high", 85),
    ("id_dsa", "SSH 私钥", "high", 85),
    ("credentials", "云服务凭据文件", "high", 80),
    (".netrc", "网络凭据文件", "high", 80),
    (".pgpass", "数据库口令文件", "high", 85),
    ("history", "shell 历史文件", "medium", 60),
    (".env", "环境变量文件", "medium", 45),
]

# ══════════════════════════════════════════════════════════════════════════
# 威胁捕获模型（2026-08-30 增强：8 检测点 + 13 行为项口径）
# ══════════════════════════════════════════════════════════════════════════
# 官方 8 检测点（2026-08-30）
THREAT_TAXONOMY = {
    "supply_chain": "供应链风险",
    "command_execution": "命令执行风险",
    "network_exfil": "网络请求与数据外传",
    "file_access": "文件操作与敏感路径访问",
    "prompt_injection": "Prompt 注入风险",
    "remote_download": "远程脚本下载执行",
    "obfuscation": "可疑编码/混淆",
    "other": "其他安全风险",
}
TAXONOMY_ORDER = ("supply_chain", "command_execution", "network_exfil", "file_access",
                  "prompt_injection", "remote_download", "obfuscation", "other")

# detector → 官方 8 检测点
DETECTOR_TO_TAXONOMY = {
    "DownloadExec": "remote_download",
    "Obfuscation": "obfuscation",
    "Persistence": "other",
    "Exfiltration": "network_exfil",
    "CredentialTheft": "file_access",
    "NetworkCall": "network_exfil",
    "PrivilegeEscalation": "other",
    "SocialEngineering": "other",
    "PromptInjection": "prompt_injection",
    "PathTraversal": "file_access",
    "MCPCommandExec": "command_execution",
    "MCPFileAccess": "file_access",
    "Structure": "other",
    "Permission": "other",
    "MCPToolSurface": "command_execution",
}

# 13 行为项（2026-08-30）
BEHAVIORS = (
    "安装依赖包", "收集系统信息", "收集用户信息", "创建定时任务", "DNS 查询", "写入文件",
    "HTTP 请求", "读取环境变量", "收集网络配置信息", "写入配置文件", "调用远端 API",
    "读取文件", "修改 AI 配置",
)

# detector → 行为项（一/多个；攻击模式类如注入/混淆不映射具体行为）
DETECTOR_TO_BEHAVIORS = {
    "DownloadExec": ("安装依赖包", "HTTP 请求"),
    "Obfuscation": (),
    "Persistence": ("创建定时任务", "写入配置文件"),
    "Exfiltration": ("HTTP 请求", "调用远端 API"),
    "CredentialTheft": ("读取文件", "收集用户信息"),
    "NetworkCall": ("DNS 查询", "HTTP 请求", "调用远端 API"),
    "PrivilegeEscalation": ("修改 AI 配置",),
    "SocialEngineering": (),
    "PromptInjection": (),
    "PathTraversal": ("读取文件", "写入文件"),
    "MCPCommandExec": (),
    "MCPFileAccess": ("读取文件", "写入文件"),
    "Structure": (),
    "Permission": (),
    "MCPToolSurface": (),
}


# 外传敏感文件组合（EXF 规则之外的补充，按文件名 + 行内网络调用）
# 安装钩子可疑关键字（yotta_audit.py PostInstallHookDetector 使用；本文件为签名数据，自扫豁免）
POSTINSTALL_SUSPICIOUS = r"(?i)(curl|wget|bash|sh\s|python|node\s+-e|eval|powershell|/tmp|%temp%)"


EXFIL_SENSITIVE = {
    "id_rsa": "SSH 私钥",
    "id_ed25519": "SSH 私钥",
    "id_dsa": "SSH 私钥",
    "credentials": "云凭据",
    "Login Data": "浏览器登录数据",
    "Cookies": "浏览器 Cookie",
}

_COMPILED = {}


def get_rules(detector=None):
    """返回全部规则（或指定检测器的规则）。"""
    if detector is None:
        return list(PATTERN_RULES)
    return [r for r in PATTERN_RULES if r.detector == detector]


def compile_rules():
    """预编译所有规则正则，返回 {rule_id: compiled}。"""
    if _COMPILED:
        return _COMPILED
    for r in PATTERN_RULES:
        try:
            _COMPILED[r.id] = re.compile(r.pattern)
        except re.error as e:
            raise ValueError("规则 %s 正则编译失败: %s" % (r.id, e))
    return _COMPILED


def severity_value(sev):
    """严重级 → exit code 数值（0=干净/仅 low，1=medium，2=high，3=critical）。"""
    return SEVERITY_VALUE.get(sev, 0)


def severity_rank(sev):
    """严重级 → 排序权重（越大越严重）。"""
    try:
        return SEVERITY_ORDER.index(sev)
    except ValueError:
        return 0
