---
name: boxyard-cli
description: Use the Boxyard CLI to manage, find, inspect, sync, include, exclude, group, rename, or copy boxes. Use when the user asks about boxyard command usage, Boxyard config files, locating box folders, rclone-backed storage, sync status, or shell/TUI helpers.
---

# Boxyard CLI Skill

Use this skill when the user wants to **use** Boxyard, not develop Boxyard itself.

Boxyard is a Python CLI for managing and syncing folders ("boxes") across local and remote storage using rclone or local storage. A box has data, metadata, optional sync configuration, group membership, and sync records.

## Where generated data should live

Generated data — including large outputs — generally belongs **inside** the box it relates to, not in some sibling directory chosen to dodge syncing. Do not move heavy outputs out of a box to keep it "small". The whole point of Boxyard is that syncing makes large boxes comfortable to live with: anything you don't want pushed can be excluded from sync via the box's `conf/.rclone_exclude` / `conf/.rclone_filters` (see "Per-box sync configuration"), or the box itself can be excluded locally with `boxyard exclude`. Keep data colocated with its box and control sync with filters — don't fragment it to avoid sync.

## Before running commands

- If operating from this repository checkout, prefer:

  ```bash
  cd /path/to/boxyard && uv run boxyard ...
  ```

  If Boxyard is already installed in the environment, `boxyard ...` is also fine.

- Read-only commands are safe to run without confirmation: `--help`, `list`, `tree`, `path`, `which`, `box-status`, `yard-status`, `list-groups`.
- Ask before running commands that can modify local or remote state: `init`, `new`, `sync`, `multi-sync`, `sync-missing-meta`, `include`, `exclude`, `delete`, `rename`, `sync-name`, `add-to-group`, `remove-from-group`, `add-parent`, `remove-parent`, `create-user-symlinks`, `copy`, `force-push`.
- Be especially careful with:
  - `boxyard new --from PATH` / `-f PATH`: moves `PATH` into Boxyard unless `--copy` is supplied.
  - `boxyard exclude`: syncs first by default, then removes the local data copy.
  - `boxyard delete`: deletes a box.
  - `boxyard sync --sync-setting replace|force`: can overwrite data depending on direction/status.
  - `boxyard force-push --force`: destructively overwrites remote data from a local source folder.

## Configuration files and important paths

Default files and folders:

```text
~/.config/boxyard/config.toml          # main Boxyard config
~/.config/boxyard/boxyard_rclone.conf  # Boxyard's rclone config
~/.config/boxyard/default.rclone_exclude
~/.boxyard/                            # default boxyard_data_path
~/boxes/                               # default user_boxes_path; included box data appears here
~/box-groups/                          # default user_box_groups_path; group symlinks appear here
```

The config file controls the real locations. Important config keys:

```toml
default_storage_location = "..."
boxyard_data_path = "~/.boxyard"
user_boxes_path = "~/boxes"
user_box_groups_path = "~/box-groups"
max_concurrent_rclone_ops = 3

[storage_locations.my-remote]
storage_type = "rclone" # or "local"
store_path = "boxyard"
```

Derived paths:

```text
<boxyard_data_path>/boxyard_meta.json          # cached local box index
<boxyard_data_path>/local_store/<storage>/     # local metadata/conf roots by storage location
<boxyard_data_path>/sync_records/              # local sync records
<boxyard_data_path>/sync_backups/              # local sync backups
<boxyard_data_path>/remote_indexes/            # cached remote index lookups
```

For a box with index name `<box_id>__<name>`:

```text
<user_boxes_path>/<box_id>__<name>/                         # data path for included boxes
<boxyard_data_path>/local_store/<storage>/<index>/           # local box root
<boxyard_data_path>/local_store/<storage>/<index>/boxmeta.toml
<boxyard_data_path>/local_store/<storage>/<index>/conf/
```

Remote/rclone stores use this layout under the storage location's `store_path`:

```text
boxes/<index>/data/
boxes/<index>/boxmeta.toml
boxes/<index>/conf/
sync_records/<index>/<data|meta|conf>.rec
sync_backups/
```

The global CLI option for non-default config is:

```bash
boxyard --config /path/to/config.toml <command> ...
```

