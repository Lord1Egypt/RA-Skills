# Configure an explicit TokenLab layer for OpenCode

Requirements: Python 3.11+ and an installed OpenCode CLI, version 1.18.31 or newer. The installed-client check pins official `opencode-ai@1.18.31`; it does not establish compatibility with every later release. There are no Python package dependencies. See the official [custom provider](https://opencode.ai/docs/providers/#custom-provider) and [configuration layers](https://opencode.ai/docs/config/#custom-path) references.

The helper creates a separate `tokenlab.jsonc` layer. OpenCode loads it only when that invocation selects it with `OPENCODE_CONFIG`. It does not edit your normal OpenCode configuration, account, permissions, or default model. This separation matters: putting the only configured provider into an automatically loaded file can change OpenCode's implicit default even without setting `model`.

## Preview and apply

Run from this repository root, or substitute the script's installed location:

```bash
python3 skills/tokenlab-api-integration/scripts/configure_opencode.py --model gpt-5.6-luna
python3 skills/tokenlab-api-integration/scripts/configure_opencode.py --model gpt-5.6-luna --apply
```

On Windows PowerShell, use `py -3` in place of `python3`. The preview prints the target path, provider/model, endpoint, and environment-variable reference.

The default target is `$XDG_CONFIG_HOME/opencode/tokenlab.jsonc`, or `~/.config/opencode/tokenlab.jsonc` when that variable is unset or empty. Use `--config <path>` for another independent layer, `--provider tokenlab-personal` for another name, or `--opencode-bin <path>` for a specific CLI. Automatically loaded filenames such as `opencode.json` and `opencode.jsonc` are rejected. Existing provider entries in known user configuration files and saved accounts are checked for name conflicts; the helper does not take them over or widen a provider allowlist.

An existing `OPENCODE_CONFIG` selecting another file or an inline `OPENCODE_CONFIG_CONTENT` is a conflict. Keep that setup and run the helper in a separate launch environment. Project, organization, and managed settings remain authoritative; this helper does not override their policies or prove every merged setting. Use the actual target path printed by the helper in the launch commands below.

Choose a current model whose public detail contract declares `openai_chat_completions`. This helper configures `@ai-sdk/openai-compatible` and does not fetch model availability, infer capabilities, or silently switch protocols.

## Launch and check

Provide the complete `TOKENLAB_API_KEY` through your local secret manager or session environment. The JSONC contains only `{env:TOKENLAB_API_KEY}`; never pass a key to this helper or commit it to a file.

macOS/Linux, using the default path when `XDG_CONFIG_HOME` is unset:

```bash
OPENCODE_CONFIG="$HOME/.config/opencode/tokenlab.jsonc" opencode models tokenlab
OPENCODE_CONFIG="$HOME/.config/opencode/tokenlab.jsonc" opencode --model tokenlab/gpt-5.6-luna
```

Windows PowerShell, restoring the prior process environment afterward:

```powershell
$previousConfig = $env:OPENCODE_CONFIG
try {
  $env:OPENCODE_CONFIG = "$HOME\.config\opencode\tokenlab.jsonc"
  opencode models tokenlab
  opencode --model tokenlab/gpt-5.6-luna
} finally {
  if ($null -eq $previousConfig) {
    Remove-Item Env:OPENCODE_CONFIG -ErrorAction SilentlyContinue
  } else {
    $env:OPENCODE_CONFIG = $previousConfig
  }
}
```

Start normally without this layer to retain the ordinary setup. Do not add `OPENCODE_CONFIG` to a shell profile just to follow this guide. Native Windows and WSL have separate installations and configuration paths.

Model discovery demonstrates local configuration loading. It does not validate the key, availability, tool behavior, continuation, or billing. A live inference test requires its own authorization and a matching TokenLab request record. OpenCode's `debug config` can expose resolved credentials; do not paste or log its raw output.

## Update and restore

Repeat the helper with another explicit model to update its unedited layer. Identical runs make no writes. Existing JSONC values, comments, ordering, and formatting are retained; OpenCode output omits a BOM because the client otherwise rewrites it on load. The original backup retains every original byte, including BOM/CRLF.

```bash
python3 skills/tokenlab-api-integration/scripts/configure_opencode.py --restore
python3 skills/tokenlab-api-integration/scripts/configure_opencode.py --restore --apply
```

Use the same `--config` and `--provider` when customized. Restore returns the original file bytes, or removes the layer if it was initially absent. It consumes the `.tokenlab.jsonc.tokenlab.tokenlab-backup` original backup and does not create unlimited update history. Updates never replace that original with a later generated version.

User edits, linked files, a conflicting provider, changed files between inspection and writing, and invalid backups stop the helper. If a previous run was interrupted, retain the backup; retry or restore after confirming no helper is running. Remove a leftover `.tokenlab.jsonc.tokenlab-setup.lock` only after that check. Restoring does not require the client to remain installed.

## Verification scope

Unit coverage includes lossless insertion, preview, repeated runs, updates, original-byte restoration, interrupted writes, concurrent changes, existing accounts, cross-file provider conflicts, empty environment variables, and both clients' JSONC syntax. The installed-client suite pins OpenCode 1.18.31 on Ubuntu, macOS, and Windows in CI. On macOS it runs with OS-denied networking. It verifies ordinary configuration loading excludes TokenLab, explicit loading resolves the intended provider, and default model/permission/account bytes remain intact. No paid model request is part of this suite; CI setup alone is not a passed CI result.

A separate first-request test changes only the endpoint in a disposable generated layer to a local receiver. The pinned client sends Chat Completions without `temperature`; it adds `max_tokens: 32000` and may make an auxiliary title request as well as the main request. This checks actual request serialization and streamed-result delivery. It does not prove current upstream parameter acceptance or billing; the public model detail must supply those constraints, and a separately authorized live test must confirm the result.
