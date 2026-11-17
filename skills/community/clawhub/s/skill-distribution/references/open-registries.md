# Open registries: GitHub, skills.sh, agentskill.sh, ClawHub, Hermes

## GitHub (do this first)

Every other channel either reads the repo or accepts it as the source.

1. Create a public repo with the layout from SKILL.md (`skills/<name>/SKILL.md`).
2. Add a `LICENSE` and a `README.md` with install lines per agent.
3. Add the repo topics `agent-skills` and `claude-skills` (plus `gemini-cli-extension` if it is also a Gemini extension) so topic pages and scrapers find it.
4. Tag releases (`v1.0.0`) when the skill changes meaningfully.

Large scraped indexes (SkillsMP and similar) list public repos containing a SKILL.md automatically; there is nothing to submit and no way to opt in faster.

## skills.sh (Vercel)

There is no upload and no submission form. skills.sh hosts nothing: the `skills` CLI clones GitHub repos, and the leaderboard is built from anonymous install telemetry. A skill shows up after people install it.

- Users install with: `npx skills add owner/repo` (also accepts full git URLs, a subfolder URL such as `https://github.com/owner/repo/tree/main/skills/my-skill`, and local paths).
- The CLI finds skills in `skills/`, `skills/.curated/` and agent folders like `.claude/skills/`, up to three levels deep.
- Scaffold a new one with `npx skills init my-skill`.
- `metadata.internal: true` hides a skill unless the user sets `INSTALL_INTERNAL_SKILLS=1`.
- Installs made with `DISABLE_TELEMETRY=1` or `DO_NOT_TRACK=1` are not counted.
- The site runs routine security audits; the "Official" section is for verified makers and is not self-serve.

To get listed: put the exact `npx skills add owner/repo` line in the README and wherever the skill is announced. Rank follows real installs.

Docs: https://skills.sh/docs · https://github.com/vercel-labs/skills

## agentskill.sh

Submit at https://agentskill.sh/submit — either a GitHub repository (it scans the repo for every SKILL.md) or a direct link to one SKILL.md.

- Connect the GitHub account to claim skills from your repos and orgs, get the verified badge and see analytics.
- Updates: daily sync by default; for instant sync add a repo webhook to `https://agentskill.sh/api/webhooks/github` (content type `application/json`, push events only). A direct-URL submission is updated by re-submitting.
- Each skill gets automated quality and security scores, shown on its page.

## ClawHub (OpenClaw registry)

A real registry with accounts and versioned uploads.

```bash
npm i -g clawhub
clawhub login          # device-code login: prints a code and a URL to approve in the browser
clawhub whoami
clawhub skill publish ./skills/my-skill \
  --slug my-skill --name "My Skill" --version 1.0.0 \
  --changelog "First release" --tags latest
```

- **Login is device-code only.** The CLI prints a short code and a URL; the user opens the URL, signs in with GitHub and enters the code. The old browser-callback login was removed because it could hand API tokens to loopback redirects. If the browser shows "CLI login has moved", the first attempt used the old flow: update the CLI (`npm i -g clawhub@latest`) and run `clawhub login` again. The login is the user's step; wait for `clawhub whoami` to show their handle before publishing.
- The GitHub account must be old enough to pass ClawHub's upload gate.
- Older guides write `clawhub publish`; the current docs use `clawhub skill publish <path>`. Run `clawhub --help` to see which the installed version expects.
- Version must be semver. Patch for wording fixes, minor for content improvements, major for workflow rewrites.
- **Everything on ClawHub is MIT-0.** Confirm the user accepts that before the first publish.
- Bundle limit 50 MB; hidden files and symlinks are ignored.
- Automated checks run on every release; held or blocked releases disappear from the public catalog.
- Declare required env vars and binaries under `metadata.openclaw` so the page shows them and installs do not fail silently.

Docs: https://docs.openclaw.ai/clawhub · https://docs.openclaw.ai/clawhub/skill-format

## Hermes skills hub (Nous Research)

Hermes follows the same Agent Skills format and aggregates several registries. Reported commands (from secondary sources — confirm in the Hermes docs before running):

- Publish to a GitHub repo: `hermes skills publish skills/my-skill --to github --repo owner/repo`
- Let users add the repo as a source: `hermes skills tap add owner/repo`

Hub installs pass a scanner for exfiltration, prompt injection and destructive commands.

Docs: https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills
