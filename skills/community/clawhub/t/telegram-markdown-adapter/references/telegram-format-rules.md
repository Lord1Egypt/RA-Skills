# Telegram Format Rules

Use this reference when adapting markdown-heavy content into Telegram-safe output.

## 1. Heading conversion

### Input
```md
# Main Title
## Section Title
### Minor Title
```

### Preferred Telegram output
```text
**Main Title**

**Section Title**

**Minor Title**
```

Optional: add emoji only when it improves scanning, not as decoration spam.

## 2. Divider conversion

### Input
```md
---
```

### Output
```text
───
```

## 3. Table conversion

Telegram is poor for Markdown tables. Convert them.

### Input
```md
| Name | Status | Note |
|---|---|---|
| API | Done | Stable |
| Bot | Blocked | Waiting |
```

### Output
```text
**API**
- Status: Done
- Note: Stable

**Bot**
- Status: Blocked
- Note: Waiting
```

For comparisons, prefer repeated blocks or `A: ... / B: ...` lines.

## 4. Checklist conversion

### Input
```md
- [ ] Fix Telegram formatting
- [x] Install skill
```

### Output
```text
- ☐ Fix Telegram formatting
- ✅ Install skill
```

If the surrounding tone is more natural, `- 待办：...` is also acceptable.

## 5. Bullet and nesting rules

Telegram reads best with shallow nesting.

### Preferred
- one level of bullets
- at most one nested level when truly needed
- break complex trees into separate sections

### Avoid
- three or more nested bullet levels
- long bullets with multiple clauses

## 6. Code handling

### Keep inline code for
- commands
- file paths
- env vars
- identifiers

### Keep fenced code blocks only when
- code is the main artifact
- the user needs copy/paste fidelity
- syntax matters more than readability

### Otherwise
- summarize the meaning
- include only the shortest useful snippet

## 7. Link handling

### Prefer
- raw visible URLs when the user may want to tap or copy them
- one link per line or bullet when several links are included
- Telegram HTML links when clean labels improve readability and the send path supports HTML safely

### Avoid
- relying on Markdown inline links like `[label](url)` when simple raw URLs are clearer
- burying important URLs inside long paragraphs

## 8. HTML mode safe subset

OpenClaw Telegram delivery supports HTML parse mode with plain-text fallback on parse errors.

### Safe subset
- `<b>`
- `<i>`
- `<u>`
- `<s>`
- `<code>`
- `<pre>`
- `<a href="...">label</a>`

### Use HTML when
- bold section labels matter
- inline code should be visually precise
- links need clean labels
- the message is a structured alert / report / summary

### Avoid
- deep nesting
- unsupported tags
- mixed Markdown and HTML in the same final rendering
- unescaped raw `<`, `>`, `&`

## 9. Long reply splitting

Split long Telegram replies when any of these is true:
- more than 5 major sections
- many bullets under each section
- mixed prose plus code plus lists
- report feels visually heavy

### Good split pattern
Message 1:
- headline
- context
- sections 1–2

Message 2:
- sections 3–4
- next steps

## 10. Style target

Aim for output that feels like:
- Markdown in spirit
- Telegram in rendering

That means:
- clear sections
- bold section labels
- compact bullets
- no raw syntax leakage unless deliberately preserved
- readable links
- controlled code usage
- HTML emphasis where it improves clarity without fragility

## 11. Style selection matrix

Use this matrix when the content feels table-like.

| Situation | Best style |
|---|---|
| Short technical fields, alignment matters | Style 1: monospace pseudo-table |
| Explanatory content, mobile readability matters | Style 2: card blocks |
| Short status-heavy summary, Telegram vibe matters | Style 4: emoji column style |
| Unclear / mixed | Style 2: card blocks |

### Quick tests

#### Choose Style 1 when
- most cells are short
- row count is modest
- comparison precision matters
- the block benefits from equal-width presentation

#### Choose Style 2 when
- at least one field tends to become a sentence
- the user will read rather than scan
- the content is more report-like than dashboard-like

#### Choose Style 4 when
- status cues matter more than exact alignment
- emoji improves scan speed
- the content should feel lighter and more chat-native

## 11. Example transformation

### Raw draft
```md
# Weekly Update

## Progress
| Area | State | Notes |
|---|---|---|
| Search | Done | Brave switched to web |
| Compaction | In Progress | guardian disabled |

## TODO
- [ ] Monitor stability
- [x] Update memory
```

### Telegram-safe version
```text
**Weekly Update**

**Progress**

**Search**
- State: Done
- Notes: Brave switched to web

**Compaction**
- State: In Progress
- Notes: guardian disabled

**TODO**
- ☐ Monitor stability
- ✅ Update memory
```
