# Add TokenLab to Hermes without changing the existing default

This helper targets official Hermes **0.21.3** (`v2026.9.14`, source `345cd2b057a452236de401d3534b8502a7465e8d`). It adds one named provider to the active `config.yaml`. It preserves other settings and their comments, saved accounts, the active account and the default model. It never asks for, prints or stores a new TokenLab key. Existing credential files stay unchanged, and the helper never requests inference.

Use the existing Hermes installation. The helper does not install or upgrade Hermes, change permissions, or run `hermes model`: that wizard changes the default model and active account. Native `hermes config set` rewrites YAML without preserving comments, so it is not used for this change. See the official [named provider contract](https://hermes-agent.nousresearch.com/docs/integrations/providers#named-custom-providers).

## Select the existing Python runtime and configuration

Run `hermes --version` to find the installed version and **Install directory**. For the official source installer, its Python is `<Install directory>/venv/bin/python` on macOS/Linux or `<Install directory>\venv\Scripts\python.exe` on Windows. Other distribution layouts must use their actual installed runtime. The helper uses the PyYAML **6.0.3** already included in Hermes 0.21.3. It does not run pip or guess another Python installation.

Run the helper directly with that Python, or pass its exact path with `--hermes-python` from Python 3.11+. A missing or different parser stops setup. Restoration only needs Python 3.11+, even after Hermes is removed.

For configuration, the helper honors `HERMES_HOME`; otherwise it uses `~/.hermes` on macOS/Linux or `%LOCALAPPDATA%\hermes` on Windows. It follows the root's `active_profile` when selecting the active named profile. Use `--hermes-home` to select an exact directory instead. Preview prints the chosen file. The install directory and configuration directory are different; do not substitute one for the other.

## Preview, apply and restore

Run from the installed `tokenlab-api-integration` Skill folder. Set `HERMES_PYTHON` below to the actual interpreter path identified above. It contains a path, not a credential.

macOS/Linux:

```bash
"$HERMES_PYTHON" scripts/configure_hermes.py --model gpt-5.6-luna
"$HERMES_PYTHON" scripts/configure_hermes.py --model gpt-5.6-luna --apply
```

Windows PowerShell:

```powershell
& $HermesPython scripts/configure_hermes.py --model gpt-5.6-luna
& $HermesPython scripts/configure_hermes.py --model gpt-5.6-luna --apply
```

Choose a current public model whose detail contract supports Chat Completions and tools. Use `--provider tokenlab-personal` when the default name is already owned by another configuration. Use `--hermes-bin` if the intended Hermes executable is not on PATH. The helper requires an explicit model and stores only `key_env: TOKENLAB_API_KEY`.

Rerunning unchanged setup is idempotent. An update remains reversible to the original pre-setup file. Restore with the same home and provider name:

```bash
python3 scripts/configure_hermes.py --restore
python3 scripts/configure_hermes.py --restore --apply
```

On Windows use `py -3` instead of `python3`. If setup created the file, restore removes it; otherwise restore puts back the original bytes. A later manual edit, edited backup, same-name provider/account, linked target, invalid or ambiguous YAML, concurrent change, active managed scope, or inherited WSL policy stops automatic setup. Do not remove policies or user edits to force it through. Preserve the backup and use the manual guide for that setup. Remove a leftover `.config.yaml.tokenlab-setup.lock` only after confirming no helper is running.

## Load the configuration explicitly

Set `TOKENLAB_API_KEY` through the intended profile's trusted `.env` or process environment without printing it or putting it in chat. Use the same `HERMES_HOME` printed by preview. Follow the helper's exact loading and launch commands: for a root directory they include `--profile default`, avoiding an unrelated sticky profile; a named `profiles/<name>` directory uses its explicit `HERMES_HOME`.

For a root configuration, after selecting that home for the current process:

```bash
hermes --profile default config get providers.tokenlab.api
hermes --profile default chat --provider custom:tokenlab --model gpt-5.6-luna
```

Use process-scoped environment changes and restore their prior values afterward. Normal launches retain the prior model and account. Inspecting the provider only verifies configuration loading, not key validity. Only when the user chooses a billable test should the client send a small task; inspect the complete response and matching TokenLab request record. A tool round trip and continuation are separate from configuration inspection.

## Verification scope

The tests exercise real fixed Hermes 0.21.3 with fake credentials, isolated configuration and loopback responses, alongside preview, idempotency, ownership conflicts and exact-byte restoration. The installed-client CI has separate macOS, Linux and native Windows jobs; a configured job is not a successful run. WSL, managed deployments, arbitrary future versions, production routing and billing are not implied by local or CI fixture results.
