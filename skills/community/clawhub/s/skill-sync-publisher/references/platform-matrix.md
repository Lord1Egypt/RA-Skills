# Platform matrix

The source is a public GitHub repository. A platform is only acted on when its
state is `enabled`; first use asks the user to choose `enabled`, `disabled`, or
`deferred`.

| Platform | First action | Later action | Auth/CLI |
|---|---|---|---|
| GitHub | inspect remote and choice | commit/push target files | `gh auth status`, `git` |
| Awesome Codex Plugins | PR to curated list | update PR/list entry | GitHub auth; plugin manifest required |
| HOL Registry | quote then publish | publish new version | `npx @hol-org/registry` |
| skills.sh | public-source/index check | index check | no stable publisher CLI assumed |
| SkillsMP | submit public GitHub URL | index check | browser/manual fallback |
| LobeHub | import/submit GitHub URL | refresh check | browser/manual fallback |
| ClawHub | dry-run then publish | dry-run then publish version | `clawhub` |
| Cursor Directory | submit GitHub URL | index check | browser/manual fallback |

Platform behavior is intentionally conservative: discovery pages and indexers
are not treated as upload APIs unless a supported endpoint is verified at run
time.

For a directory platform, `planned` is an actionable handoff rather than
success. The user completes the web submission while logged in, then reruns
`bin/skill-sync status <skill-dir>` or a targeted sync to record the result.
