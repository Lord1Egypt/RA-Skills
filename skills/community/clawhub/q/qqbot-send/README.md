# qqbot-send

An OpenClaw skill for sending files through QQBot end to end.

It combines two responsibilities into one skill:

1. stage local files into the QQBot media relay directory
2. send the staged path with QQ rich-media tagging

## What this skill does

When a user asks to send a local file to QQ, this skill decides the safest path automatically.

### Local absolute-path file
For files like desktop files, downloads, and workspace-external files, the skill:

1. runs `python scripts/stage_media.py <source_path>`
2. copies the file into:
   - `~/.openclaw/media/qqbot/`
3. uses the returned path with:
   - `<qqmedia>...</qqmedia>`

### Already staged file
If the file is already inside the QQBot relay directory, it sends it directly.

### URL media
If the source is an HTTP(S) URL, it can be sent directly with `<qqmedia>...</qqmedia>`.

## Repository layout

```text
qqbot-send/
├─ SKILL.md
├─ README.md
├─ LICENSE
├─ .gitignore
└─ scripts/
   └─ stage_media.py
```

## Script behavior

The bundled script:

- accepts a single file path argument
- checks that the file exists
- rejects files larger than 10 MB
- preserves the file extension
- copies the file instead of changing the original
- writes to `~/.openclaw/media/qqbot/`
- prints the staged absolute path

## Example

```bash
python scripts/stage_media.py "C:\Users\zyk\Desktop\resume.pdf"
```

Example output:

```text
C:\Users\zyk\.openclaw\media\qqbot\9b0f3b80-19b2-410b-adfc-438d6028b93a.pdf
```

Then send:

```xml
<qqmedia>C:\Users\zyk\.openclaw\media\qqbot\9b0f3b80-19b2-410b-adfc-438d6028b93a.pdf</qqmedia>
```

## Notes

- This skill replaces the old split flow where staging and sending were handled by separate skills
- The final delivery format still uses QQBot rich-media tagging
- Staged media output is not part of this repository
