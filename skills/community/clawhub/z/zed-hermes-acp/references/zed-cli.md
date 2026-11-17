# Zed CLI Reference (Linux) — Script & Command-line Integration

Distilled from Zed's CLI docs for the `zed-hermes-acp` skill. Covers opening
files/directories from the command line, controlling Zed from scripts, and the
flags most useful for agent/workflow automation. Linux-only — macOS/Windows
sections (release-channel switching, WSL) are omitted.

## Installation (Linux)
The CLI is included with Zed packages. The binary name may vary by distribution
(commonly `zed` or `zeditor`). Add it to your `PATH` or call it by full name.

## Usage
```sh
zed [OPTIONS] [PATHS]...
```

## Opening Files and Directories
```sh
zed myfile.txt                                 # open a file
zed ~/projects/myproject                       # open a directory as a workspace
zed file1.txt file2.txt ~/projects/myproject   # open multiple paths
zed myfile.txt:42                              # open at line 42
zed myfile.txt:42:10                           # open at line 42, column 10
```

## Options
### `-w`, `--wait`
Wait for all opened files to be closed before the CLI exits. When opening a
directory, waits until the window is closed. Useful for tools that expect an
editor to block until editing is complete (e.g. `git commit`):
```sh
export EDITOR="zed --wait"
git commit
```

### `-n`, `--new`
Open paths in a new workspace window, even if already open elsewhere:
```sh
zed -n ~/projects/myproject
```

### `-a`, `--add`
Add paths to the currently focused workspace instead of opening a new window.
With multiple windows open, files open in the focused window:
```sh
zed -a newfile.txt
```

### `-r`, `--reuse`
Reuse an existing window, replacing its current workspace with the new paths:
```sh
zed -r ~/projects/different-project
```

### `-e`, `--existing`
Open paths in an existing Zed window instead of creating a new one:
```sh
zed -e myfile.txt
```
By default (without `-n`, `-a`, `-r`, or `-e`), directories open in the current
window's sidebar. Change this default with the `cli_default_open_behavior`
setting.

### `--diff`
Open a diff view comparing two files. Can be specified multiple times:
```sh
zed --diff file1.txt file2.txt
zed --diff old.rs new.rs --diff old2.rs new2.rs
```

### `--foreground`
Run Zed in the foreground, keeping the terminal attached. Useful for debugging:
```sh
zed --foreground
```

### `--user-data-dir`
Use a custom directory for all user data (database, extensions, logs) instead of
the default. Linux default: `$XDG_DATA_HOME/zed` (typically `~/.local/share/zed`):
```sh
zed --user-data-dir ~/.zed-custom
```

### `-v`, `--version`
Print Zed's version and exit:
```sh
zed --version
```

### `--completions`
Generate shell completions for the `zed` CLI:
```sh
eval "$(zed --completions bash)"        # ~/.bashrc
eval "$(zed --completions zsh)"         # ~/.zshrc
zed --completions fish | source          # ~/.config/fish/config.fish
```

### `--uninstall`
Uninstall Zed and remove all related files (macOS and Linux only):
```sh
zed --uninstall
```

### `--zed`
Specify a custom path to the Zed application or binary:
```sh
zed --zed /path/to/Zed myfile.txt
```

## Reading from Standard Input
Pass `-` as the path to read from stdin. This creates a temporary file with the
stdin content and opens it in Zed:
```sh
echo "Hello, World!" | zed -
cat myfile.txt | zed -
ps aux | zed -
```

## URL Handling
The CLI can open `zed://`, `file://`, and `ssh://` URLs:
```sh
zed zed://settings
zed file:///Users/whatever/.zshrc
zed ssh://me@example.com/abs/path
zed ssh://me@example.com:/abs/path
zed ssh://me@example.com/~/project
zed ssh://me@example.com:~/project
```

## Using Zed as Your Default Editor
Set Zed as the default editor for Git and other tools:
```sh
export EDITOR="zed --wait"
export VISUAL="zed --wait"
```
Add these lines to your shell configuration file (e.g. `~/.bashrc`, `~/.zshrc`).

## Exit Codes
| Code | Meaning                                           |
| ---- | ------------------------------------------------- |
| `0`  | Success                                           |
| `1`  | Error (details printed to stderr)                 |

When using `--wait`, the exit code reflects whether the files were saved before
closing.
