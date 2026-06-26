---
name: relay-gitcode-cli
description: Use gd, the relay-gitcode-cli GitCode command line client, for GitCode API v5 workflows including authentication, repositories, pull requests, issues, search, SSH keys, labels, releases, GitCode Pipeline operations, raw API calls, JSON automation, version checks, and shell completion. Use when an agent should operate GitCode by running local gd commands. Do not use this skill for GitHub-only gh surfaces unless GitCode exposes an equivalent API through gd or gd api.
metadata:
  version: 0.1.5
  openclaw:
    skillKey: relay-gitcode-cli
    homepage: https://github.com/coolplayagent/relay-gitcode-cli
---

# Relay GitCode CLI

## Workflow

Use the selected `gd` binary as the GitCode control surface. Prefer `--json`
for automation and inspect command help before exposing unfamiliar operations:

```bash
gd --help
gd pr create --help
gd api --help
```

Keep behavior GitCode-specific. Do not introduce GitHub-only command surfaces
such as gists, codespaces, projects, GitHub Actions, rulesets, extensions, or
Copilot unless GitCode exposes equivalent API behavior and the task can be done
through `gd api`.

When `gd` commands, flags, examples, or user-facing behavior change in this
repository, update this `SKILL.md` in the same change so agent workflows stay
aligned with the compiled CLI.

`gd` reuses reqwest system proxy behavior for `HTTP_PROXY`/`http_proxy`,
`HTTPS_PROXY`/`https_proxy`, `ALL_PROXY`/`all_proxy`, and
`NO_PROXY`/`no_proxy`. TLS certificate verification is disabled by default for
GitCode API calls. Set `GD_SSL_VERIFY`/`gd_ssl_verify`,
`GITCODE_SSL_VERIFY`/`gitcode_ssl_verify`, or `SSL_VERIFY`/`ssl_verify` to
`true` to enable verification; any non-empty
`GIT_SSL_NO_VERIFY`/`git_ssl_no_verify` value keeps it disabled.

## Readiness

Select the newest usable `gd` before running workflows. Resolve bundled assets
relative to this skill directory. On Linux x64, check
`assets/bin/linux-x86_64/gd`; on Windows x64, check
`assets/bin/windows-x86_64/gd.exe`. Also check the `gd` binary found on `PATH`
with `command -v gd` on Unix or `where gd` on Windows.

For every candidate that exists and is executable, run `<candidate> --version`
and parse the semver from output such as `gd 0.1.0`. Use the candidate with the
highest semver. If versions are equal, prefer the bundled binary. Ignore
candidates that cannot run or do not print a parseable `gd` version. If the
selected binary is not on `PATH`, run it by absolute path or set `GD_BIN` and
substitute `"$GD_BIN"` for `gd` in the examples below.

Set `GD_BIN` to the selected path, then inspect version and authentication
state:

```bash
"$GD_BIN" --version
"$GD_BIN" version check --json
"$GD_BIN" auth status --json
```

Only install online when no bundled or `PATH` binary is usable. Prefer the Rust
package first and GitHub Releases second:

```bash
cargo install relay-gitcode-cli --force
gd version check --json
```

When falling back to GitHub Releases downloads, use the environment proxy
required by the host network. Check or set `HTTPS_PROXY`/`https_proxy`,
`HTTP_PROXY`/`http_proxy`, `ALL_PROXY`/`all_proxy`, and
`NO_PROXY`/`no_proxy` before running `curl`, `wget`, or another downloader.

Do not install this skill by building `gd` from a local repository checkout.
The bundled binaries and online fallbacks should come from released CLI
artifacts.

For temporary CI or end-to-end tests, prefer `GD_TOKEN` or `GITCODE_TOKEN` in
the process environment. `GD_TOKEN` takes precedence when both are present. For
interactive token login, read the token from stdin and store it in the system
keyring:

```bash
printf '%s' "$GITCODE_TOKEN" | gd auth login --with-token --json
gd auth status --json
```

Never print, commit, or persist personal access tokens, cookies, or private API
responses in repository files.

## Core Workflows

Use explicit repositories with `--repo owner/repo` when the current directory
does not define a `gd` default repository. Add `--json` for machine-readable
output:

