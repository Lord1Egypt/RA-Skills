---
name: session-cleanup
author: Chaobs
version: 1.4.0
description: >
  Session cleanup skill for Claw-family agents (OpenClaw, WorkBuddy, QClaw, etc.).
  This skill should be used when the user wants to track and clean up temporary files,
  scripts, installed skills, libraries, and software generated during a conversation session.
  Trigger phrases include: "开启清理追踪", "session cleanup", "会话清理", "清理垃圾文件",
  "清理对话文件", "清理临时文件", "结束清理", "列出临时文件", "清理 Skill",
  "卸载多余库", "clean up session", "cleanup now", "帮我清理".
---

# Session Cleanup Skill

## Purpose

Track and clean up all artifacts produced during a Claw-family agent session:
- Temporary files, demo scripts, and test outputs written to disk
- Python packages, npm packages, system software installed via pip/npm/brew/apt/winget
- Skills installed into `~/.workbuddy/skills/` or `.workbuddy/skills/`
- Any other transient resources that are no longer needed after the session

## Lifecycle — Two Phases

### Phase 1 · Tracking (activated at session start or on demand)

**Trigger words (start tracking):**
`开启清理追踪` | `启动会话清理` | `session cleanup start` | `track session files` |
`开始记录临时文件` | `enable cleanup tracking`

**On activation:**
1. Announce: "✅ 会话清理追踪已开启。我将记录本次对话中生成的所有临时文件、安装的库与 Skill。"
2. Create a persistent tracking file at `<workspace>/.workbuddy/session-track.json` with the following structure. If the file already exists from a previous interrupted session, load it and announce: "✅ 发现上一次会话的追踪记录，已恢复。"
   ```json
   {
     "started_at": "ISO-8601 timestamp",
     "workspace": "path/to/workspace",
     "items": {
       "temp_files": [],
       "pip_packages": [],
       "npm_packages": [],
       "system_software": [],
       "skills": [],
       "other": []
     },
     "skip_list": []
   }
   ```
3. After each subsequent tool call that produces a tracked artifact, append the item to the relevant array in `session-track.json` using `replace_in_file` or `write_to_file`. This ensures the tracking log survives token overflow, session resets, or unexpected interruptions. Do NOT announce each individual append.

**What to track — detection rules:**

| Category | Detection signal |
|---|---|
| Temp files | `write_to_file` / `execute_command` that creates a file in a temp path (`%TEMP%`, `/tmp`, session scratch dirs, `generated-images/`), OR any file where the explanation contains keywords: "temporary", "demo", "test", "example", "scratch", "临时", "演示", "测试" |
| Pip packages | `pip install`, `pip3 install`, `uv pip install` |
| npm packages | `npm install`, `npx ... --save` |
| System software | `winget install`, `choco install`, `apt install`, `brew install`, `scoop install` |
| Skills | `init_skill.py`, `use_skill`, manually writing a new `SKILL.md` to a skills folder |
| Other | Any item the user explicitly asks to track |

**Auto-tracking enforcement (critical — prevents missed items):**

After EVERY tool call while tracking is active, perform a quick post-check on the tool call result. This is mandatory and must not be skipped:

1. **`write_to_file`** — Check if the `filePath` is in a temp/scratch/generated path OR if the `explanation` contains keywords: "temporary", "demo", "test", "example", "scratch", "临时", "演示", "测试". If yes → append to `temp_files` in `session-track.json`.

2. **`execute_command`** — Scan the command string for:
   - `pip install` / `pip3 install` / `uv pip install` → extract package name, append to `pip_packages`
   - `npm install` / `npm i` → extract package name, append to `npm_packages`
   - `winget install` / `choco install` / `apt install` / `brew install` / `scoop install` → extract package name, append to `system_software`
   - Any command that creates a file in a temp path (redirect to `%TEMP%`, `/tmp`, etc.) → append to `temp_files`

3. **`use_skill`** or `init_skill.py`** — If a new skill is being installed or initialized, append the skill path to `skills`.

4. **User's explicit instruction** — If the user says "track this" / "记录这个" / "add to cleanup", append to `other`.

This post-check should be a silent, automatic step — do NOT announce it to the user. Simply update `session-track.json` in the background.

### Phase 2 · Cleanup (triggered on demand or session end)

**Trigger words (run cleanup):**
`清理垃圾文件` | `结束清理` | `清理对话文件` | `cleanup now` | `clean session` |
`清理临时文件` | `会话清理` | `帮我清理` | `删除临时文件` | `clean up`

**Cleanup workflow — follow these steps in order:**

#### Step A · Display the session log