`boxyard init` uses `--config-path` and `--data-path` to create a config/data directory. The shell helper honors `BOXYARD_CONFIG_PATH`; normal Typer CLI commands should be given `--config` when using a non-default config.

`DEFAULT_BOX_GROUPS` can add default groups at runtime. It is parsed as a TOML list string, for example:

```bash
export DEFAULT_BOX_GROUPS='["ctx/mac", "work"]'
```

## How to find where boxes are

Use these patterns first.

### Find the box containing the current directory or any path

```bash
boxyard which
boxyard which --path /some/path
boxyard which --path /some/path --json
boxyard which --path /some/path --index-name
```

`which` reports the box name, box id, index name, storage location, groups, local data path, and whether the box is included.

### Get a box's data folder

```bash
boxyard path --box-name NAME --pick-first
boxyard path --box-id BOX_ID
boxyard path --box INDEX_NAME
```

`boxyard path` defaults to the **data** path. By default it filters to included boxes. Use `--all` when you need to select from included and excluded boxes.

Interactive selector:

```bash
boxyard path --interactive
boxyard path -I --browse-mode groups
boxyard path -I --browse-mode tree
```

### Get non-data paths for a box

```bash
boxyard path --box-name NAME --pick-first --path-option root
boxyard path --box-name NAME --pick-first --path-option meta
boxyard path --box-name NAME --pick-first --path-option conf
boxyard path --box-name NAME --pick-first --path-option sync-record-data
boxyard path --box-name NAME --pick-first --path-option sync-record-meta
boxyard path --box-name NAME --pick-first --path-option sync-record-conf
```

### Find the top-level included boxes folder

Read `user_boxes_path` from the config. Included boxes are usually symlinked or stored under:

```text
~/boxes/<index_name>
```

Commands:

```bash
boxyard list --show-status
boxyard path --box INDEX_NAME
```

`●` means included locally; `○` means known metadata exists but local data is excluded/not present.

## Common discovery commands

```bash
boxyard list
boxyard list --show-status
boxyard list --output-format json
boxyard list --view groups --show-status
boxyard list --view tree --show-status
boxyard tree --show-status
boxyard list-groups --all --include-virtual
boxyard yard-status
```

Group filters support boolean expressions over group names:

```bash
boxyard list --group-filter 'work AND NOT archived'
boxyard path --group-filter 'ctx/mac OR ctx/linux' --interactive
```

Other list filters:

```bash
boxyard list --include-group GROUP
boxyard list --exclude-group GROUP
boxyard list --children-of BOX
boxyard list --descendants-of BOX
boxyard list --parent-of BOX
boxyard list --ancestors-of BOX
boxyard list --roots
boxyard list --leaves
```

## Box selection options

Many commands accept one of:

```bash
--box INDEX_NAME       # full <box_id>__<name>
--box-id BOX_ID        # <timestamp>_<subid>
--box-name NAME        # defaults to contains matching for many commands
```

Name matching options:

```bash
--name-match-mode exact|contains|subsequence
--name-match-case
--pick-first           # available on `path`; use only when ambiguity is acceptable
```

If no box is provided for some commands, Boxyard may infer it from the current working directory when inside `<user_boxes_path>/<index_name>/...`.

## Creating boxes

Create an empty box:

```bash
boxyard new --box-name NAME
```

Create from an existing folder, moving the folder into Boxyard:

```bash
boxyard new --from /path/to/folder
```

Copy from an existing folder instead of moving it:

```bash
boxyard new --from /path/to/folder --copy
```

Clone a git repo as a new box:

```bash
boxyard new --git-clone git@github.com:user/repo.git
```

Useful options:

```bash
boxyard new --box-name NAME --storage-location STORAGE
boxyard new --box-name NAME --group GROUP --group OTHER_GROUP
boxyard new --box-name NAME --parent PARENT_BOX
boxyard new --box-name NAME --no-initialise-git
```

## Syncing

Sync one box:

```bash
boxyard sync --box-name NAME
boxyard sync --box INDEX_NAME
boxyard sync --box-id BOX_ID
```

Sync only selected parts:

```bash
boxyard sync --box-name NAME --sync-choices meta
boxyard sync --box-name NAME --sync-choices conf
boxyard sync --box-name NAME --sync-choices data
```

Sync settings and direction:

