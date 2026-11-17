---
name: strix
description: >
  Use when the user is getting started with Strix, choosing which Strix
  skill to run, installing from source, building the sandbox image, or
  writing a Strix .env. Start here before a Strix pentest, scan, or
  vulnerability fix.
license: Apache-2.0
metadata:
  author: usestrix
  homepage: https://docs.strix.ai
---

# Start with Strix

This skill picks how to run Strix and prepares the git checkout. Flags, the headless scan, exit codes, and the short result read live in the job skill you open next.

The checkout is the current directory when its `pyproject.toml` names `strix-agent`. Clone only when it does not.

Job skills are files in that checkout, not installed agent skills. After step 1 names one, read `<checkout>/skills/<skill-name>/SKILL.md` and follow that file. A missing file stops the run.

Stay in the checkout so reports land in `<checkout>/strix_runs/`.

The command prefix depends on the path from step 1. A preinstalled `strix` uses the binary on `PATH`. `uv run --env-file .env strix` is the prefix only after steps 3–5 have written `.env` and `.venv`.

| Reach this when | File |
| --- | --- |
| Scan lifecycle, agent graph, sandbox tools | [references/how-it-works.md](references/how-it-works.md) |
| A run directory exists and the short result read is not enough | [references/reports.md](references/reports.md) |
| Any setting beyond the `.env` block in step 4 | [references/configuration.md](references/configuration.md) |

## 1. Pick the path

| Situation | Job skill |
| --- | --- |
| `strix --version` already works, or the user wants the install script or pipx, then a general pentest | Step 2 for the skill files, then `penetration-testing-with-strix`. Skip steps 3–5 |
| This git checkout, or Strix is not installed and the user wants to build it | Steps 2–5, then the row that matches the job |
| No Docker, no LLM key, or a team dashboard | `managed-pentesting-with-strix`. Skip steps 2–5 |
| A whole product, and which test is still open | `application-security-testing` |
| A live web app | `web-app-penetration-testing` |
| An API | `api-security-testing` |
| An OWASP Top 10 assessment | `owasp-top-10-testing` |
| White-box review of a repo or tree | `find-security-vulnerabilities-in-code` |
| Fix findings from a finished run | `fix-security-vulnerabilities-with-strix` |
| CI or a pull-request gate | `ci-security-scanning-with-strix` |

Read the chosen job skill before launching a scan. That file confirms the target is one the user is allowed to test. A target the user did not name, or did not allow, stops here.

Every job skill except `managed-pentesting-with-strix` is read from `<checkout>/skills/<skill-name>/SKILL.md`. Step 2 creates that checkout before the read. `managed-pentesting-with-strix` is the one row that skips the checkout: read its file from the checkout when one already exists, and stop to report the missing path when it does not.

A preinstalled `strix` still uses the checkout skill files. Launch that scan with the `strix` binary already on `PATH`. Use `uv run --env-file .env strix` only after steps 3–5 have written `.env` and `.venv`.

**Done when** one row is chosen, its required setup steps are named, and the job skill file has been read.

## 2. Checkout

The working directory is the current directory when its `pyproject.toml` contains `name = "strix-agent"`. Otherwise:

```bash
git clone https://github.com/usestrix/strix.git
cd strix
```

**Done when** `pyproject.toml` names `strix-agent` and `containers/Dockerfile` is present.

| If this fails | First repair | Still failing |
| --- | --- | --- |
| `pyproject.toml` lacks `name = "strix-agent"` | Stop using that directory and clone the canonical URL | Stop. Report the path and the `name` line |
| `git clone` is non-zero | Re-run once against the same URL | Stop. Report the exit code. Leave the partial directory |

## 3. Sandbox image

Run `docker info` first. A non-zero exit stops the build. Switch to `managed-pentesting-with-strix` only when the user accepts a path with no local Docker.

From the checkout:

```bash
bash scripts/docker.sh
```

`scripts/docker.sh` tags `strix-sandbox:<tag>`. The tag defaults to `dev`. The first argument replaces it (`bash scripts/docker.sh 1.3.1`). The build is a Kali image plus the toolchains in `containers/Dockerfile`; wait for it.

**Done when** the script prints `Done: strix-sandbox:dev` (or the tag you passed) and `docker image inspect strix-sandbox:dev` exits 0.

