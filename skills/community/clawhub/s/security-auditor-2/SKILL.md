# SKILL.md — Security Auditor

> 让 AI Agent 具备自动化安全审计能力：依赖漏洞扫描、敏感信息检测、API 安全检查、凭证泄露检测。

## 技能说明

本技能帮助开发者在代码提交前自动检查：
- 依赖包已知漏洞（CVE 检测）
- 硬编码密钥、Token、密码检测
- API 安全问题（暴露端口、缺少鉴权）
- Git 历史中的敏感信息泄露
- Docker 镜像安全问题

## 核心脚本

| 脚本 | 功能 |
|------|------|
| `scripts/secret_scanner.py` | 扫描代码中的密钥/Token/密码 |
| `scripts/dependency_audit.py` | 检查依赖 CVE 漏洞 |
| `scripts/api_security_check.py` | API 端点安全检测 |
| `scripts/docker_audit.py` | Docker 镜像安全扫描 |

## 使用方法

### 1. 敏感信息扫描
```bash
python3 scripts/secret_scanner.py --path ./src
```

### 2. 依赖漏洞检查
```bash
pip install safety pip-audit
safety check
pip-audit
```

### 3. Git 历史敏感信息检查
```bash
python3 scripts/secret_scanner.py --scan-git
```

## 检测规则示例

| 类型 | 正则匹配 |
|------|----------|
| AWS Key | `AKIA[0-9A-Z]{16}` |
| GitHub Token | `gh[pousr]_[A-Za-z0-9_]{36,}` |
| Private Key | `-----BEGIN.*PRIVATE KEY-----` |
| API Key | `[aA][pP][iI]_?[kK][eE][yY].*['"][A-Za-z0-9]{20,}` |
| Password | `password\s*[=:]\s*['"][^'"]+['"]` |

## 安全报告格式

```
=== Security Audit Report ===
Scanned: /path/to/repo
Files:   234

🚨 CRITICAL (3)
  [secret]  .env:3    - AWS_ACCESS_KEY_ID=AKIA...EXPOSED
  [secret]  config.py - GITHUB_TOKEN=ghp_...EXPOSED
  [secret]  db.py     - DB_PASSWORD='admin123'

⚠️  WARNING (2)
  [api]    api.py:45   - No auth on /admin endpoint
  [docker] Dockerfile  - Running as root user

✅ PASSED (229)
```

## 集成 OpenClaw

```
Security Auditor Agent → 接收代码/仓库 → 扫描 → 生成报告 → 标记风险
```

## 注意事项

- 扫描前请确保有代码的合法访问权限
- 误报率较高的规则建议人工复核
- 生产环境建议配合专业安全工具（Snyk、Dependabot）
