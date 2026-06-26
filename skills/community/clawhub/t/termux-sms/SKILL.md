---
name: termux-sms
description: Send SMS text messages directly from the user's Android device using the Termux API. Use this skill when the user asks you to text, SMS, or send a message to a phone number or contact and you are running on (or have SSH access to) their Android phone (e.g., Fold 7) with Termux installed. Do NOT use this for WhatsApp or web-based messaging.
metadata:
  {
    "openclaw":
      {
        "emoji": "💬",
        "requires": { "bins": ["termux-sms-send"] },
        "install":
          [
            {
              "id": "apt",
              "kind": "apt",
              "package": "termux-api",
              "bins": ["termux-sms-send"],
              "label": "Install Termux API (apt)",
            },
          ],
      },
  }
---

# Termux SMS

Use `termux-sms-send` when the user explicitly asks you to send an SMS or text message to a contact or phone number.
This skill requires that OpenClaw is running within Termux on an Android device, or that you are executing commands on an Android node via SSH/remote execution where the `termux-api` package is installed.

## Safety & Boundaries
- Require an explicit recipient phone number and message text.
- Confirm the recipient and the exact message text with the user before sending.
- If the user provides a name instead of a number, ask them for the number first (unless you have a contact list reference available).
- Do not spam or send bulk messages.

## Usage

To send a text message, use the `termux-sms-send` command. 

```bash
termux-sms-send -n <phone_number> "<message_text>"
```

### Examples

Send a simple text:
```bash
termux-sms-send -n "+14155551212" "Hey, I am running 5 minutes late."
```

Send a multi-line text:
```bash
termux-sms-send -n "5558675309" "Grocery list:
- Milk
- Eggs
- Bread"
```

Send to multiple numbers (comma-separated):
```bash
termux-sms-send -n "+14155551212,5558675309" "Meeting is moved to 3 PM."
```

## Troubleshooting
- If the command fails with a permission error, remind the user that they must install the **Termux:API app** from F-Droid (or Google Play) and grant it SMS permissions on their Android device.
- Ensure the `termux-api` package is installed inside the Termux environment (`pkg install termux-api`).