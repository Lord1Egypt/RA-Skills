# Privacy

Soul Archive stores your data **locally only**, on your own machine.

## Where the data lives

```
~/.agent-commons/skills_data/soul-archive/
```

Plaintext JSON files. Open and edit any time with any text editor.

## Who can see it

- **You** — full read/write access via the filesystem.
- **The AI agent you're using** (e.g. Claude Code, Cursor, your own scripts) — when you trigger Soul Chat, Soul Context, or any extraction, the relevant slices of your archive are passed to that agent's prompt. Whether the agent forwards anything to its provider's servers depends on **that agent's privacy policy**, not on Soul Archive.
- **No one else.** Soul Archive itself has no servers, no telemetry, no analytics, no remote sync.

## How to opt out

- **Stop auto-extraction**: edit `~/.agent-commons/skills_data/soul-archive/config.json`, set `auto_extract`, `auto_reflect`, and `auto_context_inject` to `false`. After this, nothing is captured unless you explicitly trigger it.
- **Disable specific axes**: in the same `config.json`, flip any axis under `extract_dimensions` to `false`.
- **Delete everything**: `rm -rf ~/.agent-commons/skills_data/soul-archive`. There is no other copy.
- **Export your data**: every file is plaintext JSON. Copy the directory anywhere.

## Sensitive topics

Health, finance, and intimate relationships require explicit confirmation by default (`require_confirmation_for` in `config.json`).

## Defaults

`auto_extract` and `auto_context_inject` are **on** by default — Soul Archive is designed for you to capture *yourself*, so an opt-in default would defeat the purpose for the typical single-user setup. If you prefer manual triggering, flip them off as described above.

## License

MIT. Code and data are yours.
