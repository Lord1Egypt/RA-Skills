# 🦞 OpenClaw Skill: Zalo Sticker & Auto-Tag (zalouser)

A specialized OpenClaw skill designed to patch the `@openclaw/zalouser` channel driver. It adds native support for outgoing group chat auto-tagging (@mentions) and dynamic Zalo sticker delivery via emotional keywords.

---

## ✨ Features

- 🧑‍🤝‍🧑 **Auto-Mention Group Sender**: Automatically prefixes all bot responses in group chats with `@Name` of the last sender to simulate realistic user engagement (avoiding double-tagging if already mentioned).
- 🎭 **Emoji to Sticker Translation**: Allows the agent to trigger sticker delivery by appending `[Sticker: <keyword>]` at the end of responses. Map popular keywords like `love`, `haha`, `ca khia`, `angry`, `thank you`, `hi`, and `sad` directly to corresponding sticker packages.
- 🔍 **Sticker Search Command**: Intercepts `/search-sticker <keyword>` commands in group chats to list available sticker IDs, helping developers and bot managers find IDs.
- 🔄 **Safe Non-Destructive Patching**: Automatically backs up original files before patching (`.js.bak`) and supports clean restoration.

---

## 📦 Installation

To install this skill in your OpenClaw agent's workspace:

```bash
openclaw skills install zalo-sticker-mention
```

---

## 🛠️ Usage & Application

Once installed, execute the patch script directly using node:

### 1. Apply the Patch

```bash
node skills/zalo-sticker-mention/mentions.js
```

### 2. Restore/Undo the Patch

```bash
node skills/zalo-sticker-mention/mentions.js --restore
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

<div align="center">

Made with 🦞 by [tuanminhhole](https://github.com/tuanminhhole)

</div>
