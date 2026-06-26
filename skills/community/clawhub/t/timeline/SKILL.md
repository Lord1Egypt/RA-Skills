---
name: timeline
description: Log dated events and facts to a queryable personal timeline. Use when the user wants to record something that happened (medical events, family moments, milestones) without cluttering the calendar. Not for scheduling — for remembering.
metadata:
  openclaw:
    triggers:
      - "log that"
      - "save to timeline"
      - "add to timeline"
      - "record that"
      - "timeline"
---

# Timeline Skill

A personal event log for dated facts that don't belong on a calendar.

## Use Cases

- "Colette had a fever yesterday" → log it
- "Started Doxycycline for MRSA" → log it with #medical tag
- "First day Noah rode a bike" → log it with #milestone tag
- "When did Colette last have a fever?" → search timeline

## Commands

### Log an event

```bash
# Basic
timeline log "Colette had a fever"

# With date (defaults to today)
timeline log "Started Doxycycline" --date 2026-02-25

# With tags
timeline log "MRSA infection #2, started Doxycycline" --tags medical,andrew

# With both
timeline log "Noah's first bike ride" --date 2026-02-20 --tags milestone,noah
```

### Search

```bash
# Full-text search
timeline search "fever"

# By tag
timeline search --tag medical

# By date range
timeline search --from 2026-02-01 --to 2026-02-28

# Combined
timeline search "MRSA" --tag medical --from 2026-01-01
```

### List recent

```bash
# Last 10 entries (default)
timeline list

# Last N entries
timeline list --limit 30

# By tag
timeline list --tag family
```

## Storage

Events stored in: `{vault}/Timeline.md`

Format:
```markdown
## 2026-02-25

- **08:30** Colette had a fever #family #medical
- **21:00** Started Doxycycline for MRSA #medical #andrew

## 2026-02-20

- **14:00** Noah's first bike ride without training wheels #milestone #noah
```

## Integration Points

- **QMD searchable** — indexed automatically
- **Briefings** — surface recent entries in morning brief
- **Heartbeat** — could prompt "anything to log?" at end of day
- **Medical folder** — cross-link medical events to Medical/ notes

## Implementation

Script: `scripts/timeline.sh` (or `timeline.js`)

Dependencies:
- Vault path from environment or config
- Date parsing (GNU date or node)
- Simple grep/ripgrep for search

## Future Ideas

- Categories with separate files (Medical Timeline, Family Timeline)
- Export to CSV/JSON
- Stats ("how many fevers this year?")
- Reminders ("it's been 6 months since last dentist visit")