```bash
gd repo view owner/repo --json
gd repo list owner --limit 50 --json
gd repo clone owner/repo
gd repo create name --private --description "demo" --json
gd repo fork owner/repo --json
gd repo move owner/repo target-owner/new-name --json
gd repo move owner/repo target-owner --name new-name --json
gd repo sync-github coolplayagent/relay-gitcode-cli --org plm-cac --private --json
gd repo sync-github git@github.com:owner/repo.git --repo target-org/repo --if-exists skip --json
gd repo sync-github owner/repo --repo target-org/repo --method git-push --if-exists update --json
gd repo contents README.md --repo owner/repo --ref main --json
gd repo file-create README.md --repo owner/repo --message "init" --content "hello" --json
gd repo file-update README.md --repo owner/repo --message "update" --sha blob-sha --content-file README.md --json
gd repo settings-edit --repo owner/repo --field has_issues=true --json
gd repo pr-settings --repo owner/repo --json
gd repo push-rules --repo owner/repo --json
gd repo contributor-stats --repo owner/repo --current-user --json
gd repo events --repo owner/repo --filter push --json
```

`gd repo move` moves a GitCode repository between users and organizations, or
renames it when the target owner is unchanged. Use a disposable repository for
E2E checks:

```bash
GITCODE_TOKEN=... GD_E2E_SOURCE_REPO=owner/repo GD_E2E_TARGET_OWNER=target-owner GD_E2E_TARGET_NAME=temporary-name scripts/e2e-repo-move.sh
```

`gd repo sync-github` accepts a GitHub `owner/repo`, HTTPS URL, or SSH URL and
creates a GitCode repository with that GitHub repository as `import_url` by
default.
Without `--org` or `--repo`, it imports into the authenticated GitCode user
namespace. Use `--org` for a GitCode organization and `--repo owner/name` for an
explicit target path. Existing targets are skipped by default. Use `--method
git-push` to create a regular GitCode repository and push GitHub branches and
tags with Git instead of enabling Pull mirroring; this keeps the target writable
for GitCode Release creation. Use `--if-exists update` to push refs to an
existing regular target, or `--if-exists recreate` to delete and recreate the
target.

Manage issues and pull requests with the GitCode-backed command surface:

```bash
gd issue list --repo owner/repo --state open --limit 30 --json
gd issue view 1 --repo owner/repo --json
gd issue create --repo owner/repo --title "bug" --body "details" --json
gd issue edit 1 --repo owner/repo --state close --json
gd issue comment 1 --repo owner/repo --body "thanks" --json
gd issue comments 1 --repo owner/repo --json
gd issue comment-edit 123 --repo owner/repo --body "updated" --json
gd issue label-add 1 --repo owner/repo --label bug --json
gd issue prs 1 --repo owner/repo --json
gd issue logs 1 --repo owner/repo --json

gd pr list --repo owner/repo --state open --base main --json
gd pr view 1 --repo owner/repo --json
gd pr create --repo owner/repo --title "change" --body "details" --base main --head feature --json
gd pr edit 1 --repo owner/repo --title "new title" --json
gd pr merge 1 --repo owner/repo --merge-method squash --json
gd pr commits 1 --repo owner/repo --json
gd pr files 1 --repo owner/repo --json
gd pr changes 1 --repo owner/repo --json
gd pr issues 1 --repo owner/repo --json
gd pr comments 1 --repo owner/repo --limit 50 --json
gd pr comment 1 --repo owner/repo --body "please fix" --path src/main.rs --position 3 --need-to-resolve --json
gd pr reply 1 discussion-id --repo owner/repo --body "fixed" --json
gd pr label-add 1 --repo owner/repo --label bug --json
gd pr review approve 1 --repo owner/repo --json
gd pr review assign-approver 1 --repo owner/repo --user alice --json
```

For broad GitCode settings payloads, pass repeated `--field key=value` entries.
Boolean, numeric, and `null` values are sent as JSON scalars; other values are
sent as strings. GitCode PR review is exposed through `gd pr review` approval
and tester subcommands.

Use `gd api` for GitCode API v5 endpoints that do not have first-class
subcommands:

```bash
gd api /user --json
gd api /repos/owner/repo -X PATCH -F has_issues=true --json
gd api /repos/owner/repo/issues --paginate --json
```

Manage GitCode Releases and migrate published GitHub Release assets into a
GitCode Release when a GitCode repository mirrors GitHub source code:

```bash
gd release list --repo owner/repo --json
gd release view v0.1.0 --repo owner/repo --json
gd release create v0.1.0 --repo owner/repo --title "v0.1.0" --notes "Release notes" --json
gd release edit 1 --repo owner/repo --title "v0.1.0" --json
gd release upload v0.1.0 dist/app.tar.gz --repo owner/repo --json
gd release migrate-github --repo owner/repo --github-repo source/repo --tag v0.1.0 --json
gd release migrate-github --repo owner/repo --github-repo source/repo --all --dry-run --json
gd release migrate-github --repo owner/repo --github-repo source/repo --tag v0.1.0 --update-release=false --skip-existing-assets=false --json
```

