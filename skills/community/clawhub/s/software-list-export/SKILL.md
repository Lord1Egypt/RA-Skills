---
name: software-list-export
description: "Export installed software to CSV with versions and likely download URLs. Invoke when the user wants a machine inventory or reinstall list for a new computer."
---

# Software List Export

Use for software inventory and migration prep. Output one CSV the user can review and use as a reinstall checklist on a new computer.

## Workflow

1. Detect the operating system first: Windows, macOS, or Linux.
2. Ask the user first where to save the CSV file and the possible filename (both are optional), otherwise use the current directory, and default name is `software-list-{timestamp}.csv`. Use current time as the {timestamp}. 
3. Collect installed software from native sources:
   - Windows: Use `scripts/export-software-list.ps1`. If fail, prefer `winget list`, then supplement with uninstall registry entries for software not covered by `winget`. The checked-in script already implements this Windows workflow and prints raw structured records to stdout.
   - macOS: prefer `brew list` and `brew list --cask`, include `mas list` if available, then supplement with `/Applications` and `~/Applications`.
   - Linux: prefer the distro package manager (`apt`, `dnf`, `pacman`, `zypper`), then include `flatpak` and `snap` when present.
4. Normalize software names, merge duplicates, and keep the most useful version/source details.
5. Rank results by yourself, not in the script, **you should think, sort and edit the csv directly**. The model should place the most user-oriented software first. End-user apps should come before runtimes, redistributables, drivers, SDKs, language packs, browser helpers, and other support components. End user apps often has meanful names.
6. For each item, add a likely download or package home URL when it can be determined with reasonable confidence. Do not fabricate URLs. If the URL is not provided directly by CLI or package-manager output, note in `comments` that the URL may not be a real download URL.
7. After processing the raw records, export the final results to a CSV with the columns `name,version,download_url,comments`.
8. Tell the user the path to the CSV file.

## Platform Notes

- Windows PowerShell 5 compatibility matters. Avoid newer syntax such as `??` that is only available in later PowerShell versions.
- `scripts/export-software-list.ps1` is Windows-only. Do not run it on macOS or Linux.
- `scripts/export-software-list.ps1` is a raw collector, not a full exporter. It prints structured CLI output and does not write the final CSV file.
- On Windows, `winget list` output is column-aligned text and may contain wrapped or localized content. Prefer parsing by header column positions instead of splitting on repeated spaces.
- Use uninstall registry entries as the conservative fallback on Windows when `winget` data is incomplete or ambiguous.
- If a URL comes from registry metadata, heuristics, or other non-CLI sources, treat it as a likely vendor or product URL rather than a guaranteed installer link.
- If terminal output shows PSReadLine rendering errors but the export command still reports a valid CSV path and successful completion, treat the export as successful and report the file path to the user.
- When encoding may affect non-ASCII app names, prefer UTF-8 output for the CSV.
- On Windows, common non-user-facing items include `Microsoft Visual C++ Redistributable`, `.NET`, `SDK` runtimes/targeting packs, drivers, updates, WebView runtimes, and OEM helper components. Push these behind user-facing apps instead of showing them first.

## Output Example

```csv
name,version,download_url,comments
"TRAE","1.0.0","https://trae.com/","Detected from local installation. Likely reinstallable manually from vendor site."
"Git","2.49.0","https://git-scm.com/downloads","Detected from package manager. Likely reinstallable automatically."
```

## Scripts

- Primary helper: `scripts/export-software-list.ps1`
- Scope: Windows only
- Expected usage: run the script on Windows, capture its structured CLI output, then let the model rank/filter the records and write the final CSV separately.

## Rules

- Use the language that the user asked for.
- DO NOT read, delete, or modify any files except the CSV file you are creating or editing.
- If there is any agreement required, ask the user first.
- On Windows, prefer running the checked-in helper script before inventing new export logic during the task.
- On macOS and Linux, do not use the Windows helper script.
- Prefer system-native inventory sources before heuristics.
- Keep the helper script focused on collection. Let the model handle ranking, user-facing ordering, and final CSV writing.
- Mark uncertainty in `comments` when version, source, or reinstall path is incomplete.
- If the URL is not provided in CLI or package-manager output, state in `comments` that the URL may not be real or may be a vendor/product page instead of a direct download.
- If a package manager export is available, note in `comments` whether the app is likely reinstallable automatically or only manually.
- On Windows, prefer reliability over coverage: avoid aggressive matching that creates false duplicates between registry entries and `winget` results.
- Prefer a user-friendly ordering. Sort user-facing apps first, and de-prioritize infrastructure entries such as redistributables, runtimes, frameworks, patches, drivers, SDKs, and similar dependencies.
