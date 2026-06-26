# Workspace File Roles

Each file has ONE job. Content belongs in exactly one place.

| File | Role | Contains | Does NOT contain |
|---|---|---|---|
| `AGENTS.md` | Behavioral rules | Workflows, conventions, safety, git rules | Credentials, personality, user info |
| `TOOLS.md` | Credential map | 1Password refs, env vars, service configs, gotchas | Behavioral rules, personality |
| `MEMORY.md` | Long-term index | Curated facts, project index, preferences (≤150 lines) | Raw logs, full project details |
| `USER.md` | User profile | Personal info, preferences, style, priorities | Agent behavior, credentials |
| `SOUL.md` | Personality | Tone, voice, identity, boundaries | Credentials, user info |
| `IDENTITY.md` | Name card | Name, creature type, emoji | Everything else |
| `HEARTBEAT.md` | Proactive checks | Rate limit gate, check routines | Credentials, personality |

## Cross-Reference Rules

- Pointers are OK (e.g., `AGENTS.md` saying "see TOOLS.md for credentials")
- Duplicating content across files is NOT OK
- `MEMORY.md` may briefly reference 1Password rules (security preference) but not credential details
- Credential-adjacent content (API keys, env vars, 1Password items) → `TOOLS.md` only
