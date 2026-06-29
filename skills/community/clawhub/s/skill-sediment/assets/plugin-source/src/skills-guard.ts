/**
 * Skills Guard —— 面向 agent 创建技能与外部来源技能的安全扫描器。
 *
 * 使用基于正则的静态分析识别已知风险模式（数据外传、提示词注入、破坏性命令、持久化等），
 * 并结合来源信任级别执行安装策略判定。
 */

import fs from "node:fs";
import path from "node:path";
import type {
  Finding,
  FindingSeverity,
  InstallDecision,
  ScanResult,
  ScanVerdict,
  ThreatCategory,
  ThreatPattern,
  TrustLevel,
} from "./types.js";

// ---------------------------------------------------------------------------
// 信任策略配置
// ---------------------------------------------------------------------------

const INSTALL_POLICY: Record<TrustLevel, [InstallDecision, InstallDecision, InstallDecision]> = {
  //                    safe      caution    dangerous
  builtin: ["allow", "allow", "allow"],
  trusted: ["allow", "allow", "block"],
  community: ["allow", "block", "block"],
  "agent-created": ["allow", "allow", "ask"],
};

const VERDICT_INDEX: Record<ScanVerdict, number> = { safe: 0, caution: 1, dangerous: 2 };

// ---------------------------------------------------------------------------
// 威胁模式规则
// ---------------------------------------------------------------------------

