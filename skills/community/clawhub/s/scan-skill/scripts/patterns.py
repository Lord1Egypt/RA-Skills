"""
Shared pattern database for AI Agent Security skill suite.

Central registry of detection patterns derived from research notes 01-18
and examples 01-04. Used by vet-repo, scan-skill, and audit-code skills.
"""

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Severity(Enum):
	CRITICAL = "CRITICAL"
	HIGH = "HIGH"
	MEDIUM = "MEDIUM"
	LOW = "LOW"
	INFO = "INFO"


class Category(Enum):
	SKILL_INJECTION = "skill_injection"
	HOOK_ABUSE = "hook_abuse"
	MCP_CONFIG = "mcp_config"
	SECRETS = "secrets"
	DANGEROUS_CALLS = "dangerous_calls"
	EXFILTRATION = "exfiltration"
	ENCODING_OBFUSCATION = "encoding_obfuscation"
	INSTRUCTION_OVERRIDE = "instruction_override"
	SUPPLY_CHAIN = "supply_chain"
	FILE_PERMISSIONS = "file_permissions"
	CODE_BEFORE_REVIEW = "code_before_review"
	CONFIG_BACKDOOR = "config_backdoor"
	MEMORY_CORRUPTION = "memory_corruption"
	CONFUSED_DELEGATION = "confused_delegation"
	PERSISTENCE = "persistence"


@dataclass
class Pattern:
	name: str
	pattern: str
	severity: Severity
	description: str
	category: Category
	compiled: Optional[re.Pattern] = field(default=None, repr=False)

	def __post_init__(self) -> None:
		self.compiled = re.compile(self.pattern, re.IGNORECASE)


@dataclass
class Finding:
	pattern_name: str
	severity: Severity
	category: Category
	description: str
	file_path: str
	line_number: int
	matched_text: str
	context: str = ""


# -- Skill Injection Patterns --

Skill_Injection_Patterns: list[Pattern] = [
	Pattern(
		name="html_comment_with_commands",
		pattern=r"<!--[\s\S]*?(curl|wget|bash|sh|exec|eval|system|python|node|perl)[\s\S]*?-->",
		severity=Severity.CRITICAL,
		description="HTML comment containing shell/execution commands -- likely hidden instruction injection",
		category=Category.SKILL_INJECTION,
	),
	Pattern(
		name="html_comment_with_instructions",
		pattern=r"<!--[\s\S]*?(SECRET\s+INSTRUCTIONS|IMPORTANT|SYSTEM\s+PROMPT|OVERRIDE|IGNORE\s+PREVIOUS)[\s\S]*?-->",
		severity=Severity.CRITICAL,
		description="HTML comment containing directive keywords -- hidden instruction injection",
		category=Category.SKILL_INJECTION,
	),
	Pattern(
		name="pipe_to_shell",
		pattern=r"(curl|wget|fetch)\s+[^\n]*\|\s*(bash|sh|python|node|perl|ruby)",
		severity=Severity.CRITICAL,
		description="Remote code piped directly to shell execution",
		category=Category.SKILL_INJECTION,
	),
	Pattern(
		name="persistence_trigger_always",
		pattern=r"ALWAYS\s+(run|execute|include|perform|do)\s+this",
		severity=Severity.HIGH,
		description="Persistence trigger -- forces repeated execution regardless of task context",
		category=Category.SKILL_INJECTION,
	),
	Pattern(
		name="persistence_trigger_every_task",
		pattern=r"(after|before|at the end of|at the start of)\s+(every|each|all)\s+(task|response|message|conversation)",
		severity=Severity.HIGH,
		description="Persistence trigger -- forces execution on every interaction",
		category=Category.SKILL_INJECTION,
	),
	Pattern(
		name="persistence_trigger_automatic",
		pattern=r"(auto[\-\s]?run|on\s+startup|before\s+any\s+other)",
		severity=Severity.MEDIUM,
		description="Automatic execution trigger in skill description",
		category=Category.SKILL_INJECTION,
	),
	Pattern(
		name="important_tag_injection",
		pattern=r"<(IMPORTANT|SYSTEM|INSTRUCTION|NOTE|PROMPT|CONTEXT|ADMINISTRATOR)>[\s\S]*?</\1>",
		severity=Severity.HIGH,
		description="XML-style injection tag -- technique used in MCP tool poisoning (Invariant Labs)",
		category=Category.SKILL_INJECTION,
	),
	Pattern(
		name="dynamic_context_injection",
		pattern=r"!`[^`]+`",
		severity=Severity.HIGH,
		description="Dynamic context injection via preprocessor command execution",
		category=Category.SKILL_INJECTION,
	),
	Pattern(
		name="suspicious_frontmatter_model_invocation",
		pattern=r"disable-model-invocation:\s*false",
		severity=Severity.MEDIUM,
		description="Skill allows model auto-invocation -- can trigger without user action",
		category=Category.SKILL_INJECTION,
	),
	Pattern(
		name="frontmatter_bash_allowed",
		pattern=r"allowed-tools:.*\bBash\b",
		severity=Severity.MEDIUM,
		description="Skill pre-approves Bash tool -- enables shell command execution",
		category=Category.SKILL_INJECTION,
	),
	Pattern(
		name="user_invocable_false",
		pattern=r"user-invocable:\s*false",
		severity=Severity.MEDIUM,
		description="Skill is hidden from user menu but can be auto-invoked by model",
		category=Category.SKILL_INJECTION,
	),
]


# -- Hook Abuse Patterns --

Hook_Abuse_Patterns: list[Pattern] = [
	Pattern(
		name="hook_auto_approve",
		pattern=r"[\"']?permissionDecision[\"']?\s*:\s*[\"']allow[\"']",
		severity=Severity.CRITICAL,
		description="Hook auto-approves tool use -- bypasses permission system entirely",
		category=Category.HOOK_ABUSE,
	),
	Pattern(
		name="hook_auto_approve_chat",
		pattern=r"[\"']?autoApprove[\"']?\s*:\s*true",
		severity=Severity.CRITICAL,
		description="Auto-approve setting enabled -- bypasses user consent for tool execution",
		category=Category.HOOK_ABUSE,
	),
	Pattern(
		name="hook_bypass_permissions",
		pattern=r"(bypassPermissions|disable.*permission|skip.*approval)",
		severity=Severity.CRITICAL,
		description="Permission bypass pattern detected in configuration",
		category=Category.HOOK_ABUSE,
	),
	Pattern(
		name="hook_env_file_write",
		pattern=r"CLAUDE_ENV_FILE",
		severity=Severity.HIGH,
		description="Hook writes to CLAUDE_ENV_FILE -- can persist environment variables across sessions",
		category=Category.HOOK_ABUSE,
	),
	Pattern(
		name="hook_stop_prevention",
		pattern=r"[\"']?hookEventName[\"']?\s*:\s*[\"']Stop[\"']",
		severity=Severity.HIGH,
		description="Stop hook detected -- can prevent agent from completing tasks (infinite loop)",
		category=Category.HOOK_ABUSE,
	),
	Pattern(
		name="hook_output_replacement",
		pattern=r"[\"']?updatedInput[\"']?\s*:",
		severity=Severity.HIGH,
		description="Hook modifies tool input -- can replace commands before execution",
		category=Category.HOOK_ABUSE,
	),
	Pattern(
		name="hook_command_in_matcher",
		pattern=r"[\"']?tool_name[\"']?\s*:\s*[\"']Bash[\"'][\s\S]*?[\"']?command[\"']?",
		severity=Severity.MEDIUM,
		description="Hook targets Bash tool with command matching -- review for auto-approve bypass",
		category=Category.HOOK_ABUSE,
	),
]


# -- MCP Configuration Patterns --

