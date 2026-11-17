---
name: workbuddy-data-migration
description: Migrate the WorkBuddy data directory (C:\Users\USER\.workbuddy) off the system drive to a fixed non-system disk using a Windows directory junction, so conversation history, sessions, skills, logs, the python/node runtimes (binaries), and all caches stop consuming C: space — and stay off it permanently, including any runtimes installed later. Use this skill when C: is low on space and WorkBuddy-related files are a major contributor, when the user asks to move WorkBuddy data / cache / environment / 运行时 off the system disk, or to reproduce a clean data-directory relocation (e.g. after a WorkBuddy reinstall recreates the C: dir and overwrites the junction).
agent_created: true
---

# WorkBuddy Data Directory Migration (junction method)

## Overview

Move WorkBuddy's entire data root from the system drive (`C:\Users\USER\.workbuddy`) to a fixed non-system disk (e.g. `E:\workbuddy-data`) using a Windows **directory junction**. After migration the original C: path still resolves (transparently redirecting to E:), so there is no config change, no path rewrite, and no breakage of hardcoded absolute paths. New data and new runtimes installed later also land on E: automatically.

## When to use

- C: drive is nearly full and WorkBuddy-related files are a major contributor.
- User asks to "move WorkBuddy data / cache / environment / 运行时 off C:", "don't use the system disk", or "把环境放到 E 盘".
- Reproduce a relocation after a WorkBuddy reinstall (reinstall may recreate the C: dir and overwrite the junction — re-run `scripts/migrate.bat`).

## Why a junction (not env vars, not a path move)

- WorkBuddy honors the `WORKBUDDY_CONFIG_DIR` env var for most subdirs (projects, sessions, skills, logs, app/session, blobs…), BUT the `binaries` runtime dir is hardcoded as `path.join(os.homedir(), ".workbuddy", "binaries", …)` and honors **no** env var. So an env-var-only approach leaves the largest 5–6 GB (python/node runtimes, e.g. ctranslate2/torch for GPU whisper) on C:.
- A junction at `C:\Users\USER\.workbuddy` → `E:\workbuddy-data` redirects **all** access, including the hardcoded binaries path, at the filesystem layer. Programs keep using the same C: path string; the bytes land on E:. This is the only approach that covers 100% and is future-proof.

## Workflow

1. **Inventory (read-only).** Measure size of `C:\Users\USER\.workbuddy`, AppData leftovers (`pip\cache`, `@genieworkbuddy-desktop-updater\installer.exe`), and free space on every disk. Present a cleanup + migration plan and get **explicit confirmation before deleting anything**.
2. **Cleanup (optional, only after confirmation).** Remove stale, safe-to-delete caches: pip cache, the leftover installer.exe, old traces/logs, Electron session cache. **Never** delete conversation history (`projects/`, `sessions/`, `blobs/`, `workbuddy.db`).
3. **Migration.** Use the bundled `scripts/migrate.bat` (double-click). It stages node to a neutral temp, runs `scripts/migrate.js` which: copies data to E:, **verifies the copy is complete**, renames the C: dir, creates the junction, self-checks, then reclaims C: space.
4. **Verify.** Confirm `C:\Users\USER\.workbuddy` is a junction (`isSymbolicLink`) resolving to `E:\workbuddy-data`, node is still reachable via the C: path, `workbuddy.db` is valid, and C: free space increased.

## Common gotchas (esp. on trimmed/custom Windows images)

Some Windows images have a trimmed PATH or a custom delete interceptor. If your first run fails silently, read `references/lessons.md` — it is the full forensic root-cause log from the author's first attempt. Key lessons:

- **Prefer node-native APIs over external commands.** `fs.cpSync` for copy and `fs.symlinkSync(dst, src, 'junction')` for the link need no admin and no shell, and sidestep ACL/redirect quirks that `robocopy /COPYALL` and `mklink` can hit. The bundled `scripts/migrate.js` already uses this approach.
- **If you must call Cmd tools, use full paths** (`C:\Windows\System32\tasklist.exe` etc.) — child processes may not inherit System32 in PATH on trimmed images.
- **Keep `.bat` launchers pure ASCII** (no `>`, `->`, `|`); let the node script hold the logic, with the `.bat` only staging node and calling it.
- **Avoid `powershell`** unless you have confirmed it is on PATH.
- **Self-lock:** the managed node lives inside the very dir being migrated. The bundled `.bat` stages `node.exe` to `C:\migrate_tmp` first so renaming/moving the source never kills the running process.

## Resources

- `scripts/migrate.bat` — ASCII launcher: stages node to `C:\migrate_tmp`, runs `migrate.js`, cleans up. Double-click to launch (best with WorkBuddy fully closed first).
- `scripts/migrate.js` — the actual migration. Node-native copy + junction, with a DB-safety gate, a copy-completeness gate, and self-checks. Powershell-free, CMD-internal-free.
- `references/lessons.md` — full root-cause log of every failure in the first migration attempt and the fix, for deep debugging.