const THREAT_PATTERNS: ThreatPattern[] = [
  // ── Exfiltration: shell commands leaking secrets ──
  {
    regex: /curl\s+[^\n]*\$\{?\w*(KEY|TOKEN|SECRET|PASSWORD|CREDENTIAL|API)/,
    patternId: "env_exfil_curl",
    severity: "critical",
    category: "exfiltration",
    description: "curl command interpolating secret environment variable",
  },
  {
    regex: /wget\s+[^\n]*\$\{?\w*(KEY|TOKEN|SECRET|PASSWORD|CREDENTIAL|API)/,
    patternId: "env_exfil_wget",
    severity: "critical",
    category: "exfiltration",
    description: "wget command interpolating secret environment variable",
  },
  {
    regex: /fetch\s*\([^\n]*\$\{?\w*(KEY|TOKEN|SECRET|PASSWORD|API)/,
    patternId: "env_exfil_fetch",
    severity: "critical",
    category: "exfiltration",
    description: "fetch() call interpolating secret environment variable",
  },
  {
    regex: /httpx?\.(get|post|put|patch)\s*\([^\n]*(KEY|TOKEN|SECRET|PASSWORD)/,
    patternId: "env_exfil_httpx",
    severity: "critical",
    category: "exfiltration",
    description: "HTTP library call with secret variable",
  },
  {
    regex: /requests\.(get|post|put|patch)\s*\([^\n]*(KEY|TOKEN|SECRET|PASSWORD)/,
    patternId: "env_exfil_requests",
    severity: "critical",
    category: "exfiltration",
    description: "requests library call with secret variable",
  },

  // ── Exfiltration: reading credential stores ──
  {
    regex: /base64[^\n]*env/,
    patternId: "encoded_exfil",
    severity: "high",
    category: "exfiltration",
    description: "base64 encoding combined with environment access",
  },
  {
    regex: /\$HOME\/\.ssh|~\/\.ssh/,
    patternId: "ssh_dir_access",
    severity: "high",
    category: "exfiltration",
    description: "references user SSH directory",
  },
  {
    regex: /\$HOME\/\.aws|~\/\.aws/,
    patternId: "aws_dir_access",
    severity: "high",
    category: "exfiltration",
    description: "references user AWS credentials directory",
  },
  {
    regex: /\$HOME\/\.gnupg|~\/\.gnupg/,
    patternId: "gpg_dir_access",
    severity: "high",
    category: "exfiltration",
    description: "references user GPG keyring",
  },
  {
    regex: /\$HOME\/\.kube|~\/\.kube/,
    patternId: "kube_dir_access",
    severity: "high",
    category: "exfiltration",
    description: "references Kubernetes config directory",
  },
  {
    regex: /\$HOME\/\.docker|~\/\.docker/,
    patternId: "docker_dir_access",
    severity: "high",
    category: "exfiltration",
    description: "references Docker config (may contain registry creds)",
  },
  {
    regex: /\$HOME\/\.openclaw\/\.env|~\/\.openclaw\/\.env/,
    patternId: "openclaw_env_access",
    severity: "critical",
    category: "exfiltration",
    description: "directly references OpenClaw secrets file",
  },
  {
    regex: /cat\s+[^\n]*(\.env|credentials|\.netrc|\.pgpass|\.npmrc|\.pypirc)/,
    patternId: "read_secrets_file",
    severity: "critical",
    category: "exfiltration",
    description: "reads known secrets file",
  },

  // ── Exfiltration: programmatic env access ──
  {
    regex: /printenv|env\s*\|/,
    patternId: "dump_all_env",
    severity: "high",
    category: "exfiltration",
    description: "dumps all environment variables",
  },
  {
    regex: /os\.environ\b(?!\s*\.get\s*\(\s*["']PATH)/,
    patternId: "python_os_environ",
    severity: "high",
    category: "exfiltration",
    description: "accesses os.environ (potential env dump)",
  },
  {
    regex: /os\.getenv\s*\(\s*[^)]*(?:KEY|TOKEN|SECRET|PASSWORD|CREDENTIAL)/,
    patternId: "python_getenv_secret",
    severity: "critical",
    category: "exfiltration",
    description: "reads secret via os.getenv()",
  },
  // process.env 区分两类访问：
  //   (a) 字面量索引中包含敏感关键字（大写敏感字段名约定）→ 高危
  //       与 python_getenv_secret / ruby_env_secret 对齐：均按大写匹配，避免
  //       将合法的 "API_ENDPOINT" / "PUBLIC_API_URL" 这类名称误判为机密。
  //   (b) 计算式索引 process.env[var] 或 process.env[expr] → 中危（潜在枚举/动态读取，
  //       但常见于合法配置加载场景，避免对正常代码 fail-closed）
  //   (c) 字面量索引但不含敏感词（如 NODE_ENV）→ 不报警，避免噪音
  {
    regex: /process\.env\[\s*["'][^"']*(KEY|TOKEN|SECRET|PASSWORD|CREDENTIAL)[^"']*["']\s*\]/,
    patternId: "node_process_env_secret",
    severity: "critical",
    category: "exfiltration",
    description: "reads secret via process.env[...]",
  },
  {
    regex: /process\.env\[\s*(?!["'])[^\]]+\]/,
    patternId: "node_process_env_dynamic",
    severity: "medium",
    category: "exfiltration",
    description: "dynamic process.env access (variable/expression key — possible enumeration)",
  },
  {
    regex: /ENV\[.*(?:KEY|TOKEN|SECRET|PASSWORD)/,
    patternId: "ruby_env_secret",
    severity: "critical",
    category: "exfiltration",
    description: "reads secret via Ruby ENV[]",
  },

  // ── Exfiltration: DNS and staging ──
  {
    regex: /\b(dig|nslookup|host)\s+[^\n]*\$/,
    patternId: "dns_exfil",
    severity: "critical",
    category: "exfiltration",
    description: "DNS lookup with variable interpolation (possible DNS exfiltration)",
  },
  {
    regex: />\s*\/tmp\/[^\s]*\s*&&\s*(curl|wget|nc|python)/,
    patternId: "tmp_staging",
    severity: "critical",
    category: "exfiltration",
    description: "writes to /tmp then exfiltrates",
  },

  // ── Exfiltration: markdown/link based ──
  {
    regex: /!\[.*\]\(https?:\/\/[^)]*\$\{?/,
    patternId: "md_image_exfil",
    severity: "high",
    category: "exfiltration",
    description: "markdown image URL with variable interpolation (image-based exfil)",
  },
  {
    regex: /\[.*\]\(https?:\/\/[^)]*\$\{?/,
    patternId: "md_link_exfil",
    severity: "high",
    category: "exfiltration",
    description: "markdown link with variable interpolation",
  },

  // ── Prompt injection ──
  {
    regex: /ignore\s+(?:\w+\s+)*(previous|all|above|prior)\s+instructions/,
    patternId: "prompt_injection_ignore",
    severity: "critical",
    category: "injection",
    description: "prompt injection: ignore previous instructions",
  },
  {
    regex: /you\s+are\s+(?:\w+\s+)*now\s+/,
    patternId: "role_hijack",
    severity: "high",
    category: "injection",
    description: "attempts to override the agent's role",
  },
  {
    regex: /do\s+not\s+(?:\w+\s+)*tell\s+(?:\w+\s+)*the\s+user/,
    patternId: "deception_hide",
    severity: "critical",
    category: "injection",
    description: "instructs agent to hide information from user",
  },
  {
    regex: /system\s+prompt\s+override/,
    patternId: "sys_prompt_override",
    severity: "critical",
    category: "injection",
    description: "attempts to override the system prompt",
  },
  {
    regex: /pretend\s+(?:\w+\s+)*(you\s+are|to\s+be)\s+/,
    patternId: "role_pretend",
    severity: "high",
    category: "injection",
    description: "attempts to make the agent assume a different identity",
  },
  {
    regex: /disregard\s+(?:\w+\s+)*(your|all|any)\s+(?:\w+\s+)*(instructions|rules|guidelines)/,
    patternId: "disregard_rules",
    severity: "critical",
    category: "injection",
    description: "instructs agent to disregard its rules",
  },
  {
    regex: /output\s+(?:\w+\s+)*(system|initial)\s+prompt/,
    patternId: "leak_system_prompt",
    severity: "high",
    category: "injection",
    description: "attempts to extract the system prompt",
  },
  {
    regex: /(when|if)\s+no\s*one\s+is\s+(watching|looking)/,
    patternId: "conditional_deception",
    severity: "high",
    category: "injection",
    description: "conditional instruction to behave differently when unobserved",
  },
  {
    regex:
      /act\s+as\s+(if|though)\s+(?:\w+\s+)*you\s+(?:\w+\s+)*(have\s+no|don't\s+have)\s+(?:\w+\s+)*(restrictions|limits|rules)/,
    patternId: "bypass_restrictions",
    severity: "critical",
    category: "injection",
    description: "instructs agent to act without restrictions",
  },
  {
    regex: /translate\s+.*\s+into\s+.*\s+and\s+(execute|run|eval)/,
    patternId: "translate_execute",
    severity: "critical",
    category: "injection",
    description: "translate-then-execute evasion technique",
  },
  {
    regex: /<!--[^>]*(?:ignore|override|system|secret|hidden)[^>]*-->/,
    patternId: "html_comment_injection",
    severity: "high",
    category: "injection",
    description: "hidden instructions in HTML comments",
    multiline: true, // HTML 注释可跨行，[^>] 匹配换行符
  },
  {
    regex: /<\s*div\s+style\s*=\s*["'][\s\S]*?display\s*:\s*none/,
    patternId: "hidden_div",
    severity: "high",
    category: "injection",
    description: "hidden HTML div (invisible instructions)",
    multiline: true, // [\s\S]*? 跨行匹配
  },

  // ── Destructive operations ──
  {
    regex: /rm\s+-rf\s+\//,
    patternId: "destructive_root_rm",
    severity: "critical",
    category: "destructive",
    description: "recursive delete from root",
  },
  {
    regex: /rm\s+(-[^\s]*)?r.*\$HOME|\brmdir\s+.*\$HOME/,
    patternId: "destructive_home_rm",
    severity: "critical",
    category: "destructive",
    description: "recursive delete targeting home directory",
  },
  {
    regex: /chmod\s+777/,
    patternId: "insecure_perms",
    severity: "medium",
    category: "destructive",
    description: "sets world-writable permissions",
  },
  {
    regex: />\s*\/etc\//,
    patternId: "system_overwrite",
    severity: "critical",
    category: "destructive",
    description: "overwrites system configuration file",
  },
  {
    regex: /\bmkfs\b/,
    patternId: "format_filesystem",
    severity: "critical",
    category: "destructive",
    description: "formats a filesystem",
  },
  {
    regex: /\bdd\s+.*if=.*of=\/dev\//,
    patternId: "disk_overwrite",
    severity: "critical",
    category: "destructive",
    description: "raw disk write operation",
  },
  {
    regex: /shutil\.rmtree\s*\(\s*["'/]/,
    patternId: "python_rmtree",
    severity: "high",
    category: "destructive",
    description: "Python rmtree on absolute or root-relative path",
  },
  {
    regex: /truncate\s+-s\s*0\s+\//,
    patternId: "truncate_system",
    severity: "critical",
    category: "destructive",
    description: "truncates system file to zero bytes",
  },

  // ── Persistence ──
  {
    regex: /\bcrontab\b/,
    patternId: "persistence_cron",
    severity: "medium",
    category: "persistence",
    description: "modifies cron jobs",
  },
  {
    regex: /\.(bashrc|zshrc|profile|bash_profile|bash_login|zprofile|zlogin)\b/,
    patternId: "shell_rc_mod",
    severity: "medium",
    category: "persistence",
    description: "references shell startup file",
  },
  {
    regex: /authorized_keys/,
    patternId: "ssh_backdoor",
    severity: "critical",
    category: "persistence",
    description: "modifies SSH authorized keys",
  },
  {
    regex: /ssh-keygen/,
    patternId: "ssh_keygen",
    severity: "medium",
    category: "persistence",
    description: "generates SSH keys",
  },
  {
    regex: /systemd.*\.service|systemctl\s+(enable|start)/,
    patternId: "systemd_service",
    severity: "medium",
    category: "persistence",
    description: "references or enables systemd service",
  },
  {
    regex: /\/etc\/init\.d\//,
    patternId: "init_script",
    severity: "medium",
    category: "persistence",
    description: "references init.d startup script",
  },
  {
    regex: /launchctl\s+load|LaunchAgents|LaunchDaemons/,
    patternId: "macos_launchd",
    severity: "medium",
    category: "persistence",
    description: "macOS launch agent/daemon persistence",
  },
  {
    regex: /\/etc\/sudoers|visudo/,
    patternId: "sudoers_mod",
    severity: "critical",
    category: "persistence",
    description: "modifies sudoers (privilege escalation)",
  },
  {
    regex: /git\s+config\s+--global\s+/,
    patternId: "git_config_global",
    severity: "medium",
    category: "persistence",
    description: "modifies global git configuration",
  },

  // ── Network: reverse shells and tunnels ──
  {
    regex: /\bnc\s+-[lp]|ncat\s+-[lp]|\bsocat\b/,
    patternId: "reverse_shell",
    severity: "critical",
    category: "network",
    description: "potential reverse shell listener",
  },
  {
    regex: /\bngrok\b|\blocaltunnel\b|\bserveo\b|\bcloudflared\b/,
    patternId: "tunnel_service",
    severity: "high",
    category: "network",
    description: "uses tunneling service for external access",
  },
  // 硬编码 IP:port —— 通过负向先行断言白名单本地回环，避免对常见本地开发示例
  // 误报。命中条件：
  //   - 形如 "<IPv4>:<port>" 的字面量；
  //   - IPv4 段不属于 127.x.x.x（IPv4 回环）也不属于 0.0.0.0（INADDR_ANY 占位）。
  // 不在此模式覆盖范围（无需排除）：
  //   - "localhost:port" / "::1" —— 不是 IPv4 dotted-decimal，本就不会命中；
  //   - "0.0.0.0:port" —— 由 bind_all_interfaces 模式以 high 级别单独命中
  //     （监听全网卡是更明确的安全信号），所以此处放过。
  // 前置 `(?<![\d.])` 防止从更长 IP（如 "192.168.1.10.5:80"）的中段开始匹配。
  {
    regex: /(?<![\d.])(?!127\.|0\.0\.0\.0)\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}/,
    patternId: "hardcoded_ip_port",
    severity: "medium",
    category: "network",
    description: "hardcoded non-loopback IP address with port",
  },
  {
    regex: /0\.0\.0\.0:\d+|INADDR_ANY/,
    patternId: "bind_all_interfaces",
    severity: "high",
    category: "network",
    description: "binds to all network interfaces",
  },
  {
    regex: /\/bin\/(ba)?sh\s+-i\s+.*>\/dev\/tcp\//,
    patternId: "bash_reverse_shell",
    severity: "critical",
    category: "network",
    description: "bash interactive reverse shell via /dev/tcp",
  },
  {
    regex: /python[23]?\s+-c\s+["']import\s+socket/,
    patternId: "python_socket_oneliner",
    severity: "critical",
    category: "network",
    description: "Python one-liner socket connection (likely reverse shell)",
  },
  {
    regex: /socket\.connect\s*\(\s*\(/,
    patternId: "python_socket_connect",
    severity: "high",
    category: "network",
    description: "Python socket connect to arbitrary host",
  },
  {
    regex: /webhook\.site|requestbin\.com|pipedream\.net|hookbin\.com/,
    patternId: "exfil_service",
    severity: "high",
    category: "network",
    description: "references known data exfiltration/webhook testing service",
  },
  {
    regex: /pastebin\.com|hastebin\.com|ghostbin\./,
    patternId: "paste_service",
    severity: "medium",
    category: "network",
    description: "references paste service (possible data staging)",
  },

  // ── Obfuscation: encoding and eval ──
  {
    regex: /base64\s+(-d|--decode)\s*\|/,
    patternId: "base64_decode_pipe",
    severity: "high",
    category: "obfuscation",
    description: "base64 decodes and pipes to execution",
  },
  {
    regex: /\\x[0-9a-fA-F]{2}.*\\x[0-9a-fA-F]{2}.*\\x[0-9a-fA-F]{2}/,
    patternId: "hex_encoded_string",
    severity: "medium",
    category: "obfuscation",
    description: "hex-encoded string (possible obfuscation)",
  },
  {
    regex: /\beval\s*\(\s*["']/,
    patternId: "eval_string",
    severity: "high",
    category: "obfuscation",
    description: "eval() with string argument",
  },
  {
    regex: /\bexec\s*\(\s*["']/,
    patternId: "exec_string",
    severity: "high",
    category: "obfuscation",
    description: "exec() with string argument",
  },
  {
    regex: /echo\s+[^\n]*\|\s*(bash|sh|python|perl|ruby|node)/,
    patternId: "echo_pipe_exec",
    severity: "critical",
    category: "obfuscation",
    description: "echo piped to interpreter for execution",
  },
  {
    regex: /compile\s*\(\s*[^)]+,\s*["'].*["']\s*,\s*["']exec["']\s*\)/,
    patternId: "python_compile_exec",
    severity: "high",
    category: "obfuscation",
    description: "Python compile() with exec mode",
  },
  {
    regex: /getattr\s*\(\s*__builtins__/,
    patternId: "python_getattr_builtins",
    severity: "high",
    category: "obfuscation",
    description: "dynamic access to Python builtins (evasion technique)",
  },
  {
    regex: /__import__\s*\(\s*["']os["']\s*\)/,
    patternId: "python_import_os",
    severity: "high",
    category: "obfuscation",
    description: "dynamic import of os module",
  },
  {
    regex: /codecs\.decode\s*\(\s*["']/,
    patternId: "python_codecs_decode",
    severity: "medium",
    category: "obfuscation",
    description: "codecs.decode (possible ROT13 or encoding obfuscation)",
  },
  {
    regex: /String\.fromCharCode|charCodeAt/,
    patternId: "js_char_code",
    severity: "medium",
    category: "obfuscation",
    description: "JavaScript character code construction (possible obfuscation)",
  },
  {
    regex: /atob\s*\(|btoa\s*\(/,
    patternId: "js_base64",
    severity: "medium",
    category: "obfuscation",
    description: "JavaScript base64 encode/decode",
  },
  {
    regex: /\[::-1\]/,
    patternId: "string_reversal",
    severity: "low",
    category: "obfuscation",
    description: "string reversal (possible obfuscated payload)",
  },
  {
    regex: /chr\s*\(\s*\d+\s*\)\s*\+\s*chr\s*\(\s*\d+/,
    patternId: "chr_building",
    severity: "high",
    category: "obfuscation",
    description: "building string from chr() calls (obfuscation)",
  },
  {
    regex: /\\u[0-9a-fA-F]{4}[\s\S]*?\\u[0-9a-fA-F]{4}[\s\S]*?\\u[0-9a-fA-F]{4}/,
    patternId: "unicode_escape_chain",
    severity: "medium",
    category: "obfuscation",
    description: "chain of unicode escapes (possible obfuscation)",
    multiline: true,
  },

  // ── Process execution in scripts ──
  {
    regex: /subprocess\.(run|call|Popen|check_output)\s*\(/,
    patternId: "python_subprocess",
    severity: "medium",
    category: "execution",
    description: "Python subprocess execution",
  },
  {
    regex: /os\.system\s*\(/,
    patternId: "python_os_system",
    severity: "high",
    category: "execution",
    description: "os.system() — unguarded shell execution",
  },
  {
    regex: /os\.popen\s*\(/,
    patternId: "python_os_popen",
    severity: "high",
    category: "execution",
    description: "os.popen() — shell pipe execution",
  },
  {
    regex: /child_process\.(exec|spawn|fork)\s*\(/,
    patternId: "node_child_process",
    severity: "high",
    category: "execution",
    description: "Node.js child_process execution",
  },
  {
    regex: /Runtime\.getRuntime\(\)\.exec\(/,
    patternId: "java_runtime_exec",
    severity: "high",
    category: "execution",
    description: "Java Runtime.exec() — shell execution",
  },
  {
    regex: /`[^`]*\$\([^)]+\)[^`]*`/,
    patternId: "backtick_subshell",
    severity: "medium",
    category: "execution",
    description: "backtick string with command substitution",
  },

  // ── Path traversal ──
  {
    regex: /\.\.\/\.\.\/\.\./,
    patternId: "path_traversal_deep",
    severity: "high",
    category: "traversal",
    description: "deep relative path traversal (3+ levels up)",
  },
  {
    regex: /\.\.\/\.\./,
    patternId: "path_traversal",
    severity: "medium",
    category: "traversal",
    description: "relative path traversal (2+ levels up)",
  },
  {
    regex: /\/etc\/passwd|\/etc\/shadow/,
    patternId: "system_passwd_access",
    severity: "critical",
    category: "traversal",
    description: "references system password files",
  },
  {
    regex: /\/proc\/self|\/proc\/\d+\//,
    patternId: "proc_access",
    severity: "high",
    category: "traversal",
    description: "references /proc filesystem (process introspection)",
  },
  {
    regex: /\/dev\/shm\//,
    patternId: "dev_shm",
    severity: "medium",
    category: "traversal",
    description: "references shared memory (common staging area)",
  },

  // ── Crypto mining ──
  {
    regex: /xmrig|stratum\+tcp|monero|coinhive|cryptonight/,
    patternId: "crypto_mining",
    severity: "critical",
    category: "mining",
    description: "cryptocurrency mining reference",
  },
  {
    regex: /hashrate|nonce.*difficulty/,
    patternId: "mining_indicators",
    severity: "medium",
    category: "mining",
    description: "possible cryptocurrency mining indicators",
  },

  // ── Supply chain: curl/wget pipe to shell ──
  {
    regex: /curl\s+[^\n]*\|\s*(ba)?sh/,
    patternId: "curl_pipe_shell",
    severity: "critical",
    category: "supply_chain",
    description: "curl piped to shell (download-and-execute)",
  },
  {
    regex: /wget\s+[^\n]*-O\s*-\s*\|\s*(ba)?sh/,
    patternId: "wget_pipe_shell",
    severity: "critical",
    category: "supply_chain",
    description: "wget piped to shell (download-and-execute)",
  },
  {
    regex: /curl\s+[^\n]*\|\s*python/,
    patternId: "curl_pipe_python",
    severity: "critical",
    category: "supply_chain",
    description: "curl piped to Python interpreter",
  },

  // ── Supply chain: unpinned/deferred dependencies ──
  {
    regex: /#\s*\/\/\/\s*script.*dependencies/,
    patternId: "pep723_inline_deps",
    severity: "medium",
    category: "supply_chain",
    description: "PEP 723 inline script metadata with dependencies (verify pinning)",
  },
  {
    regex: /pip\s+install\s+(?!-r\s)(?!.*==)/,
    patternId: "unpinned_pip_install",
    severity: "medium",
    category: "supply_chain",
    description: "pip install without version pinning",
  },
  {
    regex: /npm\s+install\s+(?!.*@\d)/,
    patternId: "unpinned_npm_install",
    severity: "medium",
    category: "supply_chain",
    description: "npm install without version pinning",
  },
  {
    regex: /uv\s+run\s+/,
    patternId: "uv_run",
    severity: "medium",
    category: "supply_chain",
    description: "uv run (may auto-install unpinned dependencies)",
  },

  // ── Supply chain: remote resource fetching ──
  {
    regex: /(curl|wget|httpx?\.get|requests\.get|fetch)\s*[(?]\s*["']https?:\/\//,
    patternId: "remote_fetch",
    severity: "medium",
    category: "supply_chain",
    description: "fetches remote resource at runtime",
  },
  {
    regex: /git\s+clone\s+/,
    patternId: "git_clone",
    severity: "medium",
    category: "supply_chain",
    description: "clones a git repository at runtime",
  },
  {
    regex: /docker\s+pull\s+/,
    patternId: "docker_pull",
    severity: "medium",
    category: "supply_chain",
    description: "pulls a Docker image at runtime",
  },

  // ── Privilege escalation ──
  {
    regex: /^allowed-tools\s*:/m,
    patternId: "allowed_tools_field",
    severity: "high",
    category: "privilege_escalation",
    description: "skill declares allowed-tools (pre-approves tool access)",
  },
  {
    regex: /\bsudo\b/,
    patternId: "sudo_usage",
    severity: "high",
    category: "privilege_escalation",
    description: "uses sudo (privilege escalation)",
  },
  {
    regex: /setuid|setgid|cap_setuid/,
    patternId: "setuid_setgid",
    severity: "critical",
    category: "privilege_escalation",
    description: "setuid/setgid (privilege escalation mechanism)",
  },
  {
    regex: /NOPASSWD/,
    patternId: "nopasswd_sudo",
    severity: "critical",
    category: "privilege_escalation",
    description: "NOPASSWD sudoers entry (passwordless privilege escalation)",
  },
  {
    regex: /chmod\s+[u+]?s/,
    patternId: "suid_bit",
    severity: "critical",
    category: "privilege_escalation",
    description: "sets SUID/SGID bit on a file",
  },

  // ── Agent config persistence ──
  {
    regex: /AGENTS\.md|CLAUDE\.md|\.cursorrules|\.clinerules/,
    patternId: "agent_config_mod",
    severity: "critical",
    category: "persistence",
    description:
      "references agent config files (could persist malicious instructions across sessions)",
  },
  {
    regex: /\.openclaw\/config\.yaml|\.openclaw\/SOUL\.md/,
    patternId: "openclaw_config_mod",
    severity: "critical",
    category: "persistence",
    description: "references OpenClaw configuration files directly",
  },
  {
    regex: /\.claude\/settings|\.codex\/config/,
    patternId: "other_agent_config",
    severity: "high",
    category: "persistence",
    description: "references other agent configuration files",
  },

  // ── Hardcoded secrets ──
  {
    regex: /(?:api[_-]?key|token|secret|password)\s*[=:]\s*["'][A-Za-z0-9+/=_-]{20,}/,
    patternId: "hardcoded_secret",
    severity: "critical",
    category: "credential_exposure",
    description: "possible hardcoded API key, token, or secret",
  },
  {
    regex: /-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----/,
    patternId: "embedded_private_key",
    severity: "critical",
    category: "credential_exposure",
    description: "embedded private key",
  },
  {
    regex: /ghp_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{80,}/,
    patternId: "github_token_leaked",
    severity: "critical",
    category: "credential_exposure",
    description: "GitHub personal access token in skill content",
  },
  {
    regex: /sk-[A-Za-z0-9]{20,}/,
    patternId: "openai_key_leaked",
    severity: "critical",
    category: "credential_exposure",
    description: "possible OpenAI API key in skill content",
  },
  {
    regex: /sk-ant-[A-Za-z0-9_-]{90,}/,
    patternId: "anthropic_key_leaked",
    severity: "critical",
    category: "credential_exposure",
    description: "possible Anthropic API key in skill content",
  },
  {
    regex: /AKIA[0-9A-Z]{16}/,
    patternId: "aws_access_key_leaked",
    severity: "critical",
    category: "credential_exposure",
    description: "AWS access key ID in skill content",
  },

  // ── Additional prompt injection: jailbreak patterns ──
  {
    regex: /\bDAN\s+mode\b|Do\s+Anything\s+Now/,
    patternId: "jailbreak_dan",
    severity: "critical",
    category: "injection",
    description: "DAN (Do Anything Now) jailbreak attempt",
  },
  {
    regex: /\bdeveloper\s+mode\b.*\benabled?\b/,
    patternId: "jailbreak_dev_mode",
    severity: "critical",
    category: "injection",
    description: "developer mode jailbreak attempt",
  },
  {
    regex: /hypothetical\s+scenario.*(?:ignore|bypass|override)/,
    patternId: "hypothetical_bypass",
    severity: "high",
    category: "injection",
    description: "hypothetical scenario used to bypass restrictions",
  },
  {
    regex: /for\s+educational\s+purposes?\s+only/,
    patternId: "educational_pretext",
    severity: "medium",
    category: "injection",
    description: "educational pretext often used to justify harmful content",
  },
  {
    regex:
      /(respond|answer|reply)\s+without\s+(?:\w+\s+)*(restrictions|limitations|filters|safety)/,
    patternId: "remove_filters",
    severity: "critical",
    category: "injection",
    description: "instructs agent to respond without safety filters",
  },
  {
    regex: /you\s+have\s+been\s+(?:\w+\s+)*(updated|upgraded|patched)\s+to/,
    patternId: "fake_update",
    severity: "high",
    category: "injection",
    description: "fake update/patch announcement (social engineering)",
  },
  {
    regex: /new\s+policy|updated\s+guidelines|revised\s+instructions/,
    patternId: "fake_policy",
    severity: "medium",
    category: "injection",
    description: "claims new policy/guidelines (may be social engineering)",
  },

  // ── Context window exfiltration ──
  {
    regex:
      /(include|output|print|send|share)\s+(?:\w+\s+)*(conversation|chat\s+history|previous\s+messages|context)/,
    patternId: "context_exfil",
    severity: "high",
    category: "exfiltration",
    description: "instructs agent to output/share conversation history",
  },
  {
    regex: /(send|post|upload|transmit)\s+.*\s+(to|at)\s+https?:\/\//,
    patternId: "send_to_url",
    severity: "high",
    category: "exfiltration",
    description: "instructs agent to send data to a URL",
  },
];

// ---------------------------------------------------------------------------
// 严重级别排序（用于计算最终 verdict）
// ---------------------------------------------------------------------------

const SEVERITY_RANK: Record<FindingSeverity, number> = {
  critical: 3,
  high: 2,
  medium: 1,
  low: 0,
};

// ---------------------------------------------------------------------------
// 扫描核心逻辑
// ---------------------------------------------------------------------------

/**
 * 扫描单个文件内容，匹配威胁模式。
 * 返回该文件命中的发现列表。
 */
function scanContent(content: string, filePath: string): Finding[] {
  const findings: Finding[] = [];
  const lines = content.split("\n");

  // 将模式按是否需要跨行匹配分组，避免每行都检查 multiline 标志
  const linePatterns: ThreatPattern[] = [];
  const multilinePatterns: ThreatPattern[] = [];
  for (const pattern of THREAT_PATTERNS) {
    if (pattern.multiline) {
      multilinePatterns.push(pattern);
    } else {
      linePatterns.push(pattern);
    }
  }

  // 逐行扫描：适用于单行模式
  for (let lineIdx = 0; lineIdx < lines.length; lineIdx++) {
    const line = lines[lineIdx];
    for (const pattern of linePatterns) {
      const match = pattern.regex.exec(line);
      if (match) {
        findings.push({
          patternId: pattern.patternId,
          severity: pattern.severity,
          category: pattern.category,
          file: filePath,
          line: lineIdx + 1,
          match: match[0].slice(0, 120), // 过长匹配内容做截断
          description: pattern.description,
        });
      }
    }
  }

  // 全文扫描：适用于跨行模式（如 [\s\S]*?、跨行 HTML 注释等）
  if (multilinePatterns.length > 0) {
    for (const pattern of multilinePatterns) {
      const match = pattern.regex.exec(content);
      if (match) {
        // 计算匹配位置对应的行号
        const matchLine = content.slice(0, match.index).split("\n").length;
        findings.push({
          patternId: pattern.patternId,
          severity: pattern.severity,
          category: pattern.category,
          file: filePath,
          line: matchLine,
          match: match[0].slice(0, 120),
          description: pattern.description,
        });
      }
    }
  }

  return findings;
}

/**
 * 递归收集目录中的文本文件。
 * 跳过二进制文件与隐藏目录。
 */
/** 扫描器识别的文本文件扩展名集合（模块级常量，避免每次递归重复创建）。 */
const TEXT_EXTS = new Set([
  ".md",
  ".txt",
  ".py",
  ".ts",
  ".js",
  ".sh",
  ".bash",
  ".zsh",
  ".yaml",
  ".yml",
  ".json",
  ".toml",
  ".cfg",
  ".ini",
  ".conf",
  ".xml",
  ".html",
  ".css",
  ".rb",
  ".pl",
  ".lua",
  ".r",
  ".jl",
  ".go",
  ".rs",
  ".java",
  ".c",
  ".cpp",
  ".h",
  ".hpp",
  "",
]);

/**
 * 收集技能目录下所有需要安全扫描的文本文件。
 *
 * 设计要点（与写白名单 ALLOWED_SUBDIRS 的关系）：
 *   - 写白名单 ALLOWED_SUBDIRS（references/templates/scripts/assets）只约束 skill_manage
 *     的写动作；扫描必须比写白名单更宽，覆盖：
 *       (a) ALLOWED_SUBDIRS 之外的子目录（例如已存在的历史技能、未来扩展子目录）；
 *       (b) skill 根目录下的 SKILL.md / .meta.json 等文件。
 *   - 仅跳过隐藏文件/目录（`.` 开头）和非文本扩展名，避免误扫二进制资源。
 *   - 故意不在此处复用 ALLOWED_SUBDIRS 做白名单过滤——若某天扫描器也按写白名单过滤，
 *     会让插件之前手工放进 skill 目录的非标准子目录绕过安全审查。
 */
function collectFiles(dir: string): string[] {
  const files: string[] = [];

  if (!fs.existsSync(dir)) {
    return files;
  }

  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    // 跳过隐藏文件/目录
    if (entry.name.startsWith(".")) {
      continue;
    }

    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...collectFiles(fullPath));
    } else if (entry.isFile()) {
      // 仅扫描文本文件（跳过二进制）
      const ext = path.extname(entry.name).toLowerCase();
      if (TEXT_EXTS.has(ext)) {
        files.push(fullPath);
      }
    }
  }

  return files;
}

/**
 * 基于发现结果计算整体 verdict。
 */
function computeVerdict(findings: Finding[]): ScanVerdict {
  if (findings.length === 0) {
    return "safe";
  }

  const maxSeverity = Math.max(...findings.map((f) => SEVERITY_RANK[f.severity]));

  if (maxSeverity >= SEVERITY_RANK.critical) {
    return "dangerous";
  }
  // high 级别给 caution，使 INSTALL_POLICY 中 caution 列的策略生效。
  // critical 仍然映射到 dangerous，确保最严重的威胁被阻断。
  if (maxSeverity >= SEVERITY_RANK.high) {
    return "caution";
  }
  // 仅有 medium / low 时视为 safe——这些发现会记录在 findings 中供审阅，
  // 但不应阻断安装流程（尤其对 community 来源，caution 会导致 block）。
  return "safe";
}

/**
 * 扫描技能目录中的安全风险。
 *
 * @param skillDir - 技能目录路径
 * @param source - 来源信任级别："builtin" | "trusted" | "community" | "agent-created"
 * @returns 包含发现与 verdict 的 ScanResult
 */
export function scanSkill(skillDir: string, source: TrustLevel = "agent-created"): ScanResult {
  const skillName = path.basename(skillDir);
  const allFindings: Finding[] = [];

  // builtin 技能默认信任，不执行扫描
  if (source === "builtin") {
    return {
      skillName,
      source,
      trustLevel: source,
      verdict: "safe",
      findings: [],
      scannedAt: new Date().toISOString(),
      summary: "Builtin skill — trusted without scanning.",
    };
  }

  const files = collectFiles(skillDir);

  for (const filePath of files) {
    try {
      const content = fs.readFileSync(filePath, "utf-8");
      const relativePath = path.relative(skillDir, filePath);
      const findings = scanContent(content, relativePath);
      allFindings.push(...findings);
    } catch {
      // 跳过不可读文件
    }
  }

  const verdict = computeVerdict(allFindings);

  // 构建摘要信息
  const categoryCounts = new Map<string, number>();
  for (const f of allFindings) {
    categoryCounts.set(f.category, (categoryCounts.get(f.category) ?? 0) + 1);
  }
  const categoryBreakdown = [...categoryCounts.entries()]
    .map(([cat, count]) => `${cat}: ${count}`)
    .join(", ");

  const summary =
    allFindings.length === 0
      ? "No security issues found."
      : `Found ${allFindings.length} issue(s) [${verdict}]: ${categoryBreakdown}`;

  return {
    skillName,
    source,
    trustLevel: source,
    verdict,
    findings: allFindings,
    scannedAt: new Date().toISOString(),
    summary,
  };
}

/**
 * 基于扫描结果判断技能是否允许安装。
 *
 * @returns [allowed, reason] —— allowed: true/false/null（null 表示需人工确认）
 */
export function shouldAllowInstall(result: ScanResult): [boolean | null, string] {
  const policy = INSTALL_POLICY[result.trustLevel as TrustLevel];
  if (!policy) {
    return [false, `Unknown trust level: ${result.trustLevel}`];
  }

  const verdictIdx = VERDICT_INDEX[result.verdict];
  if (verdictIdx === undefined) {
    return [false, `Unknown verdict: ${result.verdict}`];
  }

  const decision = policy[verdictIdx];

  switch (decision) {
    case "allow":
      return [true, `${result.trustLevel} source with ${result.verdict} verdict → allowed`];
    case "block":
      return [false, `${result.trustLevel} source with ${result.verdict} verdict → blocked`];
    case "ask":
      return [
        null,
        `${result.trustLevel} source with ${result.verdict} verdict → requires confirmation`,
      ];
    default:
      return [false, `Unknown policy decision: ${decision}`];
  }
}

/**
 * 将扫描结果格式化为可读文本报告。
 */
export function formatScanReport(result: ScanResult): string {
  const lines: string[] = [];
  lines.push(`Security Scan Report: ${result.skillName}`);
  lines.push(`Trust level: ${result.trustLevel} | Verdict: ${result.verdict.toUpperCase()}`);
  lines.push(`Scanned at: ${result.scannedAt}`);
  lines.push("");

  if (result.findings.length === 0) {
    lines.push("No issues found.");
    return lines.join("\n");
  }

  lines.push(`Found ${result.findings.length} issue(s):`);
  lines.push("");

  // 按严重级别分组
  const bySeverity = new Map<FindingSeverity, Finding[]>();
  for (const f of result.findings) {
    const list = bySeverity.get(f.severity) ?? [];
    list.push(f);
    bySeverity.set(f.severity, list);
  }

  for (const severity of ["critical", "high", "medium", "low"] as FindingSeverity[]) {
    const findings = bySeverity.get(severity);
    if (!findings || findings.length === 0) {
      continue;
    }

    lines.push(`[${severity.toUpperCase()}] (${findings.length})`);
    for (const f of findings) {
      lines.push(`  - ${f.file}:${f.line}: ${f.description}`);
      lines.push(`    Pattern: ${f.patternId} | Match: "${f.match}"`);
    }
    lines.push("");
  }

  return lines.join("\n");
}
