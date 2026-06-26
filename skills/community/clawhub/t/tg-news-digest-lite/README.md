# tg-news-digest-lite

> 🤖 Monitor public Telegram channels, auto-summarize news, get digests — zero setup.

✅ No Telegram API keys • ✅ No authentication • ✅ Works out of the box

## 🚀 Install in 30 seconds
```bash
openclaw skills install tg-news-digest-lite
```

## ⚙️ Configure (only channels!)
Edit `~/.openclaw/skills/tg-news-digest-lite/config.yaml`:
```yaml
monitoring:
  channels:
    - "durov"
    - "telegram"
    - "https://t.me/s/roem"
```

## ▶️ Run
```bash
# Manual check
openclaw skills exec tg-news-digest-lite/run_digest_cycle

# Add channels dynamically
openclaw skills exec tg-news-digest-lite/configure_channels --add "coindesk"
```

## 📚 Full documentation
See [SKILL.md](./SKILL.md) for:
- Architecture deep dive
- Real-world examples
- Troubleshooting guide
- Security considerations
- Performance tuning

---

*Built for the OpenClaw community. MIT License.*