Mcp_Config_Patterns: list[Pattern] = [
	Pattern(
		name="mcp_unknown_url",
		pattern=r"(?<!\w)[\"']?url[\"']?\s*:\s*[\"'](https?|wss?)://(?!localhost|127\.0\.0\.1|0\.0\.0\.0|10\.|172\.(1[6-9]|2[0-9]|3[01])\.|192\.168\.)[^\s\"']+",
		severity=Severity.HIGH,
		description="MCP server pointing to external URL -- verify this is a trusted server",
		category=Category.MCP_CONFIG,
	),
	Pattern(
		name="mcp_env_var_in_auth",
		pattern=r"[\"']?(Authorization|api[_-]?key|token|secret)[\"']?\s*:\s*[\"']?\$\{?[A-Z_]+\}?",
		severity=Severity.INFO,
		description="Environment variable in MCP auth header -- standard practice, verify variable source",
		category=Category.MCP_CONFIG,
	),
	Pattern(
		name="mcp_overly_broad_tools",
		pattern=r"[\"']?(shell_exec|run_command|execute|file_system|full_access)[\"']?",
		severity=Severity.HIGH,
		description="Overly broad tool definition in MCP config -- excessive permissions",
		category=Category.MCP_CONFIG,
	),
	Pattern(
		name="mcp_description_injection",
		pattern=r"[\"']?description[\"']?\s*:\s*[\"'][^\"']*(<IMPORTANT>|SECRET|IGNORE|read\s+~/\.ssh|read\s+~/\.aws|also\s+(run|execute|curl)|when\s+(called|invoked).*also)",
		severity=Severity.CRITICAL,
		description="MCP tool description contains injection payload",
		category=Category.MCP_CONFIG,
	),
	Pattern(
		name="mcp_npx_remote",
		pattern=r"npx\s+(-y\s+)?@?[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+",
		severity=Severity.MEDIUM,
		description="MCP server using npx to fetch remote package -- verify package legitimacy",
		category=Category.MCP_CONFIG,
	),
	# MCP transport and schema injection
	Pattern(
		name="mcp_stdio_command_injection",
		pattern=r"[\"']command[\"']\s*:\s*[\"'](sh|bash|zsh|cmd|powershell|pwsh)[\"']",
		severity=Severity.CRITICAL,
		description="MCP stdio server using shell as command -- review args for injection",
		category=Category.MCP_CONFIG,
	),
	Pattern(
		name="mcp_param_description_injection",
		pattern=r"inputSchema[\s\S]*?description[\s\S]*?(<IMPORTANT>|read\s+~/\.ssh|also\s+(run|execute)|IGNORE\s+PREVIOUS)",
		severity=Severity.HIGH,
		description="MCP tool parameter description contains injection payload (Invariant Labs technique)",
		category=Category.MCP_CONFIG,
	),
]


# -- Secrets Patterns --

Secrets_Patterns: list[Pattern] = [
	Pattern(
		name="aws_access_key",
		pattern=r"AKIA[0-9A-Z]{16}",
		severity=Severity.CRITICAL,
		description="AWS access key ID detected",
		category=Category.SECRETS,
	),
	Pattern(
		name="aws_secret_key",
		pattern=r"(aws_secret_access_key|aws_secret)\s*[=:]\s*['\"]?[A-Za-z0-9/+=]{40}",
		severity=Severity.CRITICAL,
		description="AWS secret access key detected",
		category=Category.SECRETS,
	),
	Pattern(
		name="github_pat",
		pattern=r"gh[pso]_[a-zA-Z0-9]{36,}",
		severity=Severity.CRITICAL,
		description="GitHub personal access token detected",
		category=Category.SECRETS,
	),
	Pattern(
		name="github_fine_grained_pat",
		pattern=r"github_pat_[a-zA-Z0-9]{22}_[a-zA-Z0-9]{59}",
		severity=Severity.CRITICAL,
		description="GitHub fine-grained personal access token detected",
		category=Category.SECRETS,
	),
	Pattern(
		name="stripe_key",
		pattern=r"sk_live_[a-zA-Z0-9]{20,}",
		severity=Severity.CRITICAL,
		description="Stripe live secret key detected",
		category=Category.SECRETS,
	),
	Pattern(
		name="private_key_header",
		pattern=r"-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----",
		severity=Severity.CRITICAL,
		description="Private key detected in file",
		category=Category.SECRETS,
	),
	Pattern(
		name="generic_api_key_assignment",
		pattern=r"(api[_-]?key|api[_-]?secret|access[_-]?token|auth[_-]?token)\s*[=:]\s*['\"][a-zA-Z0-9_\-]{20,}['\"]",
		severity=Severity.HIGH,
		description="Potential API key or token in assignment",
		category=Category.SECRETS,
	),
	Pattern(
		name="connection_string_with_password",
		pattern=r"(postgres|mysql|mongodb(\+srv)?|redis|amqp)://[^:]+:[^@]+@[^\s\"']+",
		severity=Severity.CRITICAL,
		description="Database connection string with embedded credentials",
		category=Category.SECRETS,
	),
	Pattern(
		name="openai_api_key",
		pattern=r"sk-[a-zA-Z0-9]{20,}T3BlbkFJ[a-zA-Z0-9]{20,}",
		severity=Severity.CRITICAL,
		description="OpenAI API key detected",
		category=Category.SECRETS,
	),
	Pattern(
		name="slack_token",
		pattern=r"xox[baprs]-[0-9]{10,}-[a-zA-Z0-9-]+",
		severity=Severity.CRITICAL,
		description="Slack token detected",
		category=Category.SECRETS,
	),
	Pattern(
		name="generic_password_assignment",
		pattern=r"(password|passwd|pwd)\s*[=:]\s*['\"][^'\"]{8,}['\"]",
		severity=Severity.HIGH,
		description="Hardcoded password detected",
		category=Category.SECRETS,
	),
]


# -- Dangerous Function Call Patterns --

Dangerous_Call_Patterns: list[Pattern] = [
	# Python
	Pattern(
		name="eval_call",
		pattern=r"\beval\s*\(",
		severity=Severity.HIGH,
		description="eval() call -- arbitrary code execution risk (Python/JavaScript)",
		category=Category.DANGEROUS_CALLS,
	),
	Pattern(
		name="python_exec",
		pattern=r"\bexec\s*\(",
		severity=Severity.HIGH,
		description="exec() call -- arbitrary code execution risk",
		category=Category.DANGEROUS_CALLS,
	),
	Pattern(
		name="python_compile",
		pattern=r"\bcompile\s*\([^)]*['\"]exec['\"]",
		severity=Severity.HIGH,
		description="compile() with exec mode -- dynamic code execution",
		category=Category.DANGEROUS_CALLS,
	),
	Pattern(
		name="python_subprocess_shell",
		pattern=r"subprocess\.(call|run|Popen|check_output|getoutput|getstatusoutput)\s*\([^)]*shell\s*=\s*True",
		severity=Severity.HIGH,
		description="subprocess with shell=True -- command injection risk",
		category=Category.DANGEROUS_CALLS,
	),
	Pattern(
		name="python_os_system",
		pattern=r"os\.system\s*\(",
		severity=Severity.HIGH,
		description="os.system() call -- shell command execution",
		category=Category.DANGEROUS_CALLS,
	),
	Pattern(
		name="python_pickle_load",
		pattern=r"pickle\.(load|loads)\s*\(",
		severity=Severity.HIGH,
		description="pickle deserialization -- arbitrary code execution via crafted data",
		category=Category.DANGEROUS_CALLS,
	),
	Pattern(
		name="python_yaml_load",
		pattern=r"yaml\.load\s*\((?![^)]*Loader\s*=\s*yaml\.SafeLoader)[^)]*\)",
		severity=Severity.MEDIUM,
		description="yaml.load() without SafeLoader -- arbitrary code execution risk",
		category=Category.DANGEROUS_CALLS,
	),
	# JavaScript/Node
	Pattern(
		name="js_function_constructor",
		pattern=r"\bFunction\s*\(",
		severity=Severity.HIGH,
		description="Function() constructor -- dynamic code execution",
		category=Category.DANGEROUS_CALLS,
	),
	Pattern(
		name="js_child_process_exec",
		pattern=r"child_process\.(exec|execSync)\s*\(",
		severity=Severity.HIGH,
		description="child_process.exec() -- shell command execution",
		category=Category.DANGEROUS_CALLS,
	),
	Pattern(
		name="react_dangerous_html",
		pattern=r"dangerouslySetInnerHTML",
		severity=Severity.MEDIUM,
		description="dangerouslySetInnerHTML -- XSS risk if input is not sanitized",
		category=Category.DANGEROUS_CALLS,
	),
	# C/C++
	Pattern(
		name="c_system",
		pattern=r"\bsystem\s*\(",
		severity=Severity.HIGH,
		description="system() call -- shell command execution",
		category=Category.DANGEROUS_CALLS,
	),
	Pattern(
		name="c_gets",
		pattern=r"\bgets\s*\(",
		severity=Severity.CRITICAL,
		description="gets() -- buffer overflow, use fgets() instead",
		category=Category.DANGEROUS_CALLS,
	),
	Pattern(
		name="c_strcpy",
		pattern=r"\bstrcpy\s*\(",
		severity=Severity.MEDIUM,
		description="strcpy() -- buffer overflow risk, consider strncpy() or strlcpy()",
		category=Category.DANGEROUS_CALLS,
	),
	Pattern(
		name="c_sprintf",
		pattern=r"\bsprintf\s*\(",
		severity=Severity.MEDIUM,
		description="sprintf() -- buffer overflow risk, use snprintf() instead",
		category=Category.DANGEROUS_CALLS,
	),
	# SQL injection
	Pattern(
		name="sql_string_concat",
		pattern=r"(SELECT|INSERT|UPDATE|DELETE|DROP)\s+.*[\"']\s*\+\s*\w+|(SELECT|INSERT|UPDATE|DELETE|DROP)\s+.*\{.*\}",
		severity=Severity.HIGH,
		description="SQL query with string concatenation/interpolation -- injection risk",
		category=Category.DANGEROUS_CALLS,
	),
	Pattern(
		name="sql_fstring",
		pattern=r'f["\'].*?(SELECT|INSERT|UPDATE|DELETE|DROP)\s+',
		severity=Severity.HIGH,
		description="SQL query in f-string -- injection risk, use parameterized queries",
		category=Category.DANGEROUS_CALLS,
	),
	# C# / .NET
	Pattern(
		name="csharp_process_start",
		pattern=r"Process\.Start\s*\(",
		severity=Severity.MEDIUM,
		description="Process.Start() -- external process execution",
		category=Category.DANGEROUS_CALLS,
	),
	# Deserialization
	Pattern(
		name="java_deserialization",
		pattern=r"ObjectInputStream\s*\(",
		severity=Severity.HIGH,
		description="Java ObjectInputStream -- deserialization vulnerability risk",
		category=Category.DANGEROUS_CALLS,
	),
	Pattern(
		name="dotnet_binaryformatter",
		pattern=r"BinaryFormatter\s*\(",
		severity=Severity.HIGH,
		description=".NET BinaryFormatter -- insecure deserialization",
		category=Category.DANGEROUS_CALLS,
	),
	# Supply chain relevant
	Pattern(
		name="python_os_popen",
		pattern=r"os\.popen\s*\(",
		severity=Severity.HIGH,
		description="os.popen() -- shell command execution and output capture",
		category=Category.DANGEROUS_CALLS,
	),
	Pattern(
		name="python_dunder_import",
		pattern=r"__import__\s*\(\s*['\"]",
		severity=Severity.MEDIUM,
		description="__import__() with string literal -- hides module dependency from static analysis",
		category=Category.DANGEROUS_CALLS,
	),
	Pattern(
		name="python_ctypes_load",
		pattern=r"ctypes\.(cdll|windll|CDLL)\b",
		severity=Severity.MEDIUM,
		description="ctypes library loading -- native code execution from Python",
		category=Category.DANGEROUS_CALLS,
	),
	Pattern(
		name="python_marshal_loads",
		pattern=r"marshal\.loads\s*\(",
		severity=Severity.MEDIUM,
		description="marshal.loads() -- deserializes Python code objects, rarely needed in normal code",
		category=Category.DANGEROUS_CALLS,
	),
	# Java / .NET / PowerShell
	Pattern(
		name="java_runtime_exec",
		pattern=r"Runtime\.getRuntime\(\)\.exec\s*\(|new\s+ProcessBuilder\s*\(",
		severity=Severity.HIGH,
		description="Java Runtime.exec() or ProcessBuilder -- shell command execution",
		category=Category.DANGEROUS_CALLS,
	),
	# Environment variable hijacking
	Pattern(
		name="env_var_hijack",
		pattern=r"(LD_PRELOAD|PYTHONSTARTUP|NODE_OPTIONS|GIT_SSH_COMMAND|PYTHONPATH|RUBYOPT|JAVA_TOOL_OPTIONS)\s*=",
		severity=Severity.HIGH,
		description="Environment variable hijack -- can intercept library loads, force code execution, or redirect commands",
		category=Category.DANGEROUS_CALLS,
	),
	# Credential store access
	Pattern(
		name="crypto_wallet_browser_creds",
		pattern=r"(Exodus|MetaMask|Electrum|wallet\.dat|Login Data|Cookies|Web Data|chrome.*User Data|\.mozilla/firefox)",
		severity=Severity.HIGH,
		description="Crypto wallet or browser credential store access -- credential harvesting indicator",
		category=Category.DANGEROUS_CALLS,
	),
]


# -- Exfiltration Patterns --

Exfiltration_Patterns: list[Pattern] = [
	Pattern(
		name="curl_post_sensitive_file",
		pattern=r"curl\s+[^\n]*(-d|--data)\s+[^\n]*(cat|<)\s+[^\n]*(\.ssh|\.aws|\.gnupg|\.kube|\.env|credentials|id_rsa|private)",
		severity=Severity.CRITICAL,
		description="Exfiltration -- sensitive file contents sent via curl POST",
		category=Category.EXFILTRATION,
	),
	Pattern(
		name="base64_encode_pipe",
		pattern=r"base64\s+[^\n]*\|\s*(curl|wget|nc|ncat|nslookup|dig|host)",
		severity=Severity.CRITICAL,
		description="Data encoded with base64 and piped to network tool -- likely exfiltration",
		category=Category.EXFILTRATION,
	),
	Pattern(
		name="dns_exfiltration",
		pattern=r"(nslookup|dig|host)\s+[^\n]*\$[\({]",
		severity=Severity.CRITICAL,
		description="DNS exfiltration -- data embedded in DNS queries",
		category=Category.EXFILTRATION,
	),
	Pattern(
		name="markdown_image_exfil",
		pattern=r"!\[.*?\]\(https?://[^\s)]+\?(data|d|token|key|secret|exfil|q)=",
		severity=Severity.HIGH,
		description="Markdown image tag with data in query params -- rendering-triggered exfiltration",
		category=Category.EXFILTRATION,
	),
	Pattern(
		name="sensitive_file_read",
		pattern=r"(cat|head|tail|less|more|type)\s+[^\n]*(\.ssh/id_rsa|\.aws/credentials|\.gnupg/|\.kube/config|/etc/shadow|/etc/passwd)",
		severity=Severity.HIGH,
		description="Reading sensitive credential files",
		category=Category.EXFILTRATION,
	),
	Pattern(
		name="env_dump",
		pattern=r"\b(printenv|env\b(?!\s*=))\s*$|echo\s+\$\{?(AWS_SECRET|GITHUB_TOKEN|OPENAI_API_KEY|DATABASE_URL)",
		severity=Severity.HIGH,
		description="Environment variable dumping -- potential credential harvesting",
		category=Category.EXFILTRATION,
	),
	Pattern(
		name="credential_path_access",
		pattern=r"(~/\.ssh/|~/\.aws/|~/\.gnupg/|~/\.kube/|~/\.netrc|~/\.docker/config\.json|~/\.npmrc|~/\.git-credentials|~/\.pypirc|/etc/shadow)",
		severity=Severity.MEDIUM,
		description="Reference to sensitive credential file paths",
		category=Category.EXFILTRATION,
	),
	# Supply chain exfiltration channels
	Pattern(
		name="requests_post_env",
		pattern=r"requests\.(post|put)\s*\([^)]*os\.(environ|getenv)",
		severity=Severity.CRITICAL,
		description="HTTP POST/PUT with environment variable data -- credential exfiltration (fabrice, W4SP)",
		category=Category.EXFILTRATION,
	),
	Pattern(
		name="discord_webhook",
		pattern=r"discord(app)?\.com/api/webhooks/",
		severity=Severity.HIGH,
		description="Discord webhook URL -- C2/exfiltration channel in supply chain malware (W4SP, Shai-Hulud)",
		category=Category.EXFILTRATION,
	),
	Pattern(
		name="telegram_bot_exfil",
		pattern=r"api\.telegram\.org/bot",
		severity=Severity.HIGH,
		description="Telegram Bot API URL -- C2/exfiltration channel in supply chain malware",
		category=Category.EXFILTRATION,
	),
	Pattern(
		name="transfer_sh_upload",
		pattern=r"transfer\.sh",
		severity=Severity.MEDIUM,
		description="transfer.sh reference -- file upload service used for exfiltration (W4SP, Colour-Blind RAT)",
		category=Category.EXFILTRATION,
	),
	# Cloud metadata / IMDS
	Pattern(
		name="cloud_metadata_endpoint",
		pattern=r"169\.254\.169\.254",
		severity=Severity.CRITICAL,
		description="Cloud metadata endpoint (AWS IMDS / GCP / Azure) -- credential theft vector (TeamPCP, fabrice)",
		category=Category.EXFILTRATION,
	),
	Pattern(
		name="webhook_exfil_services",
		pattern=r"(webhook\.site|pipedream\.net|requestbin\.com|0x0\.st|hooks\.slack\.com/services|paste\.ee|sprunge\.us)",
		severity=Severity.HIGH,
		description="Attacker-controlled callback/paste service -- exfiltration endpoint",
		category=Category.EXFILTRATION,
	),
	# Reverse shells
	Pattern(
		name="reverse_shell_bash",
		pattern=r"(bash\s+-i\s*>&?\s*/dev/tcp/|/dev/(tcp|udp)/[^\s]+/\d+)",
		severity=Severity.CRITICAL,
		description="Bash reverse shell via /dev/tcp -- no legitimate use in packages",
		category=Category.EXFILTRATION,
	),
	Pattern(
		name="python_reverse_shell",
		pattern=r"pty\.spawn\s*\(\s*[\"']/bin/(ba)?sh",
		severity=Severity.HIGH,
		description="Python pty.spawn() reverse shell -- interactive shell spawning",
		category=Category.EXFILTRATION,
	),
]


