# Failure Pattern Reference

Real-world skill triggering failures collected from GitHub Issues, Reddit, and community forums (2026).

## Pattern 1: Missing Trigger Phrases (65% of cases)

**Source:** GitHub openclaw/openclaw#43410, agentskills.io, philschmid.de

**Symptom:** Skill is installed correctly but never auto-activates.

**Root Cause:** Description describes capability but not WHEN to use it.

**Example (from audit of 52 built-in OpenClaw skills):**
- 34 of 52 skills (65%) had descriptions like `"Manages calendar events"` with no trigger condition
- After adding trigger phrases, activation rate improved from ~30% to ~90%

**Fix:**
```
Before: "Manages calendar events."
After: "ALWAYS invoke when the user asks to create, view, edit, or delete calendar events, schedule meetings, check availability, or set reminders. Do NOT use for email or task management."
```

## Pattern 2: YAML Parsing Failure (15% of cases)

**Source:** GitHub openclaw/openclaw#29981

**Symptom:** Skill doesn't appear in `openclaw skills` output at all.

**Root Cause:** Colon (`:`) in description field breaks YAML parsing.

**Example:**
```yaml
# BROKEN - colon breaks parsing
description: Use when: the user asks about weather
```

**Fix:**
```yaml
# FIXED - wrapped in quotes
description: "Use when the user asks about weather, temperature, or forecasts"
```

**Other YAML issues:**
- Multi-line descriptions truncated (only first line read)
- Missing `---` delimiters
- Tabs instead of spaces

## Pattern 3: Token Budget Overflow (10% of cases)

**Source:** dev.to (lizechengnet), claudefa.st

**Symptom:** Skill triggers when fewer skills are installed, stops after adding more.

**Root Cause:** Agent has a character budget for skill descriptions. When exceeded, skills are silently dropped.

**Detection:**
```bash
# Count total description characters
find ~/.openclaw/skills -name "SKILL.md" -exec head -5 {} \; | wc -c
```

**Fix:**
- Trim every description to essential trigger + keywords only
- Set `SLASH_COMMAND_TOOL_CHAR_BUDGET=30000` (Claude Code)
- Move detailed info to SKILL.md body

## Pattern 4: Skill Not Discovered (5% of cases)

**Source:** GitHub openclaw/openclaw#43735, #29122, #10386, #12092

**Symptom:** Skill file exists on disk but agent doesn't see it.

**Root Causes:**
1. Wrong directory: skill in `~/.openclaw/workspace/skills/` but agent looks in `~/.openclaw/skills/`
2. Symlink issues: symlinked skill directories are skipped for security
3. Session caching: skills added mid-session aren't visible until restart
4. Registry failure: file exists but skill registry doesn't index it

**Fix:**
```bash
# Verify skill is discovered
openclaw skills list

# If missing, check paths
ls ~/.openclaw/skills/
ls <workspace>/.agents/skills/
ls <workspace>/skills/

# Restart gateway after adding skills
openclaw gateway restart
```

## Pattern 5: Sub-Agent Isolation (3% of cases)

**Source:** Reddit r/AI_Agents, r/clawdbot

**Symptom:** Skill works in main agent but not in spawned sub-agents.

**Root Cause:** Isolated sub-agent sessions don't inherit parent's workspace skills.

**Fix:**
- Install skill in global path: `~/.openclaw/skills/`
- Or use `sessionTarget: "main"` for tasks needing the skill
- Or copy skill to sub-agent's workspace

## Pattern 6: Capabilities Mismatch (2% of cases)

**Source:** Reddit r/openclaw (multiple posts)

**Symptom:** Skill activates but agent says "I'm just a model" or asks for API keys it already has.

**Root Cause:** Skill requires tools/capabilities not enabled in the active runtime profile.

**Fix:**
```yaml
# In config.yaml, ensure tools profile includes needed capabilities
tools:
  - messaging
  - browser
  - exec
  # Add whatever the skill needs
```

## Statistics Summary

| Failure Pattern | Frequency | Severity | Auto-Fixable |
|----------------|-----------|----------|--------------|
| Missing trigger phrases | 65% | High | Partially |
| YAML parsing errors | 15% | Critical | Yes |
| Token budget overflow | 10% | Medium | Yes |
| Skill not discovered | 5% | Critical | Yes |
| Sub-agent isolation | 3% | Medium | Manual |
| Capabilities mismatch | 2% | High | Manual |

*Based on analysis of GitHub issues, Reddit posts, and community reports from Jan-Jun 2026.*
