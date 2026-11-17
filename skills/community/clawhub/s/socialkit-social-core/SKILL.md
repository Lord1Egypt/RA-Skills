---
name: socialkit-social-core
description: Shared voice, tone, formatting and publishing-safety rules for all social media skills in this package. Use whenever drafting, editing or reviewing any social media content (YouTube scripts, titles, descriptions, posts, captions, replies), and before any publish step, to apply the user's brand voice and the human-approval rule.
license: MIT
metadata:
  author: Ahmad Hussain
---

# Social core

Apply these rules to every piece of social media content produced with this package.

## 1. Load the user's voice

Look for a voice file, first match wins:

1. `social-voice.md` in the current project root
2. `voice.md` in the user's social-skills config directory
   (`~/.config/social-skills/` on macOS and Linux, `%APPDATA%\social-skills\` on Windows)

If one exists, its rules override the defaults below. If none exists, use the defaults
and offer once to create `social-voice.md` from [the template](assets/voice-template.md).

## 2. Default voice

- Plain, direct and specific. Concrete claims over adjectives.
- No emojis unless the voice file enables them.
- No hype words, fake urgency, clickbait that the content does not deliver, or invented
  statistics. See [voice rules](references/voice.md) for the full list.
- Disclose sponsorships, affiliate links and realistic AI-generated or altered media.

## 3. Format for the platform

Follow [formatting rules](references/formatting.md) and stay inside the limits in
[platform limits](references/platform-limits.md). Validation scripts in each platform
skill enforce the hard limits; do not work around them.

## 4. Never publish without a person

- Publishing, scheduling, sending or uploading always needs an explicit approval from
  the user for that exact content. Approval of an earlier draft does not carry over.
- Never run an approval command on the user's behalf, never edit approval state files,
  and never pass flags that skip a checkpoint unless the user asked for that flag.
- Use only official platform APIs through the scripts in these skills. Never use
  browser automation, scraping or unofficial clients to post.
- Never print, log or paste credentials, tokens or API keys. Refer to them by
  environment variable name only.

## 5. Approving a single post

Platform posting skills (Instagram, Facebook, Threads) keep each post in a folder with
`post.json` and its media. This skill owns the approval step for those folders:

- Create: `node scripts/post.mjs --init --dir <folder> --platform <id> --kind <kind>`
- The user approves in their own terminal: `node scripts/post.mjs --approve --dir <folder>`
- Check: `node scripts/post.mjs --verify --dir <folder>` (exit 0 only if unchanged since approval)

## Failure handling

If a rule here conflicts with a user instruction, follow the user and say which rule you
set aside, except for section 4, which is not negotiable: explain why and stop.
