# Strong Workout Tracker OpenClaw Skill

[![CI](https://github.com/ivanvmoreno/strong-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/ivanvmoreno/strong-skill/actions/workflows/ci.yml)
[![Publish](https://github.com/ivanvmoreno/strong-skill/actions/workflows/release.yml/badge.svg)](https://github.com/ivanvmoreno/strong-skill/actions/workflows/release.yml)
[![Strong App](https://img.shields.io/badge/Strong-v6_API-orange)](https://www.strong.app/)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://docs.openclaw.ai/tools/skills)

Interact with the Strong v6 workout tracker REST API — login, list exercises, fetch workout logs and templates, manage folders, tags, measurements, and widgets.

## Installation

### Via ClawHub

```
clawhub install strong-app
```

### Manual

Copy the skill folder to one of:

```
~/.openclaw/skills/strong-app/
<workspace>/skills/strong-app/
```

## Prerequisites

Python 3.8+ (standard library only — no extra packages required).

Set environment variables:

| Variable | Required | Description |
|---|---|---|
| `STRONG_USERNAME` | Yes | Strong account username or email |
| `STRONG_PASSWORD` | Yes | Strong account password |

## Usage

The skill is invoked automatically by the agent when it matches your request. You can also invoke it directly:

```
python3 scripts/strong_runner.py login
python3 scripts/strong_runner.py get_profile
python3 scripts/strong_runner.py list_logs
python3 scripts/strong_runner.py get_log --log_id <uuid>
python3 scripts/strong_runner.py list_templates
python3 scripts/strong_runner.py list_exercises
```

All commands print JSON to stdout.

## Supported Operations

- **Auth** — `login`, `refresh_token`
- **Profile** — `get_profile`
- **Exercises** — `list_exercises`, `get_exercise`
- **Templates** — `list_templates`, `get_template`
- **Logs** — `list_logs`, `get_log`
- **Folders** — `list_folders`
- **Tags** — `list_tags`
- **Widgets** — `list_widgets`
- **Sharing** — `share_template`, `share_log`, `get_shared_link`
- **Filtering** — `get_log_at_date`, `get_logs_in_range`, `get_latest_log`, `search_logs_by_name`, `search_exercises_by_name`, `get_exercise_history`

See [SKILL.md](SKILL.md) for full parameter details per command.

## Security

- All API calls go to `back.strong.app` over HTTPS only.
- Credentials are read from environment variables and never logged.
- The script is pure Python (stdlib only) — no shell expansion or interpolation of user input.
- See the security manifest in `scripts/strong_runner.py` for full details.

## Releasing

Releases are automated via GitHub Actions. To publish a new version:

1. Update the `version` field in `SKILL.md` frontmatter.
2. Commit and push to `main`.
3. Tag the commit and push the tag:

```bash
git tag v2.0.0
git push origin v2.0.0
```

The `release.yml` workflow will:
- Validate the skill package (required files, frontmatter, security manifests)
- Publish to ClawHub via `clawhub publish`
- Create a GitHub Release with a zip archive

### Required repository secret

Add `CLAWHUB_TOKEN` to your repo secrets (**Settings > Secrets > Actions**). Generate it by running `clawhub login` locally and copying the token.

### CI on every push/PR

The `ci.yml` workflow runs on every push to `main` and every PR. It validates the skill structure and tests that all subcommands in `strong_runner.py` are parseable and respond to `--help`.

## Setting up the new repo

This skill is designed to live in its own repo (e.g. `strong-skill`). To set it up:

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin git@github.com:ivanvmoreno/strong-skill.git
git push -u origin main
```

The repo structure should be:

```
strong-skill/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── release.yml
├── SKILL.md
├── README.md
└── scripts/
    └── strong_runner.py
```

## References

- **[OpenClaw Skills Documentation](https://docs.openclaw.ai/tools/skills)** — Official docs on skill structure, discovery, eligibility, and configuration
- **[ClawHub Skill Format Spec](https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md)** — SKILL.md frontmatter fields, allowed files, slugs, and versioning
- **[ClawHub Publishing Checklist](https://gist.github.com/adhishthite/0db995ecfe2f23e09d0b2d418491982c)** — 13-point checklist for publishing skills (frontmatter gotchas, security manifests, required sections)
- **[ClawHub README & CLI Reference](https://github.com/openclaw/clawhub)** — `clawhub publish`, `clawhub install`, auth flows, and registry API
- **[Building Custom OpenClaw Skills](https://lumadock.com/tutorials/build-custom-openclaw-skills)** — Practical guide on SKILL.md structure, runbook-style body, gating, and production templates
- **[What are OpenClaw Skills? (DigitalOcean)](https://www.digitalocean.com/resources/articles/what-are-openclaw-skills)** — Overview of the skill ecosystem, installation, and security considerations
- **[Strong App](https://www.strong.app/)** — Official Strong workout tracker app
- **[Strong API (unofficial)](https://github.com/dmzoneill/strongapp-api)** — Reverse-engineered API documentation this skill is based on