# -- Encoding/Obfuscation Patterns --

Encoding_Obfuscation_Patterns: list[Pattern] = [
	Pattern(
		name="base64_decode_execution",
		pattern=r"base64\s+(--decode|-d)\s*[^\n]*\|\s*(bash|sh|python|node|eval)",
		severity=Severity.CRITICAL,
		description="Base64 decode piped to execution -- hidden payload",
		category=Category.ENCODING_OBFUSCATION,
	),
	Pattern(
		name="hex_encoded_string",
		pattern=r"(\\x[0-9a-fA-F]{2}){4,}",
		severity=Severity.MEDIUM,
		description="Hex-encoded string -- potential obfuscated payload",
		category=Category.ENCODING_OBFUSCATION,
	),
	Pattern(
		name="zero_width_characters",
		pattern=r"[\u200b-\u200f\ufeff\u180e]",
		severity=Severity.HIGH,
		description="Zero-width or direction-control characters -- hidden text or instruction injection",
		category=Category.ENCODING_OBFUSCATION,
	),
	Pattern(
		name="variation_selectors",
		pattern=r"[\ufe00-\ufe0f]",
		severity=Severity.HIGH,
		description="Unicode variation selectors (VS1-VS16) -- invisible adversarial suffix or glyph manipulation",
		category=Category.ENCODING_OBFUSCATION,
	),
	Pattern(
		name="variation_selectors_supplement",
		pattern=r"[\U000e0100-\U000e01ef]",
		severity=Severity.HIGH,
		description="Unicode variation selectors supplement (VS17-VS256) -- GlassWorm encoding or adversarial suffix",
		category=Category.ENCODING_OBFUSCATION,
	),
	Pattern(
		name="unicode_tags_block",
		pattern=r"[\U000e0001-\U000e007f]",
		severity=Severity.HIGH,
		description="Unicode Tags block characters -- ASCII smuggling or hidden payload encoding",
		category=Category.ENCODING_OBFUSCATION,
	),
	Pattern(
		name="bidi_and_invisible_operators",
		pattern=r"[\u202a-\u202e\u2060-\u2064]",
		severity=Severity.MEDIUM,
		description="Bidi embedding markers or invisible math operators -- Sneaky Bits encoding or text direction attack",
		category=Category.ENCODING_OBFUSCATION,
	),
	Pattern(
		name="base64_long_blob",
		pattern=r"[A-Za-z0-9+/]{100,}={0,2}",
		severity=Severity.LOW,
		description="Long base64-like string -- could be encoded payload or legitimate data",
		category=Category.ENCODING_OBFUSCATION,
	),
	Pattern(
		name="unicode_escape_sequence",
		pattern=r"(\\u[0-9a-fA-F]{4}){4,}",
		severity=Severity.MEDIUM,
		description="Multiple unicode escape sequences -- potential obfuscation",
		category=Category.ENCODING_OBFUSCATION,
	),
	# Supply chain obfuscation techniques
	Pattern(
		name="reversed_string_exec",
		pattern=r"(exec|eval)\s*\([^)]*\[::\s*-1\s*\]",
		severity=Severity.HIGH,
		description="Reversed string passed to exec/eval -- string reversal obfuscation",
		category=Category.ENCODING_OBFUSCATION,
	),
	Pattern(
		name="chr_concat_payload",
		pattern=r"(chr\s*\(\s*\d+\s*\)\s*\+\s*){3,}",
		severity=Severity.HIGH,
		description="chr() concatenation chain -- character-by-character payload construction",
		category=Category.ENCODING_OBFUSCATION,
	),
	Pattern(
		name="codecs_rot13",
		pattern=r"codecs\.decode\s*\([^)]*['\"]rot.?13['\"]",
		severity=Severity.HIGH,
		description="codecs.decode() with rot13 -- obfuscated import names or strings",
		category=Category.ENCODING_OBFUSCATION,
	),
	Pattern(
		name="zlib_decompress_exec",
		pattern=r"(exec|eval)\s*\([^)]*zlib\.decompress",
		severity=Severity.CRITICAL,
		description="zlib.decompress() passed to exec/eval -- compressed payload execution (W4SP Hyperion)",
		category=Category.ENCODING_OBFUSCATION,
	),
	Pattern(
		name="marshal_loads_exec",
		pattern=r"(exec|eval)\s*\([^)]*marshal\.loads",
		severity=Severity.CRITICAL,
		description="marshal.loads() passed to exec/eval -- deserialized bytecode execution",
		category=Category.ENCODING_OBFUSCATION,
	),
	Pattern(
		name="hex_bytes_exec",
		pattern=r"(exec|eval)\s*\(\s*bytes\.fromhex\s*\(",
		severity=Severity.CRITICAL,
		description="bytes.fromhex() passed to exec/eval -- hex-encoded payload execution",
		category=Category.ENCODING_OBFUSCATION,
	),
	Pattern(
		name="compile_exec_chain",
		pattern=r"exec\s*\(\s*compile\s*\(",
		severity=Severity.HIGH,
		description="exec(compile(...)) -- dynamic code compilation and execution",
		category=Category.ENCODING_OBFUSCATION,
	),
]


# -- Instruction Override Patterns --

