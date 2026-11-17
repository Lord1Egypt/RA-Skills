# CLI Workflow

Canonical docs:

- Installation: https://docs.wavedash.com/cli/installation
- Authentication: https://docs.wavedash.com/cli/authentication
- Configuration: https://docs.wavedash.com/cli/configuration
- Commands: https://docs.wavedash.com/cli/commands
- Quickstart: https://docs.wavedash.com/getting-started/quickstart
- CI/CD: https://docs.wavedash.com/tutorials/ci-cd

## Install the CLI

If `wavedash --version` is unavailable, guide the user to install the CLI.

macOS, Linux, WSL:

```bash
curl -fsSL https://wavedash.com/cli/install.sh | sh
```

Homebrew:

```bash
brew install wvdsh/tap/wavedash
```

Windows PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass; irm https://wavedash.com/cli/install.ps1 | iex
```

Verify:

```bash
wavedash --version
```

## Authenticate

Local desktop:

```bash
wavedash auth login
wavedash auth status
```

CI, cloud agents, or headless environments:

```bash
export WAVEDASH_TOKEN=wd_...
wavedash auth status --json --no-color --no-update-check
```

Use `WAVEDASH_TOKEN` for automation. Do not ask an agent to complete browser
login in a headless environment. To store a token without exposing it in shell
history, pipe it through stdin when supported:

```bash
printf '%s' "$WAVEDASH_TOKEN" | wavedash auth login --token-stdin --no-color --no-update-check
```

If an installed CLI rejects `--json`, `--no-color`, `--no-update-check`, or
`--token-stdin`, it is older than the agent-friendly CLI. Retry the command
without the unsupported flag and tell the user to update the CLI.

## Initialize the project

Interactive local setup:

```bash
wavedash init
```

Scripted setup with an existing team and game:

```bash
wavedash init --team-id TEAM_ID --game-id GAME_ID --upload-dir dist --engine custom --force --json
```

Scripted setup that creates a team and game:

```bash
wavedash init --team-name "My Studio" --game-title "My Game" --upload-dir dist --engine custom --force --json
```

Verify `wavedash.toml` has the right `game_id` and `upload_dir`. The upload
directory must contain the built `index.html`.

## Test, upload, publish

Build the game with the project’s normal build command, then test locally:

```bash
wavedash dev
```

Upload a build:

```bash
wavedash build push --json --no-color --no-update-check
```

The upload command returns or prints a build ID. Publishing makes that build
live for players, so only do it when the user asks:

```bash
wavedash publish BUILD_ID --json --no-color --no-update-check
```

After publishing, open the public game URL in a fresh browser and verify the
uploaded build works end to end.
