---
name: server-log-analysis
description: Connect to remote servers over SSH, read sibling config.yaml to understand service metadata and log locations, download only required log snippets to local temp for analysis, and diagnose issues from evidence. Use when users ask to troubleshoot remote service logs, investigate backend exceptions, or perform SSH-based log diagnostics.
---

# Server Log Analysis

## Purpose

Use this Skill to investigate service issues when logs are stored on remote servers.

This Skill assumes:

- The agent can connect to servers via SSH or equivalent remote execution tooling.
- `config.yaml` in this Skill directory defines service metadata, log paths, and business context.
- Before deep analysis, relevant log snippets should be copied to local `temp/` first.

## Required Reading

- Read `config.yaml` first.
- Read `reference.md` when field details or command patterns are needed.

## Core Workflow

1. Read `config.yaml`.
2. Map the user issue to one or more configured services.
3. Define the smallest necessary investigation scope:
   - target service
   - target host
   - relevant time window
   - candidate log files
4. Connect to the target server via SSH or available remote tools.
5. Perform remote checks before downloading:
   - file existence and file size
   - last modified time
   - whether keyword filtering or tail output is sufficient
6. Download only minimal required log snippets to configured local `temp/`.
7. Analyze local copies for errors, timing correlation, repeated failures, and likely root cause.
8. Output concise diagnosis with conclusions, evidence, uncertainty, and follow-up actions.

## Investigation Rules

- Prioritize service definitions and business context in `config.yaml`; do not guess.
- Prefer remote filtering before full download:
  - narrow time window first
  - then filter by keywords
  - use tail first for recent incidents
- Download full logs only when snippets are insufficient.
- Local filenames should clearly include service, host, and time range.
- Unless explicitly requested, do not fetch sensitive files, binaries, or unrelated large archives.
- For cross-service issues, analyze primary service first, then expand to dependencies.

## Service Selection

When user intent is ambiguous:

1. Use service `aliases`, `keywords`, and `description` in `config.yaml`.
2. Pick the service with the highest semantic match.
3. If still unclear, ask the user which service to inspect before remote connection.

## Remote Pre-Check Checklist

Before downloading logs, confirm:

- host configuration matches target service
- configured log files exist
- which log file was updated most recently
- whether rolling logs must be included
- whether issue is recent or historical

Common remote checks include:

- file metadata checks
- recent log tail checks
- quick keyword search
- time-window extraction
- process/service status when needed

## Local Download Rules

Store downloaded logs under configured `local_temp_dir`.

Recommended filename format:

`<service>__<host>__<log_name>__<time_hint>.log`

Priority order:

1. recent tail logs
2. keyword-filtered snippets
3. explicit time-window snippets
4. full file as last resort

## Analysis Focus

Focus on:

- startup failures
- repeated exceptions
- timeout and connection issues
- resource pressure signals
- failures in DB/cache/message queue/DNS/HTTP upstream dependencies
- config errors exposed by stack traces or startup logs
- timestamp alignment across related services

The response should include:

- issue summary
- key evidence
- preliminary cause
- confidence level
- next verification steps

## Security Constraints

- Treat `config.yaml` as operations metadata; do not store plaintext secrets.
- Prefer environment variables, key files, or external secret managers for SSH credentials.
- Unless explicitly requested, do not modify remote files or restart services.
- Unless requested, do not auto-delete downloaded logs.

## Exception Handling

If remote access fails:

1. Clearly state which step failed.
2. State target host and service.
3. Ask user for correct SSH access method, network path, or credentials.

If configured log path does not exist:

1. Clearly identify missing path.
2. Check whether alternate paths are configured for the same service.
3. Ask user whether deployment paths changed.

## Quick Execution Order

Always follow this order:

1. Read `config.yaml`.
2. Identify service and host.
3. Perform remote log pre-checks.
4. Copy minimal required logs to `temp/`.
5. Analyze locally.
6. Summarize conclusions with evidence.
