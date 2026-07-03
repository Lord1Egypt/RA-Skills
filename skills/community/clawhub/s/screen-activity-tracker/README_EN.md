# 🦞 Screen Activity Tracker

> Your digital timeline, auto-logged by AI. Track your screen life like Git tracks your code.

What were you doing last Wednesday at 3 PM? You probably don't remember. But this tool does — it silently screenshots, AI-analyzes, and archives every moment, letting you time-travel back to any 5-minute interval of your digital past.

## 💡 What It Does

| You ask | It answers |
|---------|-----------|
| "How was my day?" | "3h coding, 1h meetings, 30m Twitter scrolling, 20m YouTube..." |
| "When did I last use Figma?" | "June 25, 2:30 PM — you were tweaking button colors on the homepage mockup" |
| "When did I start this project?" | "June 22, 9:30 AM — first VS Code session with screen-activity.sh" |
| "My productivity this week?" | "28 productive hours. 15% Blender, 12% Safari. Score: 7.5/10" |
| "Find a screenshot from yesterday" | Opens the exact screenshot file from that moment |
| "How much time in VS Code?" | "15 hours in the last 7 days. 3.5h peak on Thursday" |

## 🎮 Track Yourself Like an RPG Achievement System

- 🏆 **Auto Check-in**: Screenshot every 5 minutes, like a fitness tracker for your digital life
- 🧠 **AI Vision**: Multimodal model reads your screen and describes what you're doing
- 📊 **Daily Recap**: End-of-day report — where did your time go today?
- 🔍 **Time Travel**: Search "Figma" to find that design moment from three weeks ago
- 🔒 **Privacy First**: Banking/2FA apps skipped. Idle detection pauses when you're away
- 🗑️ **Auto Cleanup**: Screenshots auto-delete after 7 days

## 🚀 3 Minutes to Start

```bash
# 1. Install screenshot tool
npm install -g @steipete/peekaboo

# 2. Install the skill
openclaw skills install /path/to/screen-activity-tracker

# 3. Configure (interactive wizard, just press Enter for defaults)
python3 setup.py

# 4. Tell OpenClaw
Start screen tracking
```

Done. Every 5 minutes, your screen is captured and analyzed automatically.

## 🗣️ Voice Commands

| Say to OpenClaw | It does |
|----------------|---------|
| "Start screen tracking" | Creates a cron job |
| "Stop screen tracking" | Pauses tracking |
| "Today's screen activity summary" | Time stats + app breakdown |
| "What did I do this week?" | Weekly productivity report |
| "Search Blender" | Find all Blender usage history |
| "When did I last open Xcode?" | Exact timestamp lookup |

## 🔧 Deep Dive

### Analysis Modes

| Mode | For | Example Output |
|------|-----|---------------|
| `simple` | Everyone | `[Safari] Browsing OpenClaw docs` |
| `category` | Organizers | `[work] Coding in VS Code / [fun] Watching YouTube` |
| `productivity` | Optimization nerds | `[7/10] VS Code - writing unit tests` |
| `custom` | Hackers | Write your own prompt, analyze anything |

### Dual Backend

- **Local**: Pure Markdown files. Zero cloud. Everything on your machine.
- **SiYuan Note**: Daily auto-created docs with embedded clickable screenshots.

### Privacy Blacklist

```
"Banking app / password manager / 2FA" → automatically not screenshot
(timeline still logs "using financial app" at that time)
```

## 📂 Output Structure

```
~/screen-activity/
├── 2026-06-30.md              ← Today's digital diary
├── 2026-06-29.md
└── screenshots/
    └── 2026-06-30/
        ├── 09:30:00.png       ← Time snapshots by your AI
        ├── 09:35:00.png
        └── ...
```

Each daily log is a timeline with embedded screenshot links:

```markdown
## 2026-06-30 Screen Activity

- **09:30** VS Code editing screen-activity.sh
  ![](screenshots/2026-06-30/093000.png)
- **09:35** Safari reading GitHub Issues
  ![](screenshots/2026-06-30/093500.png)
```

## 🛠️ Requirements

- macOS + Screen Recording permission
- Python 3.x
- peekaboo CLI
- An OpenAI-compatible VL model (Qwen3.5-9B, GPT-4V, etc.)

## ❓ FAQ

<details>
<summary>Screenshots failing?</summary>
System Settings → Privacy & Security → Screen Recording → enable your terminal app.
</details>

<details>
<summary>AI analysis failing?</summary>
Check your MLX server: `curl http://your-server:18000/v1/models`
</details>

<details>
<summary>Change to 10-minute interval?</summary>
Edit `interval_minutes` in `config.json`, or just ask the AI: "Change screenshot interval to 10 minutes."
</details>

<details>
<summary>Is my data safe?</summary>
Everything stays in `~/screen-activity/` — local files, no cloud, no telemetry.
</details>

## 📄 License

MIT

## 🔗 Links

- GitHub: https://github.com/zeject/screen-activity-tracker
- ClawHub: https://clawhub.ai/zeject/screen-activity-tracker
- Lite version: https://github.com/zeject/screen-activity-tracker-lite

---

*"Where did the time go?" — let AI keep score for you.*
