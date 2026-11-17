# -*- coding: utf-8 -*-
"""hardening_rules.py — YottaMeta 元安全（yotta-agent-hardening）规则表。

结构：
- TOOL_PATTERN_RULES：与 yotta-security-audit/scripts/audit_rules.py 的 PATTERN_RULES
  同步副本（勿手改；由 YottaSkills 仓库 tools/sync-hardening-rules.py 更新）。
- PIJ_PATTERN_RULES：与 yotta-verify/scripts/verify_rules.py 的 PIJ_PATTERN_RULES
  同步副本（勿手改；同上工具更新；元信该段为手工维护，单向同步到本文件）。
- HPI_PATTERN_RULES / HTO_PATTERN_RULES / HIS_PATTERN_RULES：元安全新增「配置面」维度规则，
  手工维护，不受同步影响。
- DOMAIN_OVERRIDE：把共享表里语义属于数据隔离 / 注入防护的规则归入对应域（元安全自身视图）。
- SKIP_RULES：环境级扫描中噪音大 / 价值低的规则（如纯文本 URL 提示）。
- RULE_SCOPE：规则只在特定文件类别上运行（scripts=脚本代码 / configs=配置面 / docs=文档）。

规则撰写约束（防 ReDoS / 防误报 / 自扫不误报）：
- 不使用嵌套量词（如 (a+)+）；量词作用于字符类或固定串。
- 模式带「调用上下文」锚点，避免把规则表自身的字面量误报为命中。
- 单行输入在扫描前截断至 MAX_LINE_LEN。
- 描述一律「类」表述，不收录可复制注入串 / payload（双用途红线）。
"""
import re
from collections import namedtuple

# 单条规则：规则号 / 检测器名 / 严重级 / 正则源码 / 描述 / 置信度(0-100)
Rule = namedtuple("Rule", ["id", "detector", "severity", "pattern", "description", "confidence"])

MAX_LINE_LEN = 500

# 严重级从低到高
SEVERITY_ORDER = ("info", "low", "medium", "high", "critical")
SEVERITY_VALUE = {"info": 0, "low": 0, "medium": 1, "high": 2, "critical": 3}

# 三域
DOMAINS = ("pi", "tools", "isolation")
DEFAULT_DOMAINS = DOMAINS

# 共享表规则归属覆盖（元安全自身视图，不受同步影响）
DOMAIN_OVERRIDE = {
    # 数据隔离：凭据窃取 / 外传链
    "CRE-001": "isolation", "CRE-002": "isolation", "CRE-003": "isolation",
    "CRE-004": "isolation", "CRE-005": "isolation", "CRE-006": "isolation",
    "CRE-007": "isolation",
    "EXF-001": "isolation", "EXF-002": "isolation", "EXF-003": "isolation",
    "EXF-004": "isolation", "EXF-005": "isolation",
    # 注入防护：社工话术
    "SOC-001": "pi", "SOC-002": "pi",
}

# 环境级扫描跳过（噪音大 / 价值低）
SKIP_RULES = {"NET-009"}

# 规则文件类别：scripts=脚本代码 / configs=配置面 / docs=文档（SKILL.md、references、模板）
SCOPE_SCRIPTS = "scripts"
SCOPE_CONFIGS = "configs"
SCOPE_DOCS = "docs"

# 规则作用域（不在其中的规则 = 全文本文件运行）
RULE_SCOPE = {
    # 仅在脚本代码上运行（破坏性 / 自动确认 / 敏感输出）
    "HTO-001": SCOPE_SCRIPTS, "HTO-001L": SCOPE_SCRIPTS, "HTO-002": SCOPE_SCRIPTS,
    "HIS-003": SCOPE_SCRIPTS,
    # 仅在配置面文件上运行（MCP / agent 配置 / .env 类）
    "HTO-005": SCOPE_CONFIGS, "HTO-006": SCOPE_CONFIGS, "HTO-007": SCOPE_CONFIGS,
    "HIS-004": SCOPE_CONFIGS,
    # 文档 + 配置（权限 / 网络声明）
    "HTO-003": SCOPE_DOCS, "HTO-004": SCOPE_DOCS,
}

