---
name: skill-activator
description: |
  Skill 激活器——帮助用户发现自动化需求、匹配已有 Skill、融合生成新 Skill。
  解决"装了 OpenClaw 不知道用来做什么"的核心问题。
  Use when: (1) User says "帮我看看能自动化什么", "我能用 OpenClaw 做什么", "帮我体检", "激活", "scan my skills"
  (2) User says "帮我把这几个 Skill 组合起来", "融合 Skill", "fuse skills", "combine skills"
  (3) User says "我是产品经理/程序员/博主，有什么推荐", "推荐自动化方案"
  (4) User says "这个 Skill 不够用，能不能增强", "进化 Skill", "upgrade skill"
  (5) User asks "什么 Skill 适合我", "帮我找需求", "我该装什么 Skill"
  (6) User mentions "拿着锤子找钉子", "不知道该做什么", "Skill 吃灰了"
---

# Skill 激活器

> "你的 Skill 该醒了。"

## Core Workflow

Three-layer process: **Discover → Match → Fuse**.

### Layer 1: Discover Needs (需求发现)

Choose the appropriate discovery mode based on context:

**Mode A — Environment Scan (数字生活体检)**

1. Run `bash scripts/scan_environment.sh` to collect:
   - Installed skills list with descriptions
   - User identity from SOUL.md / USER.md / IDENTITY.md
   - Connected channels (feishu, wecom, telegram, etc.)
   - Workspace state (memory files, heartbeat config)
2. Analyze scan results to identify:
   - 🟢 Skills actively in use
   - 🟡 Skills installed but underutilized (have the skill, not using it)
   - 🔴 Capability gaps (needs not covered by any installed skill)
3. Generate personalized activation report with specific, actionable recommendations

**Mode B — Role-Based Recommendations (角色推荐)**

1. Identify user's role from SOUL.md or conversation
2. Read `references/role-templates.md` for role-specific pain points and automation ideas
3. Cross-reference with installed skills
4. Present top 3-5 recommendations ranked by: pain severity × ease of implementation

**Mode C — Pain Point Interview (痛点挖掘对话)**

1. Ask user to walk through their daily workflow
2. Listen for time-wasting patterns, repetitive tasks, context-switching pain
3. Quantify: "You spend ~X minutes/day on Y — automatable?"
4. Map each pain point to a concrete Skill combination
5. Prioritize by time saved per week

### Layer 2: Match Skills (智能匹配)

After discovering needs:

1. Check installed skills that match the need
2. Search ClawHub for additional skills: `clawhub search "<need description>"`
3. Identify gaps — needs no existing skill covers
4. Present matching plan:
   - ✅ **Already have**: installed skills that apply
   - 📦 **Recommend install**: available on ClawHub via `clawhub install <name>`
   - 🔧 **Can fuse**: combine existing skills to cover this need
   - 🆕 **Need to create**: no skill exists, suggest building one

### Layer 3: Fuse & Generate (融合生成)

When combining skills into a new workflow:

1. Read `references/fusion-guide.md` for fusion patterns and templates
2. Read each source skill's SKILL.md to understand inputs, outputs, dependencies
3. Design the pipeline (sequential, fan-out, aggregation, or enhancement)
4. Generate new fused SKILL.md with proper frontmatter, workflow steps, and error handling
5. Add any glue scripts to `scripts/` if data format conversion is needed
6. Package with `package_skill.py` for distribution

## Output Format

### Activation Report

```
🔍 Skill 激活报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 身份：{role from SOUL.md}
🔌 已连接：{channels}
📦 已安装：{N} 个 Skill

💡 发现 {N} 个自动化机会：

1️⃣ {pain point description}
   ⏱ 预计每周节省：{X} 分钟
   🧩 需要：{Skill A} + {Skill B}
   📊 可行度：⭐⭐⭐⭐⭐
   → [一键激活]

2️⃣ {pain point description}
   ...

🟡 沉睡的 Skill（装了没用）：
   - {skill name}: 它能帮你 {what it does}

📦 推荐安装：
   - {skill name}: 解决 {what problem}
   - 安装命令：clawhub install {name}
```

### Fused Skill Output

When generating a fused skill, output:
1. The complete SKILL.md content
2. Any required glue scripts
3. Installation/usage instructions
4. Packaging command: `package_skill.py <path>`

## Key Principles

- **Be specific, not generic**: "你每周花2小时做周报" > "你可以自动化一些任务"
- **Quantify savings**: Always estimate time/effort saved
- **One-click actionable**: Every recommendation should be immediately executable
- **Respect what's installed**: Prioritize solutions using skills the user already has
- **Progressive**: Start with quick wins, then suggest more advanced automations
