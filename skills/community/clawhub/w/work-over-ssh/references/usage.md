# Using Work Over SSH

## Required prompt fields

Include all four fields whenever starting work:

1. **SSH server** — the exact host or alias accepted by local `ssh`, such as
   `devbox` or `user@example.com`.
2. **Project path** — the absolute path to the remote Git project, such as
   `/srv/apps/payments`.
3. **Environment** — one of:
   - `virtualenv <path>` for a relative or absolute virtualenv path.
   - `conda name <name>` for a named Conda environment.
   - `conda prefix <absolute-path>` for a Conda environment prefix.
   - `none` when the project has no dedicated environment.
4. **Task** — the specific inspection, fix, test, or change to perform.

Do not connect until the first three fields are present. If the environment is
unknown, ask the user instead of guessing. Environment values refer to the
remote server, not the local machine.

## Recommended prompt template

```text
Use $work-over-ssh.

SSH server: <host-or-alias>
Project path: </absolute/remote/project/path>
Environment: <virtualenv PATH | conda name NAME | conda prefix PATH | none>

Task: <what you want changed, inspected, or tested>

Preserve existing uncommitted changes. Do not commit, deploy, install packages,
or restart services unless I explicitly request it.
```

Repeat these fields in every new chat or session. Do not assume that a previous
session's target or environment still applies.

## Virtualenv example

```text
Use $work-over-ssh.

SSH server: devbox
Project path: /srv/apps/payments
Environment: virtualenv .venv

Task: Fix the failing authentication tests and run the focused pytest suite.
Preserve existing uncommitted changes. Do not commit or deploy.
```

An absolute virtualenv path is also valid:

```text
Environment: virtualenv /opt/venvs/payments
```

## Conda environment example

```text
Use $work-over-ssh.

SSH server: gpu-server
Project path: /home/ml/training-service
Environment: conda name training

Task: Diagnose the CUDA import failure and report the root cause. Do not modify
files until the diagnosis is complete.
```

Use a prefix when the environment is selected by path:

```text
Environment: conda prefix /opt/conda/envs/training
```

## Project without an environment

```text
Use $work-over-ssh.

SSH server: web01
Project path: /var/www/frontend
Environment: none

Task: Inspect the current Git status and run the documented frontend tests.
```

`none` means do not add virtualenv or Conda options. It does not authorize
installing dependencies globally.

## Safe first-use prompt

Use this before requesting edits on a new server:

```text
Use $work-over-ssh.

SSH server: devbox
Project path: /srv/apps/payments
Environment: virtualenv .venv

Task: Verify the SSH connection, remote Git root, current branch and status,
and Python executable. Do not modify anything.
```

The expected first-use sequence is:

1. Verify the SSH connection and project directory.
2. Confirm the Git root, branch, and pre-existing changes.
3. Confirm the selected environment and interpreter when applicable.
4. Report the results before any mutation.

## Do not include secrets

Never put any of these values in the prompt or skill files:

- SSH passwords.
- Private keys or private-key contents.
- API tokens.
- `.env` contents.
- Conda or application credentials.

Configure SSH authentication locally before invoking the skill. The prompt
should contain only the non-secret host identifier, project path, environment
selector, and task.
