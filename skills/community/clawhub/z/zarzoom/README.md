# ZARZOOM for OpenClaw 🚀

> Post to Facebook, LinkedIn, X, Instagram, TikTok, YouTube, Threads,
> Bluesky, Pinterest, Reddit, and Google Business — through your
> OpenClaw assistant — with compliance review baked in.

## What is this?

[ZARZOOM](https://zarzoom.com) is a multi-platform social-media
posting service. You write content once; ZARZOOM publishes it to
every social account you've connected. Every submission goes through
a compliance review (a human admin checks it) before it actually
posts — that gate is by design and matters for accounts at risk of
platform takedowns.

This Skill makes ZARZOOM available inside your OpenClaw assistant.
Once installed, you can say things like:

> "Submit a short article about my morning coffee with this picture,
> post to Facebook and LinkedIn."

> "What's the status of my last submission?"

> "How did my posts do this month?"

> "Which platforms am I connected to and what's their character limit?"

…and OpenClaw will handle the API calls for you.

## What it can do

| Capability | Example prompt |
|---|---|
| Submit an article (with images) | *"Post this article about climate tech, attach the chart, hit LinkedIn and X."* |
| Submit a short | *"Write a short about my new coffee routine, post to Threads and Bluesky."* |
| Submit a video | *"Upload this 30-second reel with the caption 'morning routine'."* |
| Check submission status | *"Is my last submission approved yet?"* |
| List pending submissions | *"Show me everything that's in compliance review."* |
| List approved content | *"What articles have I posted in the last 7 days?"* |
| Read analytics | *"How are my posts doing this month? What's my top platform?"* |
| Check per-post status | *"Did my Monday article actually land on LinkedIn?"* |
| Discover platforms | *"Which platforms am I connected to and what fits where?"* |

## Installation

```bash
openclaw skills install zarzoom
```

Then edit `~/.openclaw/openclaw.json` to add your API key:

```json5
{
  skills: {
    entries: {
      "zarzoom": {
        enabled: true,
        apiKey: {
          source: "env",
          provider: "default",
          id: "ZARZOOM_API_KEY"
        },
        env: {
          ZARZOOM_API_KEY: "zarz_live_REPLACE_WITH_YOUR_KEY"
        }
      }
    }
  }
}
```

Restart OpenClaw (or wait for hot-reload). The Skill will activate
automatically when you mention ZARZOOM-relevant intent.

## Getting an API key

1. Sign up at [zarzoom.com](https://zarzoom.com) (free trial available).
2. Go to **Dashboard → API & Integrations → New developer key**:
   [zarzoom.com/dashboard/api-keys](https://zarzoom.com/dashboard/api-keys)
3. Pick the scopes you want (minimum: `api:write:content` for submissions;
   add `api:read:status`, `api:read:content`, `api:read:analytics` for the
   full Skill toolkit).
4. Copy the `zarz_live_*` key — it's shown only once.
5. Paste it into your `openclaw.json` (above).

## What happens after I submit?

Submissions don't post immediately. The flow is:

1. **You ask OpenClaw to submit** → Skill calls ZARZOOM's API.
2. **Compliance review** → a ZARZOOM admin checks the content (usually
   within hours during business days).
3. **Approved** → ZARZOOM's engine posts to every connected social
   platform that fits the content. You can see live URLs by asking
   OpenClaw for the submission's status.
4. **Rejected** → you get a category + reason. Revise and resubmit
   from the dashboard or via OpenClaw.

You can track all of this at
[zarzoom.com/dashboard/my-submissions](https://zarzoom.com/dashboard/my-submissions).

## Platforms supported (per content type)

| Platform | Article | Short | Video |
|---|---|---|---|
| Facebook | ✓ | ✓ | ✓ |
| LinkedIn | ✓ | ✓ | ✓ |
| X (Twitter) | — | ✓ | ✓ |
| Instagram | ✓ | ✓ | ✓ |
| TikTok | — | — | ✓ |
| YouTube | — | — | ✓ |
| Threads | — | ✓ | ✓ |
| Bluesky | — | ✓ | ✓ |
| Pinterest | — | ✓ (image required) | ✓ |
| Reddit | ✓ | ✓ | ✓ |
| Google Business | ✓ | ✓ | ✓ |

Per-platform text-length and video-duration limits are enforced
automatically — if your content doesn't fit on a platform, the Skill
will tell you (e.g. *"Your 2000-character article is too long for X
— I'll skip X and post to the others."*).

## Troubleshooting

**"Your ZARZOOM API key isn't working"** → your key is missing,
mistyped, or revoked. Create a new one at
[/dashboard/api-keys](https://zarzoom.com/dashboard/api-keys) and
update `openclaw.json`.

**"Rate limit exceeded"** → reads are capped at 60/min, writes at
40/day per workspace. Wait or upgrade your plan.

**"Image upload didn't complete"** → the presigned PUT to ZARZOOM's
storage failed. Try again with a fresh image attach.

**Anything else** → check
[/dashboard/api-keys/docs](https://zarzoom.com/dashboard/api-keys/docs)
for the full API reference, or use ZARZOOM support:
[zarzoom.com/contact](https://zarzoom.com/contact).

## Privacy & security

- The Skill speaks **only** to `https://zarzoom.com/api/v1/*` over HTTPS.
- Your API key never leaves your machine except in the
  `Authorization: Bearer ...` header on requests to ZARZOOM.
- Content bytes (images, videos) are uploaded directly to ZARZOOM's
  R2 storage via presigned URLs — not through ClawHub or any
  intermediary.
- Compliance review is performed by ZARZOOM staff, not by an AI.

## License

[MIT-0](LICENSE) — no rights reserved, no attribution required, fork
and rebrand freely.

## Contributing

Issues and pull requests welcome at the source repo:
[github.com/NeilDarrenLtd/ZARZOOM-WEBSITE/tree/main/openclaw-skill](https://github.com/NeilDarrenLtd/ZARZOOM-WEBSITE/tree/main/openclaw-skill).

Bug reports about the ZARZOOM API itself go to
[zarzoom.com/contact](https://zarzoom.com/contact).

---

🦞 Built for the OpenClaw ecosystem. Have fun.
