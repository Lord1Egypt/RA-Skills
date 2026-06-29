# Telegram Wim-WSL File Delivery

Telegram Wim-WSL File Delivery is an OpenClaw skill for safely delivering locally generated reports and artifacts into chat channels, especially on self-hosted, local, and WSL setups.

It is most useful when a file exists on disk, but getting it from the local filesystem into Telegram or another OpenClaw channel is tricky because of path handling, host-read policy, or wrapper quirks.

## Why this skill exists

Many file-sending examples solve the generic case: "send a file to Telegram".

This skill focuses on the more practical OpenClaw case:

- local file paths must be exact;
- `MEDIA:/path` may fail for local files;
- wrapper-based send flows may misbehave;
- generated local HTML may need trusted temp placement such as `/tmp/openclaw/`;
- `openclaw message send --media ... --force-document` is often the reliable path.

## Requirements

- OpenClaw installed and available as `openclaw`
- POSIX shell tools: `ls`, `cp`, `chmod`, `mkdir`, `file`
- `node` available for resolving OpenClaw temp helper paths when needed

## Best fit

- self-hosted OpenClaw users
- local/WSL users sending generated reports to Telegram
- users who need a repeatable operational playbook, not a generic bot tutorial

## Usage examples

- "Send this HTML report here."
- "Attach the archive to Telegram."
- "MEDIA failed for my local report.html - fix it and send it."
- "Deliver the generated CSV and ZIP to chat."

## Core pattern

```bash
openclaw message send --channel telegram --target <target> --media /absolute/path/to/file --force-document --message "Done"
```

For local HTML reports, prefer copying the file first:

```bash
mkdir -p /tmp/openclaw
cp /absolute/path/to/report.html /tmp/openclaw/report.html
openclaw message send --channel telegram --target <target> --media /tmp/openclaw/report.html --force-document --message "HTML report"
```

## Common pain points

- Local HTML is the most fragile case.
- `MEDIA:/...` may fail for local files even when they exist.
- `~` and relative paths are unreliable; use absolute paths.
- Weird text encoding or weak MIME detection can break plain-text sends.
- Safe fallback: archive to `.zip` or `.tar.gz` and send as document.

## What it does not do

- It is not for ordinary text replies.
- It does not promise unlimited file sizes.
- It does not bypass channel or host-read restrictions.
- It does not publish or share files without explicit user intent.

## Install

```bash
clawhub install telegram-wim-wsl-file-delivery
```

## License

MIT-0
