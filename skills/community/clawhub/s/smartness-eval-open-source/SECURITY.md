# Security Policy / 安全策略

---

## Supported Versions / 支持版本

| Version | Supported | Notes |
|---------|-----------|-------|
| 0.2.x | ✅ Active | Current stable release / 当前稳定版 |
| 0.1.x | ❌ | Deprecated, no security patches / 已弃用 |

---

## Reporting a Vulnerability / 报告漏洞

**Do NOT open public issues for security vulnerabilities.**
**请勿通过公开 Issue 报告安全漏洞。**

Please use [GitHub Security Advisories](https://github.com/xyva-yuangui/smartness-eval/security/advisories) to report privately.

Include / 请包含:

| Field | Description | 说明 |
|-------|-------------|------|
| **Affected version** | e.g., 0.2.1 | 受影响的版本 |
| **Reproduction steps** | Minimal steps to trigger | 最小复现步骤 |
| **Impact analysis** | What can an attacker do? | 攻击者能做什么 |
| **Suggested fix** | Optional | 建议修复方式（可选） |

We aim to respond within **48 hours** and release a fix within **7 days** for critical issues.

---

## Security Design / 安全设计

### Command Execution Safety / 命令执行安全

`eval.py` executes test commands via `subprocess.run()`. To prevent abuse, a multi-layer validation gate (`validate_command()`) is enforced **before** any command runs:

| Layer | Rule | Detail | 说明 |
|-------|------|--------|------|
| 1 | **Interpreter whitelist** | Only `python3` is allowed as the first argument | 仅允许 python3 |
| 2 | **Inline code block** | `-c` flag and any token containing `exec(` are rejected | 禁止内联代码 |
| 3 | **Absolute path block** | Any absolute path (starting with `/`) is rejected | 禁止绝对路径 |
| 4 | **Path traversal block** | Any path containing `..` segments is rejected | 禁止路径穿越 |
| 5 | **Prefix whitelist** | File paths must start with approved prefixes | 前缀白名单 |

**Allowed path prefixes / 允许的路径前缀:**
- `scripts/`
- `skills/openclaw-smartness-eval/`
- `state/`
- `benchmarks/`

Any command that fails validation is **blocked** and recorded as `BLOCKED_UNSAFE_COMMAND` in the test result.

### Network Access / 网络访问

| Feature | Default | Network behavior |
|---------|---------|-----------------|
| Core evaluation | Always on | **No network access** — completely offline / 完全离线 |
| `--llm-judge` | Off | Sends dimension summary to LLM API (no raw logs or user data) / 发送摘要，不发原始数据 |

The `--llm-judge` feature requires:
1. Explicit `--llm-judge` command-line flag
2. A valid `DEEPSEEK_API_KEY` or `OPENAI_API_KEY` environment variable

**What is sent:** dimension scores, key evidence metrics, risk flags.
**What is NOT sent:** raw logs, user messages, file contents, personal data.

### File Access / 文件访问

- All file reads are relative to the workspace root
- Only reads state files and configuration — never writes outside `state/smartness-eval/`
- Missing files are handled gracefully with fallback defaults

---

## Security Checklist for Contributors / 贡献者安全检查清单

When submitting changes, ensure:

- [ ] No `exec()`, `eval()`, `compile()`, or `__import__()` usage
- [ ] No `subprocess` calls with `shell=True`
- [ ] No `-c` flag in any test command definition
- [ ] All file paths are relative (no leading `/`)
- [ ] No `..` in any file path
- [ ] No hardcoded API keys, tokens, or credentials
- [ ] No new network calls without explicit opt-in mechanism
- [ ] Test commands only use `python3` interpreter
