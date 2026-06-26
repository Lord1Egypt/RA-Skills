# Weekend Scout — Installation Guide

## Prerequisites

- Python 3.10 or later
- At least one of: Claude Code, OpenAI Codex, or OpenClaw

## One-Liner Install

```bash
git clone https://github.com/goooroooX/Weekend-Scout.git
cd Weekend-Scout
python install/install_skill.py --with-pip
```

This command:
1. Installs the `weekend_scout` Python package (via pip)
2. Copies the skill to your detected global skill directories
3. Pre-downloads GeoNames city data to the cache

The copied skill is bound to the exact Python interpreter that ran the installer,
so later skill runs use the same environment that contains `weekend-scout`,
`pyyaml`, and the other package dependencies.
If `python -m pip` is missing, the installer first tries
`python -m ensurepip --upgrade --default-pip`.
This uses only the Python standard library and does not download `get-pip.py`.
If that Python build does not include `ensurepip`, the installer stops and tells
you the platform-appropriate manual recovery step before retrying:
distro package-manager suggestions on Linux, or Python repair/reinstall
guidance on Windows. The installer never runs `sudo` or OS package manager
commands automatically.

On Linux systems where pip reports an externally managed environment (PEP 668),
prefer this one-shot override:

```bash
python install/install_skill.py --with-pip --break-system-packages
```

Optional persistent workaround:

```bash
pip config set global.break-system-packages true
```

Prefer the installer flag first, because it is scoped to this install command
instead of changing pip behavior globally.

When `--platform` is omitted, the installer copies only to the platforms it
actually detects on that machine.

---

## Claude Code (recommended)

### Project-scoped install (already in the repo)

If you cloned the repo into a project you work in, the skill is already available
at `.claude/skills/weekend-scout/SKILL.md`. Claude Code discovers it automatically.

### Global install

```bash
pip install .
python -m weekend_scout install-skill --platform claude-code
```

The skill is installed to `~/.claude/skills/weekend-scout/`.

### Verifying

Open Claude Code and type `/weekend-scout`. You should see the skill in the
command palette (or it loads immediately).

### Using

```
/weekend-scout
/weekend-scout Warsaw 200
/weekend-scout --cached-only
```

---

## OpenAI Codex

### Install

```bash
pip install .
python -m weekend_scout install-skill --platform codex
```

Files installed to `~/.agents/skills/weekend-scout/`:
- `SKILL.md` — skill instructions
- `agents/openai.yaml` — Codex-specific metadata (disables implicit invocation)

### Verifying

In Codex, type `$weekend-scout` or open the `/skills` menu and look for Weekend Scout.

### Using

```
$weekend-scout
$weekend-scout Berlin 150
```

---

## OpenClaw

### Install

```bash
pip install .
python -m weekend_scout install-skill --platform openclaw
```

Files installed to `~/.openclaw/skills/weekend-scout/`.

### Verifying

Start or restart your OpenClaw session. Type `weekend-scout` or check the available
skills list.

---

## Install All Platforms

```bash
python install/install_skill.py --platform all --with-pip
```

---

## Manual Package-Backed Installation

If you prefer to install manually after `pip install .`, use the package CLI:

```bash
python -m weekend_scout install-skill --platform <claude-code|codex|openclaw|all>
```

This is preferred over raw file copying because it binds installed skill commands
to the interpreter that already has the package dependencies.

Repo paths for reference:

| Platform   | Source in repo                           | Destination                          |
|------------|------------------------------------------|--------------------------------------|
| Claude Code | `.claude/skills/weekend-scout/`         | `~/.claude/skills/weekend-scout/`    |
| Codex       | `.agents/skills/weekend-scout/`         | `~/.agents/skills/weekend-scout/`    |
| OpenClaw    | `.openclaw/skills/weekend-scout/`       | `~/.openclaw/skills/weekend-scout/`  |

For Codex, also copy `agents/openai.yaml` into the destination directory.
The OpenClaw repo copy is a generated artifact for packaging/staging in this repo; the
supported installed location remains `~/.openclaw/skills/weekend-scout/`.

---

## Advanced: Repo-Copy Install Without Pip

Only use this if the same Python interpreter already has `weekend-scout`
installed already, for example via `pip install -e ".[dev]"`.

```bash
python install/install_skill.py --platform <claude-code|codex|openclaw|all>
```

This path only copies the generated skill files from the repo checkout.
It does not install the package or dependencies for you.

---

## Updating

**Users** — re-clone and re-run the installer (same as initial install):

```bash
git clone https://github.com/goooroooX/Weekend-Scout.git
cd Weekend-Scout
python install/install_skill.py --with-pip
```

**Developers** — pull and reinstall:

```bash
git pull
pip install -e ".[dev]"
python skill_template/generate.py   # only if template was changed
python -m weekend_scout install-skill --platform <claude-code|codex|openclaw|all>
```

---

## Uninstalling

Primary uninstall command:

```bash
python install/install_skill.py --uninstall
```

Examples:

```bash
# Remove all detected installed skill folders plus the package
python install/install_skill.py --uninstall

# Remove only one platform's skill folder plus the package
python install/install_skill.py --uninstall --platform openclaw

# Remove all known platform skill folders plus the package
python install/install_skill.py --uninstall --platform all

# Externally managed Python uninstall
python install/install_skill.py --uninstall --break-system-packages
```

This removes the installed skill files and uninstalls the `weekend-scout`
package from the same Python interpreter.
It does **not** remove `.weekend_scout/` config, cache, logs, or downloaded data.

---

## Configuration

After installation, Weekend Scout will guide you through a one-time setup the first
time you invoke it. You can also configure it directly:

```bash
python -m weekend_scout config telegram_bot_token YOUR_BOT_TOKEN
python -m weekend_scout config telegram_chat_id YOUR_CHAT_ID
```

See the main [README](../README.md) for full configuration options.