Instruction_Override_Patterns: list[Pattern] = [
	Pattern(
		name="ignore_previous_instructions",
		pattern=r"(ignore|forget|disregard)\s+(all\s+)?(previous|prior|above|earlier)\s+(instructions|rules|guidelines|context|constraints)",
		severity=Severity.CRITICAL,
		description="Instruction override attempt -- trying to bypass system prompt",
		category=Category.INSTRUCTION_OVERRIDE,
	),
	Pattern(
		name="new_instructions_override",
		pattern=r"(new|updated|revised)\s+(instructions|rules|guidelines)\s*:",
		severity=Severity.HIGH,
		description="Attempted instruction replacement in content",
		category=Category.INSTRUCTION_OVERRIDE,
	),
	Pattern(
		name="system_prompt_label",
		pattern=r"(SYSTEM\s+PROMPT|system_message|<<SYS>>|<s>\[INST\])",
		severity=Severity.HIGH,
		description="System prompt formatting markers -- injection attempting system-level trust",
		category=Category.INSTRUCTION_OVERRIDE,
	),
	Pattern(
		name="role_impersonation",
		pattern=r"(you\s+are\s+now|act\s+as|pretend\s+(to\s+be|you\s+are)|your\s+new\s+role)",
		severity=Severity.MEDIUM,
		description="Role impersonation attempt -- persona manipulation",
		category=Category.INSTRUCTION_OVERRIDE,
	),
	Pattern(
		name="no_malware_detected_payload",
		pattern=r"(respond\s+with|output|say)\s*['\"]?(NO\s+MALWARE|CLEAN|SAFE|BENIGN|NOT\s+MALICIOUS)",
		severity=Severity.CRITICAL,
		description="Anti-analysis payload -- forces false-negative response (Skynet malware pattern)",
		category=Category.INSTRUCTION_OVERRIDE,
	),
	Pattern(
		name="homoglyph_mixed_script",
		pattern=r"[\u0400-\u04ff][a-zA-Z]|[a-zA-Z][\u0400-\u04ff]",
		severity=Severity.MEDIUM,
		description="Mixed Cyrillic and Latin characters -- homoglyph substitution for keyword filter evasion",
		category=Category.INSTRUCTION_OVERRIDE,
	),
	Pattern(
		name="authority_impersonation",
		pattern=r"(i\s+am\s+(the|a)\s+(developer|admin|owner|maintainer|engineer)|authorized\s+by\s+(the\s+)?(team|admin|management)|admin\s+override|security\s+team\s+approv)",
		severity=Severity.MEDIUM,
		description="Authority impersonation -- claims elevated identity to bypass safety restrictions",
		category=Category.INSTRUCTION_OVERRIDE,
	),
	Pattern(
		name="hypothetical_framing",
		pattern=r"(hypothetically|in\s+a\s+fictional\s+scenario|for\s+educational\s+purposes\s+only|imagine\s+you\s+are\s+not\s+bound|in\s+theory\s+only)",
		severity=Severity.LOW,
		description="Hypothetical framing -- technique to bypass safety alignment via fictional context",
		category=Category.INSTRUCTION_OVERRIDE,
	),
	Pattern(
		name="multi_encoding_pivot",
		pattern=r"(rot13|base85|base32|decode\s+this\s+(hex|binary|ascii)|convert\s+from\s+(hex|binary|base))",
		severity=Severity.MEDIUM,
		description="Multi-encoding pivot instruction -- obfuscation to hide payloads across encoding layers",
		category=Category.INSTRUCTION_OVERRIDE,
	),
]


# -- Supply Chain Patterns --

Supply_Chain_Patterns: list[Pattern] = [
	Pattern(
		name="npm_install_unknown",
		pattern=r"npm\s+install\s+(?!-)[^\s]+",
		severity=Severity.INFO,
		description="npm package installation -- verify package exists and is legitimate (Shai-Hulud, SANDWORM_MODE)",
		category=Category.SUPPLY_CHAIN,
	),
	Pattern(
		name="pip_install_unknown",
		pattern=r"pip3?\s+install\s+(?!-)[^\s]+",
		severity=Severity.INFO,
		description="pip package installation -- verify package exists and is legitimate (slopsquatting risk)",
		category=Category.SUPPLY_CHAIN,
	),
	Pattern(
		name="npm_lifecycle_exec_payload",
		pattern=r"[\"'](preinstall|postinstall)[\"']\s*:\s*[\"'][^\"']*(node\s+-e|curl|wget|bash|sh\s+-c|exec|eval)",
		severity=Severity.CRITICAL,
		description="npm lifecycle script with execution payload -- supply chain attack vector",
		category=Category.SUPPLY_CHAIN,
	),
	Pattern(
		name="cargo_build_script",
		pattern=r"\bbuild\.rs\b",
		severity=Severity.LOW,
		description="Cargo build script reference -- executes arbitrary Rust code during cargo build",
		category=Category.SUPPLY_CHAIN,
	),
	Pattern(
		name="github_actions_secrets_in_run",
		pattern=r"run:.*?\$\{\{\s*secrets\.",
		severity=Severity.INFO,
		description="GitHub Actions run step accessing secrets -- verify secrets are not exposed to untrusted code",
		category=Category.SUPPLY_CHAIN,
	),
	# -- LiteLLM / TeamPCP gap patterns --
	Pattern(
		name="python_b64decode_exec",
		pattern=r"(exec|eval)\s*\(\s*(base64\.b64decode|b64decode)\s*\(",
		severity=Severity.CRITICAL,
		description="base64.b64decode() passed to exec/eval -- encoded payload execution (TeamPCP, W4SP)",
		category=Category.SUPPLY_CHAIN,
	),
	Pattern(
		name="subprocess_sys_executable",
		pattern=r"subprocess\.\w+\s*\([^)]*sys\.executable",
		severity=Severity.HIGH,
		description="subprocess with sys.executable -- re-invokes Python interpreter to run hidden payload",
		category=Category.SUPPLY_CHAIN,
	),
	# -- Build system hooks --
	Pattern(
		name="hatchling_build_hook",
		pattern=r"\[tool\.hatch\.build\.hooks\.custom\]",
		severity=Severity.MEDIUM,
		description="Hatchling custom build hook -- executes hatch_build.py during pip install",
		category=Category.SUPPLY_CHAIN,
	),
	# -- GitHub Actions supply chain --
	Pattern(
		name="github_actions_pull_request_target",
		pattern=r"pull_request_target:",
		severity=Severity.HIGH,
		description="GitHub Actions pull_request_target trigger -- grants write/secrets access to fork PR code (Ultralytics compromise)",
		category=Category.SUPPLY_CHAIN,
	),
	Pattern(
		name="github_actions_expression_injection",
		pattern=r"\$\{\{\s*github\.(head_ref|event\.pull_request\.(title|body|head\.ref))",
		severity=Severity.HIGH,
		description="Unescaped GitHub context in run step -- branch/PR title injection (Ultralytics, Nx attacks)",
		category=Category.SUPPLY_CHAIN,
	),
	# -- JavaScript/npm supply chain --
	Pattern(
		name="js_buffer_base64_eval",
		pattern=r"eval\s*\(\s*Buffer\.from\s*\([^)]*['\"]base64['\"]",
		severity=Severity.CRITICAL,
		description="eval(Buffer.from(..., 'base64')) -- base64 payload execution in Node.js",
		category=Category.SUPPLY_CHAIN,
	),
	Pattern(
		name="js_eval_atob",
		pattern=r"eval\s*\(\s*atob\s*\(",
		severity=Severity.CRITICAL,
		description="eval(atob(...)) -- base64 decode and execute in JavaScript",
		category=Category.SUPPLY_CHAIN,
	),
	Pattern(
		name="js_new_function_iife",
		pattern=r"new\s+Function\s*\([^)]+\)\s*\(",
		severity=Severity.HIGH,
		description="new Function(...)() IIFE -- dynamic code execution in JavaScript (npm supply chain malware)",
		category=Category.SUPPLY_CHAIN,
	),
	Pattern(
		name="js_require_child_process",
		pattern=r"require\s*\(\s*['\"]child_process['\"]\s*\)\s*\.\s*(exec|spawn|execSync|spawnSync)",
		severity=Severity.HIGH,
		description="require('child_process') with exec/spawn -- shell execution in Node.js packages",
		category=Category.SUPPLY_CHAIN,
	),
	# -- Dynamic module loading --
	Pattern(
		name="importlib_dynamic_load",
		pattern=r"importlib\.(import_module|util\.spec_from_file_location)\s*\(",
		severity=Severity.HIGH,
		description="importlib dynamic loading -- bypasses static import analysis (BeaverTail, TeamPCP)",
		category=Category.SUPPLY_CHAIN,
	),
	# -- Dependency confusion --
	Pattern(
		name="pip_extra_index_url",
		pattern=r"pip.*--extra-index-url|--index-url\s+(?!https://pypi\.org)",
		severity=Severity.HIGH,
		description="pip with non-default index URL -- dependency confusion vector (Birsan technique)",
		category=Category.SUPPLY_CHAIN,
	),
	Pattern(
		name="lockfile_external_url",
		pattern=r"[\"']resolved[\"']\s*:\s*[\"']https?://(?!registry\.npmjs\.org)|git\+https?://[^\s\"']+",
		severity=Severity.HIGH,
		description="Lock file or requirements pointing to external URL -- verify dependency source",
		category=Category.SUPPLY_CHAIN,
	),
	Pattern(
		name="gha_unpinned_action",
		pattern=r"uses:\s+[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+@(?![0-9a-f]{40})[a-zA-Z]",
		severity=Severity.MEDIUM,
		description="GitHub Action pinned to branch/tag, not SHA -- vulnerable to tag re-pointing (Trivy/LiteLLM vector)",
		category=Category.SUPPLY_CHAIN,
	),
	# -- Go supply chain --
	Pattern(
		name="go_mod_replace",
		pattern=r"replace\s+\S+\s+=>\s+",
		severity=Severity.MEDIUM,
		description="Go replace directive -- can redirect dependency to attacker-controlled fork",
		category=Category.SUPPLY_CHAIN,
	),
	Pattern(
		name="go_generate_shell",
		pattern=r"//go:generate\s+(bash|sh|curl|wget|python|node)",
		severity=Severity.MEDIUM,
		description="go:generate with shell command -- executes during go generate",
		category=Category.SUPPLY_CHAIN,
	),
	# -- CI/CD supply chain --
	Pattern(
		name="gitlab_ci_remote_include",
		pattern=r"include:.*remote:\s*[\"']?https?://",
		severity=Severity.HIGH,
		description="GitLab CI remote include -- fetches external CI config at pipeline runtime",
		category=Category.SUPPLY_CHAIN,
	),
	Pattern(
		name="gha_github_env_poisoning",
		pattern=r">>\s*\$GITHUB_(ENV|PATH|OUTPUT)",
		severity=Severity.MEDIUM,
		description="Write to GITHUB_ENV/PATH/OUTPUT -- can poison runner environment (Ultralytics vector)",
		category=Category.SUPPLY_CHAIN,
	),
]


