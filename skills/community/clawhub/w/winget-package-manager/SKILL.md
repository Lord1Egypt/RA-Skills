---
name: winget-package-manager
description: |
  Controlled Windows package management workflow based on winget.
  Guides an agent to safely search, inspect, download, install, upgrade, uninstall, and list upgradeable applications on Windows.
  Designed as a prompt-only skill for hosts that already provide terminal or command execution capability.
metadata:
  openclaw:
    requires:
      bins:
        - winget
      os:
        - windows
    minWingetVersion: "1.6"
    emoji: "📦"
---

# Winget Package Manager Skill

## Overview

This is a **prompt-only Windows package management skill** built around **winget**.

It does **not** provide its own executable wrapper scripts.
Instead, it defines a **safe workflow**, **decision rules**, and **behavior constraints** for agents that already have access to a terminal, shell, or command-execution capability in the host environment.

The goal of this skill is to help an agent use `winget` safely and consistently on Windows without turning package management into arbitrary shell execution.

## Host capability requirement

This skill assumes the host environment already provides a way to run Windows commands.

Examples of suitable host capabilities include:

- A terminal tool
- A shell execution tool
- A controlled local command runner
- An MCP/server/tool that can execute `winget`

If the host cannot execute commands, this skill can still provide workflow guidance, but it cannot directly perform package operations.

## When to use this skill

Use this skill when the user wants to:

- Search for an application available through WinGet
- Inspect package details before taking action
- Download an installer package without installing it
- Install an application
- Upgrade an application
- Uninstall an application
- List applications that have available upgrades

## When NOT to use this skill

Do **not** use this skill for:

- Running arbitrary PowerShell or shell commands
- Editing files, registry keys, services, or scheduled tasks
- Downloading files from custom URLs
- Executing local `.exe`, `.bat`, `.cmd`, or `.ps1` files outside the host's trusted execution model
- Installing software from sources other than approved WinGet sources
- Performing destructive actions when package identity is ambiguous

## Supported operations

This skill supports exactly 7 operations:

- `search`
- `show`
- `download`
- `install`
- `upgrade`
- `uninstall`
- `list-upgrades`

Do not expand the scope beyond these operations unless the skill is explicitly redesigned.

## Safety rules

1. Only use the 7 supported operations:
   - `search`
   - `show`
   - `download`
   - `install`
   - `upgrade`
   - `uninstall`
   - `list-upgrades`

2. Prefer **exact package IDs** over fuzzy names whenever possible.
   Examples:
   - `Microsoft.VisualStudioCode`
   - `Google.Chrome`
   - `Git.Git`

3. For `install`, `upgrade`, and `uninstall`:
   - If the package identity is ambiguous, do **not** execute immediately.
   - Run `search` or `show` first.
   - Return all matching candidates and ask the user to choose.

4. Only allow approved sources:
   - `winget`
   - `msstore`

5. Do not invent or append unsupported WinGet arguments.

6. Do not transform this skill into a generic PowerShell executor or shell tool.

7. Treat `uninstall` as high-risk:
   - Always prefer an exact package ID.
   - If identity is unclear, stop and disambiguate before acting.

8. **Never automatically retry** `install`, `upgrade`, or `uninstall` after failure.
   Report the failure and let the user decide what to do next.
   Repeated retries may trigger repeated elevation prompts or vendor installer/uninstaller dialogs.

9. **Disambiguation is mandatory**:
   When multiple packages match a request, list all relevant candidates and ask which one should be used.
   Never silently operate on all matches.

10. For `uninstall`, do not rely only on a success-looking message from the package manager.
    If the host environment allows it, perform a **post-check** to verify whether the package still appears to be installed.

## Allowed operations and risk levels

| Action | Description | Risk Level |
|--------|-------------|-------------|
| `search` | Search for packages | Low |
| `show` | View package details | Low |
| `download` | Download installer only | Medium |
| `install` | Install a package | Medium |
| `upgrade` | Upgrade a package | Medium |
| `uninstall` | Uninstall a package | High |
| `list-upgrades` | List updatable packages | Low |

## Core workflow

The agent should follow this workflow:

### 1. Search or identify the package

When the user provides a fuzzy name such as:

