# skill-cost — Quick Reference

| Task | Command |
|------|---------|
| Full report | `bash ~/.openclaw/workspace/skills/skill-cost/skill-cost.sh report` |
| Last 7 days | `bash ~/.openclaw/workspace/skills/skill-cost/skill-cost.sh report --days 7` |
| Since date | `bash ~/.openclaw/workspace/skills/skill-cost/skill-cost.sh report --since 2026-03-01` |
| JSON output | `bash ~/.openclaw/workspace/skills/skill-cost/skill-cost.sh report --format json` |
| Top skills | `bash ~/.openclaw/workspace/skills/skill-cost/skill-cost.sh ranking` |
| Skill detail | `bash ~/.openclaw/workspace/skills/skill-cost/skill-cost.sh detail <skill-name>` |
| Compare | `bash ~/.openclaw/workspace/skills/skill-cost/skill-cost.sh compare <skill1> <skill2>` |

## Decision Guide

- User asks "which skill costs the most" → `ranking`
- User asks about a specific skill's cost → `detail <name>`
- User wants overall spending by skill → `report`
- User wants to compare two skills → `compare <a> <b>`
- User wants data for dashboards → add `--format json`
