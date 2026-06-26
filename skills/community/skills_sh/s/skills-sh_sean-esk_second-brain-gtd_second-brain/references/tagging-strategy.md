# Tagging Strategy

> Comprehensive guide to using tags in the Second Brain system

---

## Core Philosophy

**Tags vs Folders:**
- **Folders** = WHERE (organization based on actionability - PARA)
- **Tags** = WHAT (discovery and categorization)

Use folders for ONE primary dimension (actionability), use tags for everything else.

---

## Tag Hierarchy

Use nested tags with forward slashes:

```
#parent/child
#status/active
#context/computer
```

---

## Standard Tag Categories

### 1. Status Tags (Required)

**For GTD Working Documents:**
```
#status/inbox      - Just captured, not processed
#status/next       - Ready to work on
#status/active     - Currently working on
#status/waiting    - Blocked by external dependency
#status/someday    - Might do later
#status/done       - Completed, not archived
#status/archived   - Completed and filed
```

**For Knowledge Notes:**
```
#status/fleeting     - Temporary thought
#status/developing   - Being refined
#status/evergreen    - Mature, stable
```

---

### 2. Type Tags (Required - ONE per note)

**GTD Working Documents:**
```
#project          - Multi-step outcome with deadline
#task             - Single actionable item
#area             - Ongoing responsibility
```

**Knowledge Notes:**
```
#permanent-note   - Atomic, evergreen insight
#fleeting-note    - Temporary capture
#reference-note   - External source summary
```

**System Notes:**
```
#moc              - Map of Content
#meeting-note     - Meeting summary
#daily-plan       - Daily planning document
#brain-dump       - Archived brain dump
```

---

### 3. Context Tags (For Tasks Only)

Physical location or tools required:

```
#context/office      - At office with resources
#context/computer    - Any computer work
#context/phone       - Phone calls, mobile work
#context/home        - Home-specific tasks
#context/errands     - Out running errands
#context/anywhere    - Any location
```

**Usage:** Use ONLY on tasks, one per task

---

### 4. Energy Tags (For Tasks Only)

Energy level required:

```
#energy/high      - Peak focus, complex thinking
#energy/medium    - Standard work
#energy/low       - Admin, simple tasks
```

**High Energy:** Writing, coding, creative work, strategic planning
**Medium Energy:** Emails, meetings, research
**Low Energy:** Filing, data entry, routine admin

---

### 5. Time Tags (For Tasks Only)

Estimated time to complete:

```
#time/5m       - Quick wins (< 5 minutes)
#time/15m      - Short tasks (5-15 minutes)
#time/30m      - Half-hour tasks
#time/1h       - Hour-long focus work
#time/2h       - Deep work sessions
#time/4h+      - Project marathons
```

---

### 6. Area/Topic Tags

Identify domain or subject:

```
#work              - Work-related
#personal          - Personal life
#health-fitness    - Health and wellness
#learning          - Educational pursuits
#productivity      - Productivity systems
#business          - Business operations
```

**Customize these** based on your specific needs during setup.

---

### 7. Priority Tags (Optional)

For tasks and projects:

```
#priority/high
#priority/medium
#priority/low
#priority/urgent
```

---

## Tag Usage by Note Type

### Project Note

```yaml
tags:
  - project
  - work                  # Area
  - status/active
  - priority/high         # Optional
```

### Task Note

```yaml
tags:
  - task
  - personal              # Area
  - status/next
  - context/computer
  - energy/high
  - time/2h
```

### Permanent Note

```yaml
tags:
  - permanent-note
  - productivity          # Topic
  - status/evergreen
```

### Area Note

```yaml
tags:
  - area
  - health-fitness
  - status/active
```

---

## Tagging Rules

### Required Tags

Every note MUST have:
1. **Type tag** - What kind of note
2. **Status tag** - Current state

### Tag Limits

- Maximum 5-7 tags per note
- More tags = less useful
- Quality over quantity

### Naming Conventions

1. **Lowercase** - `#video-idea` not `#Video-Idea`
2. **Hyphens for spaces** - `#meeting-note` not `#meeting_note`
3. **Consistent** - Pick one naming pattern
4. **Short** - `#content` not `#content-creation-ideas`
5. **Hierarchical** - Use `/` for parent/child

### YAML Format

**Always use list syntax:**

```yaml
# ✅ Correct
tags:
  - status/active
  - project
  - work

# ❌ Wrong
tags: [status/active, project, work]
```

---

## Tag Queries

### Finding Notes

```
tag:#project tag:#status/active
tag:#permanent-note tag:#productivity
tag:#task tag:#context/computer tag:#energy/high
```

### Filtering in Daily Planning

The system uses tags to filter available tasks:

1. Filter by `#context/*` matching current context
2. Filter by `#energy/*` matching current energy
3. Filter by `#time/*` fitting available time
4. Sort by priority

---

## Anti-Patterns

### Tag Explosion

**Problem:** 50+ unique tags, most used once
**Solution:** Consolidate, use folders instead

### Redundant Tags

**Problem:** Multiple tags meaning the same thing
**Solution:** Pick ONE consistent tag

### Tag Soup

**Problem:** 15 tags on a single note
**Solution:** Limit to 5-7 max

### Inconsistent Naming

**Problem:** `#YouTube`, `#youtube`, `#content-creation`
**Solution:** Pick one naming pattern

---

## Quick Reference

### Minimum Required

```yaml
tags:
  - [type-tag]          # project, permanent-note, etc.
  - status/[status]     # active, inbox, etc.
```

### Complete Task Tagging

```yaml
tags:
  - task
  - [area-tag]          # work, personal, etc.
  - status/next
  - context/[context]   # computer, phone, etc.
  - energy/[level]      # high, medium, low
  - time/[estimate]     # 15m, 1h, etc.
```

---

**Remember:**
- Tags are for WHAT (discovery)
- Folders are for WHERE (organization)
- Less is more - keep it simple
- Consistency beats perfection
