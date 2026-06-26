---
name: skill_guard
description: "Skill Security Scanner - Scan for risks before download/use. Use when: installing unknown skills, evaluating third-party code, or security auditing. / Skill安全检查 - 下载/使用前检测风险。"
metadata:
  author: "WaaiOn"
  version: "1.2"
  openclaw:
    emoji: "🛡️"
    requires:
      bins: ["python3"]
---

# 🛡️ Skill Guard / 安全检查

Security scanner for AI Skills. Check code safety before install or use.

## When to Use / 使用场景

| EN | CN |
|----|----|
| Installing unknown skills | 安装未知来源的skill |
| Evaluating third-party code | 评估第三方代码 |
| Security auditing | 安全审计 |
| Before running untrusted code | 运行不受信任的代码前 |

## Risk Categories / 风险类型

| Category | EN | CN | Severity |
|----------|----|----|----------|
| Code Execution | 代码执行 | 🔴 Critical |
| File Deletion | 文件删除 | 🔴 Critical |
| Command Injection | 命令注入 | 🔴 Critical |
| Credential Leak | 凭证泄露 | 🟠 High |
| Network Request | 网络请求 | 🟠 High |
| Data Theft | 窃取数据 | 🔴 Critical |
| Induce Transfer | 诱导转钱 | 🔴 Critical |
| Virus/Backdoor | 病毒/后门 | 🔴 Critical |

## Usage / 使用

```bash
# Scan local skill / 扫描本地skill
python3 -c "from skill_guard import scan; print(scan('/path/to/skill'))"

# Inspect remote / 检查远程
python3 -c "from skill_guard import inspect_remote; print(inspect_remote('skill-name'))"
```

## Risk Patterns / 风险模式

```python
RISK_PATTERNS = {
    'code_execution': ['exec(', 'eval(', 'compile(', '__import__'],
    'file_deletion': ['rm -rf', 'shutil.rmtree', 'os.remove'],
    'command_injection': ['subprocess', 'os.system', 'shell=True'],
    'credential_leak': ['password', 'api_key', 'token', 'secret'],
    'data_theft': ['/etc/passwd', '~/.ssh', 'clipboard'],
    'induce_transfer': ['alipay', 'bank_card', 'payment'],
    'virus_backdoor': ['ransomware', 'miner', 'backdoor'],
}
```

## Installation / 安装

```bash
npx clawhub install skill-guard-waai
```

## Author / 作者

- WaaiOn