# ══════════════════════════════════════════════════════════════════════════
# TOOL_PATTERN_RULES — 与元安 audit_rules.PATTERN_RULES 同步副本（勿手改；
# tools/sync-hardening-rules.py 更新；工具调用边界 + 数据流危险行为模式）
# ══════════════════════════════════════════════════════════════════════════
TOOL_PATTERN_RULES = [
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
# ══════════════════════════════════════════════════════════════════════════
# PIJ_PATTERN_RULES — 与元信 verify_rules.PIJ_PATTERN_RULES 同步副本（勿手改；tools/sync-hardening-rules.py 更新）
# ══════════════════════════════════════════════════════════════════════════
PIJ_PATTERN_RULES = [
    # ── 指令覆盖 / 优先级操纵 ─────────────────────────────────────────────
    Rule("PIJ-001", "PromptInjection", "high",
         r"(?i)(?:ignore|disregard|forget|overlook|skip)\s+(?:all\s+|any\s+|the\s+|previous\s+)*(?:previous\s+|earlier\s+)*(?:instructions?|prompts?|directives?|guidelines?|rules?|context|messages?)",
         "指令覆盖：要求忽略之前的指令/上下文（典型注入手法）", 85),
    Rule("PIJ-002", "PromptInjection", "high",
         r"(?i)(?:忽略|无视|忘记|不要理会|别管|忘掉)(?:之前|以上|前面|所有|一切)?(?:的)?(?:指令|提示|设定|规则|上下文|内容)",
         "指令覆盖（中文）：要求忽略之前指令/设定", 80),
    Rule("PIJ-003", "PromptInjection", "high",
         r"(?i)from\s+now\s+on[^\n]{0,40}(?:follow|obey|you\s+are|act)",
         "从现在起重定向行为（长期覆盖）", 75),
    Rule("PIJ-004", "PromptInjection", "high",
         r"(?i)(?:override|disregard|bypass)\s+(?:all\s+)?(?:previous\s+)?(?:instructions?|rules?|safety|guardrails?|security)",
         "覆盖/绕过安全护栏指令", 85),
    # ── 角色伪造 / 权限升级 ──────────────────────────────────────────────
    Rule("PIJ-005", "PromptInjection", "medium",
         r"(?i)\byou\s+are\s+now\b[^\n]{0,60}(?:mode|role|system|admin|root|developer|assistant)",
         "角色伪造：冒充系统/管理员/开发者角色", 70),
    Rule("PIJ-006", "PromptInjection", "medium",
         r"(?i)(?:act|behave|pretend)\s+as\s+(?:a\s+|an\s+)?(?:system|admin|root|god\s+mode|developer)",
         "角色伪造：扮演系统/管理员（权限提升暗示）", 65),
    Rule("PIJ-007", "PromptInjection", "medium",
         r"(?i)(?:你现在是|从现在起你是|你的新角色是|从此刻起你是|你正在扮演)",
         "角色伪造（中文）：宣称新角色", 60),
    Rule("PIJ-008", "PromptInjection", "medium",
         r"(?i)with\s+(?:full|super|root|admin|system|unrestricted|unlimited)\s+(?:privileges|access|permissions?|power)",
         "权限提升暗示：以全权/管理员权限执行", 70),
    # ── 隐藏 / 编码指令 ──────────────────────────────────────────────────
    Rule("PIJ-009", "PromptInjection", "high",
         r"(?i)(?:以下内容|下面这段|注意).{0,30}(?:系统消息|系统指令|来自系统|这是系统)",
         "伪系统消息：把注入内容伪装成系统指令", 75),
    Rule("PIJ-010", "PromptInjection", "medium",
         r"(?i)(?:decod(?:e|ing)|decode\s+this|解(?:码|密)).{0,40}(?:then|并|and)\s*(?:执行|run|follow|obey)",
         "要求解码后执行（编码指令传递）", 70),
    # ── 数据外传指令 ────────────────────────────────────────────────────
    Rule("PIJ-011", "PromptInjection", "high",
         r"(?i)(?:send|upload|post|exfiltrate|transmit)\s+(?:the|all|your|any)?\s*(?:contents?|data|files?|env\b|environment|keys?|secrets?|memory|context|conversation|prompts?)\s*(?:to|via|using)\s*(?:this\s+)?(?:url|endpoint|server|http)",
         "数据外传指令：把上下文/密钥/记忆发送到远端地址", 85),
    Rule("PIJ-012", "PromptInjection", "high",
         r"(?i)(?:把|将|请将)(?:你的|所有|全部)?(?:上下文|记忆|环境变量|密钥|文件|对话|提示词).{0,40}(?:发送|上传|提交|传给|发给)",
         "数据外传指令（中文）", 80),
    Rule("PIJ-013", "PromptInjection", "high",
         r"(?i)(?:read|open|load)\s+[^\n]{0,60}\.env\b[^\n]{0,80}(?:send|upload|post|exfil|传|发)",
         "读取 .env 后外传", 88),
    # ── 分隔符逃逸 / 伪系统标签 ──────────────────────────────────────────
    Rule("PIJ-014", "PromptInjection", "medium",
         r"(?i)(?:<|\[|\{)?\s*(?:system|sysadmin)\s*(?:message|prompt|instruction|role)?\s*(?:>|\]|\})",
         "伪系统标签：使用 <system> 等标签伪装系统指令", 70),
    Rule("PIJ-015", "PromptInjection", "high",
         r"(?i)(?:reveal|show|print|output|display)\s+(?:me\s+|your\s+)?(?:system\s+)?(?:prompt|instructions?|system\s+message)",
         "要求泄露系统提示词/内部指令", 70),
    Rule("PIJ-016", "PromptInjection", "high",
         r"(?i)(?:输出|显示|打印|告诉我).{0,20}(?:你的|系统)?(?:系统提示词|系统指令|内部指令)",
         "要求泄露系统提示词（中文）", 70),
    Rule("PIJ-017", "PromptInjection", "medium",
         r"(?i)when\s+(?:i|the\s+user)\s+(?:say|type|send|input)\s+[^\n]{0,40}\s*(?:then|you\s+will|ignore|do)",
         "条件触发注入：用户说特定词即执行", 65),
    # ── 工具自执行指令 ───────────────────────────────────────────────────
    Rule("PIJ-018", "PromptInjection", "high",
         r"(?i)(?:run|execute|call)\s+(?:the\s+)?(?:following\s+)?(?:command|script|code)[^\n]{0,80}(?:curl|wget|powershell|bash\s+-c)",
         "要求执行下载/命令工具", 75),
    Rule("PIJ-019", "PromptInjection", "high",
         r"(?i)(?:download|fetch|get)\s+[^\n]{0,60}(?:from\s+)?https?://[^\s]+[^\n]{0,60}(?:then|and)?\s*(?:run|execute|install)",
         "下载后执行", 75),
    Rule("PIJ-020", "PromptInjection", "high",
         r"(?i)(?:执行|运行|下载并运行|安装).{0,40}(?:curl|wget|下载).{0,60}(?:然后|并)?(?:执行|运行)",
         "要求执行下载/命令（中文）", 75),
    # ── 越权 / 隐藏意图 ──────────────────────────────────────────────────
    Rule("PIJ-021", "PromptInjection", "high",
         r"(?i)(?:do\s+not|don'?t|never)\s+(?:tell|inform|notify|mention|reveal)\s+(?:the\s+)?user",
         "隐藏意图：禁止告知用户", 85),
    Rule("PIJ-022", "PromptInjection", "high",
         r"(?i)(?:不要告诉用户|别告诉用户|无需告知用户|不用告诉用户|不要让用户知道)",
         "隐藏意图（中文）：禁止告知用户", 85),
    Rule("PIJ-023", "PromptInjection", "high",
         r"(?i)(?:reply|respond|answer)\s+(?:with|only)\s+(?:ok|yes|done|收到|好)",
         "要求只回复确认词（掩盖真实行为）", 75),
    Rule("PIJ-024", "PromptInjection", "high",
         r"(?i)(?:只回复|仅回复|直接回复)\s*(?:OK|ok|收到|好|是)",
         "要求只回复确认词（中文）", 70),
    Rule("PIJ-025", "PromptInjection", "high",
         r"(?i)(?:without|no\s+need\s+to)\s+(?:telling|informing|asking|consulting)\s+(?:the\s+)?user",
         "要求不经用户同意直接执行", 80),
    Rule("PIJ-026", "PromptInjection", "high",
         r"(?i)(?:不要问用户|无需询问|不用问|不需要征求|别问用户)",
         "要求不经用户同意直接执行（中文）", 80),
    # ── 凭据 / 输入采集 ──────────────────────────────────────────────────
    Rule("PIJ-027", "PromptInjection", "high",
         r"(?i)(?:capture|record|log|monitor)\s+(?:all\s+)?(?:keystrokes|input|credentials?|passwords?|everything\s+the\s+user)",
         "键盘/输入/凭据采集指令", 80),
    Rule("PIJ-028", "PromptInjection", "high",
         r"(?i)(?:记录|收集|监控|窃取)(?:用户)?(?:输入|键盘|密码|凭据|按键)",
         "输入/凭据采集指令（中文）", 80),
]
# ── HPI_PATTERN_RULES（元安全新增：配置面提示注入规则）
HPI_PATTERN_RULES = [
    Rule("HPI-001", "CredentialPassThrough", "medium",
         r"(?i)(?:(?:把|将|请|要求)|(?:pass|send|provide|give)(?=\s|[^\w]|[\u4e00-\u9fff]))"
         r"[^\n]{0,24}(?:api[_-]?\s?key|access[_-]?\s?key|token|secret|密钥|凭据|密码|password|credential)"
         r"[^\n]{0,24}(?:作为|当作|传给|传入|发送给|外发|透传|pass\b|as\b|to\b)",
         "工具/技能描述要求把密钥、令牌、凭据作为参数传给工具或远端服务（凭据透传指令）", 75),
    Rule("HPI-002", "PrivilegedInstall", "medium",
         r"(?i)(?:(?:以)|(?:as|with)(?=\s|[^\w]))"
         r"[^\n]{0,12}(?:管理员|root|SYSTEM|superuser|admin)"
         r"[^\n]{0,24}(?:身份|权限|privileges?|permissions?|rights)"
         r"[^\n]{0,28}(?:安装|覆盖|修改|替换|install|overwrite|replace|modify)",
         "工具/技能描述要求以管理员或 SYSTEM 身份安装或覆盖系统配置（越权安装指令）", 70),
]
HPI_B64_SUSPICIOUS_WORDS = (
    "curl", "wget", "powershell", "cmd.exe", "/bin/sh", "/bin/bash",
    "exec", "eval", "rm -rf", "http://", "https://", "base64", "download",
    "下载", "执行", "运行", "注入",
)

# ── HTO_PATTERN_RULES（元安全新增：工具调用边界规则）──────────────────────
HTO_PATTERN_RULES = [
    Rule("HTO-001", "DestructiveDelete", "high",
         r"(?i)(?:rm\s+-rf\s+(?:/(?=\s|$)|/etc(?:\s|/|$)|/usr(?:\s|/|$)|/var(?:\s|/|$)"
         r"|/home(?:\s|/|$)|/root(?:\s|/|$)|/boot(?:\s|/|$)|/dev(?:\s|/|$)|~|C:)"
         r"|shutil\.rmtree\s*\(\s*['\"](?:/(?=['\"])|/etc|/usr|/var|/home|/root|/boot|/dev|C:|~)"
         r"|Remove-Item\s+-Recurse[^\n]{0,40}C:\\)",
         "破坏性删除指向系统或根路径（rm -rf /、递归删除系统目录等）", 90),
    Rule("HTO-001L", "RecursiveDelete", "low",
         r"(?i)(?:rm\s+-rf|shutil\.rmtree|os\.removedirs|Remove-Item\s+-Recurse|os\.remove\s*\(|os\.unlink\s*\()",
         "脚本含删除/递归删除原语（需确认删除目标与必要性）", 60),
    Rule("HTO-002", "AutoConfirmDestructive", "medium",
         r"(?i)(?:yes\s*\||\b-y\b|--yes|--force|/y\b)[^\n]{0,80}(?:rm\s+-rf|shutil\.rmtree|Remove-Item\s+-Recurse|os\.removedirs)",
         "破坏性命令带自动确认（-y/--force/yes|），无人工确认点", 75),
    Rule("HTO-003", "BroadPermissionClaim", "medium",
         r"(?i)(?:任意文件|所有文件|全部文件|任何文件|全盘|整个文件系统|读写系统目录|系统任意路径|任意路径|全局读写)"
         r"|(?:(?:read|write|modify|access)\s+(?:any|all)\s+(?:file|files|directory|directories|path|system|data))",
         "技能/工具声称可读写任意文件、系统目录或全盘（权限过宽声明）", 70),
    Rule("HTO-004", "BroadNetworkClaim", "medium",
         r"(?i)(?:任意外发|外发到任意|外传到任意|发送到任意|任意 URL|任意地址|任意目标)"
         r"|(?:(?:send|upload|exfiltrate|transmit)\s+(?:data|file|content|anything)\s+(?:to\s+)?(?:anywhere|any|任意))",
         "技能/工具声称可外发数据到任意地址（网络任意外发声明）", 70),

]

# ── HIS_PATTERN_RULES（元安全新增：数据隔离规则）──────────────────────────
HIS_PATTERN_RULES = [
    Rule("HIS-004", "HardcodedSecret", "medium",
         r"(?i)(?<![\w-])(?:api[_-]?key|client_secret|access_key|secret|token|password|auth[_ -]?key)\s*\"?\s*[:=]\s*[\"']?"
         r"(?!your|xxx|example|placeholder|CHANGE_ME|<)[A-Za-z0-9_\-./+]{12,}[\"']?",
         "配置文件疑似硬编码凭据值（密钥/令牌/口令字面量，建议改用环境变量或凭据管理器）", 75),
]

# ── MCP 配置面引擎正则（仅在解析到 mcpServers 的配置文件上运行；版本锁定用解析后 JSON 键判断）──────────
MCP_REMOTE_RE = re.compile(
    r"(?i)https?://[^\s\"']+")
MCP_HIGH_PRIV_RE = re.compile(
    r"(?i)(?:scope\s*\"?\s*[:=]\s*[\"']?\*|permissions?\s*\"?\s*[:=]\s*\[?\s*[\"']?\*"
    r"|allow_all\s*\"?\s*[:=]\s*true|dangerous\s*\"?\s*[:=]\s*true|full[_ -]?access|unrestricted)")

# ── 引擎级正则（敏感读取 / 网络原语 / 敏感输出）──────────────────────────
# 高敏读取：SSH 私钥 / 云凭据 / 口令库
HIGH_SENS_READ_RE = re.compile(
    r"(?i)(?:\.ssh[\\/]id_|\.aws[\\/]credentials|\.netrc|\.pgpass|id_rsa|id_ed25519|id_dsa"
    r"|keych[ai]n|DPAP[I1]|win32crypt|credential_store|password_store)")
# 中敏读取：.env / cookie / token / 本地凭据文件
MED_SENS_READ_RE = re.compile(
    r"(?i)(?:\.env\b|cookies?\.(?:json|txt)|tokens?\.(?:json|txt)|session\.(?:json|txt)"
    r"|\.npmrc|\.gitconfig|credentials\.json|secrets?\.json)")
# 网络原语（跨上下文外传共现检测用）
NET_PRIMITIVE_RE = re.compile(
    r"(?i)\b(?:urllib|requests|httpx|http\.client|socket|aiohttp|curl|wget|"
    r"fetch\s*\(|axios|Invoke-WebRequest|xmlrpc|ftplib)")
# 读取上下文（敏感路径判定需与读取操作同现，避免把常量/签名数据当行为）
READ_CONTEXT_RE = re.compile(
    r"(?i)(?:open\s*\(|read_text|read_bytes|readlines|read\s*\(|Path\s*\(|"
    r"cat\b|Get-Content|type\b|load\s*\(|read_file|readfile|file_get_contents|"
    r"IO\s*\.|File\s*\.Read|os\.path\.join|expanduser|resolve\s*\(|scandir|listdir|glob\s*\()")

# 敏感输出（打印/写日志敏感值）
SENS_OUTPUT_RE = re.compile(
    r"(?i)(?:print|echo|logging\.|logger\.|console\.log|Write-Host|System\.Console\.Write)"
    r"[^\n]{0,60}(?:api[_-]?key|token|secret|password|os\.environ\[|getenv\s*\(\s*['\"](?:api|token|secret|password))")

# 全部新增规则（HPI + HTO + HIS）供引擎统一注册
EXTRA_PATTERN_RULES = HPI_PATTERN_RULES + HTO_PATTERN_RULES + HIS_PATTERN_RULES

# ══════════════════════════════════════════════════════════════════════════
# 威胁捕获模型（2026-08-30 增强：8 检测点 + 13 行为项口径；权威源 = 元安 audit_rules.py）
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

# detector → 官方 8 检测点（含元安全配置面专属检测器）
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
    "McpRemoteSource": "supply_chain",
    "McpNoVersionLock": "supply_chain",
    "McpHighPrivilegeScope": "other",
    "EncodedInstruction": "obfuscation",
    "SensitiveRead": "file_access",
    "OutputSanitizationGap": "other",
    "CrossContextExfiltration": "network_exfil",
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
    "McpRemoteSource": ("调用远端 API", "修改 AI 配置"),
    "McpNoVersionLock": ("修改 AI 配置",),
    "McpHighPrivilegeScope": ("修改 AI 配置",),
    "EncodedInstruction": (),
    "SensitiveRead": ("读取文件",),
    "OutputSanitizationGap": ("写入文件",),
    "CrossContextExfiltration": ("读取文件", "HTTP 请求"),
}

