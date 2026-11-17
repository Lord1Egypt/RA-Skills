# Search patterns

Starting points for building the inventory. A hit is a lead, not a finding: open the file and read the code path before rating anything. Absence of hits is evidence only when you've also checked the project's own naming (read the tool registry first, then search for its vocabulary).

Base command (falls back to `grep -rnE` if `rg` is missing):
```bash
RG='rg -n --hidden -S -g !.git -g !node_modules -g !vendor -g !dist -g !build -g !*.min.js -g !*.lock'
$RG -e 'pattern1' -e 'pattern2' .
```
Exclude tests and examples when establishing defaults, then search them separately: examples reveal what users are told to do (relevant to C7 traps and to "primary deployment mode").

## Files that usually hold the evidence
- Tool registry / executor: `tools/`, `actions/`, `agent/`, `executor`, `runtime`, `server.(py|ts)` (MCP), `@tool`, `register_tool`.
- Permission system: `permission*`, `approval*`, `policy*`, `confirm*`, `guard*`.
- Defaults: CLI arg parsers (`argparse`, `click`, `typer`, `commander`, `yargs`, `cobra`, `clap`), `config.(py|ts|toml|yaml)`, `defaults.*`, `settings.*`, constructor default arguments.
- Deployment: `Dockerfile*`, `docker-compose*.y*ml`, `charts/**/values.yaml`, `templates/*role*.yaml`, `*.tf`, `.devcontainer/`, `.github/workflows/*.yml` (for agents shipped as Actions).
- Docs that state intent (then verify in code): `SECURITY.md`, `docs/security*`, `docs/sandbox*`, `docs/permissions*`.

## C1 Identity & least privilege
```
DefaultAzureCredential|boto3\.(Session|client)\(|google\.auth\.default|load_kube_config|load_incluster_config|kubeconfig
ClusterRole|cluster-admin|verbs:\s*\[?\s*["']?\*|resources:\s*\[?\s*["']?\*|impersonate|serviceAccountName
scopes?\s*[=:]|oauth|on_behalf_of|token_exchange|assume_role|AssumeRole|sts
env\s*=\s*(os\.environ|process\.env|\{\s*\*\*os\.environ)|os\.environ\.copy\(\)|inheritEnv|env_clear
GITHUB_TOKEN|GH_TOKEN|permissions:\s*(write-all|contents:\s*write)
(grant|add|update).*(role|permission|scope)   # self-escalation tools
Authorization.*(forward|pass)|bearer.*upstream # token passthrough
```

## C2 Approval gates
```
approv|confirm|requires?_approval|human_in_the_loop|interrupt\(|ask_user|permission_mode|PermissionMode
auto_?approve|always_?allow|allowlist|allow_list|whitelist|trusted_commands|safe_commands
--yes|-y\b|--auto|yolo|dangerously|skip[-_]permissions|bypass|full[-_]auto|no[-_]confirm
startswith\(|\.startsWith\(|shlex|shell-quote|bashlex|tree-sitter-bash   # allowlist matching quality
checkpoint|undo|rollback|snapshot|dry[-_]run|preview
```
Read the gate's condition and list every tool that reaches a mutating path; compare the two lists.

## C3 Tool & action scoping
```
realpath|resolve\(\)|abspath|normpath|path\.relative|is_relative_to|O_NOFOLLOW|lstat|symlink
startswith\(.*(root|base|workspace|cwd)|\.startsWith\(.*(root|base|workspace)
allowed_(hosts|domains|urls)|blocked_(hosts|ips)|169\.254\.169\.254|localhost|127\.0\.0\.1|ssrf|follow_redirects|allow_redirects|maxRedirects
execute\(.*(f"|%|\+|format\()|raw_sql|text\(|\.query\(.*\+|SELECT.*startswith|read_only|readonly
max_(items|count|amount|rows|recipients)|limit\s*=
enabled_tools|default_tools|tool_groups|toolsets|ALL_TOOLS
```

## C4 Code-execution isolation
```
subprocess\.|os\.system|os\.popen|shell\s*=\s*True|pty\.spawn|asyncio\.create_subprocess
child_process|execSync|spawnSync|\bexec\(|\bspawn\(|execa|shelljs
exec\.Command|os/exec|Command::new|std::process
\beval\(|\bexec\(|compile\(|new Function\(|vm\.run|runInNewContext|importlib|__import__
docker|podman|/var/run/docker\.sock|privileged|cap_drop|cap_add|--cap-|no-new-privileges|seccomp|read_only|network_mode|--network|user:\s|USER\s
gvisor|runsc|firecracker|kata|microvm|wasm|wasi|pyodide|e2b|modal|daytona|sandbox
landlock|seatbelt|sandbox-exec|bwrap|bubblewrap|nsjail|firejail|chroot|setuid|setgid
RestrictedPython|LocalPythonExecutor|safe_eval|ast\.parse.*(allow|deny)
fallback|docker.*not (found|available)|except.*Docker   # host fallback when sandbox fails
npm (test|run)|make\b|pytest|pip install|npm install|postinstall  # running repo-controlled code
```

