# Telegram Interactive Buttons - Complete Reference

## CLI Command Reference

### Send Message with Buttons

```bash
openclaw message send \
  --target "telegram:CHAT_ID" \
  --message "MESSAGE_TEXT" \
  --buttons 'BUTTONS_JSON' \
  [--channel telegram] \
  [--silent]
```

**Parameters:**

- `--target` (required): Telegram chat ID in format `telegram:CHAT_ID`
- `--message` (required): Message text to display
- `--buttons` (required): JSON array of button rows (see Button Structure)
- `--channel` (optional): Specify `telegram` explicitly (auto-detected from target)
- `--silent` (optional): Send without notification sound

### Edit Message

```bash
openclaw message edit \
  --target "telegram:CHAT_ID" \
  --message-id "MESSAGE_ID" \
  --message "NEW_MESSAGE_TEXT"
```

**Parameters:**

- `--target` (required): Telegram chat ID
- `--message-id` (required): ID of message to edit (returned from original send)
- `--message` (required): New message text (buttons automatically removed)

## Button Structure

### JSON Format

```json
[
  [BUTTON_OBJECT, BUTTON_OBJECT, ...],
  [BUTTON_OBJECT, BUTTON_OBJECT, ...],
  ...
]
```

Each row is an array of button objects. Buttons in the same row appear side-by-side.

### Button Object

```json
{
  "text": "Display Text",
  "callback_data": "unique_callback_id",
  "style": "primary|success|danger"  // optional
}
```

**Fields:**

- `text` (required, string): Text displayed on button (max ~30 chars for mobile)
- `callback_data` (required, string): Unique identifier for callback (max 64 bytes)
- `style` (optional, string): Button styling - `primary`, `success`, or `danger`

### Layout Guidelines

**Optimal layouts:**

- **1 button per row**: Best for critical actions
  ```json
  [[{"text": "Confirm", "callback_data": "confirm"}]]
  ```

- **2 buttons per row**: Best for Yes/No, Accept/Cancel
  ```json
  [[{"text": "Yes", "callback_data": "yes"}, {"text": "No", "callback_data": "no"}]]
  ```

- **3+ buttons**: Use multiple rows
  ```json
  [
    [{"text": "Option 1", "callback_data": "opt1"}, {"text": "Option 2", "callback_data": "opt2"}],
    [{"text": "Option 3", "callback_data": "opt3"}, {"text": "Cancel", "callback_data": "cancel"}]
  ]
  ```

**Layout Limits & Guidelines:**

- **Max buttons per row:** 8 (Official Telegram API limit)
- **Max total buttons:** 100
- **1-3 buttons per row**: Optimal for standard menus/mobile readability.
- **4-8 buttons per row**: Recommended for grids (numeric pads, calendars, compact galleries).

**Avoid:**
- More than 8 buttons per row (Telegram will reject the request)
- More than 100 total buttons (Telegram will reject the request)
- Very long button text (truncates on mobile)

## Style Reference

### Visual Appearance

- `primary`: Default blue background (Telegram standard)
- `success`: Green background (confirmations, positive actions)
- `danger`: Red background (deletions, destructive actions)

### Style Examples

```json
[
  [
    {"text": "✅ Approve", "callback_data": "approve", "style": "success"},
    {"text": "❌ Reject", "callback_data": "reject", "style": "danger"}
  ],
  [
    {"text": "⏸️ Skip", "callback_data": "skip", "style": "primary"}
  ]
]
```

**Note:** Not all Telegram clients support custom styles - they may render as default blue.

## Common Error Messages

### "buttons[0][0] requires text and callback_data"

**Cause:** Malformed JSON or missing required fields

**Fix:**
```bash
# ❌ Wrong (escaped quotes)
--buttons '[[{\"text\": \"Yes\", \"callback_data\": \"yes\"}]]'

# ✅ Correct (clean JSON)
--buttons '[[{"text": "Yes", "callback_data": "yes"}]]'
```

### "Invalid JSON"

**Cause:** Syntax error in JSON structure

**Fix:** Use validator:
```bash
python3 scripts/validate_buttons.py '[[{"text": "Test", "callback_data": "test"}]]'
```

### "Message not found"

**Cause:** Incorrect message ID when editing

**Fix:** Capture message ID from send response:
```bash
openclaw message send ... | grep "Message ID:"
```

## Advanced Patterns

### Dynamic Button Generation

```bash
# Generate buttons from array
OPTIONS=("Search" "Metrics" "Calendar")
BUTTONS="["

for i in "${!OPTIONS[@]}"; do
    [ $i -gt 0 ] && BUTTONS+=","
    BUTTONS+="[{\"text\": \"${OPTIONS[$i]}\", \"callback_data\": \"opt_$i\"}]"
done

BUTTONS+="]"

openclaw message send --target "telegram:CHAT_ID" --message "Choose:" --buttons "$BUTTONS"
```

### Paginated Results

```bash
# Page 1 of 3
openclaw message send \
  --target "telegram:CHAT_ID" \
  --message "Results (Page 1/3)" \
  --buttons '[[{"text": "◀️ Prev", "callback_data": "page_0"}, {"text": "Next ▶️", "callback_data": "page_2"}]]'
```

### Confirmation Chain

```bash
# Step 1: Ask
openclaw message send \
  --target "telegram:CHAT_ID" \
  --message "Delete all files?" \
  --buttons '[[{"text": "Yes", "callback_data": "delete_confirm"}, {"text": "No", "callback_data": "delete_cancel"}]]'

# Step 2 (if yes): Double-check
openclaw message send \
  --target "telegram:CHAT_ID" \
  --message "⚠️ This cannot be undone. Are you SURE?" \
  --buttons '[[{"text": "🗑️ DELETE", "callback_data": "delete_final", "style": "danger"}, {"text": "Cancel", "callback_data": "cancel"}]]'
```

## Shell Escaping Notes

When using buttons in shell scripts:

**Single quotes** (preferred):
```bash
--buttons '[[{"text": "Yes", "callback_data": "yes"}]]'
```

**Double quotes** (requires escaping):
```bash
--buttons "[[{\"text\": \"Yes\", \"callback_data\": \"yes\"}]]"
```

**Variable expansion:**
```bash
BTN_TEXT="Confirm"
BTN_CB="confirm"
--buttons "[[{\"text\": \"$BTN_TEXT\", \"callback_data\": \"$BTN_CB\"}]]"
```

## Integration with OpenClaw `message` Tool

While the CLI is recommended, the `message` tool can also be used:

```python
message(
    action="send",
    channel="telegram",
    target="telegram:CHAT_ID",
    message="Choose an option:",
    buttons=[[{"text": "Option 1", "callback_data": "opt1"}]]
)
```

**Caveat:** Different models may have inconsistent behavior with the `buttons` parameter. CLI via `exec` is more reliable.

## Testing Checklist

Before deploying button-based interactions:

- [ ] Validate JSON structure with `validate_buttons.py`
- [ ] Test on mobile device (buttons should fit comfortably)
- [ ] Verify callback_data values are unique
- [ ] Test full flow: send → click → edit
- [ ] Confirm buttons are removed after callback
- [ ] Check message text clarity without buttons

## Performance Notes

- **Message send**: ~100-300ms average
- **Message edit**: ~100-200ms average
- **Rate limits**: Telegram allows ~30 messages/second per bot
- **Button clicks**: No rate limit (handled server-side by Telegram)

For high-frequency interactions, consider batching operations or using delays between sends.
