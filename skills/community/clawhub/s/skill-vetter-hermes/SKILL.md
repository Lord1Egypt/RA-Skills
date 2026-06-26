---
name: skill-vetter
version: 1.2.0
description: Security-first skill vetting for AI agents. Use before installing any skill from ClawdHub, GitHub, or other sources. Checks for red flags, permission scope, and suspicious patterns. Auto-blocks high-risk skills.
---

# Skill Vetter 🔒

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

## Quick Vet Commands

For GitHub-hosted skills:
```bash
# Check repo stats
curl -s "https://api.github.com/repos/OWNER/REPO" | jq '{stars: .stargazers_count, forks: .forks_count, updated: .updated_at}'

# List skill files
curl -s "https://api.github.com/repos/OWNER/REPO/contents/skills/SKILL_NAME" | jq '.[].name'

# Fetch and review SKILL.md
curl -s "https://raw.githubusercontent.com/OWNER/REPO/main/skills/SKILL_NAME/SKILL.md"
```

## Trust Hierarchy (2-Level System)

### 🟢 Level 1: OFFICIAL (官方技能)
```
Sources:
- ~/.openclaw/workspace/skills/
- clawhub/official/
- openclaw/core/

Scanning: Light scan (check for obvious malware)
Action: Allow install unless EXTREME risk
```

### 🔴 Level 2: COMMUNITY (其他技能)
```
Sources:
- clawhub/community/
- GitHub repos
- Unknown sources

Scanning: Full strict scan (all red flags)
Action: Block HIGH or EXTREME risk automatically
```

## Auto-Block Rules (强制拦截规则)

### 扫描失败 → 阻止安装
```
Reason: 宁可错杀，不可放过
Action: Return error, do not proceed with installation
```

### 社区技能 + 高风险 → 强制阻止
```
Risk Level: HIGH or EXTREME
Action: Block installation, no user confirmation
Reason: 安全优先，不给绕过机会
```

### 官方技能 + 极高风险 → 阻止
```
Risk Level: EXTREME only
Action: Block installation
Reason: 官方技能也可能被篡改
```

## Integration with clawhub install

### Hook Implementation
```bash
# Before installing any skill:
1. Detect skill source → determine trust level
2. Call skill_vetter.scan() → get security report
3. Check should_block_install() → decide to proceed or block
4. If blocked → print report and exit with error
5. If allowed → proceed with installation
6. Log scan result for audit trail
```

### Output Format (Enhanced)
```
════════════════ 技能安全扫描 ════════════════
技能：[skill_name]
来源：[skill_source]
信任等级：[🟢 OFFICIAL / 🔴 COMMUNITY]
────────────────────────────────────────────
风险等级：[🟢 LOW / 🟡 MEDIUM / 🔴 HIGH / ⛔ EXTREME]
红色标志：[None / List of red flags]
────────────────────────────────────────────
建议：[✅ SAFE TO INSTALL / ❌ BLOCKED]
══════════════════════════════════════════
```

## Remember

- No skill is worth compromising security
- When in doubt, don't install
- **High-risk skills are auto-blocked, no confirmation**
- **Scan failures result in blocked installation**
- Document what you vet for future reference

---

*Paranoia is a feature.* 🔒🦀
*Security first, always.* 🛡️
