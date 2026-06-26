# Prerequisites

What needs to be in place before this skill can produce a final video.

## Software (auto-installed via `npm install`)

These are bundled npm packages — running `npm install` in the project directory is sufficient.

| Package | Purpose | Notes |
|---|---|---|
| `playwright` | Browser automation + headless recording | After install: `npx playwright install chromium` (one-time, ~150MB) |
| `ffmpeg-static` | Bundled ffmpeg binary | Self-contained, no system ffmpeg needed |

## Operating system

**Required**:
- **Node.js 18+** (`node -v`)
- **CJK-capable font on the system** if your subtitles include Chinese / Japanese / Korean. The postprocess auto-detects:
  - **Windows**: Microsoft YaHei (built-in)
  - **macOS**: PingFang SC (built-in)
  - **Linux**: Noto Sans CJK SC (`apt install fonts-noto-cjk` on Debian/Ubuntu; equivalent on other distros)
- Network access to npm registry + Playwright CDN (first-time chromium download)

**Override**: set `SUBTITLE_FONT` env var to use any installed font, e.g. `SUBTITLE_FONT="SimHei"`.

## Project-specific

Things only the user can provide:

| Item | Purpose | How |
|---|---|---|
| Target URL | What web app to record | env `SCREENCAST_BASE` or edit `record.js` |
| Login credentials | If app requires auth | Manual login in browser during `npm run login` |
| Upload test files | If demo includes file upload stages | Place in any directory, reference path in flow |
| Deploy target dir | Where final.mp4 gets archived | env `DEPLOY_DIR` (default `./output/`) |

## First-run checklist

A fresh project, after `cp templates/* <working-dir>`:

```bash
cd <working-dir>
npm install                         # ~30s, includes playwright + ffmpeg-static
npx playwright install chromium     # ~2min first time, downloads chromium binary
npm run setup                       # generates cursor.png + ripple.png (~2s)
npm run login                       # opens real chrome, log in, closes (manual)
# now edit record.js stage flow
npm run ship                        # record + render + deploy + review + clean
```

If `npm run ship` succeeds, `final.mp4` is in the working directory and a timestamped copy in `output/`.

## Verifying setup

After `npm run setup`:

- `cursor.png` should exist (~3KB, 22×28 @2x)
- `ripple.png` should exist (~2KB, 80×80 @2x)

After `npm run login`:

- `storageState.json` should exist (~1-5KB, contains cookies)
- `post-login-summary.json` should list visible nav / headings / buttons (~1KB JSON)
- `post-login.png` should exist (full-page screenshot for context)

If any of these are missing, the corresponding step failed silently — re-run with `node <script>.js` directly to see the error.

## Cross-platform caveats

Tested on:
- **Windows 11** — primary development platform
- **macOS** — should work; PingFang SC built-in for CJK subtitles
- **Linux** — works if you `apt install fonts-noto-cjk` (or distro equivalent); otherwise CJK characters render as boxes

Untested on:
- **WSL** — likely works for `npm run setup` and `npm run record`; opening a real browser for `npm run login` requires X server or WSLg
- **Docker** — possible but you'd need to mount cursor.png + ripple.png + storageState.json from outside the container

## ffmpeg-static caveats

The bundled ffmpeg has libass for subtitles, libx264 for h264 encoding, and the standard filter set. If you replace `ffmpeg-static` with a system ffmpeg, ensure it has libass enabled (`ffmpeg -hide_banner -version` should mention `--enable-libass`).
