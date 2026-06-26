# `screenci record`

Use `screenci record` to capture ScreenCI videos from `.screenci.ts` scripts.

Assume the ScreenCI project is already initialized. Add new video scripts under `recordings/`.
If you are creating new videos, remove the starter `recordings/example.screenci.ts` file.

## Commands

```bash
npx screenci record
npx screenci record -c screenci.config.ts
```

## What It Does

- Runs ScreenCI video tests
- Starts the recording pipeline
- Saves output under `.screenci/<video-name>/`
- Produces at least `recording.mp4` and `data.json`

## Sign In Early

Sign-in only blocks the final recording, not authoring or testing. Get it going up front: surface the sign-in link to the user early (printed by `screenci init`, or by running `npx screenci record` once, or read from `screenci/.screenci/link-session.json`) and ask them to sign in while you build the video. The link is valid for 24 hours. For the final recording, run `npx screenci record` (no flag): off-CI it waits and records as soon as sign-in completes. Attempting it before they finish does no harm: it reprints the link, and if the timeout elapses it exits non-zero with the link still valid, so re-prompt and run again.

## Runtime Behavior

- Recording runs with local Playwright.
- When `SCREENCI_SECRET` is missing, `screenci record` waits for browser sign-in by default and continues once it completes. This is the default at an interactive terminal and in a plain non-interactive session (no terminal, no CI), so an agent does not need a flag. It prints the link, polls (every 2 seconds interactively, every 5 seconds otherwise) up to a timeout (15 minutes interactively, 5 minutes otherwise), then saves the secret and records. If the timeout elapses first, it exits **non-zero** with the link still valid, so re-surface the link and rerun once signed in. Override the timeout with `SCREENCI_POLL_AUTH_TIMEOUT_MS` (milliseconds).
- Under CI (`CI=true`), or with `SCREENCI_NONINTERACTIVE=1` or `--no-poll-auth`, `screenci record` does not wait: it prints the sign-in link and exits cleanly with exit code 0 without recording. A clean exit here is a handoff, not a finished recording, so do not treat exit code 0 as "recording done" when the output contains a sign-in link. Set `SCREENCI_SECRET` ahead of time (the expected CI setup) to record without an interactive sign-in.
- `--poll-auth` still forces waiting and is kept for backwards compatibility, but is no longer needed off-CI where waiting is already the default.
- Pending auth state is cached in `.screenci/link-session.json`, so rerunning `record` reuses the same link until it expires or completes.
- Playwright arguments can be passed through after the command.
- When API configuration and `SCREENCI_SECRET` are available, uploads may run after recording.

## Recommended Workflow

```bash
# first verify the flow
npx screenci test

# then record
npx screenci record
```

## Workflow

Always run `npx screenci test` until it passes before running `npx screenci record`. Fix failures and rerun until green.

```bash
npx screenci test   # verify selectors, flow, and narration
npx screenci record # capture the final recording
```
