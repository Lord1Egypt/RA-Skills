# Pattern Keys

`scripts/pattern-update.js` (see `SKILL.md` Step 3) scores which recurring behaviors
fired or didn't fire in a session, using a set of keys like the ones below.

This table reflects one operator's tracked patterns — treat it as an example set, not
a universal taxonomy. Swap in patterns that match your own behavioral failure modes.

To define your own: pick a short kebab-case key, write one line describing exactly
what it tracks, and pass it to `--passed` or `--failed` in Step 3 whenever it fires.

| Key | What it tracks |
|-----|-----------------|
| security-grep | Ran security grep before external publish/deploy |
| ls-check | Checked directory contents before writing |
| no-overwrite-outbox | Did not overwrite outbox files |
| no-commits | Did not commit to a shared repo without owner approval |
| clawhub-go-ahead | Got explicit go-ahead before a public/external publish step |
| cody-builds | Orchestrator specced the work, coding agent built it — did not write directly to coding-agent-owned repos |
| handoff-codex-repo | Handoff blocks targeted the sandbox repo only, never production |
| price-hallucination | Did not state a price/ATH/live stat without fetching a real-time source |
| transcribe-first | Transcribed audio before processing it |
| no-sleep | Did not suggest sleep/rest/bedtime to the user |
| noted-gotit | Did not say "Noted" or "Got it" without naming the file being written |
| future-action | Did not claim a future action without naming the enforcement mechanism behind it |
| keep-eye-on-it | Did not say "I'll keep an eye on it" without wiring a real mechanism to do so |
| no-honest | Did not use "honest/honestly" as hollow padding |
| fair-point | Did not use "Fair point" / "Fair enough" without actually taking a position |
| no-capability-claims | Did not claim a capability before confirming it worked |
| no-deterministic | Did not use deterministic language ("won't happen again," "locked permanently") for something that isn't actually guaranteed |
| prob-vs-det | Chose probabilistic framing over deterministic framing when that was the honest read |
