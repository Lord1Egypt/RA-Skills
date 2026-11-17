---
name: work-over-ssh
description: Use when editing a remote Git project over SSH.
metadata: {"openclaw":{"emoji":"🛰️","requires":{"bins":["ssh","python3"]}}}
---

# Work Over SSH

## Overview

Work on a remote Git repository while the agent runs locally. Use the local
OpenSSH client for inspection and commands, and apply reviewed Git patches for
edits. Do not require Codex, OpenClaw, Hermes, SSHFS, or an agent runtime on the
remote host.

Use `scripts/remote_workspace.py` for connection checks, bounded reads,
environment-aware commands, and checked patch application.

Before the first connection, read [references/usage.md](references/usage.md).
Require the invocation to state the SSH server, absolute remote project path,
and environment name or path. Accept `none` only when the project has no
dedicated environment. If any field is missing, ask for it before running SSH.

## When to Use

Use this skill when:

- The source repository exists on a host reachable through SSH.
- The agent must remain on the local machine.
- The project may use a Python virtualenv or Conda environment remotely.
- Inspection, editing, testing, or diagnosis must happen without SSHFS.

Do not use this skill when the repository is already available locally or when
the platform's native remote-project integration is installed and preferred.

## Requirements

Local requirements declared in metadata:

- `ssh`
- `python3`

Remote requirements:

- A POSIX-compatible shell and ordinary utilities such as `sed` and `mktemp`.
- `git` for repository checks and patch application.
- The project's existing runtime and dependencies.
- `conda` only when a Conda environment is selected.

Require key-based authentication or another non-interactive method already
configured by the user. Never request or store passwords, private keys, tokens,
or key contents.

## Resolve the Helper Path

Set `HELPER` once for the active runtime:

```bash
# OpenClaw / ClawHub
HELPER="{baseDir}/scripts/remote_workspace.py"

# Hermes Agent (use this assignment instead)
HELPER="${HERMES_SKILL_DIR}/scripts/remote_workspace.py"
```

Hermes expands `${HERMES_SKILL_DIR}` when it loads the skill. OpenClaw expands
`{baseDir}`. Confirm `test -f "$HELPER"` before the first command.

## Establish the Target

Obtain:

1. A concrete host alias from the user's local SSH configuration.
2. An absolute remote Git project root.
3. An environment selector: virtualenv path, Conda name, Conda prefix, or the
   explicit value `none`.

Run the preflight:

```bash
python3 "$HELPER" check HOST /absolute/project
```

Completion criteria:

- The command prints `connected`.
- `cwd` matches the requested project.
- `git` prints the repository root rather than `not-a-repository`.

If preflight fails, report the exact SSH error. Do not change host keys, SSH
configuration, authentication, or firewall settings without explicit user
authorization.

## Select the Project Environment

Inspect `pyproject.toml`, `requirements*.txt`, `environment.yml`, `conda.yml`,
`.python-version`, `.venv/`, `venv/`, and project documentation. Use the
environment named by the user or documentation. Ask when several plausible
environments remain.

Each helper command creates a new SSH process. Supply the environment option on
every Python, test, lint, or package command that needs it.

### Virtualenv

Use an absolute path or a path relative to the remote project root:

```bash
python3 "$HELPER" exec \
  --venv .venv HOST /absolute/project -- \
  python -c 'import sys; print(sys.executable)'

python3 "$HELPER" exec \
  --venv .venv HOST /absolute/project -- \
  python -m pytest
```

### Named Conda environment

```bash
python3 "$HELPER" exec \
  --conda-name app HOST /absolute/project -- \
  python -c 'import sys; print(sys.executable)'
```

### Conda prefix

```bash
python3 "$HELPER" exec \
  --conda-prefix /opt/conda/envs/app HOST /absolute/project -- \
  python -m pytest
```

The helper uses `conda run`; it does not rely on activation persisting. If
`conda` is absent from the non-interactive SSH `PATH`, add
`--conda-executable /absolute/path/to/conda` before `HOST`.

Run Git inspection and patch operations without an environment option. Do not
source `.env` automatically or create, update, or install packages into an
environment unless the user requests it.

## Inspect and Diagnose

Prefer bounded, one-shot commands:

```bash
python3 "$HELPER" exec \
  HOST /absolute/project -- git status --short

python3 "$HELPER" exec \
  HOST /absolute/project -- rg -n PATTERN .

python3 "$HELPER" read \
  HOST /absolute/project path/to/file --start 1 --end 240
```

Use `exec ... -- sh -lc '...'` only when pipes, redirects, expansion, or
compound shell syntax are necessary. Quote the whole shell program as one local
argument.

For an interactive program, start `ssh -tt HOST` in a persistent terminal and
send later input to that same session. Keep file inspection and editing in the
one-shot workflow unless interactivity is essential.

## Edit Safely

1. Run `git status --short`; completion means every pre-existing change is
   identified.
2. Inspect each affected file and nearby tests; completion means the patch has
   enough exact context for `git apply`.
3. Create a standard Git patch locally with paths relative to the remote
   project root.
4. Review the patch and confirm it contains no unrelated files.
5. Apply it:

```bash
python3 "$HELPER" apply-patch \
  HOST /absolute/project /local/change.patch
```

The helper sends the patch over stdin, runs `git apply --check`, and applies it
only when the check succeeds. It does not commit.

Do not edit remote files with `sed -i`, redirection, inline Python, or heredocs.
Do not overwrite an entire file when a focused patch is possible. Do not stash,
reset, clean, force-push, restart services, migrate data, or deploy unless the
user explicitly requests that action.

## Validate the Change

1. Run `git diff --check` and `git diff --stat` remotely.
2. Run focused tests in the selected project environment.
3. Run broader validation when proportionate to the change.
4. Report changed files, test results, and pre-existing dirty files.

Completion means every modified file is accounted for and every requested
validation result is reported, including failures or commands that could not
run.

## Authorization Boundaries

Read-only inspection and ordinary requested build/test commands are in scope.
Treat package installation, privilege escalation, service control, deployment,
database mutation, and destructive Git or filesystem operations as separate
actions requiring clear user authorization.

Never weaken host-key checking. Never use `StrictHostKeyChecking=no`. Never
expose an SSH shell or agent server directly to the public network.

## Common Pitfalls

1. **Assuming activation persists.** Add `--venv`, `--conda-name`, or
   `--conda-prefix` to every environment-dependent command.
2. **Guessing the environment.** Inspect project markers and ask when the
   choice remains ambiguous.
3. **Overwriting dirty work.** Record `git status --short` first and preserve
   unrelated changes.
4. **Forcing a failed patch.** Re-read the remote files and regenerate the
   patch; never bypass `git apply --check`.
5. **Retrying a mutation blindly.** After a connection interruption, inspect
   remote state before retrying.
6. **Changing SSH security to make it work.** Let the user resolve host-key or
   authentication failures through their trusted local SSH setup.

## Verification Checklist

- [ ] The SSH alias and absolute remote project root were confirmed.
- [ ] Pre-existing Git changes were identified and preserved.
- [ ] The correct virtualenv or Conda environment was verified when needed.
- [ ] Edits were applied through a reviewed, checked Git patch.
- [ ] `git diff --check` passed or its failure was reported.
- [ ] Relevant tests ran in the remote project environment.
- [ ] No credentials were requested, stored, or printed.
- [ ] No commit, deployment, service restart, or destructive action occurred
      without explicit authorization.