```bash
boxyard sync --box-name NAME --sync-setting careful
boxyard sync --box-name NAME --sync-setting replace
boxyard sync --box-name NAME --sync-setting force
boxyard sync --box-name NAME --sync-direction push
boxyard sync --box-name NAME --sync-direction pull
```

Other sync commands:

```bash
boxyard multi-sync
boxyard multi-sync --storage-location STORAGE --max-concurrent 3
boxyard multi-sync --box INDEX_NAME --box OTHER_INDEX_NAME
boxyard sync-missing-meta
boxyard box-status --box-name NAME
boxyard yard-status
```

Soft interruption is enabled by default for long operations: interrupt once or twice to stop after the current operation; repeated interrupts exit immediately.

## Include, exclude, copy

Include an excluded remote box locally:

```bash
boxyard include --box-name NAME
boxyard include --interactive
```

Exclude a local copy while keeping the remote:

```bash
boxyard exclude --box-name NAME
boxyard exclude --interactive --show-sizes
boxyard exclude --box-name NAME --skip-sync
```

Copy a remote box to an arbitrary destination without adding it to Boxyard tracking:

```bash
boxyard copy --box-name NAME --dest ./NAME-copy
boxyard copy --box-name NAME --dest ./NAME-copy --meta --conf
boxyard copy --box-name NAME --dest ./NAME-copy --overwrite
```

## Groups and hierarchy

Groups:

```bash
boxyard add-to-group --box-name NAME GROUP [OTHER_GROUP ...]
boxyard remove-from-group --box-name NAME GROUP [OTHER_GROUP ...]
boxyard list-groups --box-name NAME
boxyard list-groups --all --include-virtual
boxyard create-user-symlinks
```

Parent-child hierarchy:

```bash
boxyard add-parent --box-name CHILD --parent-name PARENT
boxyard remove-parent --box-name CHILD --parent-name PARENT
boxyard tree --show-status
boxyard list --view tree --show-status
```

## Rename, delete, and force operations

Rename:

```bash
boxyard rename --box-name OLD --new-name NEW --scope both
boxyard rename --box-name OLD --new-name NEW --scope local
boxyard rename --box-name OLD --new-name NEW --scope remote
```

Sync only the name between local and remote:

```bash
boxyard sync-name --box-name NAME --to-local
boxyard sync-name --box-name NAME --to-remote
```

Delete:

```bash
boxyard delete --box-name NAME
boxyard delete --box-name NAME --force   # needed when the box has children
```

Destructive force push:

```bash
boxyard force-push --box-name NAME --source /path/to/source --force
```

## Per-box sync configuration

Each box can have a `conf/` folder. Boxyard syncs `conf/` before `data/`, so filters travel with the box.

Special files:

```text
conf/.rclone_include  # only sync matching files
conf/.rclone_exclude  # exclude matching files
conf/.rclone_filters  # combined rclone filter rules
```

If `conf/.rclone_exclude` is absent, Boxyard uses:

```text
~/.config/boxyard/default.rclone_exclude
```

Default excludes include `.venv/`, `.pixi/`, `.trunk/`, `node_modules/`, `__pycache__/`, and `.DS_Store`.

## Shell helper

The repo includes a zsh helper:

```bash
source /path/to/boxyard/shell/boxyard.zsh
```

Default keybinding: `Ctrl+G` (`BOXYARD_WIDGET_KEY` can override it). Type a partial box name, press the keybinding, and it replaces the current word with a relative path to the selected box. It uses `boxyard-shell-helper search` and `fzf` for multiple matches.

Direct helper examples:

```bash
boxyard-shell-helper search TERM
boxyard-shell-helper search TERM --group GROUP
boxyard-shell-helper search TERM --included
boxyard-shell-helper search TERM --excluded
```

## Reference files in this repository

From this skill directory, the repository root is `../..`.

Read these for more context when needed:

- `../../README.md` — high-level usage and directory layout
- `../../src/boxyard/const.py` — default paths and constants
- `../../src/boxyard/config.py` — config model and derived paths
- `../../src/boxyard/_cli/main.py` — command definitions
- `../../src/boxyard/_cli/multi_sync.py` — `multi-sync`
- `../../src/boxyard/_models.py` — box path and metadata layout
- `../../src/boxyard/_shell_helper.py` — shell helper behavior
