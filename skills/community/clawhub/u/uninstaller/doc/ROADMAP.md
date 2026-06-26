# Roadmap

## Planned: Preserve accumulated user preference on uninstall

**Goal**: When uninstalling OpenClaw, optionally preserve user data so it can be restored on reinstall. Options should be readable for non-technical users.

### Data to preserve (verified paths)

| Item | Path | Notes |
|------|------|-------|
| **Skill list** | `~/.openclaw/skills/`, `./skills/` (workspace), `.clawhub/lock.json` | Installed skills + versions |
| **Log list** | `~/.openclaw/` (gateway logs), `~/.openclaw/sessions/` | Session transcripts, gateway logs |
| **User preferences** | `~/.openclaw/openclaw.json` (partial) | skills.enabled, tools config, etc. |
| **Credentials** | `~/.openclaw/credentials/`, `agents/*/agent/auth.json` | API keys, OAuth tokens — **optional** |

### User-facing options (non-CS friendly)

| Option | Description |
|--------|-------------|
| **Preserve skills** | Keep the list of installed skills so you don’t need to reinstall them |
| **Preserve logs** | Keep chat history and logs for reference |
| **Preserve preferences** | Keep your settings (enabled skills, etc.) |
| **Preserve credentials** | Keep saved API keys and login tokens — **optional**; skip if you want a clean slate or prefer to re-enter |

### Implementation sketch

1. Add `--preserve-preference` flag to `uninstall-oneshot.sh` with sub-options or interactive prompts
2. Before `rm -rf $STATE_DIR`, tar/zip the preserve set to `~/.openclaw-backup-YYYYMMDD/` or user-specified path
3. Document restore flow: copy back selected dirs after reinstall
4. Optionally: add `restore-preferences.sh` script

### Open questions

- Exact paths for gateway logs (check OpenClaw docs)
- What subset of `openclaw.json` is "preference" vs "runtime"
