# Video Deep Reader 2.0.5

Turn a YouTube link, video ID, or supplied transcript into timestamped notes that help you decide, understand, or verify.

## Output modes

| Mode | Best for | Result |
|---|---|---|
| Quick | A bare link or ordinary summary request | One-screen decision card |
| Deep | Learning, argument analysis, or complete notes | Timestamped outline and argument map |
| Research | Checking material claims | Deep notes plus primary-source verification |
| Batch Quick | Comparing several videos | Comparable cards and watch/skip recommendation |

A bare YouTube URL is enough when the surrounding message clearly asks to process the video. A link used only as a citation, playback target, download request, or reference in an unrelated task does not trigger the skill.

## First-use check

Doctor is read-only and does not install anything:

```bash
python3 scripts/fetch_video.py --doctor
python3 scripts/fetch_video.py --doctor --network
python3 scripts/fetch_video.py --doctor --network --proxy-port 7890
```

If the pinned dependency is missing:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements.lock
```

The lock file pins `yt-dlp==2026.8.19` and verifies the downloaded wheel hash.

## Fetch subtitles

```bash
python3 scripts/fetch_video.py "https://www.youtube.com/watch?v=..."
python3 scripts/fetch_video.py "https://youtu.be/..." --proxy-port 7890
```

The script directly calls the pinned `yt-dlp` Python API. It does not invoke a shell, read proxy credentials, or accept an arbitrary output directory.

Fetched `meta.json` and `transcript.txt` files are stored under the system temporary directory:

```text
<system-temp>/video-deep-reader-<user-id>/<channel>/<video-id>/
```

This per-user cache is not durable storage. Its root and subdirectories must be owned by the current user with `0700` permissions; files are replaced atomically with `0600` permissions and symlinks are rejected. A note is saved elsewhere only when the user explicitly requests a file.

## Follow-up retrieval

Retrieval accepts a video ID rather than an arbitrary local path:

```bash
python3 scripts/fetch_video.py --retrieve-video <video-id> --keyword "attention"
python3 scripts/fetch_video.py --retrieve-video <video-id> --at 3:20
python3 scripts/fetch_video.py --retrieve-video <video-id> --list
```

## Transcript fallback

If a video has no accessible subtitles, paste or upload a transcript. Video Deep Reader can produce all three output modes without running the fetch script.

## Language

Notes follow the language of the current request. The single helper emits JSON, status codes, and transcript text rather than localized prose; the calling agent explains results in the user's language.

## Safety

- Only YouTube URLs and strict video IDs are accepted.
- Proxy input is restricted to a loopback port and cannot contain credentials.
- Temporary cache paths are generated from validated video IDs and sanitized channel names.
- Current web research occurs only in Research mode or when explicitly requested.
- No login, access-control bypass, publishing, package installation, or durable file write occurs automatically.

## License

[MIT](LICENSE)
