# v0-cli — AI Agent Skill Reference

A CLI tool for creating and iterating on websites using [v0.dev](https://v0.dev) from the terminal.
Designed for machine/agent use — no interactive prompts.

## Prerequisites

- Node.js >= 18
- `V0_API_KEY` environment variable set (obtain from https://v0.dev/chat/settings/keys)
- Dependencies installed: `npm install` in this directory

## Invocation

```bash
node /path/to/v0-cli/src/index.js <command> [options]
```

Or if installed globally (`npm install -g @hlongvu/v0-cli`):

```bash
v0 <command> [options]
```

---

## Commands

### `create` — Create a new website

```bash
v0 create <prompt> [options]
```

**Arguments:**
- `prompt` *(required)* — Natural language description of the website to generate.

**Options:**
| Flag | Description | Default |
|------|-------------|---------|
| `-p, --privacy <privacy>` | `public`, `private`, or `unlisted` | `public` |
| `-s, --system <system>` | Custom system prompt for the AI | — |
| `--no-open` | Skip opening the browser after creation | opens browser |

**Examples:**
```bash
# Create and skip browser open (recommended for automation)
v0 create "A dark SaaS landing page with hero, features, and pricing" --no-open

# Create private chat with custom system prompt
v0 create "Admin dashboard" --privacy private --system "Use shadcn/ui components"
```

**Output (stdout):**
```
  Chat ID:  <chatId>
  Preview:  https://v0.app/chat/<chatId>
```

**Key output to parse:** `Chat ID:` line — extract the `chatId` for follow-up `chat` calls.

---

### `chat` — Send a message to an existing chat

```bash
v0 chat <chatId> <message>
```

**Arguments:**
- `chatId` *(required)* — The ID of an existing v0 chat.
- `message` *(required)* — The refinement message to send.

**Output (stdout):**
```
  Chat ID: <chatId>
  Name:    <name>
  URL:     <url>

  v0: <streamed response text>

  Preview: https://v0.app/chat/<chatId>
```

**Examples:**
```bash
v0 chat abc123xyz "Add a dark mode toggle to the header"
v0 chat abc123xyz "Make the layout responsive for mobile"
```

---

### `list` — List all chats

```bash
v0 list [options]
```

**Options:**
| Flag | Description | Default |
|------|-------------|---------|
| `-l, --limit <n>` | Max number of chats to display | `20` |

**Output format:**
```
   1. <name> [public] 3/31/2026
      ID:  <chatId>
      URL: https://v0.app/chat/<chatId>
```

---

## Automation / Agent Workflow

> **IMPORTANT — `v0 create` timeout handling:**
> `v0 create` can take a long time to complete and **may time out** before returning output.
> If the command times out or the output is lost:
> - **Do NOT rerun `v0 create`** — the project may already have been created.
> - Run `v0 list` to check if the chat was created, then use its `chatId` to continue.

```bash
# 1. Create a site, capture chatId
output=$(v0 create "A portfolio site with dark theme" --no-open 2>&1)
chatId=$(echo "$output" | grep "Chat ID:" | awk '{print $NF}')

# If chatId is empty (timeout / lost output), check if it was already created:
# v0 list --limit 5
# Then extract the chatId manually from the list output.

# 2. Send refinement messages
v0 chat "$chatId" "Add a contact form section"
v0 chat "$chatId" "Make the layout responsive for mobile"

# 3. List all chats
v0 list --limit 10
```

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `V0_API_KEY` | Yes | API key from https://v0.dev/chat/settings/keys |

---

## Error Handling

| Scenario | Behavior |
|----------|----------|
| Missing `V0_API_KEY` | Prints instructions and exits with code 1 |
| Invalid API key (401) | Prints error with link to settings page |
| Chat not found (404) | Prints error and exits with code 1 |
| Rate limit (429) | Prints error message from API |
