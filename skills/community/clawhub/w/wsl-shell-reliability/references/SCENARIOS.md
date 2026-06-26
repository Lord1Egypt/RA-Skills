# Scenarios: When to Use WSL vs PowerShell

Use these examples to apply the decision table quickly.

## Prefer WSL

### Scenario A: POSIX-heavy cleanup + build

Command intent:

- remove build output,
- export env variable,
- run shell script.

Why WSL:

- Requires POSIX semantics (`rm -rf`, `export`, `./script.sh`).

### Scenario B: Linux-first project scripts

Project has Unix-oriented scripts and CI steps.

Why WSL:

- Better parity with Linux CI/runtime behavior.

### Scenario C: Quoting is fragile in Windows shell

Nested quotes + paths with spaces + mixed separators.

Why WSL:

- Lower parsing ambiguity for POSIX-style command chains.

## Prefer PowerShell

### Scenario D: Windows package installation

Command intent: install tool with `winget` and verify in Windows context.

Why PowerShell:

- Native Windows workflow.

### Scenario E: Registry/service/system management

Command intent: inspect registry, adjust service, run system diagnostics.

Why PowerShell:

- Windows-native APIs/commands.

### Scenario F: Windows-targeted build pipeline

Command intent: run Windows-specific `.NET`/`msbuild` packaging.

Why PowerShell:

- Toolchain and output target are Windows-native.

## Fallback examples

### WSL -> PowerShell fallback

- Trigger: WSL unavailable or command fails due to distro/tool resolution.
- Action: execute equivalent PowerShell command.
- Must report shell switch and preserved intent.

### PowerShell -> WSL fallback

- Trigger: PowerShell parsing/quoting breaks POSIX-style command.
- Action: execute intent-equivalent command in WSL.
- Must report shell switch and preserved intent.
