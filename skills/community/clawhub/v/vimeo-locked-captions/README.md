# vimeo-locked-captions

A Claude Code skill for extracting auto-generated captions/transcripts from
**privacy-locked (domain-restricted) Vimeo embeds** — the kind of video where
the player itself refuses to play because of the Referer/domain check, but you
just want the transcript for analysis.

## What it solves

VC blogs, conference pages, paywalled articles often embed a Vimeo video like:

```html
<iframe src="https://player.vimeo.com/video/1195836424?h=a0154d0f4b">
```

When you visit `player.vimeo.com/video/...` directly, Vimeo says:

> Sorry, this video cannot be played here due to privacy settings.
> 由于隐私设置，该视频无法在此处播放

`yt-dlp` and browser automation hit the same wall.

But you don't need the **video stream** — you just need the **transcript**.
And it turns out Vimeo's player HTML still leaks a signed
`captions.vimeo.com/captions/{id}.vtt?expires=...&sig=...` URL when fetched
with the right `Referer` header. The captions URL itself works without
auth — Vimeo only enforces playback restrictions on the video stream, not on
the player's HTML config payload.

Three `curl` commands and you have the transcript.

## When to invoke

The skill triggers when:

1. A page embeds a Vimeo video and publishes no transcript.
2. Direct visit to `player.vimeo.com` fails with the privacy error.
3. You want a transcript-driven analysis (interview, panel, fireside chat,
   conference talk).

Real example that motivated this skill: the May 2026 Coatue × Boris Cherny
"Interview with Claude Code Creator" video — locked to `coatue.com` Referer,
no transcript on page, but the auto-generated VTT was one curl away.

## Install

Copy `SKILL.md` into your Claude Code skills directory:

```bash
mkdir -p ~/.claude/skills/vimeo-locked-captions
cp SKILL.md ~/.claude/skills/vimeo-locked-captions/SKILL.md
```

Or via [ClawHub](https://docs.openclaw.ai/clawhub/):

```bash
clawhub install vimeo-locked-captions
```

Then register it in `~/.claude/CLAUDE.md`:

```markdown
## vimeo-locked-captions
- **vimeo-locked-captions** (`~/.claude/skills/vimeo-locked-captions/SKILL.md`) —
  Extract auto-generated captions from privacy-locked Vimeo embeds when the
  player refuses to play. curl with Referer → grep text_tracks JSON → download
  signed VTT.
When the user says "the Vimeo player won't play", "extract Vimeo transcript",
"get captions from a locked Vimeo video", or supplies a Vimeo embed URL with
no transcript on the host page, invoke the Skill tool with
`skill: "vimeo-locked-captions"` before doing anything else.
```

## How it works (quick version)

Replace `{ID}`, `{HASH}`, and `{HOST}` from the embed iframe.

```bash
# 1. Fetch the player HTML and extract the captions URL
curl -s -H 'Referer: https://{HOST}/' \
  'https://player.vimeo.com/video/{ID}?h={HASH}' \
  | grep -oE '"text_tracks":\[[^]]*\]'

# 2. Download the VTT (the signed URL works without Referer)
curl -s 'https://captions.vimeo.com/captions/{CAP_ID}.vtt?expires=...&sig=...' \
  -o /tmp/transcript.vtt

# 3. Strip cues/timestamps to get plain text
awk '/-->/{next} /^[0-9]+$/{next} /^WEBVTT/{next} /^$/{next} {print}' \
  /tmp/transcript.vtt > /tmp/transcript.txt
```

Full reference (caveats, fallbacks, multilingual subtitle tracks) lives in
[SKILL.md](SKILL.md).

## Caveats

- Captions are auto-generated (`provenance: ai_generated`). Proper nouns and
  brand-name acronyms are often misheard ("Computer Use" → "CP"). Re-read with
  that bias.
- The signed URL has an `expires` parameter; if it 403s, re-fetch step 1.
- If the video has no captions enabled, `text_tracks` returns `[]`. Falling
  back to `yt-dlp --write-auto-subs` won't help (same Referer block); use
  Whisper on a screen recording instead.
- Vimeo could close this in the future. The fallback is to drive the embed
  inside Playwright with the correct Referer and read `player.getTextTracks()`
  via the [Vimeo Player SDK](https://developer.vimeo.com/player/sdk/reference#texttrack).

## License

MIT — see [LICENSE](LICENSE).

## Author

Created by [@heavenchenggong](https://github.com/heavenchenggong) while analyzing
a Coatue interview where the host page only published the embed and no
transcript. Lifted into a reusable skill so the next time it happens it's a
one-command operation.
