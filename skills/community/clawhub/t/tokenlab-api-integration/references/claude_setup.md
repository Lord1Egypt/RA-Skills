# Start Claude Code with TokenLab for one session

This helper creates an explicit Python launcher beside your existing Claude configuration. Starting ordinary `claude` keeps your normal account and default model. The helper does not install Claude Code, change permission settings, log in or out, or put a key in a file.

Requirements: Python 3.11+ and Claude Code 2.1.263+. No Python packages are needed. The CLI version and advertised session options are checked before creating or starting the launcher. Keep this installed Skill directory in place: the generated launcher imports its implementation from here.

## The actual Claude Code interface

Claude Code supports a session model through `--model` and an additional settings layer through `--settings`. Both leave the saved default intact. The launcher uses those options; it does not invent a Claude profile format or put `$TOKENLAB_API_KEY` into JSON expecting interpolation. See [session settings](https://code.claude.com/docs/en/settings) and the [CLI reference](https://code.claude.com/docs/en/cli-reference).

At launch, it reads `TOKENLAB_API_KEY` from the local environment and maps it to the child process's `ANTHROPIC_AUTH_TOKEN`. Claude sends this as Bearer authentication, supported by TokenLab's Messages endpoint. This intentionally uses Claude's gateway authentication path. Existing API-key settings, credential helpers, custom authentication headers and cloud-provider switches are disabled only for that launched session. Their saved values stay intact. This also avoids changing Claude's remembered choice between a subscription and an `ANTHROPIC_API_KEY`. See [authentication precedence](https://code.claude.com/docs/en/authentication#authentication-precedence).

The endpoint root is `https://api.tokenlab.sh`, without `/v1`. The launcher does not set permission modes, disable settings sources, or use `--bare`. Existing permission rules continue to load.

## Preview, apply and launch

Run from this repository's root, or replace the script path with its location inside your installed Skill. These examples use the default `~/.claude` directory; for a custom `CLAUDE_CONFIG_DIR`, use the exact launcher path shown in the preview.

macOS or Linux:

```bash
python3 --version
python3 skills/tokenlab-api-integration/scripts/configure_claude.py \
  --model claude-sonnet-4-6

# Review the preview, then explicitly apply it:
python3 skills/tokenlab-api-integration/scripts/configure_claude.py \
  --model claude-sonnet-4-6 --apply

# Supply TOKENLAB_API_KEY through your local secret manager or launch environment.
python3 "$HOME/.claude/tokenlab-claude.py" --auth-status
python3 "$HOME/.claude/tokenlab-claude.py"
```

Windows PowerShell, with Python 3.11+:

```powershell
py -3 --version
py -3 skills/tokenlab-api-integration/scripts/configure_claude.py `
  --model claude-sonnet-4-6

py -3 skills/tokenlab-api-integration/scripts/configure_claude.py `
  --model claude-sonnet-4-6 --apply

py -3 "$HOME\.claude\tokenlab-claude.py" --auth-status
py -3 "$HOME\.claude\tokenlab-claude.py"
```

Use `--claude-config-dir <directory>` for an explicit existing home or a temporary test directory, and `--claude-bin <executable>` if the desired CLI is not on `PATH`. Choose `--name tokenlab-claude-personal` if the default launcher name already belongs to another setup. No shell profile, PATH or execution policy is changed.

Always choose a current public model with Messages support. The example is not a live availability guarantee. Moving Claude aliases such as `sonnet`, `opus` and `default` are refused. The helper does not query model supply or test protocol compatibility. It supplies your exact primary model and clears a configured fallback chain for this session. Existing subagent/model-tier choices are not repinned; their availability and paid tool workflows need separate validation. See [model selection and fallback chains](https://code.claude.com/docs/en/model-config).

## Check what was selected

`--auth-status` invokes Claude's local authentication inspection without requesting a model response. It confirms the session Bearer source is selected, not whether the key is valid. Claude labels this source `oauth_token` and reports no API-key source; that label alone does not mean it is using your saved subscription.

In the interactive session, inspect `/status` for the active model and permissions. Do not use `/login` or `/logout` to configure this launcher. Claude normally writes its own session history and metadata; actions you explicitly take inside Claude, such as saving another default with `/model`, still have their normal effects.

A paid request is explicit, for example:

```bash
python3 "$HOME/.claude/tokenlab-claude.py" --print "Reply with OK"
```

The first version accepts only its documented launch options: `--auth-status`, `--print`, `--output-format`, and `--no-session-persistence` for print mode. It does not forward arbitrary settings, provider or model overrides. A successful response, tool round trip and continuation must be checked against TokenLab Requests separately. Configuration creation and a local auth check are not paid-request evidence.

## Conflicts and recovery

The launcher checks user settings and the working directory's `.claude` ancestry each time it starts. A settings `env` entry for `ANTHROPIC_AUTH_TOKEN`, even an empty one, overrides the shell value and cannot safely represent a dynamic TokenLab key. The helper stops on that conflict instead of silently taking over the file. It also stops on configuration-location overrides, model remapping and forced-login policies.

This first version is for personal CLI setups. Recognized managed files, cached remote settings, macOS managed preferences and Windows registry policies stop automatic setup. Claude apps gateway or another authentication source also stops the launch. WSL launch is currently refused because inherited Windows policy has not been validated. Do not remove organization policy to get past a check; keep the existing setup and use the [official managed configuration process](https://code.claude.com/docs/en/managed-settings).

Running the same configuration again changes nothing. An update first backs up the previous helper-owned launcher as `.tokenlab-claude.py.tokenlab-backup`. The helper checks its marker and content hash; an existing launcher or backup edited by somebody else is left alone. It uses the same atomic file operations as the Codex helper. Read-only settings may use dotfiles symlinks; launchers and backups may not.

```bash
python3 skills/tokenlab-api-integration/scripts/configure_claude.py --restore
python3 skills/tokenlab-api-integration/scripts/configure_claude.py --restore --apply
```

Restoration reverts the last update and consumes that backup. With no update backup, it removes the launcher the helper created. Use the same `--claude-config-dir` and `--name` as setup. It never restores over a later manual edit. A leftover `.tokenlab-claude.tokenlab-setup.lock` requires checking for another running helper before removing only the stale lock.

## Verification scope

- macOS, Python 3.13 and installed Claude Code 2.1.263: the actual helper and generated launcher were run with a temporary home, a dummy token and OS-denied networking. Claude's initial event showed the selected model, the existing `plan` permission mode and no existing API-key source. The old credential helper did not run; existing account storage was unchanged. The model call could not succeed under the network denial.
- Tests cover preview, apply, unchanged repeats, updates, restoration, concurrent edits, file ownership, linked settings, credential-free discovery and rejection of conflicting authentication sources. The Codex helper's tests, including its actual macOS CLI check, also passed after sharing the file operations.
- Claude Code 2.1.263 also passed actual local authentication inspection on macOS and in an isolated Linux ARM64 container. The generated launcher selected its session Bearer source, left the original account/settings bytes intact and did not store or print the fixture key. Linux networking was disabled; no inference was requested.
- Installed-client CI now covers macOS, Linux and native Windows with exact versions. Windows results require a successful run of that job and are not claimed from the Linux container. WSL and managed configurations remain outside this automatic slice.

```bash
python3 -m unittest discover -s tests -p 'test_configure_*.py'

# macOS only: both installed clients, disposable homes, no authenticated API requests
TOKENLAB_CODEX_OFFLINE_TEST=1 TOKENLAB_CLAUDE_OFFLINE_TEST=1 \
  python3 -m unittest discover -s tests -p 'test_configure_*.py'

# Any supported OS with the exact installed clients; temporary homes, no inference:
TOKENLAB_INSTALLED_CLIENT_TESTS=1 python3 -m unittest discover -s tests -p 'test_configure_*.py'
```