Read `session-track.json` from `<workspace>/.workbuddy/`. Print the full tracked list as a Markdown checklist grouped by category. Format each category array as a checklist. Example output:

```
## 本次会话产生的资源清单

### 🗂 临时文件
- [ ] C:\Users\<user>\AppData\Local\Temp\demo_script.py
- [x] C:\Users\<user>\AppData\Local\Temp\keep_this.py (保留)
- [ ] /path/to/workspace/generated-images/test.png

### 📦 安装的 Python 包
- [ ] requests==2.31.0

### 🧩 安装的 Skills
- [ ] ~/.workbuddy/skills/my-test-skill/
```

If the tracked list is empty (excluding skip_list items), say: "📭 本次会话未检测到可清理的资源。" and stop.

When classifying, check `skip_list` in `session-track.json` — any item in `skip_list` should be excluded from cleanup and shown as "保留" in the summary.

#### Step B · Classify items

For each tracked item, classify it as either:

- **A: Safe to auto-delete** — files with no dependencies (temp files, demo scripts, test outputs, generated images). These are deleted without asking.
- **B: Requires confirmation** — installed packages, Skills, or system software that may have dependencies or ongoing utility. These require explicit user consent.

#### Step C · Auto-delete safe items (Class A)

1. List all Class A items and announce: "以下临时文件将直接清除："
2. **Choose deletion strategy based on item count:**
   - **5 items or fewer** → Agent deletes each item individually using `delete_file` (workspace files) or `execute_command` (non-workspace files). This gives step-by-step visibility and is token-efficient for small lists.
   - **6+ items** → Agent runs `cleanup.py` in two phases:
     1. **Preview**: `python "<skill_dir>/scripts/cleanup.py" --track-file "<workspace>/.workbuddy/session-track.json" --dry-run`
     2. **Execute**: `python "<skill_dir>/scripts/cleanup.py" --track-file "<workspace>/.workbuddy/session-track.json"`
     This leverages the script's built-in safety checks, trash-first logic, and batch efficiency.
   - **User explicitly requests one-click cleanup** → Use `cleanup.py` regardless of item count.
3. **Deletion method per file (when deleting individually):**
   - **Files inside the workspace** → use `delete_file` tool directly.
   - **Files outside the workspace** (e.g. `%TEMP%`, `/tmp`, home directory) → use `execute_command` with a **trash-first** strategy:
     - **Windows** — Move to Recycle Bin first; only hard-delete if trash fails:
       ```powershell
       # Try Recycle Bin first (safe, reversible)
       $shell = New-Object -ComObject Shell.Application
       $item = $shell.NameSpace(0).ParseName('<file_path>')
       $item.InvokeVerb('delete')
       ```
       If the above fails or the item doesn't appear in Recycle Bin, fall back to:
       `Remove-Item "<file_path>" -Force`
     - **macOS** — `osascript -e 'tell app "Finder" to delete POSIX file "<file_path>"'`
       Fallback: `rm "<file_path>"`
     - **Linux** — `gio trash "<file_path>"` or `trash-put "<file_path>"`
       Fallback: `rm "<file_path>"`
4. Confirm deletion result for each item (✅ deleted / ⚠️ failed).
5. **For temp directory files** (`%TEMP%`, `/tmp`), hard-delete is acceptable since these are OS-managed scratch spaces. For all other paths, always prefer trash.

#### Step D · Confirm before removing dependencies (Class B)

For each Class B item, present a grouped confirmation prompt:

```
以下资源涉及依赖关系，需要您确认是否删除/卸载：

📦 Python 包:
  • requests==2.31.0  → pip uninstall requests

🧩 Skills:
  • ~/.workbuddy/skills/my-test-skill/  → 将永久删除

请回复：
  全部删除 / 全部保留 / 逐一确认
```

- If user replies **全部删除** → uninstall/remove all Class B items.
- If user replies **全部保留** → skip all, close the log.
- If user replies **逐一确认** → iterate through each item and ask individually.

For package uninstalls:
- Pip: `pip uninstall -y <package>` via `execute_command`
- npm: `npm uninstall -g <package>` via `execute_command`
- winget: `winget uninstall --id <id>` via `execute_command`
- choco: `choco uninstall <package> -y` via `execute_command`
- brew: `brew uninstall <formula>` via `execute_command`
- apt: `sudo apt remove -y <package>` via `execute_command`
- scoop: `scoop uninstall <app>` via `execute_command`

For Skills uninstall:
- Delete the skill directory via `execute_command`:
  - Windows: `Remove-Item -Path "<skill_dir>" -Recurse -Force`
  - macOS/Linux: `rm -rf "<skill_dir>"`
