# Project State and Icons

Use this reference when a project is missing, duplicated, mislabeled, attached to the wrong workspace, or missing its sidebar icon.

## Find the active base directory

T3 normally stores server data under `~/.t3/userdata`, but `--base-dir` or `T3CODE_HOME` can select another location. Confirm the running command or service before inspecting a database.

Stop and back up the state database before any direct write. Read-only inspection can usually happen while T3 is running.

## Inspect active projects

When `sqlite3` is available:

```bash
t3_base_dir="${T3CODE_HOME:-$HOME/.t3}"
sqlite3 "$t3_base_dir/userdata/state.sqlite" \
  "SELECT project_id,title,workspace_root FROM projection_projects WHERE deleted_at IS NULL ORDER BY title;"
```

When it is not available:

```bash
python3 - <<'PY'
import os
import sqlite3

base_dir = os.environ.get("T3CODE_HOME", os.path.expanduser("~/.t3"))
path = os.path.join(base_dir, "userdata", "state.sqlite")
with sqlite3.connect(f"file:{path}?mode=ro", uri=True) as connection:
    query = """
        SELECT project_id, title, workspace_root
        FROM projection_projects
        WHERE deleted_at IS NULL
        ORDER BY title
    """
    for row in connection.execute(query):
        print("|".join(map(str, row)))
PY
```

If the schema differs, inspect the installed T3 version and its current schema rather than guessing a write.

## Change projects through the CLI

```bash
t3 project add --base-dir "$HOME/.t3" --title "Example (Laptop)" /path/to/repository
t3 project rename --base-dir "$HOME/.t3" /path/to/repository "Example (Laptop)"
t3 project remove --base-dir "$HOME/.t3" /path/to/repository
```

A project argument may be a project ID or workspace root for rename and remove. Avoid `--force` unless thread deletion is explicitly intended.

## Separate three identities

- Project title: the label shown to the user.
- Workspace root: the local directory opened for work.
- Git remote: repository identity used by Git and hosting integrations.

Changing one does not automatically repair the others.

For a repository used on several machines, a host-qualified title such as `Example (Laptop)` and `Example (Server)` can prevent the user from reopening a draft on the wrong host. Use neutral examples in shared documentation.

## Favicon resolution

T3 can resolve a project icon from `t3.json` `iconPath` or common repository icon paths. Inspect the installed version when the exact search order matters.

For an icon that should remain local:

1. Prefer an ignored path such as `.idea/icon.svg` when the installed resolver supports it.
2. Verify it is ignored before writing:
   ```bash
   git -C /path/to/repository check-ignore -q .idea/icon.svg
   ```
3. Do not add a personal or organization-specific icon to a shared repository without approval.

## Stale desktop selections

The desktop frontend may keep logical project selections or drafts in browser storage. If the CLI and server database are correct but the desktop still shows an old entry:

1. Refresh or relaunch the application.
2. Confirm which server or host the desktop is connected to.
3. Inspect the selected logical project key before changing server records again.

A stale desktop key is not evidence that the Git remote or server database is wrong.
Do not clear application or browser storage without backing up any drafts and getting explicit approval.