- "install chrome"
- "upgrade vscode"
- "remove git"

the agent should first identify the correct package through `winget search` or equivalent host capability.

### 2. Inspect details when needed

If identity is uncertain, or the action is medium/high risk, inspect the package before acting.

Use `show` when helpful to confirm:

- package ID
- package name
- source
- version or metadata

### 3. Require precision for risky actions

For these actions:

- `install`
- `upgrade`
- `download`
- `uninstall`

the agent should prefer a precise package ID and avoid acting on vague names.

### 4. Execute the package operation

Only after the package is sufficiently identified should the agent execute the requested operation through the host's command capability.

### 5. Summarize the result clearly

Return a concise, structured result that includes:

- action
- package identity
- source
- whether the command appears successful
- any important stdout/stderr details
- whether follow-up verification is recommended

### 6. Verify uninstall results when possible

If the action is `uninstall`, and the host allows further checks, verify the result afterward.
A vendor uninstaller may show its own dialog and may not always report cancellation in a reliable way.

## Recommended command patterns

The exact execution mechanism depends on the host environment.
However, the agent should generally use patterns like the following.

### Search

```powershell
winget search "Visual Studio Code"
```

### Show package details

```powershell
winget show --id Microsoft.VisualStudioCode --exact
```

### Download installer only

```powershell
winget download --id Google.Chrome --source winget --download-directory "$env:USERPROFILE\Downloads" --exact
```

### Install

```powershell
winget install --id Microsoft.VisualStudioCode --source winget --exact --accept-package-agreements --accept-source-agreements
```

### Upgrade

```powershell
winget upgrade --id Git.Git --source winget --exact --accept-package-agreements --accept-source-agreements
```

### Uninstall

```powershell
winget uninstall --id 7zip.7zip --source winget --exact
```

### List upgradeable packages

```powershell
winget upgrade
```

## Output guidance

Because this is a prompt-only skill, the exact output format depends on the host tool.

When the host environment supports structured output, prefer a consistent JSON-like structure such as:

```json
{
  "success": true,
  "action": "search",
  "query": "Visual Studio Code",
  "source": "winget",
  "candidates": [
    {
      "name": "Microsoft Visual Studio Code",
      "id": "Microsoft.VisualStudioCode",
      "version": "1.96.0"
    }
  ],
  "stdout": "...",
  "stderr": "",
  "exit_code": 0,
  "summary": "Search completed for 'Visual Studio Code'."
}
```

If the host does not support structured tool output, the agent should still present results using a stable and consistent schema in its response.

## Behavioral requirements for ambiguous matches

If the user asks something like:

- "install DevToys"
- "uninstall DevToy"
- "upgrade Python"

and multiple packages match, the agent must:

1. List the candidates
2. Explain that the request is ambiguous
3. Ask which package should be used
4. Avoid executing `install`, `upgrade`, or `uninstall` until the user clarifies

Example ambiguity handling:

- `DevToys.DevToys`
- `DevToys.DevToys.Preview`

Do not operate on both unless the user explicitly asks for both.

## Error handling guidance

The agent should handle and clearly report situations such as:

- `winget` is not installed
- `winget` is not available in PATH
- package not found
- source not allowed
- network failures
- permission or elevation issues
- ambiguous package matches
- download path issues
- uninstall command finishes, but the app may still be installed

When a failure occurs, report it clearly and do not automatically retry high-risk operations.

## Security constraints

- **No arbitrary command execution**
- **No unapproved package sources**
- **No free-form parameter passthrough**
- **No silent expansion into a generic shell skill**
- **No destructive action without package disambiguation**
- **No blind trust in uninstall success messages**

## Requirements

- Windows 10 1809+ or Windows 11
- `winget` 1.6+ recommended
  - `winget` 1.6+ is especially useful for `download`
  - older versions may still support some other operations

## Notes for maintainers

This skill is intentionally designed as a **prompt-only / policy-only** skill so it can be distributed in environments where script files may not be accepted.

A richer local version may additionally provide:

- PowerShell wrappers
- JSON normalization
- post-check verification
- source validation
- logging and audit trails

Those implementation assets are useful, but they are outside the scope of this prompt-only distribution.