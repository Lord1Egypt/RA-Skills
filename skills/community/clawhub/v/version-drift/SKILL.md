---
name: version-drift
description: "One command to check if your entire stack is up to date. SSHes into servers, queries APIs, and compares installed versions against latest — across every service you run."
metadata: {"clawdbot":{"emoji":"📊","requires":{"pip":["pyyaml"]}}}
---

# Version Drift

**One command. Your entire stack. Are you current?**

You run things. Lots of things. Docker on a VPS. Node.js on a web server. Home Assistant on a Pi. Postgres in a container. Python on your laptop. They each update on their own schedule, and you check them... sometimes. Usually after something breaks.

Version Drift fixes that. It SSHes into your servers, queries your APIs, runs local commands, and compares what's **actually installed** against what's **latest available**. One config file. One command. One answer.

```
$ python3 drift.py check

Version Drift Report — 2026-03-16 08:30 UTC

Host             Check          Installed    Latest       Status
─────────────────────────────────────────────────────────────────
web-1            node           20.11.0      22.14.0      🔴 MAJOR
web-1            redis          7.2.4        7.4.2        ⚠️  DRIFT
nas              docker         27.5.1       28.0.1       ⚠️  DRIFT
home-assistant   core           2026.2.5     2026.3.3     ⚠️  DRIFT
this-machine     python         3.13.1       3.13.1       ✅ CURRENT
this-machine     openclaw       2026.3.13    2026.3.13    ✅ CURRENT

Summary: 2/6 current · 3 drifting · 1 major
```

## How is this different?

- **Dependency scanners** (npm audit, pip-audit) check your *code*. This checks your *servers*.
- **Release trackers** tell you GitHub has a new release. This tells you *your server is behind*.
- **Uptime monitors** tell you if something is *running*. This tells you if it's *current*.

Version Drift is the only tool that bridges the gap between "a new version exists" and "my infrastructure is running it."

## How it works

1. You write a `config.yaml` listing your hosts and what to check
2. For each check, you tell it:
   - How to get the **installed** version (a shell command, or an API endpoint)
   - Where to find the **latest** version (GitHub, npm, PyPI, Docker Hub, or any HTTP endpoint)
3. Run `python3 drift.py check` and get a report

That's it. No agents to install on every server. No dashboards. No SaaS. Just a script and a config file.

## Setup

```bash
pip install pyyaml          # optional — falls back to JSON config
cp config.example.yaml config.yaml
# Edit config.yaml with your hosts and checks
python3 drift.py check
```

## What you can check

**Anything you can get a version number from.** The installed version comes from a shell command (local or SSH) or an API response. The latest version comes from one of these sources:

| Source | Example | Checks |
|--------|---------|--------|
| GitHub Releases | `repo: "grafana/grafana"` | Any open-source project with GitHub releases |
| GitLab Releases | `project: "gitlab-org/gitlab"` | GitLab.com or self-managed GitLab projects |
| Gitea/Forgejo | `base_url: "https://codeberg.org"` | Forgejo/Gitea-compatible release APIs |
| npm Registry | `package: "next"` | Node.js packages |
| PyPI | `package: "django"` | Python packages |
| Docker Hub tags | `repo: "library/postgres"` | Highest stable semver tag, with optional regex pinning |
| OCI image digest | `image: "traefik", tag: "v3.4"` | Docker Hub, GHCR, Quay, and other registry-v2 images |
| Custom HTTP | `url: "https://..."` | Anything with a JSON API |

**Three ways to check installed versions:**

| Method | Use when |
|--------|----------|
| `ssh` | Checking a remote server you have SSH access to |
| `http` | Checking a service that exposes its version via API (Home Assistant, Grafana, Gitea, etc.) |
| `local` | Checking the machine running the script |

## Example configs

The `config.example.yaml` includes four ready-to-adapt templates:

1. **Homelab stack** — Docker, nginx, Postgres, Home Assistant, Python, Node
2. **Production/DevOps** — web servers, Redis, PM2, API gateways
3. **Docker-heavy** — Traefik, Grafana, Postgres containers
4. **Python/Data Science** — PyTorch, CUDA, pip packages on GPU boxes

Delete the ones you don't need, uncomment the ones you do, fill in your details.

