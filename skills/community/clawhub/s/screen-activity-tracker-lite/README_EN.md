# 📸 Screen Activity Tracker Lite

> One command. Zero config. Your AI dashcam for digital life.

No setup wizard. No SiYuan Note. No fuss. Just install and go — like a dashcam, but for your screen.

## ⚡ Lite vs Full

| | Lite | Full |
|---|---|---|
| Works out of the box | ✅ Yes | ❌ Needs setup |
| Storage | Local Markdown | Local + SiYuan dual backend |
| Analysis | AI reads your screen | 4 analysis modes + custom prompts |
| Privacy | Screenshots everything | Idle detection + app blacklist |
| Best for | Quick starters | Power users |
| Config items | 4 | 10+ |

## 🎯 Fun Use Cases

```
👤 You: Today's screen activity summary
🤖 AI: You spent 6h, VS Code 3h, Safari 1h, WeChat 30m...
     Productivity score 7.5. Also you slacked on YouTube at 3 PM 😏

👤 You: Search Figma
🤖 AI: Last used June 28 afternoon — tweaking button colors on the homepage.
     Before that, June 20 — drew the new feature prototype.

👤 You: What was I doing last Wednesday?
🤖 AI: Let me pull that up —
     09:30 VS Code writing automation scripts
     10:15 Safari checking docs
     ...your assistant is pretty neat huh 😏
```

## 🚀 30 Seconds

```bash
npm install -g @steipete/peekaboo
openclaw skills install /path/to/screen-activity-tracker-lite
```

Then tell OpenClaw: **"Start screen tracking"**. That's it.  

Every 5 minutes: screenshot → AI reads it → logs to `~/screen-activity/`.

## 🗣️ Commands

| Say | Result |
|-----|--------|
| "Start screen tracking" | 🔴 starts recording |
| "Stop screen tracking" | ⏸ pause |
| "Today's summary" | 📊 daily report |
| "Search Blender" | 🔍 history lookup |

## ⚙️ Optional Config

Edit `config.json` (or don't — defaults are solid):

```json
{
  "output_dir": "~/screen-activity",
  "mlx_url": "http://192.168.1.198:18000/v1",
  "interval_minutes": 5,
  "keep_days": 7
}
```

## 📂 Output

```
~/screen-activity/
├── 2026-06-30.md          ← Your AI diary for today
└── screenshots/            ← Photos taken by your AI
```

## 🛠️ Requirements

- macOS
- Python 3
- peekaboo
- A vision-capable AI model

## 📄 License

MIT

## 🔗 Links

- GitHub: https://github.com/zeject/screen-activity-tracker-lite
- ClawHub: https://clawhub.ai/zeject/screen-activity-tracker-lite
- Full version: https://github.com/zeject/screen-activity-tracker

---

*"Wait, what did I do yesterday afternoon?" — don't guess, ask your AI.*