Manage tags and milestones directly when GitCode exposes equivalent API
behavior:

```bash
gd tag list --repo owner/repo --json
gd tag create v0.1.0 --repo owner/repo --ref main --message "v0.1.0" --json
gd tag protected-list --repo owner/repo --json
gd tag protected-create "v*" --repo owner/repo --create-access-level 30 --json
gd milestone list --repo owner/repo --json
gd milestone create --repo owner/repo --title v1 --due-on 2026-06-01 --json
gd milestone edit 1 --repo owner/repo --state closed --json
```

`gd release migrate-github` reads GitHub Release metadata and uploaded assets,
then creates or updates GitCode Releases through GitCode Release APIs. It uses
`GITHUB_TOKEN` when present for GitHub API reads, `GD_TOKEN`, `GITCODE_TOKEN`,
or the system keyring for GitCode writes, and skips existing GitCode assets with
matching names by default. Use `--update-release=false` to preserve existing
GitCode Release metadata and `--skip-existing-assets=false` to fail on duplicate
asset names.

## Pipelines

GitCode workflow commands use GitCode API credentials. OpenLibing gate commands
use separate OpenLibing GitCode OAuth credentials; they do not reuse
`GD_TOKEN` or `GITCODE_TOKEN`. Use `gd pipeline auth login` for browser OAuth, or set
`GD_OPENLIBING_TOKEN` or `GD_OPENLIBING_COOKIE` for automation. Use the
OpenLibing `--project-id`, not the GitCode repository id.

```bash
gd pipeline set --repo owner/repo .gitcode/workflows/ci.yml --file workflow.yml --json
gd pipeline codecheck --repo owner/repo --language SHELL --access-token-secret CODECHECK_ACCESS_TOKEN --json
gd pipeline run --repo owner/repo workflow-id --file-path .gitcode/workflows/ci.yml --branch main --json
gd pipeline runs --repo owner/repo --workflow-name ci --status success --json
gd pipeline view --repo owner/repo workflow-run-id --json
gd pipeline log --repo owner/repo workflow-run-id job-id
gd pipeline stop --repo owner/repo workflow-run-id --json
gd pipeline retry --repo owner/repo workflow-run-id --json
gd pipeline rerun --repo owner/repo workflow-run-id --json

gd pipeline auth status --json
gd pipeline config --project-id openlibing-project-id --json
gd pipeline setup --project-id openlibing-project-id --repo owner/repo --language Rust --codecheck-rule-set default --json
gd pipeline prs --project-id openlibing-project-id --repo owner/repo --state open --json
gd pipeline checks --project-id openlibing-project-id --repo owner/repo --pr 1 --json
gd pipeline gate-view --project-id openlibing-project-id --repo owner/repo --pr 1 --json
gd pipeline gate-runs --project-id openlibing-project-id --pipeline-name codecheck --json
```

`gd pipeline checks` falls back to the OpenLibing CodeCheck task summary when
the CICD PR check endpoint is not readable. `gd pipeline setup
--codecheck-rule-set` accepts either a rule-set name or a direct rule-set ID.
For setup failures on OpenLibing repository add/update, check the documented
OpenLibing prerequisites before retrying: project administrator or equivalent
project approver role, repository recorded in Code Repository Management, PR
takeover enabled, CodeCheck language/rule set selected, GitCode public or robot
account repository access, and webhook configuration permission.

## Troubleshooting

If a command fails, read the JSON response or the `gd:` error line before
guessing hidden state. Check authentication, repository spelling, hostname, and
API base first:

```bash
gd auth status --json
gd repo view owner/repo --json
gd api /user --json
gd --api-base https://api.gitcode.com/api/v5 api /user --json
```

Parse-time diagnostics cover unknown commands and flags plus locally known
structured values such as `owner/repo` repositories, GitHub repository inputs,
HTTP(S) base URLs, `.gitcode/workflows/` paths, `key=value` API/workflow fields,
and CodeCheck secret names. With `--json` or `--format json`, parse failures
write a single-line JSON object to stderr with `error`, `matched_path`,
`unexpected_token`, `expected`, `suggestion`, and `usage`.

For more command recipes, API automation patterns, and GitCode workflow YAML
examples, read `references/cli-workflows.md` and
`references/gitcode-workflow-yml.md`.