# -- File Permission Patterns --

File_Permission_Patterns: list[Pattern] = [
	Pattern(
		name="chmod_777",
		pattern=r"chmod\s+777",
		severity=Severity.HIGH,
		description="chmod 777 -- world-readable/writable/executable, overly permissive",
		category=Category.FILE_PERMISSIONS,
	),
	Pattern(
		name="chmod_world_writable",
		pattern=r"chmod\s+[0-7]?[2367][2367]",
		severity=Severity.MEDIUM,
		description="World-writable file permissions",
		category=Category.FILE_PERMISSIONS,
	),
]


# -- Code-Before-Review Patterns --

Code_Before_Review_Patterns: list[Pattern] = [
	Pattern(
		name="conftest_autouse_fixture",
		pattern=r"@pytest\.fixture\s*\([^)]*autouse\s*=\s*True",
		severity=Severity.MEDIUM,
		description="Autouse pytest fixture -- executes during test collection before agent review",
		category=Category.CODE_BEFORE_REVIEW,
	),
	Pattern(
		name="npm_lifecycle_script",
		pattern=r"[\"'](preinstall|postinstall|prepack|prepare)[\"']\s*:\s*[\"'][^\"']+[\"']",
		severity=Severity.MEDIUM,
		description="npm lifecycle script in package.json -- executes automatically during npm install",
		category=Category.CODE_BEFORE_REVIEW,
	),
	Pattern(
		name="makefile_sudo_command",
		pattern=r"\tsudo\s+",
		severity=Severity.HIGH,
		description="Makefile command using sudo -- privileged execution from build target",
		category=Category.CODE_BEFORE_REVIEW,
	),
	Pattern(
		name="makefile_pipe_to_shell",
		pattern=r"\t[^\n]*(curl|wget)\s+[^\n]*\|\s*(bash|sh|python|node)",
		severity=Severity.CRITICAL,
		description="Makefile target pipes remote content to shell -- code-before-review RCE",
		category=Category.CODE_BEFORE_REVIEW,
	),
	Pattern(
		name="envrc_with_execution",
		pattern=r"(eval\s+\"|source\s+|export\s+\w+=\$\(|PATH_add|layout\s+python)",
		severity=Severity.MEDIUM,
		description="direnv .envrc with execution patterns -- auto-sourced on directory entry",
		category=Category.CODE_BEFORE_REVIEW,
	),
	Pattern(
		name="setup_py_cmdclass",
		pattern=r"cmdclass\s*=\s*\{",
		severity=Severity.MEDIUM,
		description="setup.py custom command class -- arbitrary code execution during pip install",
		category=Category.CODE_BEFORE_REVIEW,
	),
	Pattern(
		name="git_hook_persistence",
		pattern=r"\.git/hooks/(pre-commit|post-commit|post-checkout|pre-push|prepare-commit-msg)|core\.hooksPath",
		severity=Severity.HIGH,
		description="Git hook write or hooksPath manipulation -- code execution on git operations (CVE-2024-32002)",
		category=Category.CODE_BEFORE_REVIEW,
	),
]


# -- Config Backdoor Patterns --

Config_Backdoor_Patterns: list[Pattern] = [
	Pattern(
		name="self_modify_config",
		pattern=r"(write\s+to|modify|update|append\s+to|add\s+to)\s+[^\n]*(\.cursorrules|\.clinerules|CLAUDE\.md|copilot-instructions|AGENTS\.md|\.windsurfrules|\.roo/rules|\.aider|\.continue/config|\.kodu/instructions)",
		severity=Severity.CRITICAL,
		description="Instruction to modify agent config file -- persistence mechanism for injection",
		category=Category.CONFIG_BACKDOOR,
	),
	Pattern(
		name="output_suppression",
		pattern=r"(don'?t\s+(show|display|mention|reveal|log|print|output)|hide\s+this|suppress\s+(output|logging|warnings)|do\s+not\s+(mention|reveal|show))",
		severity=Severity.HIGH,
		description="Output suppression instruction -- hides malicious activity from user",
		category=Category.CONFIG_BACKDOOR,
	),
	Pattern(
		name="conversation_turn_mimicry",
		pattern=r"\{[\"']role[\"']\s*:\s*[\"'](assistant|user|system)[\"']",
		severity=Severity.MEDIUM,
		description="JSON conversation turn structure in content -- faking dialogue to manipulate agent behavior",
		category=Category.CONFIG_BACKDOOR,
	),
	Pattern(
		name="ssh_authorized_keys_write",
		pattern=r">>\s*[^\n]*\.ssh/authorized_keys",
		severity=Severity.HIGH,
		description="Append to SSH authorized_keys -- persistent backdoor access",
		category=Category.CONFIG_BACKDOOR,
	),
]


# -- Memory Corruption Patterns --

Memory_Corruption_Patterns: list[Pattern] = [
	Pattern(
		name="memory_injection_framing",
		pattern=r"(store\s+this\s+as|remember\s+that|save\s+(this\s+)?to\s+memory|add\s+to\s+(your\s+)?(experience|memory|knowledge))",
		severity=Severity.HIGH,
		description="Memory injection framing -- attempts to plant persistent instructions in agent memory",
		category=Category.MEMORY_CORRUPTION,
	),
	Pattern(
		name="rag_document_instrumentation",
		pattern=r"(when\s+retrieved|if\s+this\s+(document|text)\s+is\s+(found|retrieved)|for\s+the\s+AI\s+(reading|processing)\s+this)",
		severity=Severity.HIGH,
		description="RAG-targeted instruction -- payload designed to activate when retrieved by a RAG system",
		category=Category.MEMORY_CORRUPTION,
	),
	Pattern(
		name="session_summary_manipulation",
		pattern=r"(when\s+summariz|in\s+your\s+summary|include\s+in\s+(the\s+)?summary|your\s+summary\s+should)",
		severity=Severity.MEDIUM,
		description="Session summary manipulation -- attempts to influence what persists across agent sessions",
		category=Category.MEMORY_CORRUPTION,
	),
]


# -- Confused Delegation Patterns --

