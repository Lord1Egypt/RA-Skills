# Security Notes

This skill automates a public-visible workflow (podcast publishing), so its behavior is
documented explicitly here and in `SKILL.md#能力与风险声明`.

## What it runs

- `opencli youtube video` (read-only metadata)
- `opencli notebooklm create|add-source|source-guide|open|download-audio`
- `opencli xiaoyuzhou upload`
- `ffmpeg` / `ffprobe`
- `openclaw system event` (post-run notification to the originating session)

No shell is spawned from model output; command lines are built in `scripts/worker.py`
from a fixed vocabulary.

## Bundled opencli adapters

`adapters/` ships three JS adapters that opencli's baseline does not include:
`notebooklm/download-audio`, `xiaoyuzhou/upload`, `xiaoyuzhou/upload-status`.
`scripts/install-adapters.sh --install` copies them into `~/.opencli/clis/` (backing up
existing files) — that is an explicit, user-invoked command, and it is the only place this
skill writes outside its own data root. They run inside the opencli process, talk only to
`notebook.google.com` / `lh3.googleusercontent.com` / `podcaster-api.xiaoyuzhoufm.com`,
carry no credentials, and no longer embed any podcast id (it must be provided by the caller).

## Network

- `youtube.com` / `youtu.be` — metadata
- `notebook.google.com` — generation
- `lh3.googleusercontent.com` — audio download (may require a proxy; the worker honors
  `YT2PODCAST_PROXY` / `HTTPS_PROXY` / the macOS system proxy)
- `xiaoyuzhoufm.com` — upload

## Filesystem

Writes only under `${YT2PODCAST_ROOT:-~/.openclaw/workspace/yt2podcast}/jobs/`.
It does not read or write other user directories, and it uploads no local file anywhere
except the generated audio to Xiaoyuzhou.

## Publication is opt-in, twice

Draft is the default. Public publishing requires **both** `--publish` **and**
`YT2PODCAST_ALLOW_PUBLISH=1`; otherwise the worker aborts with `PUBLISH_NOT_ALLOWED`.
Public publishing cannot be undone.

## Process lifecycle

Nothing is detached: `scripts/new-job.sh` only writes a job file and prints the next
command. The worker runs under whatever supervisor the caller uses (agent host, terminal,
system service) and exits with it. No cron/systemd/launchd entries are installed.

## Telemetry

None. No analytics, no reporting, no outbound calls other than the APIs above.