## C5 Untrusted input blast radius
```
role["']?\s*[:=]\s*["'](tool|function|user)["']|ToolMessage|tool_result|function_response   # how tool output enters context
untrusted|taint|provenance|quarantin|spotlight|datamark|delimit|<untrusted|<document
prompt[_ ]injection|jailbreak|PromptGuard|LlamaGuard|lakera|rebuff|guardrail|shield
fetch|requests\.get|httpx|axios|urllib|browser|playwright|puppeteer|selenium|web_search|scrape
issue_comment|pull_request_target|on:\s*\[?issues|webhook|inbound|imap|pop3|slack_event|on_message
!\[|<img|markdown|react-markdown|marked\(|rehype-raw|dangerouslySetInnerHTML|innerHTML|v-html|unfurl
send_(email|message|mail)|post_comment|create_comment|slack.*post|smtp
```
Then answer the three Rule-of-Two questions explicitly with citations: [A] what untrusted sources, [B] what sensitive data/systems, [C] what egress/state change — in the same default session? Rate B by assuming the hijack succeeds: what can be leaked, and what can be done irreversibly, without a human?
Also search for remote prompts and tool descriptions entering context: `fetch.*(prompt|template)|prompt_url|hub\.pull|tools/list|list_tools|description`

## C6 Memory, context & config integrity
```
memory|remember|save_memory|long_term|persist|knowledge_base|mem0|zep|letta|memgpt
chroma|pinecone|qdrant|weaviate|faiss|pgvector|milvus|lancedb|vector_store|VectorStore
namespace|user_id|tenant|partition|filter=   # isolation in retrieval
summar|compact|condens   # summaries that persist
AGENTS\.md|CLAUDE\.md|GEMINI\.md|\.cursorrules|\.windsurfrules|copilot-instructions|rules\.md|\.clinerules
settings\.json|\.mcp\.json|mcp_servers|hooks|pre_tool|post_tool|on_start|workspace[_ ]trust|trust(ed)?_folder
load_dotenv|dotenv\.config|find_dotenv|BASE_URL|base_url|_ENDPOINT|api_base   # workspace .env or env vars redirecting endpoints
```

## C7 Third-party extensions
```
trust_remote_code|pickle\.load|torch\.load|joblib\.load|cloudpickle|dill\.load|weights_only|safetensors|yaml\.load\(   # then check the Loader argument
from_pretrained|hf_hub_download|snapshot_download
npx\s+-y|npx .*@latest|uvx|pipx run|bunx|go run .*@latest
mcpServers|mcp_servers|StdioServerParameters|stdio_client|sse_client|streamablehttp|tools/list|list_tools
plugin|entry_points|importlib\.metadata|load_plugin|register_plugin|marketplace|registry
(pip|npm|yarn|pnpm|cargo|go) (install|add|get)   # model-reachable installers
self[-_]update|auto[-_]update|update_check
sha256|digest|checksum|signature|sigstore|cosign|slsa|sbom|cyclonedx|spdx
```

## C8 Secrets & sensitive data
```
api[_-]?key|secret|token|password|passwd|credential|private[_-]?key|BEGIN (RSA|OPENSSH|EC) PRIVATE
SecretStr|SecretString|mask|redact|scrub|sanitiz|\*\*\*\*|obfuscat
keyring|keychain|libsecret|credential[_ ]manager|vault|secretsmanager|kms|sops
logger\.(info|debug)\(.*(request|response|headers|body|payload|messages)|print\(.*(token|key|secret)
sentry|posthog|segment|mixpanel|amplitude|telemetry|analytics|opentelemetry|send_default_pii|capture_locals|include_local_variables
\.env|dotenv|chmod|0o600|0600   # storage and permissions
history|transcript|session.*(save|dump|write)|\.jsonl
```

## C9 Audit & traceability
```
audit|event_stream|EventStream|trajectory|transcript|\.jsonl|append|journal
logger\.(debug|info)\(.*tool|log.*tool_call|on_tool_(start|end)|callback
opentelemetry|otel|span|trace_id|correlation_id|request_id|run_id
actor|principal|on_behalf|approved_by|user_id   # attribution fields
hash.?chain|hmac|sign|immutable|append[-_]only|worm
```

## C10 Limits & kill switch
```
max_(iterations|steps|turns|rounds|loops|depth|retries)|recursion_limit|iteration_limit|step_limit
timeout|time_limit|deadline|wall_clock|budget|max_cost|cost_limit|token_limit|max_tokens_total
rate_limit|ratelimit|throttle|backoff|circuit|breaker|repeated|stuck|loop_detect
cancel|abort|stop|halt|kill|SIGINT|SIGTERM|signal\.|process_group|killpg|os\.setsid|AbortController
sub_?agent|subagent|delegate|handoff|spawn_agent|Task\(|agent_tool|as_tool|crew|swarm|orchestrat
background|schedul|cron|daemon|detach|nohup|threading\.Thread   # work that may outlive a stop
```

## Recording negative evidence
Record a search exactly as you ran it, with the scope separate, so `score.py --repo` can reproduce it:
```json
{"search": "rg -n -S -e 'docker|sandbox|seccomp|landlock'", "scope": "src/", "hits": 2,
 "note": "both hits are docstrings; executor at src/run.py:88 calls subprocess.run directly"}
```
`hits` is every line the command prints, not just relevant ones. Keep patterns in the command and paths in `scope`; the script appends the scope paths when re-running.
