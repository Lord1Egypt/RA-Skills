# Digest Template

Best for quick scanning. Each message summarized in one line, grouped by channel.

## Output Format

```markdown
# {Channel names} · Briefing
**Time range:** {start date} ~ {end date}

---

## Key Points

- {one-line gist}
- {one-line gist}
...

---

N messages across M channels
```

## Rules

- Extract the core information; cut filler and redundancy.
- One line per message.
- Merge multiple messages covering the same event into a single bullet.
- Order by importance — lead with the most significant.
