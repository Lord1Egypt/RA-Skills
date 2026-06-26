# Domotics Skill Template

Template for creating domotics skills extracted from recurring learnings or issues.

---

## SKILL.md Template

```markdown
---
name: skill-name-here
description: "Domotics pattern this skill solves and when to use it."
---

# Skill Name

Brief context: what automation reliability, safety, or energy problem this addresses.

## Quick Reference

| Situation | Action |
|-----------|--------|
| [Trigger] | [Response] |
| [Trigger] | [Response] |

## Scope and Safety

- Documentation/reminder only; does not directly actuate devices
- Human confirmation required for high-impact actions
- Safe fallback when signals are ambiguous

## Diagnostic Steps

1. Verify trigger and timeline
2. Validate sensors/devices/integrations
3. Confirm rule precedence and guard conditions
4. Apply remediation and verify stability

## Promotion Target

- Home automation playbook | Device compatibility matrix | Automation rule library | Safety automations

## Source

- Entry ID: LRN-YYYYMMDD-XXX or DOM-YYYYMMDD-XXX
- Category: automation_conflict | sensor_drift | device_unreachable | integration_break | energy_optimization | safety_rule_gap | occupancy_mismatch | latency_jitter
- Extraction Date: YYYY-MM-DD
```

---

## Extraction Checklist

- [ ] Pattern is recurring and verified
- [ ] Safety constraints are explicit
- [ ] No private household secrets included
- [ ] Promotion target is selected
- [ ] Source entry is linked
- [ ] Generated content is self-contained

