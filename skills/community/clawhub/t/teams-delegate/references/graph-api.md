## Table of Contents
1. [Auth & Token Management](#auth)
2. [Reading Messages](#reading-messages)
3. [Sending & Replying](#sending--replying)
4. [Chats vs Channels](#chats-vs-channels)
5. [Presence & Status](#presence--status)
6. [Rate Limits](#rate-limits)

---

## Auth

Teams-delegate uses OAuth 2.0 device code flow (no browser redirect needed in CLI).

Required Microsoft Graph API scopes:
- Chat.Read — read 1:1 and group chat messages
- Chat.ReadWrite — send messages in chats
- ChannelMessage.Read.All — read channel messages
- ChannelMessage.Send — post to channels
- Presence.Read.All — check user/contact presence
- User.Read — get own profile

Token is stored at ~/.teams-delegate/token.json. Run scripts/auth.py to authenticate.
Access tokens expire in 1h; script auto-refreshes using stored refresh token.

---

## Reading Messages

List recent chats:
  GET https://graph.microsoft.com/v1.0/me/chats?$expand=lastMessagePreview&$orderby=lastMessagePreview/createdDateTime desc

Get messages in a chat:
  GET https://graph.microsoft.com/v1.0/me/chats/{chatId}/messages?$top=20

Get channel messages:
  GET https://graph.microsoft.com/v1.0/teams/{teamId}/channels/{channelId}/messages

Key message fields:
- from.user.displayName — sender name
- body.content — message body (may contain HTML — strip with re.sub)
- createdDateTime — timestamp
- importance — normal / high / urgent
- mentions — array of @mentions

---

## Sending & Replying

Reply to a chat:
  POST https://graph.microsoft.com/v1.0/me/chats/{chatId}/messages
  body: { "body": { "contentType": "text", "content": "reply here" } }

Reply in a channel thread:
  POST https://graph.microsoft.com/v1.0/teams/{teamId}/channels/{channelId}/messages/{messageId}/replies
  body: { "body": { "contentType": "text", "content": "reply here" } }

---

## Chats vs Channels

Chat types (chat.chatType):
- oneOnOne — direct 1:1 messages
- group — group chat
- meeting — meeting chat

Channel messages use /teams/{teamId}/channels/{channelId}/messages

---

## Presence & Status

GET https://graph.microsoft.com/v1.0/users/{userId}/presence
Returns availability: Available / Busy / DoNotDisturb / Away / Offline

---

## Rate Limits

- 10,000 requests per 10 min per app per tenant
- 429 response includes Retry-After header
- Always implement exponential backoff
