# Example Scripts

These examples demonstrate common Telegram button patterns using OpenClaw CLI.

## Setup

Before running examples, replace `YOUR_CHAT_ID` with your actual Telegram chat ID:

```bash
# Find your chat ID by sending a message to your bot, then:
openclaw message send --target "telegram:YOUR_CHAT_ID" --message "Test"
```

Make scripts executable:

```bash
chmod +x *.sh
```

## Examples

### 1. basic_yes_no.sh

**Complexity:** Beginner

**Use case:** Simple confirmation dialogs

Sends a basic Yes/No message with two buttons. Perfect for:
- User confirmations
- Binary choices
- Simple approval workflows

**Run:**
```bash
./basic_yes_no.sh
```

---

### 2. workflows_menu.sh

**Complexity:** Intermediate

**Use case:** Multi-option menus

Sends a 3x2 grid menu with workflow options. Demonstrates:
- Multi-row button layout
- Emoji usage for visual clarity
- Descriptive callback naming

**Run:**
```bash
./workflows_menu.sh
```

---

### 3. full_flow_example.sh

**Complexity:** Advanced

**Use case:** Complete callback handling

Demonstrates the full interaction lifecycle:
1. Send interactive message
2. Capture message ID
3. Handle callback (simulated)
4. Send confirmation
5. Edit original message

This is the **recommended pattern** for production use.

**Run:**
```bash
./full_flow_example.sh
```

**Interactive:** This script prompts you to choose which button was "clicked" to demonstrate different callback paths.

---

## Common Patterns

### Pattern 1: Immediate Action
User clicks → Action executes → Confirmation sent → Buttons removed

```bash
# User clicks "Delete"
openclaw message send --target "$TARGET" --message "✅ Deleted"
openclaw message edit --target "$TARGET" --message-id "$ID" --message "Action: [Completed]"
```

### Pattern 2: Confirmation Chain
User clicks → Ask for confirmation → Execute → Final message

```bash
# User clicks "Delete All"
openclaw message send --target "$TARGET" \
    --message "⚠️ Are you SURE?" \
    --buttons '[[{"text": "Yes, delete", "callback_data": "confirm_delete"}]]'
```

### Pattern 3: Navigation
User clicks → Show new menu → Keep navigating

```bash
# User clicks "Settings"
openclaw message send --target "$TARGET" \
    --message "Settings:" \
    --buttons '[[{"text": "Account", "callback_data": "settings_account"}], [{"text": "← Back", "callback_data": "main_menu"}]]'
```

## Tips

- Always capture the message ID when sending buttons
- Edit messages after callback to remove buttons
- Use descriptive callback_data (e.g., `wf_search` not `btn1`)
- Keep 1-2 buttons per row for mobile UX
- Test on actual Telegram mobile client

## Troubleshooting

If buttons don't appear:
1. Validate JSON: `python3 ../../scripts/validate_buttons.py 'YOUR_JSON'`
2. Check quotes: Use single quotes around `--buttons` argument
3. Verify target format: Must be `telegram:CHAT_ID`
