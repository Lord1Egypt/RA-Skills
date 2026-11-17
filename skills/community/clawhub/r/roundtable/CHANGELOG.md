# Changelog

## [0.5.0] - 2026-08-31

### Fixed
- Step 3 said to wait for the sub-agents without calling `sessions_yield`. Without the yield the Captain frequently synthesised while Round 1 was still running, producing an answer built on one or two of the three responses.
- Replaced the bare model aliases (`codex`, `sonnet`) in the defaults table and in all three `sessions_spawn` examples with full `provider/model` references. `sessions_spawn` skips an unrecognised model value without an error, so the alias produced a plausible answer from the wrong model.
- Noted that OpenClaw 2.0 moved the Codex models from `codex/*` and `openai-codex/*` to `openai/*`.
- Removed `package.json`. It declared an npm package that was never published and had no `main`, dependencies, or scripts. ClawHub CLI 0.22+ refuses to publish any folder containing a `package.json` as a skill.

### Added
- Frontmatter `metadata.openclaw` block. The skill previously shipped none.
- Sub-agent limits section: `maxChildrenPerAgent` defaults to 5, sub-agents do not inherit `cron` and `message`, and Scholar needs `web_search` in the tool profile.

## [0.4.1] - 2026-03-27

- Initial published release tracked in this file.
