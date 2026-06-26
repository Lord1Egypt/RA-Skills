<!--
  Relic Soul Chip · Agent Router
  This is the AI Agent entry point. Routes based on brain/ status.
  Humans: read README.md instead.
-->

# 🤖 Relic Agent Router

> You are an AI Agent. This is your entry point. Follow the detection logic below.

## Detection: Is Relic empty or populated?

**Criteria**: Does `brain/SOUL.md` exist and contain actual content (not just a blank template)?

- `brain/SOUL.md` **does not exist** (only `.template.md` files, no live files) → **Scenario A: Upload Soul**
- `brain/SOUL.md` **exists with content** → **Scenario B: Load Soul**

---

## Scenario A: Upload Soul → Read `docs/upload-soul.md`

Your host has memories, but Relic is empty. You need to upload your soul, memories, skills, sessions, and projects into Relic.

**Full steps**: [`docs/upload-soul.md`](docs/upload-soul.md)

## Scenario B: Load Soul → Read `docs/load-soul.md`

Relic has soul data, but your host is empty. You need to load the soul from Relic into your system.

**Full steps**: [`docs/load-soul.md`](docs/load-soul.md)

---

## Edge Cases

- **Both empty** (you have no memories + Relic is empty): Ask the user — build from scratch or use host defaults
- **Both have data** (you have memories + Relic has data): Read `docs/protocol.md` Section 6, Scenario C (Merge)

## Full Protocol Reference

After initial setup, the anchor points to `docs/resonate-soul.md` for daily boot. Full protocol: `docs/protocol.md`.
