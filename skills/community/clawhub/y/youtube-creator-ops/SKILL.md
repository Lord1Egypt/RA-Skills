---
name: youtube-creator-ops
description: OpenClaw YouTube Publisher is a public ClawHub YouTube publishing skill. Use it when the user says "youtube creator ops", "youtube publisher", "YouTube Studio publish", or wants to publish a YouTube Short through a logged-in browser profile with a reusable run report.
version: 1.1.5
homepage: https://github.com/zack-dev-cm/youtube-creator-ops
license: MIT-0
user-invocable: true
metadata: {"openclaw":{"homepage":"https://github.com/zack-dev-cm/youtube-creator-ops","skillKey":"youtube-creator-ops","requires":{"anyBins":["python3","python"]}}}
---

# OpenClaw YouTube Publisher

Search intent: `youtube creator ops`, `youtube publisher`, `youtube studio publish`, `shorts publisher`

## Goal

Use OpenClaw to publish a YouTube Short in a logged-in browser session and save a reusable record
of the run:

- one machine-readable run manifest
- one structured provenance block for sources such as Midjourney, Suno, or local editors
- one ordered publish log with screenshots and URLs
- one structural bundle check
- one shareable markdown report

This skill is for YouTube Studio publishing through OpenClaw.
It assumes the browser profile is already authenticated.

## Use This Skill When

- the user wants to publish a YouTube Short through OpenClaw
- the short was assembled from Midjourney visuals, Suno audio, or local edits and that provenance should stay in the same bundle
- you need one clean record of upload, checks, visibility, and final URL
- the same YouTube Studio workflow keeps getting repeated from memory
- a failed publish needs screenshots, expected-versus-actual steps, and a reusable report
- the run should stay visible instead of hidden background automation

## Quick Start

1. Initialize the run manifest.
   - Use `python3 {baseDir}/scripts/init_youtube_creator_run.py --out <json> --run-id <id> --channel <channel> --goal <goal>`.
   - Add `--browser-profile`, `--stage dry_run|live`, `--visibility`, `--video-file`, `--title`, repeatable `--asset-source`, repeatable `--provenance`, and repeatable `--surface` fields.
   - Recommended asset source labels:
     - `visual:midjourney:<job-or-board>`
     - `audio:suno:<track-or-project>`
     - `edit:<tool>:<timeline-or-export>`
   - Recommended structured provenance JSON:
     - `{"role":"visual","provider":"midjourney","asset_id":"job-123","source_url":"https://midjourney.com/jobs/job-123","prompt_ref":"board-a","model":"v7","license":"internal-review","public_credits_required":false}`
     - `{"role":"audio","provider":"suno","asset_id":"track-04","source_url":"https://suno.com/song/track-04","prompt_ref":"chorus-a","model":"v4","license":"creator-plan","attribution_text":"Music draft from Suno.","public_credits_required":true}`

2. Execute the YouTube Studio flow through OpenClaw.
   - Open the Studio page in a logged-in profile.
   - Record each meaningful step with `append_youtube_creator_step.py`.
   - Capture screenshots and public URLs as the run progresses.

3. Default to `dry_run`.
   - Keep the manifest in `dry_run` stage until the final publish click is intentionally approved.
   - Switch to `live` only when the user wants the run to reach a public or unlisted post.

4. Pause for manual auth if needed.
   - If YouTube shows CAPTCHA, passkey, login, or 2FA, stop the automated step log and let the user complete it in the same browser profile.
   - Resume only after the authenticated Studio session is back.

5. Check the bundle before sharing it.
   - Use `python3 {baseDir}/scripts/check_youtube_creator_bundle.py --manifest <json> --repo-root <repo> --out <json>`.
   - Fix missing screenshots, incomplete failed steps, or private/absolute asset paths before sharing the bundle.

6. Render the report.
   - Use `python3 {baseDir}/scripts/render_youtube_creator_report.py --manifest <json> --out <md>`.
   - The default report keeps only public YouTube, Midjourney, and Suno URLs and redacts browser profile labels, private artifact paths, and non-public URLs found inside step text or provenance notes.
   - Share the report instead of loose screenshots and chat fragments.

## Operating Rules

### Profile rules

- Use a logged-in browser profile dedicated to the publishing context when possible.
- Do not claim a run is autonomous if login, CAPTCHA, passkey, or 2FA still requires a manual step.
- Keep the publish run in one visible browser session.
- Treat the final publish click as a deliberate user-approved action, even when the earlier steps are automated.

### Publish rules

- Record expected result and actual result for every step that matters.
- Capture a screenshot for failed or blocked steps and important checkpoints.
- Store final published URL when the run succeeds.
- Record upstream asset provenance when Midjourney, Suno, CapCut, or another editor was part of the content chain.
- If public credits or attribution are required for Midjourney, Suno, or another provider, keep that text in provenance and make sure the publish metadata includes it where needed.
- Prefer relative artifact paths so the bundle can move between machines.

### Safety rules

- Do not store cookies, secrets, or access tokens in notes or artifacts.
- Do not use private absolute filesystem paths in the final bundle.
- Treat moderation delays and post-processing lag as publish outcomes to record, not as silent success.

## Bundled Scripts

- `scripts/init_youtube_creator_run.py`
  - Create a machine-readable manifest for one YouTube publish run.
- `scripts/append_youtube_creator_step.py`
  - Append one publish step to the manifest.
- `scripts/check_youtube_creator_bundle.py`
  - Validate the resulting run bundle before sharing or final review.
- `scripts/render_youtube_creator_report.py`
  - Render a concise markdown report from the publish manifest.