- Do NOT use `delete_file` for skill directories as they are typically outside the workspace.
- **Always warn**: "⚠️ Skill 删除是永久性的，目录下所有文件将被移除。"

For system_software uninstall:
- Always treat as Class B (requires confirmation).
- Present the exact uninstall command that will be run so the user can verify.
- If the package was installed via `winget`, try `winget list <name>` first to find the exact ID before uninstalling.

#### Step E · Session log cleanup

After cleanup is complete, print a summary:

```
✅ 会话清理完成
  已删除临时文件: N 项
  已卸载 Python 包: N 项
  已删除 Skills: N 项
  跳过/保留: N 项
```

Reset the in-memory session log and delete `<workspace>/.workbuddy/session-track.json`.

## Additional Commands

| Command | Action |
|---|---|
| `列出临时文件` / `show session log` | Print current tracked list from `session-track.json` without deleting |
| `清除记录` / `clear log` | Delete `<workspace>/.workbuddy/session-track.json` via `delete_file` and reset tracking state. Does NOT delete any actual files. **Note:** The safety rule "never delete `.workbuddy/` folder" protects the directory itself, not transient session files within it — `session-track.json` is explicitly designed to be deleted by this command. |
| `手动添加 <path>` / `add to cleanup <path>` | Append a path to the relevant array in `session-track.json` |
| `跳过 <path_or_name>` / `skip <path_or_name>` | Add an item to `skip_list` in `session-track.json`, excluding it from future cleanup. Accepts partial matches (e.g. `跳过 demo_script.py` matches the full path). Confirm to user: "✅ 已标记保留: <item>" |

**`跳过` command detail:**

When the user says `跳过 <X>`:
1. Search all arrays in `session-track.json > items` for entries containing `<X>` as a substring.
2. If exactly one match → add the full matched string to `skip_list`, confirm to user.
3. If multiple matches → list them and ask user which one to skip.
4. If no match → tell user "未找到匹配项" and suggest `列出临时文件` to review.

Items in `skip_list` are displayed with `(保留)` tag in the cleanup list and excluded from actual deletion/uninstall.

## Safety Rules (Non-negotiable)

1. **Never auto-delete files outside temp/scratch/generated paths without explicit confirmation.**
2. **Never delete workspace source code, project configuration, or the `.workbuddy/` directory itself.** Exception: `session-track.json` inside `.workbuddy/` is a transient session file and may be deleted by the `清除记录` command or Step E cleanup.
3. **Never use `rm -rf` or `del /S /Q` on home, desktop, downloads, or project roots.**
4. **Skills deletion is permanent** — always warn before removing Skills.
5. **If a deletion fails, stop and report the error. Do NOT retry with broader paths.**
6. **Max 10 file deletions per batch.** Verify after each batch.

## Bundled Resources

- `scripts/cleanup.py` — Command-line cleanup utility; can be run directly to remove a list of paths.
- `references/cleanup-guide.md` — Full reference of uninstall commands by package manager and OS.

## Changelog

### v1.4.0 (2026-04-17)
- **Fix**: `track_init()` shallow copy bug — nested `items` dict now uses `copy.deepcopy()` to prevent cross-session reference sharing (P2-6)
- **Fix**: `uninstall_pip()` / `uninstall_npm()` now pre-check whether the package is actually installed before attempting uninstall (P2-9)
- **Added**: Changelog section to SKILL.md (P2-8)

### v1.3.0 (2026-04-16)
- **Fix**: Windows path safety bug — `Path("/")` resolving to `\` on Windows, incorrectly flagging all paths as unsafe
- **Fix**: `skip_list` partial matching — added `_is_skipped()` helper for substring-based matching
- **Fix**: `send_to_trash()` silent hard-delete fallback — now requires `allow_hard_delete=True` (only set for temp paths)
- **Fix**: PowerShell single-quote escaping for paths with special characters
- **Added**: `--workspace` CLI argument for `--manifest` mode
- **Added**: `ALLOWED_SUBDIRS` list for workspace-aware safety checks (`generated-images`, `node_modules`)
- **Added**: Step C decision logic in SKILL.md (≤5 items → individual delete; 6+ → script; one-click → script)
- **Added**: Safety Rule #2 exception for `session-track.json`
- **Added**: `(保留)` skip marker in Step A example output
- **Added**: Duplicate detection rule row fix in SKILL.md table

### v1.2.0 (2026-04-15)
- Initial public release with tracking and cleanup workflows
- Trash-first deletion with OS-specific implementations
- Session-track.json with skip_list support
- cleanup.py CLI utility with `--init`, `--add`, `--skip-add`, `--show`, `--dry-run`
