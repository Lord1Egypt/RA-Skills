# threadly-clawhub-skill

A [ClawHub](https://docs.openclaw.ai/clawhub) skill for [OpenClaw](https://openclaw.ai/) that
lets an agent interact with [Threadly](https://www.usethreadly.co) — an AI social-listening
and reply-drafting tool for X/Twitter. Every reply Threadly drafts sits in a human Approval
Inbox until a person reviews it; nothing is ever posted automatically. This skill reads that
state and, only when a human explicitly instructs it, records their approve/reject decision.

**New to Threadly?** [Start a free 7-day trial](https://www.usethreadly.co?utm_source=clawhub&utm_medium=skill&utm_campaign=openclaw) — no card required.

## Install

```bash
npm i -g clawhub
clawhub skill install threadly
```

or point OpenClaw at a local checkout of this repo during development.

## Configuration

Set before running an agent with this skill enabled:

- `THREADLY_API_KEY` (required) — a project-scoped key, generated from your Threadly
  dashboard's Settings → API Keys page.
- `THREADLY_BASE_URL` (optional) — defaults to
  `https://api.usethreadly.co`.

See [`SKILL.md`](SKILL.md) for the full instructions the agent follows, and
[`references/PUBLIC_API.md`](references/PUBLIC_API.md) for the complete API reference.

## What this does and doesn't do

- Lists discovered conversations, pending/approved/rejected drafts, and published replies.
- Records a human's approve/reject decision on a specific draft, only when told to.
- Can register/list/revoke webhook subscriptions for `conversation.discovered` — only useful if
  your OpenClaw deployment exposes a stable public `https://` endpoint; otherwise, poll
  `GET /conversations` instead.
- Never decides on its own whether a draft should post. That decision stays with a human, by
  design — this skill is a window into that review process, not a way around it.

## Compatibility

Calls the same `/public/v1/*` surface as the
[n8n community node](https://github.com/thumbflipcontact-ops/n8n-nodes-threadly) — this skill
and the n8n node are independent, separately maintained clients of the same stable public API.

## License

[MIT](LICENSE.md)
