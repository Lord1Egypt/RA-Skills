# Chat Reference

## Message Operations

### Send Message as Bot

```bash
dws chat message send-by-bot --robot-code <BOT_CODE> --group <GROUP_ID> --title "<title>" --text "<content>"
```

**Parameters:**
- `--robot-code`: Bot robot code from DingTalk app settings
- `--group`: Group conversation ID
- `--title`: Message title (for markdown messages)
- `--text`: Message content (supports `@filename` for file input)

**Example:**
```bash
# Send from file
dws chat message send-by-bot --robot-code "robot123" --group "conv123" --title "Weekly Report" --text @report.md

# Send from stdin
cat message.md | dws chat message send-by-bot --robot-code "robot123" --group "conv123" --title "Update"
```

### Send Message as User

```bash
dws chat message send --conversation-id <convId> --text "<content>"
```

### Recall Message

```bash
dws chat message recall --conversation-id <convId> --message-id <msgId>
```

## Group Operations

### List Groups

```bash
dws chat group list [--limit <N>]
```

### Get Group Info

```bash
dws chat group get --group-id <groupId>
```

**Example:**
```bash
dws chat group get --group-id "conv123" --jq '.result | {name: .name, memberCount: .memberCount}'
```

### Create Group

```bash
dws chat group create --name "<group-name>" --user-ids <userId1,userId2>
```

### Add Members

```bash
dws chat group add-members --group-id <groupId> --user-ids <userId1,userId2>
```

### Remove Members

```bash
dws chat group remove-members --group-id <groupId> --user-ids <userId1,userId2>
```

## Topic/Thread Operations

### List Topics

```bash
dws chat topic list --group-id <groupId>
```

### Reply to Topic

```bash
dws chat topic reply --group-id <groupId> --topic-id <topicId> --text "<content>"
```

## Bot Operations

### Get Bot Info

```bash
dws chat bot get --robot-code <BOT_CODE>
```

### Send Single Chat Message

```bash
dws chat bot send-single --robot-code <BOT_CODE> --user-id <userId> --text "<content>"
```

## Common Patterns

### Send Message to Multiple Groups

```bash
# Get group IDs
dws chat group list --jq '.result[] | select(.name | contains("Project")) | .conversationId'

# Send to each (use script for batch)
for group in $GROUPS; do
  dws chat message send-by-bot --robot-code "robot123" --group "$group" --title "Notice" --text "Meeting at 3pm"
done
```

### Search Groups by Name

```bash
dws chat group list --jq '.result[] | select(.name | contains("Engineering")) | {id: .conversationId, name: .name}'
```

### Send Rich Text Message

```bash
# Markdown format
dws chat message send-by-bot --robot-code "robot123" --group "conv123" \
  --title "## Weekly Summary" \
  --text "### Completed\n- Task 1\n- Task 2\n\n### Next Week\n- Task 3"
```
