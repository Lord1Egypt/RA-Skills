---
name: skill-builder-pro
description: >
  Automated Skill development tool.
  User provides prompt + feature description, and the agent auto-completes the full
  ClawHub Skill creation, testing, and publishing workflow.
version: 1.3.0
metadata:
  openclaw:
    requires:
      bins:
        - clawhub
        - python3
    emoji: "🏗️"
    homepage: https://clawhub.ai/BusTes01/skill-builder-pro
    models:
      - gpt-4
      - deepseek-v4-flash
      - gemini-2.0-flash
---

# 🏗️ Skill Builder Pro

A **meta-skill that produces Skills**. User describes what they want, and the agent auto-completes the full journey from ideation to ClawHub publishing. Turns AI into your skill development team.

## Workflow

```
User describes idea → Requirement analysis → Generate SKILL.md → Build directory → Validate locally → Publish to ClawHub
```

## Step-by-Step

### Step 1: Requirement Gathering

Agent collects from user:

```
1. Skill name (slug, e.g., `my-skill-name`)?
2. One-line description?
3. Required tools / APIs? (curl, web_search, Python...)
4. Does it need API keys? User registration needed?
5. Target audience?
6. Key features (1-3)?
7. Output format? (Markdown / text / JSON / image)
8. Free or paid? Price if paid?
```

### Step 2: Generate Directory Structure

Create standard Skill structure in `clawhub-skills/`:

```
└── <skill-name>/
    ├── SKILL.md              # Main file (YAML frontmatter + instructions)
    ├── scripts/              # Helper scripts (optional)
    └── references/           # Reference docs (optional)
```

### Step 3: Write SKILL.md

Generate ClawHub-compliant SKILL.md with:
- YAML frontmatter (`name`, `description`, `version`, `metadata.openclaw`)
- English section first, Chinese section second, separated by `---`
- English model names only
- Feature explanation, usage steps, configuration notes
- Output examples and behavior guidelines

### Step 4: Local Validation

```bash
clawhub skill publish ./<skill-name> --dry-run
```

Check:
- YAML frontmatter format
- metadata declarations complete
- File size within limits
- No external path leaks

### Step 5: Privacy Security Scan (Mandatory)

**Run before every publish:**

```bash
grep -in "AIzaSy\|sk-\|password\|secret\|@gmail\|@qq\|/home/\|192\.168" ./<skill-name>/SKILL.md
```

Scan checklist:
- ❌ Usernames / nicknames → replace with generic terms
- ❌ API keys / tokens → should be env vars, never hardcoded
- ❌ Email addresses → remove or use placeholder
- ❌ Local file paths → use relative or pseudo-paths
- ❌ Internal IPs → use `localhost` or generic IPs
- ❌ Passwords / secrets → never in SKILL.md
- ❌ Personal habits / schedules → generalize

### Step 6: Publish

After confirmation:

```bash
export PATH="$PATH:$(npm root -g)/.bin"

clawhub skill publish ./<skill-name> \
  --slug <slug> \
  --name "<Display Name>" \
  --version <new-version>
```

### Step 7: Post-Publish Verification

```bash
clawhub inspect <username>/<skill-name>
```

Confirm successful listing and return the ClawHub link to the user.

## Bilingual Convention

All skills published via this builder follow this convention:
- **One SKILL.md with two sections**: English section first, Chinese section second, separated by `---`
- **Model names**: always in English (e.g., `gpt-4`, `deepseek-v4-flash`, `sana`, `flux`)
- **YAML frontmatter description**: English only

## Required YAML Frontmatter

```yaml
---
name: <slug-name>
description: <one-line description in English>
version: 1.0.0
metadata:
  openclaw:
    requires:
      env: []        # Required env vars
      bins: []       # Required executables
    primaryEnv: ""   # Primary auth credential
    emoji: "<emoji>"
    models: []       # Compatible models
---
```

## Important Notes

1. **No personal info** in SKILL.md — names, API keys, passwords, paths
2. **Declare all dependencies** — env vars, bins must be complete
3. **Semantic versioning** — 1.0.0, 1.1.0, 2.0.0
4. **Honest about limitations** — clearly state what the skill cannot do
5. **Bilingual format** — English section + Chinese section, not mixed

## Skill Architecture Patterns

### Shared Component Pattern
Extract reusable capabilities into standalone skills that others depend on:
- `complex-memory-manager` — Privacy-aware memory (T1/T2/T3), encryption, cleanup
- `self-iteration-engine` — Usage logging, feedback loops, auto-update decisions

Other skills declare dependency:
```yaml
metadata:
  openclaw:
    requires:
      skills:
        - complex-memory-manager
        - self-iteration-engine
```

When a shared component is updated, check ALL dependent skills for backward compatibility.

### Private Skill Pattern
Some skills are for personal use and should NOT be published:
- Do not run `clawhub publish` for them
- Mark clearly in description: `【⚠️ 私人使用，不发布到 ClawHub】`
- Still apply privacy scanning and security checks

