---
name: vibe-sanitizer
description: Use this skill when an agent needs to scan a Git repository for secrets, credentials, or machine-specific file paths, then sanitize safe findings in place or export a sanitized shareable copy using the bundled Python source in ./src.
version: 1.1.0
---

# vibe-sanitizer

Use this skill to scan a Git repository for secrets, credentials, or machine-specific file paths and make a repository safer before commit, before sharing, or before publishing.

This skill is for local agent workflows in Codex, Claude Code, OpenClaw, and similar coding agents that can read repositories and run shell commands.


## When To Use

| Use this skill when the user wants to... | Recommended action |
| --- | --- |
| Scan a repo before commit | `scan --scope working-tree` or `scan --scope staged` |
| Audit tracked files or a commit | `scan --scope tracked` or `scan --scope commit` |
| Fix safe findings in the original repo | `sanitize --mode in-place` |
| Create a shareable sanitized copy | `export --output ...` |
| Check AI-assisted or vibe-coded repos for leaked paths | Use normal scan flow with path detectors enabled |

## What It Catches

| Category | Detectors |
| --- | --- |
| Private material | PEM-style private key blocks |
| API keys and tokens | OpenAI-style keys, AWS access key ids, GitHub tokens, Slack tokens, bearer tokens |
| Credentials in text | URLs with embedded credentials, quoted secret-like assignments |
| Machine-specific paths | Workspace paths, home-directory paths, temporary paths, Windows user-directory paths |

| Finding class | Meaning |
| --- | --- |
| Fixable | Safe to rewrite in place |
| Review-required | Should be flagged, but not auto-rewritten in the original repo |

## Runtime Setup

| Step | Command |
| --- | --- |
| Verify bundled CLI | `cd {{skill_dir}}/src && python3 -m vibe_sanitizer.cli --help` |
| If not in audited repo | Pass `--root {{repo_dir}}` |
| If verification fails | Confirm `{{skill_dir}}/src/vibe_sanitizer/cli.py` exists and `python3` is available |

## Workflow

| Step | Action |
| --- | --- |
| 1 | Confirm the target repository root |
| 2 | Run the bundled CLI from `{{skill_dir}}/src` |
| 3 | Use the narrowest useful scope |
| 4 | Run `scan` first |
| 5 | Summarize findings by file, detector, severity, and fixability |
| 6 | Never print raw secret values |
| 7 | Use `sanitize --mode in-place` only for safe pre-commit cleanup |
| 8 | Use `export` when the user wants a separate sanitized copy |

## Scope Guide

| Scope | Use when |
| --- | --- |
| `working-tree` | Checking tracked and untracked files that are not ignored |
| `staged` | Checking what is about to be committed |
| `tracked` | Auditing tracked repository files |
| `commit` | Auditing one specific commit |

## Commands

| Task | Command |
| --- | --- |
| Verify CLI | `cd {{skill_dir}}/src && python3 -m vibe_sanitizer.cli --help` |
| Working tree scan | `cd {{skill_dir}}/src && python3 -m vibe_sanitizer.cli scan --root {{repo_dir}} --scope working-tree` |
| Staged scan | `cd {{skill_dir}}/src && python3 -m vibe_sanitizer.cli scan --root {{repo_dir}} --scope staged` |
| Tracked audit | `cd {{skill_dir}}/src && python3 -m vibe_sanitizer.cli scan --root {{repo_dir}} --scope tracked --format json` |
| Commit audit | `cd {{skill_dir}}/src && python3 -m vibe_sanitizer.cli scan --root {{repo_dir}} --scope commit --commit <sha>` |
| Safe in-place cleanup | `cd {{skill_dir}}/src && python3 -m vibe_sanitizer.cli sanitize --root {{repo_dir}} --scope staged --mode in-place` |
| Shareable export | `cd {{skill_dir}}/src && python3 -m vibe_sanitizer.cli export --root {{repo_dir}} --scope tracked --output ../safe-share` |
| Starter config | `cd {{skill_dir}}/src && python3 -m vibe_sanitizer.cli init-config --path {{repo_dir}}/.vibe-sanitizer.yml` |

## Guardrails

| Rule | Requirement |
| --- | --- |
| Secret handling | Never paste full secrets or full local paths into the response |
| Reporting | Prefer masked snippets such as `sk-***abcd` |
| Scope | Prefer the narrowest scope that answers the request |
| In-place rewrite | Do not auto-rewrite review-required findings unless explicitly requested |
| Export | Do not export into a directory inside the source repository |
| Repo model | Do not treat an exported copy as the default replacement for the main repo |
| Runtime assumption | Do not assume a global `vibe_sanitizer` install when bundled source exists |

## Agent Response Style

| Include | Avoid |
| --- | --- |
| Scope used | Raw credentials |
| Counts by severity when useful | Full local machine paths |
| Grouping by file when useful | Unnecessary command noise |
| Which findings are fixable | Implying review-required findings were auto-fixed |
| Which findings need manual review |  |

## Supported CLI Commands

| Command | Purpose |
| --- | --- |
| `scan` | Report findings |
| `sanitize` | Rewrite only safe findings in place |
| `export` | Create a separate sanitized copy |
| `init-config` | Create a starter config file |
