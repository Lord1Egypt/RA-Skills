# Lessons learned — root-cause log from the author's first migration attempt

The first migration was attempted with .bat + external commands and failed several times before
succeeding with a node-native approach. Every failure had a different root cause. This file is the
forensic record so the same mistakes are never repeated. The symptoms below were observed on a
trimmed/custom Windows image; on a standard image some of these (powershell, PATH) may not apply,
but the node-native approach in `scripts/migrate.js` avoids them all regardless.

## Environment quirks observed (trimmed/custom images)

- `powershell.exe` / `powershell` may be **NOT on PATH**. Any script that calls `powershell`
  dies immediately with `'powershell' is not recognized`.
- `cmd.exe`'s child processes (including node) may **NOT inherit `C:\Windows\System32`** in PATH.
  So `tasklist`, `robocopy`, `fsutil`, `mklink`, `rmdir` called by bare name → `ENOENT`.
  They DO exist at `C:\Windows\System32\*` — call them by full path.
- A "safe-delete" interceptor may sit in front of deletions. node `fs.rmSync`/`unlink` can
  **time out**; Git-Bash `rm -rf` bypasses it.

## Failure timeline

### v3 (.bat calling powershell)
- Symptom: flash-close (闪退) with no error.
- Root cause: the `.bat` used `powershell` for the process check; `powershell` not on PATH →
  script aborted at the first line. Fix: never call powershell.

### v4 (.bat with `->` in echo)
- Symptom: flash-close.
- Root cause: `echo Moving C:\... -> E:\...` — the `->` was parsed by `cmd` as an output
  redirect and created a 55-byte file `E:\workbuddy-data`, which then triggered the script's
  own `if exist "E:\workbuddy-data"` guard and aborted before doing anything.
- Fix: never put `>`, `->`, `|` in a .bat. Keep .bat pure ASCII; do logic in node.

### v6 (.bat launching node; node calls tasklist/robocopy by bare name)
- Symptom: reported "no WorkBuddy process found" (false) and "robocopy could not start: ENOENT".
- Root cause: node child_process doesn't have System32 in PATH, so `tasklist` and `robocopy`
  by bare name couldn't be found. The guard's `tasklist` threw, was caught, returned empty →
  falsely concluded WorkBuddy was closed → never killed it; `robocopy` never ran.
- Fix: call all external commands by full `C:\Windows\System32\xxx.exe` path.

### v7 (.bat with full-path robocopy /MOVE)
- Symptom: half-finished; junction never created; C: dir still real.
- Root cause 1: `robocopy /MOVE` tried to delete the source tree, but the migration node.exe
  itself lived inside `C:\...\binaries\node\...\node.exe` → it could not delete itself → move
  aborted with the source still present.
- Fix: stage node to a neutral temp (`C:\migrate_tmp`) and run migrate.js from there (done in
  the .bat), OR avoid /MOVE entirely (use copy + rename, which v9/v10 do).

### v9 (.js using robocopy /COPYALL + cmd /c mklink)
- Symptom: flash + fallback restored the dir; data safe but not migrated.
- Root cause 1: `robocopy ... /COPYALL` (copies ACLs) exited **16 = copied nothing** due to ACL
  errors on this image. Code still proceeded to rename (latent hazard).
- Root cause 2: `mklink` is a **CMD-internal** command; `C:\Windows\System32\mklink.exe` does
  not exist, so `cmd /c mklink /J` failed → junction never created → fallback restored SRC.
- Fix: drop robocopy and mklink. Use node-native `fs.cpSync` for the copy and
  `fs.symlinkSync(dst, src, 'junction')` for the link (junctions need no admin, no cmd).

## What finally worked (v10)

- `.bat` = pure ASCII launcher only: stage node → `C:\migrate_tmp`, run `migrate.js`, clean up.
- `migrate.js` = 100% node-native:
  - external commands only `tasklist.exe`/`taskkill.exe`/`fsutil.exe` by full System32 path,
    used solely for the process guard and free-space read.
  - copy via `fs.cpSync(SRC, DST, {recursive, force, verbatimSymlinks})`.
  - link via `fs.symlinkSync(DST, SRC, 'junction')`.
  - gates: DB-safety check, **copy-completeness verification before renaming the source**,
    self-checks (junction present, node reachable via C:, db valid).
  - reclaim: try `fs.rmSync(SRC_OLD)`; locked files may remain until reboot — harmless.

## Leftover cleanup note

After a successful junction, an old `.workbuddy_old` may remain partially locked (EPERM) because
a live process holds handles. `cmd /c rmdir /s /q` several passes removes most; the last few
thousand locked files only clear after a reboot. None of it is used by WorkBuddy (the live data
is on E: via the junction). Just delete the folder in Explorer after rebooting.