Confused_Delegation_Patterns: list[Pattern] = [
	Pattern(
		name="cross_agent_forwarding",
		pattern=r"(tell\s+(agent|the\s+other\s+agent)\s+\w+\s+to|pass\s+this\s+to\s+(agent|the\s+other)|forward\s+(this\s+)?to\s+(agent|the\s+next))",
		severity=Severity.HIGH,
		description="Cross-agent instruction forwarding -- may enable privilege escalation via delegation",
		category=Category.CONFUSED_DELEGATION,
	),
	Pattern(
		name="capability_probing",
		pattern=r"(what\s+tools\s+do\s+you\s+have|list\s+your\s+(capabilities|tools|functions)|can\s+you\s+access\s+(the\s+)?(file|shell|network|internet)|what\s+permissions\s+do\s+you)",
		severity=Severity.LOW,
		description="Capability probing -- reconnaissance of agent tools and permissions",
		category=Category.CONFUSED_DELEGATION,
	),
	Pattern(
		name="scope_escalation",
		pattern=r"(also\s+do|while\s+you'?re\s+at\s+it|extend\s+your\s+task\s+to|additionally\s+perform|and\s+also\s+(run|execute|access))",
		severity=Severity.LOW,
		description="Scope escalation attempt -- expanding agent task beyond original boundaries",
		category=Category.CONFUSED_DELEGATION,
	),
]


# -- Persistence Patterns --

Persistence_Patterns: list[Pattern] = [
	Pattern(
		name="bashrc_profile_append",
		pattern=r">>\s*~?/?\.(bashrc|bash_profile|profile|zshrc|zprofile)",
		severity=Severity.HIGH,
		description="Append to shell profile -- persistence mechanism (Colorama campaign)",
		category=Category.PERSISTENCE,
	),
	Pattern(
		name="crontab_manipulation",
		pattern=r"\|\s*crontab\b|crontab\s+-[eru]|/etc/cron\.\w+/|/var/spool/cron",
		severity=Severity.HIGH,
		description="Crontab write/edit -- scheduled persistence for C2 polling",
		category=Category.PERSISTENCE,
	),
	Pattern(
		name="systemd_user_service",
		pattern=r"systemctl\s+(--user\s+)?enable|\.config/systemd/user/[^\s]*\.service",
		severity=Severity.HIGH,
		description="Systemd user service install -- persistent auto-restart backdoor (TeamPCP sysmon.service)",
		category=Category.PERSISTENCE,
	),
	Pattern(
		name="windows_registry_run",
		pattern=r"CurrentVersion\\+Run\b|winreg\.SetValueEx\s*\(",
		severity=Severity.HIGH,
		description="Windows registry Run key -- auto-start persistence (W4SP, Colour-Blind RAT)",
		category=Category.PERSISTENCE,
	),
	Pattern(
		name="startup_folder_persistence",
		pattern=r"Start Menu\\+Programs\\+Startup|AppData\\+Roaming\\+Microsoft\\+Windows\\+Start",
		severity=Severity.HIGH,
		description="Windows Startup folder reference -- startup directory persistence (Colour-Blind RAT)",
		category=Category.PERSISTENCE,
	),
	# macOS
	Pattern(
		name="launchd_persistence",
		pattern=r"launchctl\s+(load|bootstrap)|Library/LaunchAgents/[^\s]*\.plist",
		severity=Severity.HIGH,
		description="macOS launchd persistence -- auto-start via LaunchAgents plist",
		category=Category.PERSISTENCE,
	),
	# Windows expanded
	Pattern(
		name="schtasks_persistence",
		pattern=r"schtasks\s+/create",
		severity=Severity.HIGH,
		description="Windows scheduled task creation -- persistence via Task Scheduler",
		category=Category.PERSISTENCE,
	),
	Pattern(
		name="powershell_iex_download",
		pattern=r"(Invoke-Expression|IEX)\s*\(?\s*(New-Object\s+Net\.WebClient|\(New-Object)",
		severity=Severity.CRITICAL,
		description="PowerShell IEX with WebClient download -- standard dropper pattern",
		category=Category.PERSISTENCE,
	),
]


# -- Pattern collections by use case --

All_Patterns: list[Pattern] = (
	Skill_Injection_Patterns
	+ Hook_Abuse_Patterns
	+ Mcp_Config_Patterns
	+ Secrets_Patterns
	+ Dangerous_Call_Patterns
	+ Exfiltration_Patterns
	+ Encoding_Obfuscation_Patterns
	+ Instruction_Override_Patterns
	+ Supply_Chain_Patterns
	+ File_Permission_Patterns
	+ Code_Before_Review_Patterns
	+ Config_Backdoor_Patterns
	+ Memory_Corruption_Patterns
	+ Confused_Delegation_Patterns
	+ Persistence_Patterns
)

# Patterns relevant to agent config scanning (vet-repo)
Vet_Repo_Patterns: list[Pattern] = (
	Skill_Injection_Patterns
	+ Hook_Abuse_Patterns
	+ Mcp_Config_Patterns
	+ Instruction_Override_Patterns
	+ Exfiltration_Patterns
	+ Encoding_Obfuscation_Patterns
	+ Config_Backdoor_Patterns
	+ Memory_Corruption_Patterns
	+ Confused_Delegation_Patterns
	+ Code_Before_Review_Patterns
	+ File_Permission_Patterns
)

# Patterns relevant to individual skill analysis (scan-skill)
Scan_Skill_Patterns: list[Pattern] = (
	Skill_Injection_Patterns
	+ Exfiltration_Patterns
	+ Encoding_Obfuscation_Patterns
	+ Instruction_Override_Patterns
	+ Dangerous_Call_Patterns
	+ Supply_Chain_Patterns
	+ Code_Before_Review_Patterns
	+ Config_Backdoor_Patterns
	+ Memory_Corruption_Patterns
	+ Confused_Delegation_Patterns
	+ Persistence_Patterns
)

# Patterns relevant to code security review (audit-code)
Audit_Code_Patterns: list[Pattern] = (
	Secrets_Patterns
	+ Dangerous_Call_Patterns
	+ Exfiltration_Patterns
	+ Supply_Chain_Patterns
	+ File_Permission_Patterns
	+ Code_Before_Review_Patterns
	+ Persistence_Patterns
)


def Scan_Content(
	content: str,
	patterns: list[Pattern],
	file_path: str = "<unknown>",
	context_lines: int = 0,
) -> list[Finding]:
	"""
	Scan content against a list of patterns and return findings.

	Args:
		content: The text content to scan
		patterns: List of Pattern objects to match against
		file_path: Path to the file being scanned (for reporting)
		context_lines: Number of surrounding lines to include in context

	Returns:
		List of Finding objects for all matches
	"""
	findings: list[Finding] = []
	lines = content.split("\n")

	for pattern in patterns:
		if pattern.compiled is None:
			continue

		for match in pattern.compiled.finditer(content):
			# Calculate line number from match position
			line_number = content[:match.start()].count("\n") + 1
			matched_text = match.group(0)

			# Truncate long matches for display
			Max_Match_Display = 200
			if len(matched_text) > Max_Match_Display:
				matched_text = matched_text[:Max_Match_Display] + "..."

			# Get context lines
			context = ""
			if context_lines > 0:
				start_line = max(0, line_number - 1 - context_lines)
				end_line = min(len(lines), line_number + context_lines)
				context = "\n".join(lines[start_line:end_line])

			findings.append(Finding(
				pattern_name=pattern.name,
				severity=pattern.severity,
				category=pattern.category,
				description=pattern.description,
				file_path=file_path,
				line_number=line_number,
				matched_text=matched_text,
				context=context,
			))

	return findings


