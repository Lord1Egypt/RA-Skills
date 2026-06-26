# Trio Vision — Distribution Materials

## 1. OpenClaw Discord Post (#skills channel)

Copy-paste the below into the OpenClaw Discord #skills channel:

---

**trio-vision — Turn Any Camera Into a Smart Camera**

Just shipped a new skill that lets your OpenClaw agent watch any live camera feed and tell you what's happening — in plain English.

**What it does:**
- Ask your agent questions about any live stream ("is anyone at my front door?")
- Set up smart alerts: "tell me when a package is delivered" — get notified only when it actually happens
- Get periodic summaries of any stream ("summarize this construction site every 10 minutes")

Works with YouTube Live, Twitch, RTSP cameras, and HLS streams. Powered by Trio's Vision AI.

**Install:**
```
clawhub install trio-vision
```

**Quick test** (set `TRIO_API_KEY` first — free 100 credits at https://console.machinefi.com):
> "Is anyone visible on this stream? [paste any live stream URL]"

**Cost:** $0.01 per check, $0.02/min for continuous monitoring. Way cheaper than enterprise video AI.

**GitHub:** https://github.com/drandrewlaw/trio-openclaw-skill
**Trio Console:** https://console.machinefi.com

Feedback welcome!

---

## 2. Trio Docs — OpenClaw Integration Section

Add this to https://docs.machinefi.com under a new "OpenClaw Integration" page:

---

### OpenClaw Integration

Use Trio directly from your OpenClaw AI agent. Ask questions about live video streams, set up smart alerts, and get periodic summaries — all in natural language through your chat.

#### Install

```bash
clawhub install trio-vision
```

Or install from GitHub:

```bash
git clone https://github.com/drandrewlaw/trio-openclaw-skill.git ~/.openclaw/skills/trio-vision
```

#### Setup

1. Get your API key at [console.machinefi.com](https://console.machinefi.com) (100 free credits on signup)
2. Set the environment variable:
   ```bash
   export TRIO_API_KEY="your_key_here"
   ```
3. Restart your OpenClaw gateway

#### Usage Examples

| What You Say | What Happens | Cost |
|-------------|-------------|------|
| "Is anyone at my front door?" | Instant answer with VLM explanation | $0.01 |
| "Alert me when a package is delivered" | Continuous monitoring, notifies on match | $0.02/min |
| "Summarize this stream every 10 min" | Periodic narrative digests | $0.02/min |

#### Supported Streams

- YouTube Live
- Twitch
- RTSP/RTSPS cameras
- HLS streams

#### Links

- [ClawHub listing](https://clawhub.ai) — search "trio-vision"
- [GitHub source](https://github.com/drandrewlaw/trio-openclaw-skill)
- [Trio Console](https://console.machinefi.com)

---

## 3. awesome-openclaw-skills PR (Deferred)

**Status:** Not yet eligible. Their requirements:
- Skill must be in the official OpenClaw skills monorepo (`github.com/openclaw/skills/`)
- Must have "real community usage" — brand new skills are not accepted
- No crypto/blockchain skills (we're fine here)

**Action:** Revisit after the skill has ClawHub installs and community adoption. Consider also publishing to the official OpenClaw skills monorepo.

**Entry format when ready:**
```markdown
- [trio-vision](https://github.com/openclaw/skills/tree/main/skills/drandrewlaw/trio-vision/SKILL.md) - Smart camera alerts and live stream analysis via Vision AI.
```

Category: `smart-home-and-iot.md`
