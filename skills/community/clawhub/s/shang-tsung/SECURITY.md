# Security

## What Shang Tsung Does

Shang Tsung writes and reads plain Markdown files inside your local workspace directory. That is the complete scope of its operation.

- `souls-helper.sh` creates and reads numbered `.md` files in `souls/[AGENT_NAME]/`
- `PROOF_OF_LIFE.md`, `MEMORY.md`, and `memory/YYYY-MM-DD.md` are plain text files in your workspace
- All file paths are local. Nothing is written outside the workspace directory.

## What Shang Tsung Does NOT Do

- No network access of any kind
- No HTTP requests, no webhooks, no API calls
- No credential access — no passwords, tokens, API keys, or secrets
- No browser access — no browser attachment, no cookie capture, no session reuse
- No system access beyond reading and writing Markdown files in your workspace
- No data transmission of any kind — nothing leaves your machine

## The Privacy Boundary in AGENTS-template.md

The template instructs agents to load `MEMORY.md` only in private/direct sessions with the agent's owner. This is a **privacy protection**, not a capability restriction.

`MEMORY.md` is the agent's curated long-term memory. It may contain personal context that the owner has shared with their agent over time. Loading it in a group chat would expose that personal context to other participants — which is not what the owner wants. The instruction exists to protect the owner's privacy, not to hide anything from security reviewers.

## Verifying the Script

`scripts/souls-helper.sh` is a ~200-line bash script that can be read in under two minutes. It contains:

- Filesystem operations: `mkdir`, file reads, file writes
- String processing: `basename`, `grep -oE`, `printf`, `sed`
- A template generator using `cat <<EOF`
- No network utilities (`curl`, `wget`, `ssh`, `nc`, etc.)
- No credential handling
- No subprocess spawning beyond standard shell operations

You are encouraged to read it before installing. It does exactly what it says.

## Reporting

If you find a genuine security concern, open an issue at the repository's GitHub Issues page.