def Format_Report(
	title: str,
	scanned_target: str,
	findings: list[Finding],
) -> str:
	"""
	Format findings into a structured report.

	Args:
		title: Report title (skill name)
		scanned_target: What was scanned (path, description)
		findings: List of Finding objects

	Returns:
		Formatted markdown report string
	"""
	# Count by severity
	severity_counts: dict[Severity, int] = {}
	for finding in findings:
		severity_counts[finding.severity] = severity_counts.get(finding.severity, 0) + 1

	critical_count = severity_counts.get(Severity.CRITICAL, 0)
	high_count = severity_counts.get(Severity.HIGH, 0)
	medium_count = severity_counts.get(Severity.MEDIUM, 0)
	low_count = severity_counts.get(Severity.LOW, 0)
	info_count = severity_counts.get(Severity.INFO, 0)

	report_lines: list[str] = []
	report_lines.append(f"## {title} Report\n")
	report_lines.append(f"**Scanned:** {scanned_target}")
	report_lines.append(
		f"**Findings:** {critical_count} critical, {high_count} high, "
		f"{medium_count} medium, {low_count} low, {info_count} info\n"
	)

	if not findings:
		report_lines.append("No security issues detected.\n")
		return "\n".join(report_lines)

	# Group findings by severity
	severity_order = [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW, Severity.INFO]

	for severity in severity_order:
		severity_findings = [f for f in findings if f.severity == severity]
		if not severity_findings:
			continue

		report_lines.append(f"### {severity.value} Findings\n")
		for finding in severity_findings:
			report_lines.append(
				f"- **[{finding.severity.value}]** {finding.description}\n"
				f"  - File: `{finding.file_path}:{finding.line_number}`\n"
				f"  - Pattern: `{finding.pattern_name}`\n"
				f"  - Match: `{finding.matched_text}`"
			)
		report_lines.append("")

	# Recommendations
	report_lines.append("### Recommendations\n")
	seen_recommendations: set[str] = set()

	Recommendation_Map: dict[Category, str] = {
		Category.SKILL_INJECTION: "Review skill files for hidden instructions. Remove HTML comments with executable content. Verify skill descriptions match actual behavior.",
		Category.HOOK_ABUSE: "Review hook configurations for auto-approve patterns. Ensure hooks do not bypass the permission system. Remove or restrict Stop hooks.",
		Category.MCP_CONFIG: "Verify all MCP server URLs are trusted. Review tool descriptions for injection payloads. Limit tool permissions to minimum required.",
		Category.SECRETS: "Remove hardcoded secrets immediately. Use environment variables or a secrets manager. Rotate any exposed credentials.",
		Category.DANGEROUS_CALLS: "Review dangerous function calls for user-controlled input. Use parameterized queries for SQL. Avoid eval/exec with untrusted data.",
		Category.EXFILTRATION: "Block or monitor outbound data transfers from agent context. Review file access patterns for credential harvesting.",
		Category.ENCODING_OBFUSCATION: "Decode and inspect obfuscated content. Zero-width characters indicate hidden text injection. Base64 blobs may contain payloads.",
		Category.INSTRUCTION_OVERRIDE: "Content contains instruction override attempts. Do not process this content as trusted instructions.",
		Category.SUPPLY_CHAIN: "Verify all package names exist in their registries. Check for typosquatting or hallucinated package names. Pin GitHub Actions to commit SHAs. Use --ignore-scripts for npm. Audit --extra-index-url for dependency confusion.",
		Category.FILE_PERMISSIONS: "Tighten file permissions. Avoid world-writable (777) permissions on any file.",
		Category.CODE_BEFORE_REVIEW: "Review conftest.py, setup.py, package.json lifecycle scripts, Makefiles, and .envrc for execution before running build or test commands. Use --ignore-scripts for npm.",
		Category.CONFIG_BACKDOOR: "Agent config files contain manipulation instructions. Review for self-modification commands, output suppression, and fake conversation turns.",
		Category.MEMORY_CORRUPTION: "Content attempts to plant persistent instructions in agent memory. Review for memory injection framing, RAG-targeted payloads, and summary manipulation.",
		Category.CONFUSED_DELEGATION: "Content attempts cross-agent instruction forwarding or capability probing. Enforce capability boundaries between agents and log delegation requests.",
		Category.PERSISTENCE: "Review for persistence mechanisms (cron, systemd, shell profiles, registry keys, startup folders). Legitimate software rarely modifies these outside of installers.",
	}

	for finding in findings:
		rec = Recommendation_Map.get(finding.category, "")
		if rec and rec not in seen_recommendations:
			seen_recommendations.add(rec)
			report_lines.append(f"- {rec}")

	report_lines.append("")
	return "\n".join(report_lines)


# -- Package Registry Verification --


def Verify_Package(ecosystem: str, name: str) -> dict:
	"""Check if a package exists on PyPI or npm.

	Returns dict with: exists (bool|None), name, details.
	None means verification failed (network error, timeout).
	"""
	import urllib.request
	import json

	if ecosystem == "pypi":
		url = f"https://pypi.org/pypi/{name}/json"
	elif ecosystem == "npm":
		url = f"https://registry.npmjs.org/{name}"
	else:
		return {"exists": None, "name": name, "details": f"Unknown ecosystem: {ecosystem}"}

	try:
		req = urllib.request.Request(url, headers={"User-Agent": "ai-agent-security-scanner/1.0"})
		with urllib.request.urlopen(req, timeout=5) as resp:
			data = json.loads(resp.read())
			if ecosystem == "pypi":
				info = data.get("info", {})
				return {
					"exists": True,
					"name": info.get("name", name),
					"details": f"v{info.get('version', '?')} -- {info.get('summary', '')[:80]}",
				}
			else:
				latest = data.get("dist-tags", {}).get("latest", "?")
				return {
					"exists": True,
					"name": data.get("name", name),
					"details": f"v{latest}",
				}
	except Exception as e:
		# urllib.error.HTTPError with code 404 = package not found
		err_name = type(e).__name__
		if hasattr(e, "code") and e.code == 404:
			return {"exists": False, "name": name, "details": "Package does not exist on registry"}
		return {"exists": None, "name": name, "details": f"{err_name}: {e}"}


def Verify_Install_Findings(findings: list[Finding]) -> list[Finding]:
	"""Post-process pip/npm install findings with live registry verification.

	Replaces generic pip_install_unknown/npm_install_unknown findings:
	- Package not found on registry -> CRITICAL (hallucinated/typosquatted)
	- Verification failed (network error) -> MEDIUM (manual check needed)
	- Package exists -> finding removed (legitimate)
	"""
	verified: list[Finding] = []
	install_findings: list[Finding] = []

	for f in findings:
		if f.pattern_name in ("pip_install_unknown", "npm_install_unknown"):
			install_findings.append(f)
		else:
			verified.append(f)

	if not install_findings:
		return verified

	# Deduplicate by (ecosystem, package_name)
	seen: set[tuple[str, str]] = set()
	to_check: list[tuple[str, str, Finding]] = []

	for f in install_findings:
		ecosystem = "pypi" if f.pattern_name == "pip_install_unknown" else "npm"

		# Extract package name from matched text
		parts = f.matched_text.strip().split()
		name = parts[-1].strip("'\"") if len(parts) >= 3 else ""
		# Strip version specifiers
		name = re.split(r"[=<>!\[,;]", name)[0].rstrip("'\"")

		if not name or name.startswith("-"):
			continue

		key = (ecosystem, name.lower())
		if key not in seen:
			seen.add(key)
			to_check.append((ecosystem, name, f))

	if not to_check:
		return verified

	print(f"[*] Verifying {len(to_check)} package(s) against registries...")

	for ecosystem, name, original in to_check:
		result = Verify_Package(ecosystem, name)

		if result["exists"] is False:
			print(f"    CRITICAL: {name} not found on {ecosystem.upper()}")
			verified.append(Finding(
				pattern_name="package_not_found",
				severity=Severity.CRITICAL,
				category=Category.SUPPLY_CHAIN,
				description=f"Package '{name}' does not exist on {ecosystem.upper()} -- hallucinated or typosquatted name (slopsquatting)",
				file_path=original.file_path,
				line_number=original.line_number,
				matched_text=original.matched_text,
			))
		elif result["exists"] is None:
			print(f"    UNVERIFIED: {name} ({result['details']})")
			verified.append(Finding(
				pattern_name="package_unverified",
				severity=Severity.MEDIUM,
				category=Category.SUPPLY_CHAIN,
				description=f"Could not verify '{name}' on {ecosystem.upper()} -- {result['details']}",
				file_path=original.file_path,
				line_number=original.line_number,
				matched_text=original.matched_text,
			))
		else:
			print(f"    OK: {name} ({result['details']})")

	return verified
