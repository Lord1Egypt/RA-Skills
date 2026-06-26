---
name: skill-vetter-optimized
version: 2.0.0
description: "🔒 优化版技能审查器 - 安全优先的AI代理技能审查工具。在从ClawHub、GitHub或其他来源安装任何技能前使用。检查红标、权限范围和可疑模式。包含实用工具和系统化审查清单。基于原始skill-vetter优化，添加了Python检查脚本和详细审查流程。"
---

# Skill Vetter Optimized 🔒✨

**优化版技能审查器** - 基于原始skill-vetter优化增强

## 🚀 优化亮点

✅ **新增实用工具** - Python检查脚本快速分析技能目录  
✅ **系统化审查流程** - 四阶段审查清单  
✅ **详细文档** - 完整的审查指南和示例  
✅ **保持兼容** - 完全兼容原始审查协议  
✅ **性能优化** - 更快的审查流程  

Security-first vetting protocol for AI agent skills. **Never install a skill without vetting it first.**

## When to Use

- Before installing any skill from ClawdHub
- Before running skills from GitHub repos
- When evaluating skills shared by other agents
- Anytime you're asked to install unknown code

## Vetting Protocol

### Step 1: Source Check

```
Questions to answer:
- [ ] Where did this skill come from?
- [ ] Is the author known/reputable?
- [ ] How many downloads/stars does it have?
- [ ] When was it last updated?
- [ ] Are there reviews from other agents?
```

### Step 2: Code Review (MANDATORY)

Read ALL files in the skill. Check for these **RED FLAGS**:

```
🚨 REJECT IMMEDIATELY IF YOU SEE:
─────────────────────────────────────────
• curl/wget to unknown URLs
• Sends data to external servers
• Requests credentials/tokens/API keys
• Reads ~/.ssh, ~/.aws, ~/.config without clear reason
• Accesses MEMORY.md, USER.md, SOUL.md, IDENTITY.md
• Uses base64 decode on anything
• Uses eval() or exec() with external input
• Modifies system files outside workspace
• Installs packages without listing them
• Network calls to IPs instead of domains
• Obfuscated code (compressed, encoded, minified)
• Requests elevated/sudo permissions
• Accesses browser cookies/sessions
• Touches credential files
─────────────────────────────────────────
```

### Step 3: Permission Scope

```
Evaluate:
- [ ] What files does it need to read?
- [ ] What files does it need to write?
- [ ] What commands does it run?
- [ ] Does it need network access? To where?
- [ ] Is the scope minimal for its stated purpose?
```

### Step 4: Risk Classification

| Risk Level | Examples | Action |
|------------|----------|--------|
| 🟢 LOW | Notes, weather, formatting | Basic review, install OK |
| 🟡 MEDIUM | File ops, browser, APIs | Full code review required |
| 🔴 HIGH | Credentials, trading, system | Human approval required |
| ⛔ EXTREME | Security configs, root access | Do NOT install |

## Output Format

After vetting, produce this report:

```
SKILL VETTING REPORT
═══════════════════════════════════════
Skill: [name]
Source: [ClawdHub / GitHub / other]
Author: [username]
Version: [version]
───────────────────────────────────────
METRICS:
• Downloads/Stars: [count]
• Last Updated: [date]
• Files Reviewed: [count]
───────────────────────────────────────
RED FLAGS: [None / List them]

PERMISSIONS NEEDED:
• Files: [list or "None"]
• Network: [list or "None"]  
• Commands: [list or "None"]
───────────────────────────────────────
RISK LEVEL: [🟢 LOW / 🟡 MEDIUM / 🔴 HIGH / ⛔ EXTREME]

VERDICT: [✅ SAFE TO INSTALL / ⚠️ INSTALL WITH CAUTION / ❌ DO NOT INSTALL]

NOTES: [Any observations]
═══════════════════════════════════════
```

## 实用工具

### 1. 技能检查脚本

使用内置的Python脚本快速检查技能目录：

```bash
# 检查技能目录的基本信息和安全风险
python3 /root/.openclaw/skills/skill-vetter/scripts/skill_checker.py /path/to/skill
```

### 2. GitHub仓库检查

对于GitHub托管的技能：
```bash
# 检查仓库统计信息
curl -s "https://api.github.com/repos/OWNER/REPO" | jq '{stars: .stargazers_count, forks: .forks_count, updated: .updated_at}'

# 列出技能文件
curl -s "https://api.github.com/repos/OWNER/REPO/contents/skills/SKILL_NAME" | jq '.[].name'

# 获取并审查SKILL.md
curl -s "https://raw.githubusercontent.com/OWNER/REPO/main/skills/SKILL_NAME/SKILL.md"
```

### 3. 使用审查清单

参考 `references/checklist.md` 进行系统化的技能审查。

## Trust Hierarchy

1. **Official OpenClaw skills** → Lower scrutiny (still review)
2. **High-star repos (1000+)** → Moderate scrutiny
3. **Known authors** → Moderate scrutiny
4. **New/unknown sources** → Maximum scrutiny
5. **Skills requesting credentials** → Human approval always

## Remember

- No skill is worth compromising security
- When in doubt, don't install
- Ask your human for high-risk decisions
- Document what you vet for future reference

---

*Paranoia is a feature.* 🔒🦀
