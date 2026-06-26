# TikTok Selectors (subject to change)

## Inbox
https://www.tiktok.com/messages

## Elements

Search input:
input[placeholder="Search"]

Chat item:
div[data-e2e="chat-item"]

Message box:
div[contenteditable="true"]

Send trigger:
Keyboard Enter

## Notes
- Prefer data-e2e attributes
- Avoid brittle XPath
- Always use wait_for_selector