### Knowledge Accumulation Pattern
Skills needing cross-session learning should:
- Store concepts in `memory/concepts/<slug>.md`
- Use `complex-memory-manager` for tiered persistence
- Use `self-iteration-engine` for usage tracking

---

# 🏗️ Skill Builder Pro

一个**生产Skill的Skill**。用户只需描述想要的功能，即可自动完成从构思到上架的完整流程。把AI变成你的Skill开发团队。

## 工作流程

```
用户描述想法 → 需求分析 → 生成SKILL.md → 构建目录 → 本地验证 → 发布上架
```

## 分步指南

### 第一步：需求分析

Agent 向用户收集以下信息：

```
1. Skill名称叫什么？（如：my-skill-name）
2. 一句话描述？
3. 需要用到哪些工具或API？（curl、web_search、Python等）
4. 是否需要API Key？用户自行注册？
5. 目标用户是谁？
6. 主要功能点（1-3个）？
7. 输出格式偏好？（Markdown、文本、JSON、图片）
8. 是否免费？如付费，价格？
```

### 第二步：生成目录结构

在 `clawhub-skills/` 下创建标准Skill结构：

```
└── <skill-name>/
    ├── SKILL.md              # 主文件（YAML frontmatter + 说明）
    ├── scripts/              # 辅助脚本（可选）
    └── references/           # 参考文档（可选）
```

### 第三步：编写SKILL.md

生成符合ClawHub规范的SKILL.md，包含：
- YAML frontmatter（name、description、version、metadata.openclaw）
- 上半部分纯英文、下半部分纯中文，中间用 `---` 分隔
- 模型名称仅使用英文
- 功能说明、使用步骤、配置说明、输出示例、行为准则

### 第四步：本地验证

```bash
clawhub skill publish ./<skill-name> --dry-run
```

检查：
- YAML frontmatter格式正确
- metadata声明完整
- 文件尺寸在限制内
- 无外部路径泄露

### 第五步：隐私安全检查（必做）

**每次发布前运行：**

```bash
grep -in "AIzaSy\|sk-\|password\|secret\|@gmail\|@qq\|/home/\|192\.168" ./<skill-name>/SKILL.md
```

检查项：
- ❌ 用户昵称/真实姓名 → 改为通用表述
- ❌ API Key / Token → 应使用环境变量，绝不硬编码
- ❌ 邮箱地址 → 删除或替换为占位符
- ❌ 本地文件路径 → 使用相对路径或伪路径
- ❌ 内网IP地址 → 使用localhost或通用IP
- ❌ 密码/密钥明文 → 绝不出现
- ❌ 个人作息/偏好习惯 → 泛化处理

### 第六步：发布上架

确认后发布：

```bash
export PATH="$PATH:$(npm root -g)/.bin"

clawhub skill publish ./<skill-name> \
  --slug <slug> \
  --name "<显示名称>" \
  --version <新版本>
```

### 第七步：发布后检查

```bash
clawhub inspect <username>/<skill-name>
```

确认上架成功，将ClawHub链接返回给用户。

## 双语约定

通过此工具发布的所有Skill遵循以下约定：
- **单个SKILL.md包含两个独立区段**：上半部分纯英文，下半部分纯中文，用 `---` 分隔
- **模型名称**：一律使用英文（如 `gpt-4`、`deepseek-v4-flash`、`sana`、`flux`）
- **YAML frontmatter描述**：英文

## 必填YAML Frontmatter字段

```yaml
---
name: <slug名称>
description: <英文一句话描述>
version: 1.0.0
metadata:
  openclaw:
    requires:
      env: []        # 需要的环境变量
      bins: []       # 需要的可执行文件
    primaryEnv: ""   # 主要认证凭证
    emoji: "<emoji>"
    models: []       # 兼容模型
---
```

## 注意事项

1. SKILL.md中不得包含个人信息——姓名、API Key、密码、路径
2. 声明所有依赖——env vars、bins要完整
3. 遵循语义化版本——1.0.0、1.1.0、2.0.0
4. 诚实说明限制——明确告知技能不能做什么
5. 双语格式——英文区段 + 中文区段，不混写

## Skill 架构模式

### 共享组件模式
将可复用能力抽取为独立skill供其他skill依赖：
- `complex-memory-manager` — 隐私感知记忆管理（T1/T2/T3）、加密、清理
- `self-iteration-engine` — 使用日志、反馈循环、自动更新决策

其他skill在YAML frontmatter中声明依赖。更新共享组件时需检查所有依赖技能的向后兼容。

### 私人Skill模式
部分skill仅供个人使用，不发布：
- 不执行 `clawhub publish`
- 描述中标注 `【⚠️ 私人使用，不发布到 ClawHub】`
- 仍需执行隐私检查

### 知识积累模式
需要跨会话学习的skill应：
- 概念存入 `memory/concepts/<slug>.md`
- 使用 `complex-memory-manager` 做层级化持久存储
- 使用 `self-iteration-engine` 追踪使用和优化
