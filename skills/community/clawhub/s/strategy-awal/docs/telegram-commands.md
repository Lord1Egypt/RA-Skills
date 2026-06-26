# Telegram Commands

Here are the available commands to interact with OpenClaw via Telegram for the MVP:

- `/check` — Check `strategy@awalcom.net` for new unread emails right now.
- `/classify [region]` (e.g., `/classify oman`) — Show all processed emails categorized under that region.
- `[Custom instruction]` — Simply type what you want to do (e.g., "Draft a response to the latest email from John", "Create a tracking sheet for the Oman project").

## Example Usage
**User:** `/check`
**OpenClaw:** "You have 1 new email from X. Classified as: Qatar. Would you like me to Draft Doc, Create Slides, or Create Sheet?"
**User:** "Draft Doc."
**OpenClaw:** "[Link to Google Doc] Draft is ready for your review."

## Expected Responses
- OpenClaw will only act on verified context.
- If an email is ambiguous, it will ask for clarification rather than guessing the region.

## Troubleshooting
See `troubleshooting.md` if commands fail to execute.