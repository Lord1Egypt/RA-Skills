# Reference: Reliability Notes for Windows Terminal Execution

This document supports `SKILL.md` with detailed operational guidance.

## 1) Shell mismatch is the top failure class

Typical mismatch symptoms:

- POSIX syntax executed in PowerShell/CMD (`export`, `rm -rf`, `./script.sh`).
- Quoting behavior diverges between bash and PowerShell.
- Commands work in one shell and fail in another without code changes.

Mitigation:

1. Choose shell first.
2. Generate command syntax for that shell.
3. Translate only if fallback is required.

## 2) Paths and quoting

- Windows path example: `D:\repo\my app`.
- WSL path equivalent: `/mnt/d/repo/my app`.

Rules:

- Keep one path style per command unless interop is explicit.
- Quote paths with spaces.
- Avoid deeply nested one-liners when crossing shell boundaries.

## 3) Line endings and script behavior

- Windows default line endings differ from Linux defaults.
- Shell scripts edited on Windows may contain `\r` and fail in bash.

Mitigation:

- Normalize line endings for scripts used in WSL.
- Keep repository policy explicit (e.g., with `.gitattributes`).

## 4) WSL filesystem and performance

- I/O-heavy operations may vary significantly by location.
- Linux-side project directories often provide better Linux tool behavior.
- Cross-boundary access is useful but can be slower/less predictable for
  watch/build-heavy workflows.

## 5) Environment leakage and tool resolution

- Windows path/tool leakage into WSL may cause accidental `.exe` resolution.
- Profile scripts can introduce non-deterministic behavior.

Mitigation:

- Prefer deterministic WSL invocation (`--noprofile --norc`).
- Resolve tools explicitly when reliability matters.

## 6) Installation policy

- Do not install package managers/tools just to preserve a preferred shell.
- Prefer whichever shell already has required tools when risk is low.
- Install only when task explicitly requires it.

## 7) Fallback communication contract

When fallback occurs, always state:

1. failing shell + symptom,
2. chosen fallback shell,
3. confirmation that command intent remains unchanged.
