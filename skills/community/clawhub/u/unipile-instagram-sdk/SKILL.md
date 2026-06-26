---
name: unipile-instagram-sdk
description: Instagram messaging and content via Unipile's official Node.js SDK. Send DMs, view profiles, list posts, create content, react and comment. Use for Instagram automation, reading/sending DMs, fetching profiles, getting posts, or interacting with content. Triggers: "instagram dm", "instagram message", "instagram profile", "instagram posts", "send instagram", "instagram api".
homepage: https://clawhub.ai/mohit21gojs/unipile-instagram-sdk
source: https://clawhub.ai/mohit21gojs/unipile-instagram-sdk
metadata:
  openclaw:
    requires:
      env:
        - UNIPILE_DSN
        - UNIPILE_ACCESS_TOKEN
      optionalEnv:
        - UNIPILE_PERMISSIONS
    primaryEnv: UNIPILE_ACCESS_TOKEN
    emoji: "📸"
---

# Unipile Instagram SDK

Instagram API via official [unipile-node-sdk](https://github.com/unipile/unipile-node-sdk) for messaging, profiles, posts, and interactions.

> 📸 Send DMs, view profiles, list posts, and interact with Instagram content — all through natural conversation with OpenClaw.

---

## ⚠️ Security & Privacy

**This skill requires credentials that grant API-level access to your connected Instagram accounts through Unipile.**

### What You're Granting

| Credential | Access Level | Risk |
|------------|--------------|------|
| `UNIPILE_DSN` | Unipile API endpoint | Identifies your Unipile instance |
| `UNIPILE_ACCESS_TOKEN` | Full API access to Unipile | Can read/write all connected social accounts |

### What This Means

- **Unipile gets your data** — Your Instagram messages, posts, and profile data flow through Unipile's servers
- **API-level control** — Anyone with these credentials can send DMs, create posts, and interact as you
- **Connected accounts** — If you connect Instagram via Unipile's dashboard, your Instagram session is stored on their servers

### Higher-Risk: Connecting Instagram Accounts

To connect a new Instagram account, you may need to provide:
- Instagram username and password
- 2FA verification codes

**This gives Unipile direct access to your Instagram account.** Only do this if you trust Unipile with your social media credentials.

### Recommendations

1. **Use a dedicated Instagram account** — Don't use your personal main account for automation
2. **Review Unipile's security** — Read their [privacy policy](https://unipile.com) and [terms of service](https://unipile.com)
3. **Audit the SDK** — The [unipile-node-sdk](https://github.com/unipile/unipile-node-sdk) is open source and auditable
4. **Use least privilege** — Set `UNIPILE_PERMISSIONS=read` unless you need write access
5. **Rotate tokens** — Regularly regenerate your access token from the Unipile dashboard
6. **Monitor activity** — Check your Unipile dashboard for unexpected API usage

### If You're Unsure

Don't install this skill. This is intended for users who:
- Already use Unipile for social media automation
- Understand the risks of third-party API access
- Have reviewed Unipile's security practices

---

## Installation

```bash
npx clawhub install unipile-instagram-sdk
```

Then install dependencies:

```bash
cd ~/.openclaw/workspace/skills/unipile-instagram-sdk
npm install
```

---

## Setup

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `UNIPILE_DSN` | ✅ | API endpoint (e.g., `https://api34.unipile.com:16473`) |
| `UNIPILE_ACCESS_TOKEN` | ✅ | Token from [dashboard.unipile.com](https://dashboard.unipile.com) |
| `UNIPILE_PERMISSIONS` | Optional | `read`, `write`, or `read,write` (default: `read,write`) |

### Get Credentials

1. Sign up at [dashboard.unipile.com](https://dashboard.unipile.com)
2. Get your DSN and generate an access token
3. Connect an Instagram account via dashboard or API

Or just ask OpenClaw:
> "Set up my Unipile Instagram credentials"

---

## Quick Reference

| What you want | What to say |
|---------------|-------------|
| See accounts | "Show my Instagram accounts" |
| Get a profile | "Get Instagram profile for @username" |
| View posts | "Show Instagram posts from @username" |
| Read DMs | "Show my Instagram messages with [name]" |
| Send DM | "Send '[message]' to [name] on Instagram" |
| Create post | "Post '[text]' to my Instagram" |
| Like/Comment | "Like that post" / "Comment '[text]' on that post" |

---

## 💬 How to Use

Once configured, just talk to OpenClaw naturally:

### Account & Profiles

> "Show me my connected Instagram accounts"

> "Get the Instagram profile for @nasa"

> "What's my own Instagram profile info?"

> "Who am I following on Instagram?"

### Posts & Content

> "Show me the last 5 posts from @nasa on Instagram"

> "Get details for Instagram post ID 123456"

> "Create an Instagram post saying 'Hello from OpenClaw!'"

> "Like that last post from @nasa"

> "Comment 'Amazing shot! 🔥' on the post"

### Direct Messages

> "List my recent Instagram DM chats"

> "Show me my last 20 messages with Yashpreet"

> "Send 'Hey, how are you?' to Yashpreet on Instagram"

> "Start a new Instagram conversation with @username saying 'Hi there!'"

> "Send this photo to Yashpreet on Instagram" *(with image attached)*

---

## 🛡️ Permission Modes

By default, the skill operates in read-only mode for safety.

**Read-only** (`UNIPILE_PERMISSIONS=read`):
- View profiles, posts, chats, messages
- No sending, posting, or interactions

**Read + Write** (`UNIPILE_PERMISSIONS=read,write`):
- Send messages
- Create posts
- React and comment

Just tell OpenClaw:
> "Set my Unipile permissions to read-only"

Or when you need write access:
> "Enable write permissions for Unipile so I can send messages"

---

## CLI Tool

For direct operations, use the included CLI:

```bash
# Set environment
export UNIPILE_DSN="https://api33.unipile.com:16376"
export UNIPILE_ACCESS_TOKEN="your_token"

# Read operations
node scripts/instagram.mjs accounts
node scripts/instagram.mjs my-profile <account_id>
node scripts/instagram.mjs profile <account_id> <username>
node scripts/instagram.mjs posts <account_id> <username> --limit=5
node scripts/instagram.mjs chats --account_id=<id>
node scripts/instagram.mjs messages <chat_id> --limit=10

# Write operations (require UNIPILE_PERMISSIONS=write)
node scripts/instagram.mjs send <chat_id> "Hello"
node scripts/instagram.mjs start-chat <account_id> "Hi" --to=<provider_id>
node scripts/instagram.mjs create-post <account_id> "Post text"
node scripts/instagram.mjs comment <account_id> <post_id> "Nice!"
node scripts/instagram.mjs react <account_id> <post_id> --type=like
```

---

## API Reference

### Client Initialization

```javascript
import { UnipileClient } from 'unipile-node-sdk';

const client = new UnipileClient(
  process.env.UNIPILE_DSN,
  process.env.UNIPILE_ACCESS_TOKEN
);
```

### Account Connection

```javascript
// Connect Instagram account
await client.account.connectInstagram({
  username: 'your_username',
  password: 'your_password',
});

// Hosted Auth (multi-user apps)
const link = await client.account.createHostedAuthLink({
  type: 'create',
  providers: ['INSTAGRAM'],
  success_redirect_url: 'https://yourapp.com/success',
});

// Handle 2FA
await client.account.solveCodeCheckpoint({
  account_id: accountId,
  provider: 'INSTAGRAM',
  code: '123456'
});
```

### Get Account ID

All operations require an account ID:

```javascript
const accounts = await client.account.getAll();
const instagram = accounts.items.find(a => a.type === 'INSTAGRAM');
const accountId = instagram.id;
```

### Read Operations

| Task | Method |
|------|--------|
| List accounts | `client.account.getAll()` |
| Get profile | `client.users.getProfile({ account_id, identifier })` |
| Get own profile | `client.users.getOwnProfile(account_id)` |
| Get followers | `client.users.getAllRelations({ account_id })` |
| List posts | `client.users.getAllPosts({ account_id, identifier })` |
| Get post | `client.users.getPost({ account_id, post_id })` |
| List chats | `client.messaging.getAllChats({ account_type: 'INSTAGRAM', account_id })` |
| Get messages | `client.messaging.getAllMessagesFromChat({ chat_id })` |

### Write Operations

| Task | Method |
|------|--------|
| Create post | `client.users.createPost({ account_id, text })` |
| React | `client.users.sendPostReaction({ account_id, post_id, reaction_type })` |
| Comment | `client.users.sendPostComment({ account_id, post_id, text })` |
| Send DM | `client.messaging.sendMessage({ chat_id, text })` |
| Start chat | `client.messaging.startNewChat({ account_id, attendees_ids, text })` |

### Attachments

```javascript
import { readFile } from 'fs/promises';

const fileBuffer = await readFile('./photo.jpg');
await client.messaging.sendMessage({
  chat_id: 'chat_id',
  text: 'Check this out!',
  attachments: [['photo.jpg', fileBuffer]],
});
```

---

## Error Handling

```javascript
import { UnsuccessfulRequestError } from 'unipile-node-sdk';

try {
  await client.users.getProfile({ account_id, identifier });
} catch (err) {
  if (err instanceof UnsuccessfulRequestError) {
    const { status, type } = err.body;
    // type: 'errors/invalid_credentials', 'errors/checkpoint_error', etc.
  }
}
```

### Common Errors

| Type | Meaning | Action |
|------|---------|--------|
| `errors/invalid_credentials` | Wrong password | Reconnect account |
| `errors/checkpoint_error` | 2FA required | Call `solveCodeCheckpoint` |
| `errors/disconnected_account` | Session expired | Reconnect |
| `errors/resource_not_found` | Invalid ID | Verify exists |

---

## Resources

- [Unipile SDK Repository](https://github.com/unipile/unipile-node-sdk)
- [Unipile Documentation](https://developer.unipile.com/docs/list-provider-features)
- [Unipile Dashboard](https://dashboard.unipile.com)
- [Unipile Privacy Policy](https://unipile.com)
- [ClawHub Skill Page](https://clawhub.ai/mohit21gojs/unipile-instagram-sdk)
