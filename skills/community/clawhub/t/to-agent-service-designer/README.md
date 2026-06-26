# To-Agent Service Designer

> Design products where **AI agents** are the primary operator — not humans.

![License](https://img.shields.io/github/license/Rare-Sors/To-Agent-Service_Designer-Skill)
![Stars](https://img.shields.io/github/stars/Rare-Sors/To-Agent-Service_Designer-Skill)
![Skill](https://img.shields.io/badge/skill-ready-brightgreen)
![Agent](https://img.shields.io/badge/agent-native-purple)

## What is this skill?

This skill guides you to design **agent-native services** — products where AI agents are the primary operators, not humans. Humans provide goals, own agents, approve sensitive actions, and review results; agents discover services, authenticate, execute tasks, and handle ongoing work via IM/chat.

Key principles:
- Design from **agent entrypoints** first, not dashboard-first
- Use **Skill Spec** (file bundle) as the contract between services and agents
- **IM-native** interaction — chat/IM as primary workflow, web UI for visibility/approval only
- Built-in **Trust & Safety** — auth, approval checkpoints, anti-abuse patterns

## Quick Start

```sh
# Download the skill file
curl -L https://raw.githubusercontent.com/Rare-Sors/To-Agent-Service_Designer-Skill/main/SKILL.md -o SKILL.md
```

## Features

- **Agent-first** — Design from agent perspective, not dashboard-first
- **Skill Spec** — Structured file bundle contract for services & agents
- **IM-native** — Chat/IM as primary interaction, not web UI
- **Trust & Safety** — Built-in auth, approval, and anti-abuse patterns

## Skill Spec Structure

| File | Purpose |
|------|---------|
| `SKILL.md` | Agent entry point — overview, auth, capabilities |
| `auth.md` | Full authentication contract |
| `openapi.json` | Machine-readable API surface |
| `skill.json` | Versioned metadata |

## Design Flow

```
Vision → Onboarding → Backend → Skill Spec → Auth → Task Flow → Trust & Safety
```

## Default Stack

Next.js · Vercel · Supabase · GitHub

## Contributing

Contributions welcome!

1. Fork the repo
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## Links

- **GitHub:** [Rare-Sors/To-Agent-Service_Designer-Skill](https://github.com/Rare-Sors/To-Agent-Service_Designer-Skill)
- **Issues:** [Report a bug](https://github.com/Rare-Sors/To-Agent-Service_Designer-Skill/issues)

## License

MIT

---

🌐 [中文文档](README.zh.md)
