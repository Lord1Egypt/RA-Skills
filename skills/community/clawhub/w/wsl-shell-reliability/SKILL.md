---
name: wsl-shell-reliability
description: Reliability-first shell selection policy for AI agents on Windows. Choose WSL or PowerShell based on execution risk, not preference.
license: MIT
compatibility: Windows (WSL optional; recommended for POSIX-fragile workflows)
metadata:
  author: simon
  version: "2.0"
---

# WSL Shell Reliability

Use this skill to maximize terminal command success on Windows.

This skill does **not** force WSL.
It enforces a reliability-first policy:

- pick the shell with lower failure risk,
- preserve command intent across fallback,
- never switch shells silently.

## Trigger conditions

- Any terminal execution task on Windows.
- AI-generated commands that look bash/POSIX-oriented.
- Repeated failures caused by quoting/path/shell mismatch.

## One-screen decision table

| Question | If Yes | If No |
| --- | --- | --- |
| Windows-native task/tool? | Use **PowerShell/CMD** | Next question |
| POSIX/bash semantics required? | Use **WSL/bash** | Next question |
| Need Linux-first parity? | Prefer **WSL/bash** | Next question |
| High Windows-shell parse risk? | Prefer **WSL/bash** | Next question |
| Both paths low risk? | Pick shell with fewer moving parts | N/A |

Examples:

- Windows-native: `winget`, `reg`, `netsh`, `.exe/.msi`, service/system ops.
- POSIX-heavy: `rm -rf`, `export`, `./script.sh`, `grep/sed/awk`, complex pipes.

## Rule priority (conflict resolution)

Apply rules in this priority order when guidance appears to conflict:

1. **Windows-native exclusions** (must use PowerShell/CMD).
2. **Decision table hard signals** (POSIX dependence, high parse risk).
3. **Fallback policy + intent preservation**.
4. **Convenience preferences** (tool availability, fewer steps).

If still ambiguous, choose the shell with lower execution-failure risk.

## Windows-native exclusions (prefer PowerShell/CMD)

- `winget`, `scoop`, `choco`
- PowerShell cmdlets and registry/service/system commands
- `.msi`/`.exe` installer flows
- Windows-targeted `msbuild`/`.NET` packaging chains

## Execution protocol

1. Select shell with the decision table.
2. Generate syntax for that shell (do not mix grammar).
3. Execute command.
4. If failure is shell-related, fallback to the other shell.
5. Preserve intent exactly; only translate syntax.
6. State fallback explicitly.

## Shell-aware generation rules

- **WSL/bash**: POSIX syntax allowed.
- **PowerShell**: PowerShell-native quoting/escaping.
- **CMD**: use only when required by task/tool.

Do not run bash syntax directly in PowerShell/CMD.

## WSL templates

- `wsl.exe -e bash --noprofile --norc -lc "<command>"`
- `wsl.exe -e bash --noprofile --norc -lc "cd /mnt/<drive>/<path> && <command>"`

## Quick translation hints (bash -> PowerShell)

- `export FOO=bar` -> `$env:FOO = "bar"`
- `rm -rf <path>` -> `Remove-Item -Recurse -Force <path>`
- `cp -r a b` -> `Copy-Item a b -Recurse`
- `mv a b` -> `Move-Item a b`
- `cat file` -> `Get-Content file`

Use translations only when fallback requires them.

## Guardrails

- Never silently switch shells.
- Never change command semantics when switching shells.
- Never install tools just to enforce one-shell purity.
- Prefer existing toolchain in the selected shell first.

## Fallback policy

Fallback to the other shell when:

- WSL is unavailable or unstable,
- the tool cannot be resolved in current shell,
- task is clearly Windows-native,
- command fails due to shell parsing/quoting mismatch.

When falling back, report:

1. what failed,
2. why shell changed,
3. equivalent command intent preserved.

## Known limitations

- Some enterprise environments disable WSL installation/execution.
- VPN/proxy/DNS policies may break package/network operations in one shell.
- Cross-filesystem operations can have inconsistent performance.
- Security policies may block execution scripts in PowerShell.

In these cases, prefer explicit fallback and report constraints clearly.

## References

Deep technical notes and examples:

- [references/REFERENCE.md](references/REFERENCE.md)
- [references/SCENARIOS.md](references/SCENARIOS.md)
