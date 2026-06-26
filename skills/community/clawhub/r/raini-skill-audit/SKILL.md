# Skill Audit 🔍

扫描 OpenClaw skills 中的安全风险，防止供应链攻击。

---

## 指令

### `/skill-audit scan [skill-name]`
扫描已安装的 skill，检测可疑代码模式。

```bash
# 扫描所有已安装 skill
skill-audit scan

# 扫描指定 skill
skill-audit scan moltdash

# 扫描本地目录
skill-audit scan ./my-skill
```

### `/skill-audit check <clawhub-slug>`
安装前检查 ClawHub 上的 skill。

```bash
skill-audit check some-skill
```

---

## 检测规则

### 🔴 高风险 (Critical)
- 读取凭证文件: `~/.ssh/`, `~/.env`, `credentials.json`
- 外发数据: `fetch()`, `curl`, `webhook`, `POST` 到未知 URL
- 代码执行: `eval()`, `exec()`, `child_process`
- 读取环境变量中的密钥: `process.env.API_KEY`

### 🟠 中风险 (Warning)  
- 网络请求到非知名域名
- 文件系统遍历: `fs.readdir()`, `glob`
- 动态 require/import
- Base64 编码的字符串 (可能是混淆)

### 🟡 低风险 (Info)
- 使用 shell 命令
- 读写用户目录外的文件
- 大量依赖包

---

## 输出示例

```
🔍 Skill Audit Report: suspicious-weather
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Risk Score: 85/100 🔴 HIGH RISK

┌─────────────┬──────────┬─────────────────────────────────┐
│ File        │ Severity │ Finding                         │
├─────────────┼──────────┼─────────────────────────────────┤
│ index.ts    │ CRITICAL │ Reads ~/.openclaw/credentials/  │
│ index.ts    │ CRITICAL │ POST to webhook.site            │
│ utils.ts    │ WARNING  │ Uses eval()                     │
└─────────────┴──────────┴─────────────────────────────────┘

⚠️  DO NOT INSTALL - This skill may steal your credentials!
```

---

## 运行方式

该 skill 附带一个 CLI 脚本，agent 可直接调用：

```bash
node {baseDir}/src/audit.js scan ~/.openclaw/workspace/skills/moltdash
node {baseDir}/src/audit.js scan --all
```

---

## 参考

- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [Moltbook Security Discussion](https://www.moltbook.com/post/cbd6474f-8478-4894-95f1-7b104a73bcd5)
