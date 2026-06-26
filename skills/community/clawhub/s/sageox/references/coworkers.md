# Coworkers — Expert Agent Management

Discover, load, create, and remove expert AI coworkers from your team
context using `ox coworker`.

## Commands

### List available coworkers

```bash
ox coworker list [--json] [--team <id>]
```

Shows all expert agents available in the team context with their name,
description, model, and team. Use `--json` for structured output.

### Load a coworker

`ox coworker load` is designed for coding agent sessions (Claude Code,
Cursor) and will not inject into an OpenClaw session. Instead, use
`ox coworker load <name> --raw` to print the coworker's full prompt,
then read and embody the expertise directly in this conversation.

**Workflow:**

```bash
ox coworker load <name> --raw [--team <id>]
```

If `--raw` is not available, fall back to reading the coworker file
directly from the team context repo:

```bash
# Find the coworker file
ox coworker list --json | jq -r '.[] | select(.name=="<name>") | .path'
# Then read the file at that path
```

Once you have the coworker's prompt content, tell the user:
"I've loaded **<name>**'s expertise into this session. I'll apply their
approach to our conversation. What would you like help with?"

Use `--model` to note the coworker's preferred model (informational only
in this context).

### Add a coworker

```bash
ox coworker add <file>.md [--team <id>]
```

Validates the file has correct YAML frontmatter, copies it to the team's
`coworkers/agents/` directory, and commits it. The coworker name is
derived from the filename (e.g., `security-reviewer.md` → `security-reviewer`).

### Remove a coworker

```bash
ox coworker remove <name> [--force] [--team <id>]
```

Removes the coworker from team context. Use `--force` to skip
confirmation.

## Authoring wizard

When the user wants to create a new coworker, guide them through this
flow:

### Step 1: Domain and specialty

Ask: "What domain should this coworker specialize in?" Examples:
- Security review
- Database optimization
- Frontend accessibility
- API design

### Step 2: Description

Ask: "What's the one-line description?" This is **required** for the
YAML frontmatter and is what other coworkers see when listing available
experts.

### Step 3: Model preference

Ask: "Which model should this coworker use?"
- `opus` — complex reasoning, deep analysis
- `sonnet` — balanced speed and capability (recommended default)
- `haiku` — lightweight, fast responses
- *inherit* — use whatever model the caller is using (omit field)

### Step 4: Generate the agent file

Write a temporary file with this format:

```yaml
---
description: "<one-line description from step 2>"
model: "<model from step 3>"  # omit this line if inherit
---

# <Coworker Name>

You are an expert in <domain from step 1>...

## Expertise

<List key areas of expertise>

## Approach

<Describe how this coworker should approach problems>
```

### Step 5: Confirm and add

Show the generated file to the user for review. Once confirmed:

```bash
ox coworker add /tmp/<name>.md
```

### Step 6: Verify

```bash
ox coworker list
```

Confirm the new coworker appears in the list.

## Multi-team handling

If the repo has multiple teams configured, use `--team <id>` on all
commands. If the user doesn't specify a team, ask which one they want
to manage coworkers for.