## Commands

```bash
python3 drift.py check                      # table output
python3 drift.py check --json               # for crons and pipelines
python3 drift.py check --markdown           # for Discord, Slack, or docs
python3 drift.py check --changes            # include release notes for drifting items
python3 drift.py check --only web-1         # check one host only
python3 drift.py check --config /alt/path   # use a different config
python3 drift.py discover --compose docker-compose.yml  # generate image digest checks
```

## Docker / OCI image drift

For container stacks, prefer digest checks when you care about rebuilds under the same tag:

```yaml
- name: "traefik-image"
  installed: "docker inspect traefik --format '{{range .RepoDigests}}{{println .}}{{end}}' | head -1 | sed 's/.*@//'"
  latest:
    source: "oci"
    image: "traefik"
    tag: "v3.4"
    return: "digest"
```

Run `python3 drift.py discover --compose docker-compose.yml` to generate starter checks for a Compose file.

For Docker Hub version tags, `source: docker` now prefers the highest stable semver-like tag instead of blindly trusting the most recently pushed tag. Add `tag_regex` when you want to stay on a major line:

```yaml
latest:
  source: "docker"
  repo: "library/postgres"
  tag_regex: "^17\\."
```

Version comparison is semver/calver-aware enough for common forms like `v1.2.3`, `2026.5.7`, and `1.2.3-rc.1`; stable releases sort above prereleases with the same numbers.

## State tracking

Version Drift saves results between runs. On repeat checks, you'll see how long something has been drifting:

```
web-1    node    20.11.0    22.14.0    🔴 MAJOR (since 12 days ago)
```

## Changelogs

Add `--changes` to see what actually changed between your version and latest:

```
$ python3 drift.py check --changes

Host             Check          Installed    Latest       Status
─────────────────────────────────────────────────────────────────
web-1            node           20.11.0      22.14.0      🔴 MAJOR DRIFT
                                ↳ 20.11.0 → 22.14.0 (major version bump 20 → 22)
                                  22.14.0 — Notable changes: V8 13.5, require(esm) stable
                                  22.13.0 — Node.js 22.13.0 LTS 'Jod'
                                  21.7.0 — WebSocket client, import.meta.dirname
                                  ... and 12 more releases
this-machine     python         3.13.1       3.13.1       ✅ CURRENT
```

For GitHub-hosted projects, Version Drift fetches actual release notes between your installed version and latest. For npm and PyPI packages, it traces back to the GitHub repo automatically.

This makes extra API calls, so it's opt-in. Set `GITHUB_TOKEN` to avoid rate limits when checking many items.

## Automate it

Run on a cron, pipe the markdown output to Discord or Slack, and never be surprised by stale versions again:

```bash
# Weekly drift report to Discord via OpenClaw cron
python3 drift.py check --markdown
```

## Environment variables

Secrets go in env vars, not config files:

```yaml
headers:
  Authorization: "Bearer ${HA_TOKEN}"    # expanded at runtime
```

Set `GITHUB_TOKEN` to avoid GitHub API rate limits (60 req/hr unauthenticated → 5,000 with token).

## Security

Version Drift needs to talk to your servers — that's the whole point. Here's what it does and why:

- **Shell commands** — Runs version-check commands locally via `sh -c` (e.g., `docker --version`). Commands come from *your* config file, not from external sources.
- **SSH** — Connects to hosts listed in your config to run version-check commands remotely. Uses your existing SSH keys and config. Host key checking defaults to `accept-new` (trust on first use, reject if the key changes). Override per-host with `strict_host_key: "yes"` for stricter checking or `"no"` for legacy behavior.
- **HTTP requests** — Fetches version info from APIs (GitHub, npm, PyPI, Docker Hub, your services). SSL verification is **on by default**; set `verify_ssl: false` per-host only if you use self-signed certs.
- **Environment variables** — Expands `${VAR}` references in your config so you can keep secrets out of the config file.

No data leaves your machine except the version-check requests you configure. No telemetry, no analytics, no phone-home.

## Requirements

- Python 3.8+
- PyYAML (optional — can use `config.json` instead)
- SSH access to remote hosts (for SSH checks)
- That's it. No external services. No accounts. No agents to install.
