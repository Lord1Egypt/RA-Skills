# skill-zooop

Official agent skill bundle for [ZOOOP](https://zooop.ai) — an AI-native
creative platform that generates images, videos, and audio through the
most comprehensive top-tier AI models.

Give an AI agent (Claude Code, Codex, Cursor, custom GPTs, …) this skill
and it can call ZOOOP on your behalf to create AI content. Tasks are
charged against your existing ZOOOP credit balance.

## Install

### Any agent (recommended)

```bash
npx skills add zooopai/skill-zooop
```

### Claude Code

```bash
git clone https://github.com/zooopai/skill-zooop.git ~/.claude/skills/zooop
```

(This repo is a plain skill bundle, not a plugin marketplace, so
`claude plugin install` has nothing to resolve.) The bundle lands at
`~/.claude/skills/zooop/`. Claude will auto-load it
whenever the conversation mentions ZOOOP or image / video / audio
generation.

### Manual (any agent)

```bash
git clone https://github.com/zooopai/skill-zooop
```

Or, to read just the integration guide without cloning, fetch
<https://raw.githubusercontent.com/zooopai/skill-zooop/main/SKILL.md>.

## Setup

1. Sign in at <https://zooop.ai>.
2. Go to **Profile → API Keys**, click **Create key**, pick the project
   you want all tasks and uploads to land in, and copy the
   `zpk_live_…` token (shown once).
3. Expose it to your agent:

   ```bash
   export ZOOOP_API_KEY=zpk_live_...
   ```

The agent does the rest — it reads `SKILL.md`, discovers models, submits
tasks, polls until completion, and prints the output URL.

## What ZOOOP can generate

| Type  | What                                              |
| ----- | ------------------------------------------------- |
| Image | Text-to-image, image editing with mask            |
| Video | Text-to-video, image-to-video, first/last frame, lip-sync, extend, edit |
| Audio | Text-to-speech, voice cloning, sound effects, music |

For the full model list, run:

```bash
curl -fsS "https://api.zooop.ai/v1/models?type=image&subtype=default" \
  -H "Authorization: Bearer $ZOOOP_API_KEY"
```

## Docs

- **Agent integration guide** — [SKILL.md](./SKILL.md)
- **REST API reference** — [references/api-docs.md](./references/api-docs.md)
- **llms.txt discovery** — <https://api.zooop.ai/llms.txt>
- **Single-fetch bundle** — <https://api.zooop.ai/llms-full.txt>

## Issues & contributions

Found a bug in the SKILL or want to add an example? Open an issue or PR.
This bundle is mirrored from [zooop.ai](https://zooop.ai)'s internal
source, so doc fixes here flow back upstream.

## License

[MIT](./LICENSE) — use freely, no warranty.
