# Proactive send and file delivery

## Known users

QQBot plugins often track recently seen users in a local known-users file. A common path is:

- `~/.openclaw/qqbot/data/known-users.json`

Use `accountId` to distinguish which bot account the user belongs to.

## Sending a file through normal outbound flow

If the plugin supports media tags, a common pattern is:

```text
Here is your file <qqfile>/path/to/file.md</qqfile>
```

This lets the plugin upload the file through the QQ file message API.

## Notes

- Plain proactive send endpoints usually handle text only
- File delivery is often easiest through the normal outbound parser with `<qqfile>`
- If you need to reply into a recent QQ conversation, you may need the latest inbound `message_id`
