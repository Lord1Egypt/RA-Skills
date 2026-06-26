# Fusion Guide — Skill Activator

How to fuse multiple skills into a new composite skill.

## Fusion Process

### Step 1: Analyze Source Skills

For each source skill, extract:
- **Inputs**: What data/triggers does it accept?
- **Outputs**: What does it produce?
- **Dependencies**: What tools/APIs does it need?
- **Trigger patterns**: What user phrases activate it?

Read each source SKILL.md frontmatter + body to build this understanding.

### Step 2: Design the Pipeline

Map source skills into a data flow:

```
[Trigger] → [Skill A: gather] → [Skill B: transform] → [Skill C: deliver]
```

Identify:
- **Glue logic**: Data format conversions between skills
- **Error handling**: What if one step fails?
- **Configuration**: What parameters should be user-configurable?

### Step 3: Generate Fused SKILL.md

Create a new SKILL.md that:

1. Has a clear name describing the combined workflow
2. Has a description covering all trigger scenarios
3. Contains step-by-step instructions referencing source skill patterns
4. Includes any glue scripts needed for data conversion
5. Lists all dependencies from all source skills

### Step 4: Package and Test

Use `package_skill.py` to package the fused skill, then test with real scenarios.

## Fusion Patterns

### Pattern A: Sequential Pipeline

Skills execute in order. Output of one becomes input of next.

```
Example: "Hot Topic to XHS Publisher"
agent-reach (search trending) 
  → content-shapeshifter (adapt for XHS)
  → baoyu-xhs-images (generate cover)
  → xhs-publish (publish)
```

### Pattern B: Fan-out Distribution

One input distributed to multiple skills in parallel.

```
Example: "One Post, All Platforms"
[article input]
  → content-shapeshifter (XHS version) → xhs-publish
  → content-shapeshifter (WeChat version) → baoyu-post-to-wechat
  → content-shapeshifter (Twitter version) → [manual post]
```

### Pattern C: Aggregation

Multiple sources feed into one processor.

```
Example: "Morning Briefing"
gog (Gmail unread) ─┐
feishu-doc (tasks) ──┼→ [aggregate + summarize] → wecom-msg (push to chat)
github (notifications)┘
```

### Pattern D: Enhancement / Evolution

Existing skill enhanced with additional capabilities.

```
Example: "Weather Pro"
weather (base forecast)
  + wecom-schedule (check outdoor events)
  + [outfit suggestion logic]
  = weather-pro (forecast + event awareness + outfit tips)
```

## SKILL.md Template for Fused Skills

```yaml
---
name: {fused-skill-name}
description: |
  Combined workflow that {what it does end-to-end}.
  Fused from: {skill-a} + {skill-b} + {skill-c}.
  Use when: {trigger scenarios}.
---
```

```markdown
# {Fused Skill Name}

## Overview
{One paragraph explaining the end-to-end workflow}

## Prerequisites
- Requires skills: {list source skills}
- Requires channels: {list required channel connections}

## Workflow

### Step 1: {First stage}
{Instructions referencing source skill A patterns}

### Step 2: {Second stage}
{Instructions referencing source skill B patterns}

### Step 3: {Third stage}
{Instructions referencing source skill C patterns}

## Configuration
{User-configurable parameters}

## Error Handling
{What to do when individual steps fail}
```
