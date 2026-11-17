# Configure a TokenLab profile for Codex

This helper adds a separate Codex profile. It does not install Codex, store an API key, change your default model, or configure MCP and other clients.

Requirements: Python 3.11 or newer and an installed Codex CLI that supports separate profile files. There are no Python package dependencies. The helper checks the CLI version and `--help` before creating or updating a profile.

Codex 0.134.0+ loads `<CODEX_HOME>/<name>.config.toml` with `codex --profile <name>`. These are top-level configuration layers, not legacy `[profiles.<name>]` tables. See the [official configuration reference](https://learn.chatgpt.com/docs/config-file/config-advanced#profiles).

## Preview and apply

Run these commands from this repository's root. If the Skill is already installed, use its actual `scripts/configure_codex.py` path instead.

macOS, Linux or WSL:

```bash
python3 --version
python3 skills/tokenlab-api-integration/scripts/configure_codex.py \
  --model gpt-5.6-sol --reasoning-effort xhigh

# After reviewing the preview, repeat with --apply:
python3 skills/tokenlab-api-integration/scripts/configure_codex.py \
  --model gpt-5.6-sol --reasoning-effort xhigh --apply
```

Windows PowerShell, with Python 3.11+ installed:

```powershell
py -3 --version
py -3 skills/tokenlab-api-integration/scripts/configure_codex.py `
  --model gpt-5.6-sol --reasoning-effort xhigh

py -3 skills/tokenlab-api-integration/scripts/configure_codex.py `
  --model gpt-5.6-sol --reasoning-effort xhigh --apply
```

The default directory is `CODEX_HOME`, or `~/.codex` if unset. Pass `--codex-home <directory>` to select a test directory or another existing Codex home. Native Windows and WSL have separate installations and homes. Use `--codex-bin <path>` when the desired CLI is not on `PATH`.

Choose a current model that declares Responses support. The model and optional reasoning effort are explicit inputs; the helper does not fetch model availability or check whether that model supports the chosen effort. Omitting `--reasoning-effort` preserves inherited reasoning settings.

The preview shows only the intended provider, model, endpoint, environment-variable name and target path. It does not print existing configuration. The helper creates `tokenlab.config.toml` and leaves `config.toml`, `auth.json`, accounts, permission policies and the default provider unchanged. If `tokenlab` is already used by another configuration, choose a name such as `--profile tokenlab-personal`. It does not take over an existing profile.

## Start and verify

Set `TOKENLAB_API_KEY` through your existing local secret manager or launch environment. Never pass the key as a helper argument or paste it into chat. The helper only writes the environment-variable reference and does not persist the key.

Start with the same `CODEX_HOME` used above:

```bash
codex --profile tokenlab
```

Use `/status` to inspect the active model and permissions. Higher-priority project or CLI configuration can still affect the session. A successful helper run proves only the configuration operation. A real response, tool round trip and continuation require a separately authorized paid test and a matching TokenLab request record.

## Update and restore

Run the helper with the new model or effort, preview it, then add `--apply`. Repeating an identical configuration makes no writes. Only an unedited profile created by this helper can be updated. Before an update, its prior contents are saved beside it as `.tokenlab.config.toml.tokenlab-backup`.

```bash
# Preview restoration, then apply it:
python3 skills/tokenlab-api-integration/scripts/configure_codex.py --restore
python3 skills/tokenlab-api-integration/scripts/configure_codex.py --restore --apply
```

Restoration reverts the last helper update and consumes that backup. If there is no update backup, it removes the profile created by the helper. It does not retain unlimited history. To stop using TokenLab without changing any files, start Codex without this profile.

The helper checks ownership and content hashes. If you edit the profile or backup yourself, it stops instead of overwriting your work. It also stops if it detects configuration changes between inspection and writing. A leftover `.tokenlab.tokenlab-setup.lock` may indicate an interrupted helper: first confirm that no helper is running, then remove only that lock before retrying. If another helper holds the lock, this run stops and leaves that lock in place.

## Verification scope

- Local verification: macOS, Python 3.13, installed Codex 0.149.0. A temporary home and an OS rule denying all networking demonstrated selection of the profile's model/provider/effort. Execution then stopped at the deliberately missing environment key. No authenticated model request was made.
- Unit tests cover creation, unchanged repeat runs, updates, backup/restoration, ownership conflicts, linked files, concurrent changes, atomic-write failure and credential-free CLI detection.
- An isolated Linux ARM64 container also loaded installed Codex 0.149.0 with both the original default and TokenLab profile, then stopped at the missing environment key. Networking was disabled; preview, repeated apply and restoration preserved the original configuration bytes.
- Installed-client CI now covers macOS, Linux and native Windows with the exact versions under test. A configured workflow is not a passing run; Windows and WSL are not yet locally verified. Linux container results do not establish Windows or WSL behavior.

```bash
python3 -m unittest discover -s tests -p 'test_configure_codex*.py'

# macOS only; installed Codex 0.149.0, temporary home, denied networking:
TOKENLAB_CODEX_OFFLINE_TEST=1 python3 -m unittest discover -s tests -p 'test_configure_codex*.py'

# Any supported OS with the exact installed clients; temporary homes, no inference:
TOKENLAB_INSTALLED_CLIENT_TESTS=1 python3 -m unittest discover -s tests -p 'test_configure_*.py'
```
