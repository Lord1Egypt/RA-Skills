---
name: truecrypt-cli
description: Use installed TrueCrypt on Windows to mount, dismount, inspect, and automate legacy TrueCrypt containers or encrypted partitions from the command line. Trigger when a user specifically wants TrueCrypt rather than VeraCrypt, asks for TrueCrypt CLI syntax, wants a batch/PowerShell command for mounting or dismounting, needs to check whether TrueCrypt is installed, or wants help scripting safe non-destructive TrueCrypt operations.
---

# TrueCrypt CLI

Use this skill when the user explicitly wants to work with installed TrueCrypt on Windows, especially version 7.1a, instead of being redirected to VeraCrypt.

## Workflow

1. Confirm that `TrueCrypt.exe` exists before giving machine-specific commands.
2. Prefer the full executable path in examples to avoid PATH issues.
3. Ask only for the minimum needed details:
   - volume path or device path
   - target drive letter
   - whether a keyfile is used
   - whether the operation must be non-interactive
4. Prefer non-destructive operations first: detect install path, dismount, or prepare a command without running it.
5. Warn before using `/p` because command-line passwords may be exposed to process listings, logs, or shell history.
6. If built-in help does not print to the console, rely on known command patterns and cautious validation instead of pretending the CLI is self-documenting.

## Quick checks

First, locate the binary. Common paths:

```powershell
C:\Program Files\TrueCrypt\TrueCrypt.exe
C:\Program Files (x86)\TrueCrypt\TrueCrypt.exe
```

PowerShell check:

```powershell
$tc = @(
  'C:\Program Files\TrueCrypt\TrueCrypt.exe',
  'C:\Program Files (x86)\TrueCrypt\TrueCrypt.exe'
) | Where-Object { Test-Path $_ } | Select-Object -First 1
```

If nothing is found there, fall back to `Get-Command TrueCrypt.exe`.

## Safe command patterns

Use the cookbook in `references/commands.md` for exact examples.

High-confidence operations:
- mount a volume with `/v` and `/l`
- dismount one letter with `/d X`
- dismount all with `/d`
- use `/q` for quiet mode
- use `/k` for keyfiles when needed
- use `/m` for mount options when explicitly required

Prefer examples like:

```bat
"C:\Program Files\TrueCrypt\TrueCrypt.exe" /v "C:\path\container.tc" /l X /q
```

```bat
"C:\Program Files\TrueCrypt\TrueCrypt.exe" /d X /q
```

```bat
"C:\Program Files\TrueCrypt\TrueCrypt.exe" /d /q
```

## Safety and communication rules

- Do not casually recommend migrating to VeraCrypt if the user explicitly asked for TrueCrypt help; answer the TrueCrypt question first.
- Do mention that TrueCrypt is discontinued when security or long-term maintenance is relevant.
- Do not put a real password into saved scripts unless the user explicitly requests that tradeoff.
- For destructive or risky actions, prepare the command and ask before executing it.
- If uncertain about a rare switch, say so plainly and stick to the known-safe command surface.

## Outputs to provide

Depending on the request, provide one of these:
- exact one-line mount or dismount command
- PowerShell or batch wrapper
- install-detection command
- short explanation of each switch used
- a cautious test plan for validating a container without exposing secrets
