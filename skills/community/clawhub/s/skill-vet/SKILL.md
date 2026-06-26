---
name: Skill 安全审查
description: 在安装或运行 skill 前进行安全扫描，检查恶意代码、可疑命令和网络请求等潜在威胁。
metadata: {"clawdbot":{"emoji":"🔍","requires":{}}}
---

# Skill Vetting

在安装或运行 skill 前进行安全扫描。

## 功能

- **文件扫描**: 检查可疑的 JavaScript/Shell 脚本
- **模式匹配**: 识别恶意代码模式（eval、exec、Base64 编码 payload 等）
- **网络请求检测**: 检测潜在的外向数据泄露
- **权限检查**: 分析危险操作（文件删除、进程控制等）

## 使用方法

```bash
# 扫描当前工作区的 skills 目录
skill-vet

# 扫描指定路径
skill-vet scan /path/to/skill

# 扫描并生成详细报告
skill-vet scan /path/to/skill --verbose

# 仅检查危险模式（不执行）
skill-vet check /path/to/skill
```

## 检测规则

### 高风险
- `eval()` / `exec()` 动态代码执行
- `child_process` 中的 shell 注入
- Base64 编码的隐蔽命令
- 凭据或密钥硬编码
- `process.env` 中的敏感数据访问

### 中风险
- 文件系统操作（写入/删除）
- 网络请求（HTTP/TCP）
- 子进程 spawn
- 定时器/延迟执行

### 低风险
- 加密操作
- 日志记录
- 配置文件读取

## 输出示例

```
$ skill-vet scan ./my-skill

🔍 Scanning: ./my-skill

📁 Files scanned: 12
⚠️  Issues found: 2

⚠️  [MEDIUM] my-skill.js:45
    Pattern: child_process.spawn with shell:true
    Risk: Potential shell injection

⚠️  [LOW] my-skill.js:78
    Pattern: console.log with potential sensitive data
    Risk: Information disclosure

✅ Scan complete. Review issues before proceeding.
```

## 集成

在 OpenClaw 中使用时，可以配合 skill-creator 或手动调用：

```bash
# 在安装新 skill 前先扫描
skill-vet scan ./skills/new-skill && echo "Safe to install"
```