The running scan uses `STRIX_IMAGE`. Put that same tag in `.env`. When `STRIX_IMAGE` is unset, startup pulls `RuntimeSettings.image` from `strix/config/settings.py` and leaves a locally built `strix-sandbox:dev` unused. Read that default before naming the image that would be pulled.

🔴 CHECKPOINT: skipping the build is a user decision. Leave `STRIX_IMAGE` unset and let the first scan pull the published image. Continue only after the user says to skip.

| If this fails | First repair | Still failing |
| --- | --- | --- |
| `docker info` is non-zero | Start Docker and re-run `docker info` | Stop, or take the managed path after the user accepts it |
| `scripts/docker.sh` is non-zero | Re-run the same command once | Stop. Keep the tag out of `.env` |
| The script finishes but `docker image inspect` is non-zero | Inspect the tag the script printed | Stop. Use the printed tag, not `dev`, when they differ |

## 4. `.env`

Strix reads the process environment, then `~/.strix/cli-config.json`. It does not open a project `.env`. `uv run --env-file .env` loads the file into the process. Precedence and the full key list are in [references/configuration.md](references/configuration.md).

An existing `<checkout>/.env` is the config. Read its key names, not its values. Keep it when `STRIX_LLM` is set and either `LLM_API_KEY` is set or both `LLM_API_BASE` and `LLM_EXTRA_HEADERS` are set. `STRIX_IMAGE` set to a tag that `docker image inspect` accepts is also kept. A kept file skips the write below.

Write `<checkout>/.env` with mode `0600` only when no file meets that test. The path is gitignored. 🔴 CHECKPOINT: ask the user for `STRIX_LLM` and `LLM_API_KEY` when they are not already available. The key stays in the file. A key pasted into chat or into the scan command line is a stop: remove it from the command and write it only to the `0600` file.

```bash
# <checkout>/.env
STRIX_LLM=
LLM_API_KEY=
STRIX_IMAGE=strix-sandbox:dev
```

`STRIX_LLM` is the LiteLLM model id the user names. `STRIX_IMAGE` matches the tag from step 3, and is omitted only when the user chose the published image.

**Done when** the file is mode `0600` or already kept, `STRIX_LLM` is non-empty, `STRIX_IMAGE` matches an image `docker image inspect` accepts (or is absent because the user chose the published image), and a hosted API model has either a non-empty `LLM_API_KEY` or both `LLM_API_BASE` and `LLM_EXTRA_HEADERS`. Local models, Vertex AI, and Bedrock are the exceptions in the configuration reference.

| If this fails | First repair | Still failing |
| --- | --- | --- |
| The write or `chmod 0600` is non-zero | Write the file again and re-check the mode | Stop. Launch no scan |
| `STRIX_LLM` is empty, and neither `LLM_API_KEY` nor the `LLM_API_BASE` plus `LLM_EXTRA_HEADERS` pair is set | Ask once for the missing value | Stop. Leave the empty key in the `0600` file |

## 5. Virtualenv

Python 3.12 or newer. uv selects the interpreter. From the checkout:

```bash
uv sync --frozen --no-dev
uv run --env-file .env strix --version
```

`uv sync` creates `<checkout>/.venv` and installs this project into it. `--frozen` installs `uv.lock` as cloned.

**Done when** `.venv` exists and the version command prints a version.

| If this fails | First repair | Still failing |
| --- | --- | --- |
| `uv sync` is non-zero | Re-run the same command once | Stop. Report the exit code |
| `strix --version` is non-zero | Re-run with `--env-file .env` | Stop. A setup failure blocks the job skill |

A scan that returns `status: interrupted`, or whose log shows LLM `408` or `503`, is a stopped run. Leave `strix_runs/<run>/` in place. Re-run the same target once. A second interrupt stops the job. LLM HTTP errors are not a reason to rebuild the image or rewrite `.env`.

Then follow the job skill from step 1, with the `uv run --env-file .env` prefix. Pass the user's target as an absolute path or a URL. `-t .` inside this checkout tests Strix itself.

## Do not

- Install a job skill named in step 1. Read `<checkout>/skills/<skill-name>/SKILL.md`.
- Fill in scan steps when that file is missing. Stop and report the missing path.
- Treat `strix --version` exiting 0, or an empty `vulnerabilities/` directory, as a finished test. The job skill owns the scan and its result.
- Put `LLM_API_KEY` in chat or on a command line.
- Write a model id the user did not choose into `STRIX_LLM`.
