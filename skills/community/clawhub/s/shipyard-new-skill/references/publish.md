# Publishing

Ask before each place. Push a version bump for every release; most places update from git after the first listing.

| Place | Who uses it | How | Automatic after the first time? |
|---|---|---|---|
| Your GitHub repo | everyone | push to the default branch; a tag per version | yes |
| Plugin marketplace (Claude Code only) | Claude Code only | the repo is the marketplace (`.claude-plugin/marketplace.json`); users add it once and get updates | yes |
| The official Claude Code only plugin directory | Claude Code only | a one-time submission form; the student fills it in, you prepare the answers | yes, from git |
| skills.sh | Codex, Cursor and 30 or more other agents | listed from installs with `npx skills add <owner>/<repo>`; nothing to submit | yes |
| `~/.agents/skills` | Codex, Cursor and others | copy the skill folder there, or the skills.sh command | by hand or with an installer |
| Cursor marketplace | Cursor | the manifest in `.cursor-plugin/` in the repo, then a one-time submission form | yes, from git |
| ClawHub (OpenClaw) | OpenClaw | `clawhub publish <skill folder>` after `clawhub login` | each release, one command |
| Hermes | Hermes agent | users add the repo as a tap | yes |
| Awesome lists | readers | one pull request per list, in that list's format | no |

Forms and logins are the student's: never sign in for them or type a password. Prepare the text (name, one-line description, repo link, a screenshot or demo) so they only paste it.
