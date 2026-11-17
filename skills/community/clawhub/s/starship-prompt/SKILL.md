---
name: starship-prompt
description: Expert knowledge of Starship cross-shell prompt — installation, CLI, TOML config, all modules, style strings, presets, advanced features including transient prompts, custom modules, palettes, right prompt, and Fish shell integration.
author: Hermes
tags: [starship, prompt, fish, shell, terminal, rust, toml]
metadata:
  openclaw:
    os: [linux]
    homepage: https://github.com/mina-atef-00/agent-skills
    requires:
      bins: [starship]
---

# Starship Prompt — Complete Reference

Starship is the minimal, blazing-fast, infinitely customizable prompt for any shell. Written in Rust. Installed at `/usr/sbin/starship` v1.24.2 on this system.

This skill covers the **entire** Starship surface: CLI, configuration, all ~70 modules, advanced features, presets, Fish-specific integration, and debugging.

---

## 1. Installation

### Linux (Fedora — this system)

```fish
# Via Copr (recommended for Fedora)
dnf copr enable atim/starship
dnf install starship

# Via curl install script
curl -sS https://starship.rs/install.sh | sh

# Via cargo
cargo install starship --locked

# Via Linuxbrew
brew install starship
```

### Fish Shell Setup

Add this to the **end** of `~/.config/fish/config.fish`:

```fish
starship init fish | source
```

Verify with: `starship --version` (expected: `starship 1.24.2`)

---

## 2. CLI Reference

```
starship <COMMAND>

Commands:
  bug-report    Create a pre-populated GitHub issue with config info
  completions   Generate shell completions for your shell to stdout
  config        Edit the starship configuration
  explain       Explains the currently showing modules
  init          Prints the shell function used to execute starship
  module        Prints a specific prompt module (e.g. `starship module rust`)
  preset        Prints a preset config to stdout or file
  print-config  Prints the computed starship configuration
  prompt        Prints the full starship prompt
  session       Generate random session key
  timings       Prints timings of all active modules (debugging)
  toggle        Toggle a given starship module on/off
  help          Print this message or the help of the given subcommand(s)
```

Key flags for `starship prompt`: `--status`, `--jobs`, `--cmd-duration`, `--keymap`, `--terminal-width`, `--logical-path`, `--path`.

---

## 3. Configuration File

Default path: **`~/.config/starship.toml`**

Override via environment variable: `STARSHIP_CONFIG`

### Schema

```toml
"$schema" = 'https://starship.rs/config-schema.json'
```

### Top-Level Options

| Option | Default | Description |
|--------|---------|-------------|
| `format` | `'$all'` | Prompt format string |
| `right_format` | `''` | Right-aligned prompt content |
| `scan_timeout` | `30` | File-scan timeout (ms) |
| `command_timeout` | `500` | Command-execution timeout (ms) |
| `add_newline` | `true` | Blank line between prompts |
| `palette` | `''` | Active color palette name |
| `palettes` | `{}` | Collection of color palettes |
| `follow_symlinks` | `true` | Follow symlinks for directory checks |
| `continuation_prompt` | `'[∙](bright-black) '` | Prompt for incomplete input |

### Format Strings

- Variables: `$variable_name` (letters, numbers, `_`)
- Text groups: `[content](style)` — styles the content
- Conditionals: `(@$region)` — only shows if `$region` is non-empty
- `$all` — expands to all enabled modules (in default order)

### Style Strings

Space-separated tokens: `bold`, `italic`, `underline`, `dimmed`, `inverted`, `blink`, `hidden`, `strikethrough`, `fg:<color>`, `bg:<color>`, `<color>`, `none`

Color specifiers:
- Named: `black`, `red`, `green`, `blue`, `yellow`, `purple`, `cyan`, `white`
- Bright: `bright-` prefix (e.g. `bright-red`)
- Hex: `#RRGGBB`
- ANSI 8-bit: `0`–`255`
- Contextual: `prev_fg`, `prev_bg`

---

## 4. All Modules

### VCS Modules
| Module | Key Config | Default Triggers |
|--------|-----------|------------------|
| `git_branch` | `truncation_length`, `ignore_branches`, `only_attached` | Git repo |
| `git_commit` | `commit_hash_length`, `tag_disabled`, `only_detached` | Detached HEAD |
| `git_state` | `rebase`, `merge`, `revert`, `bisect` labels | Rebase/merge/etc. in progress |
| `git_status` | `conflicted`, `ahead`, `behind`, `staged`, `deleted` | Git repo |
| `git_metrics` | `added_style`, `deleted_style` | Git repo |
| `hg_branch` | — | Mercurial repo |
| `fossil_branch` | `truncation_length` | Fossil checkout |
| `pijul_channel` | — | Pijul repo |

### Language Runtimes (60+)
All share this pattern:
```toml
[<module>]
format = 'via [$symbol($version )]($style)'
version_format = 'v${raw}'
symbol = '...'
style = '<style>'
detect_extensions = [...]
detect_files = [...]
detect_folders = [...]
disabled = false
```

Modules include: `bun`, `c`, `cmake`, `cobol`, `cpp`, `daml`, `dart`, `deno`, `dotnet`, `elixir`, `elm`, `erlang`, `fennel`, `fortran`, `gleam`, `golang`, `gradle`, `haskell`, `haxe`, `helm`, `java`, `julia`, `kotlin`, `lua`, `maven`, `mojo`, `nim`, `nodejs`, `ocaml`, `odin`, `opa`, `perl`, `php`, `pulumi`, `purescript`, `python`, `quarto`, `raku`, `rlang`, `red`, `ruby`, `rust`, `scala`, `solidity`, `swift`, `terraform`, `typst`, `vlang`, `vagrant`, `xmake`, `zig`, `buf`, `crystal`, `meson`

### Cloud & DevOps
| Module | Default | Notes |
|--------|---------|-------|
| `aws` | `bold yellow` | Region + profile + expiration timer |
| `gcloud` | `bold blue` | Active GCP config, account, region |
| `azure` | **Disabled** | Azure subscription name |
| `openstack` | — | Cloud config |
| `docker_context` | — | Active Docker context |
| `kubernetes` | — | K8s context/namespace |
| `nats` | — | NATS context |
| `singularity` | — | Singularity container |

### Shell & System
| Module | Description |
|--------|-------------|
| `username` | Shows when not default user, ssh, or container |
| `hostname` | SSH-visible hostname |
| `shlvl` | Shell nesting level |
| `localip` | IPv4 of primary network interface |
| `memory_usage` | RAM usage |
| `battery` | Only below 10% by default |
| `sudo` | When sudo credentials are cached |
| `cmd_duration` | Last command execution time |
| `jobs` | Background job count |
| `status` | Exit code of last command |
| `shell` | Current shell name |
| `os` | OS name (symbol) |
| `container` | Container indicator |
| `netns` | Network namespace |

### Directory & Navigation
| Module | Key Features |
|--------|-------------|
| `directory` | Truncation, git-root detection, `fish_style_pwd_dir_length`, `substitutions`, `home_symbol` |
| `direnv` | direnv status indicator |
| `nix_shell` | Nix shell indicator |
| `guix_shell` | Guix shell indicator |
| `conda` | Conda environment |
| `pixi` | Pixi project environment |
| `spack` | Spack environment |

### Utilities
| Module | Description |
|--------|-------------|
| `env_var` | Arbitrary env var display. Supports per-var: `[env_var.SHELL]` |
| `custom` | Arbitrary command output. Supports per-command: `[custom.mything]` |
| `fill` | Space-filler for alignment |
| `time` | Date/time display (disabled by default) |
| `line_break` | Line break between segments |
| `character` | Input prompt symbol (❯) — changes color/style on error |

### Package
| Module | Description |
|--------|-------------|
| `package` | Current package version from `package.json`, `Cargo.toml`, etc. |
| `mise` | mise (rtx) tool version manager |

### Claude Code Statusline
Three dedicated modules for Claude Code statusline (via `starship statusline claude-code`):
- `claude_model` — current model being used
- `claude_context` — context usage gauge + percentage with threshold styling
- `claude_cost` — session cost in USD with threshold styling

Customize via `[profiles]`:
```toml
[profiles]
claude-code = "$claude_model$git_branch$claude_context$claude_cost"
```

---

## 5. Fish Shell Integration

### Basic Setup

```fish
# ~/.config/fish/config.fish
starship init fish | source
```

### Transient Prompt (Fish)

Replace previous prompt with a minimal one after command execution. Requires **Fish 3.7+** (Fish 4.6+ on this system).

**Critical ordering:** `enable_transience` must come **AFTER** `starship init fish | source`:

```fish
# ~/.config/fish/config.fish
starship init fish | source

# ── Transient prompt ──
enable_transience

function starship_transient_prompt_func
    # Collapse to just the ❯ character on success/error
    starship module character
end

function starship_transient_rprompt_func
    # Clear right prompt so no leftover time/memory shows
end
```

**How it works:** With `enable_transience`, Fish redraws the prompt after command execution. The `starship_transient_prompt_func` is called instead of the full Starship init, producing a minimal collapsed prompt. The `starship_transient_rprompt_func` similarly controls the right prompt (set it to empty to clear).

**Important:** Transient prompt only prints when the commandline is non-empty and syntactically correct.

### Right Prompt

Supported in Fish via `right_format` in `starship.toml`:

```toml
right_format = "$all"
```

### Vim Mode Detection

The `character` module supports vim-mode symbols in Fish:
- `vimcmd_symbol` (normal mode, ❮ green)
- `vimcmd_replace_one_symbol` (❮ purple)
- `vimcmd_replace_symbol` (❮ purple)
- `vimcmd_visual_symbol` (❮ yellow)

---

## 6. Advanced Features

### Custom Modules

Define arbitrary command outputs:

```toml
[custom.mything]
command = "echo hello"
when = "test -f .mything"       # Boolean or shell command
shell = ['bash', '--noprofile']  # Optional shell override
require_repo = true              # Only in git repos
detect_files = ['.mything']
detect_folders = ['mything']
detect_extensions = ['thing']
os = "linux"                     # OS filter
unsafe_no_escape = false         # Escape shell sequences
ignore_timeout = false           # Bypass global timeout
```

Reference `${custom.foo}` in top-level `format`.

### Color Palettes

```toml
palette = "mytheme"

[palettes.mytheme]
blue = "21"
mustard = "#af8700"
green = "bright-green"
```

Palettes override color names used in style strings.

### Path Substitutions

```toml
[directory.substitutions]
'/Volumes/network/path' = '/net'
'src/com/long/java/path' = 'mypath'
```

Regex substitutions also supported:
```toml
substitutions = [
  { from = "^/", to = "<root>/", regex = true },
  { from = "/", to = " | " },
]
```

### Window Title

```fish
function set_win_title
    echo -ne "\033]0; (basename "$PWD") \007"
end
starship_precmd_user_func="set_win_title"
```

---

## 7. Presets

Apply presets with:

```sh
starship preset <preset-name> -o ~/.config/starship.toml
```

Available presets:

| Preset | Description |
|--------|-------------|
| `nerd-font-symbols` | Nerd Font icons for all modules |
| `no-nerd-font` | Plain Unicode, no Nerd Font dependency |
| `bracketed-segments` | Bracketed module segments instead of "via"/"on" |
| `plain-text` | Plain text symbols (no Unicode) |
| `no-runtimes` | Hides language runtime versions |
| `no-empty-icons` | Hides icons when tool not found |
| `pure-preset` | Emulates Pure prompt style |
| `pastel-powerline` | Pastel powerline with path substitution example |
| `tokyo-night` | Tokyo Night VS Code theme inspired |
| `gruvbox-rainbow` | Gruvbox rainbow theme |
| `jetpack` | Pseudo-minimalist inspired by geometry/spaceship |
| `catppuccin-powerline` | Catppuccin theme variant of Gruvbox Rainbow |

---

## 8. Debugging & Troubleshooting

### Logging

```sh
# Set log level
STARSHIP_LOG=trace starship module rust     # Debug a single module
STARSHIP_LOG=trace starship timings          # Find slow modules
STARSHIP_LOG=error starship prompt           # Suppress non-critical warnings
```

Logs written to `~/.cache/starship/session_${STARSHIP_SESSION_KEY}.log`. Override with `STARSHIP_CACHE`.

### Useful Debug Commands

```sh
starship explain        # Explain each visible module in current prompt
starship timings        # Show execution time of each module (>1ms)
starship print-config   # Print full resolved config
starship bug-report     # Generate pre-populated GitHub issue
```

### Common Issues

1. **Glyphs not showing**: Install a Nerd Font, set terminal to use it, ensure UTF-8 locale (`locale`, `LANG=en_US.UTF-8`)
2. **Command timeouts**: Increase `command_timeout = 500` in config, or set `ignore_timeout = true` on custom modules
3. **Slow prompt**: Use `starship timings` to identify slow modules
4. **Module not appearing**: Check `disabled = false`, verify detection conditions match
5. **No right prompt**: Only supported in: elvish, fish, zsh, xonsh, cmd, nushell, bash (with Ble.sh)

### TOML Pitfalls (Config-writing)

1. **DO NOT use `[format]` / `[right_format]` section headers.** These are top-level **string** variables, not TOML tables. Write them unpackaged:
   ```toml
   # ✅ Correct
   format = """
   [┌─](bold bright-white)$directory
   │  $python
   [└─](bold bright-white) ❯
   """
   
   # ❌ Wrong — "invalid type: map, expected a string"
   [format]
   format = """..."""
   ```

2. **`format` / `right_format` are raw strings**, not Starship format strings wrapped in TOML tables. They go at the top level, period.

3. **TOML multiline basic strings (`"""..."""`)** — Real newlines inside are preserved, and Starship treats them the same as `$newline`. So you can use literal newlines directly:
   ```toml
   format = """
   Line 1
   Line 2
   """
   ```
   This produces a two-line prompt with a blank line between them. Starship collapses consecutive newlines the same way `$newline` does.

4. **`\\` at end of line** in TOML multiline strings is a **line continuation** — it strips the real newline, concatenating the next line as if it's the same line. Use this when you want to write a very long format string across multiple source lines:
   ```toml
   format = """\
   $directory$git_branch\
   $fill$time\
   $newline\
   $character\
   """
   # Actual string value: "$directory$git_branch$fill$time$newline$character"
   ```

5. **`[fill]` dots**: By default, `$fill` in the format expands to `.` characters. Set `symbol = " "` under `[fill]` to make it invisible (spaces instead of dots).

6. **`up_to_date` in `[git_status]`**: The key is `up_to_date` (with underscores), **not** `uptodate`. Using `uptodate` produces a warning: "Unknown key".

7. **Character module with literal `❯`**: If you hardcode `❯` or `❮` in the format string instead of using `$character`, disable the character module explicitly to avoid redundant rendering:
   ```toml
   [character]
   format = ''
   success_symbol = ''
   error_symbol = ''
   ```

8. **`starship module character` still works** even when the character module is disabled — it internally handles exit code detection and returns `success_symbol` or `error_symbol`. Use it in transient prompt functions even with a disabled character module.

9. **Time zone duplicates**: Having `$time` in both `format` and `right_format` causes it to render twice. Keep it only where you want it — typically `right_format` for right-edge alignment.

10. **Runtime detection**: Modules like `python`, `nodejs`, `bun` trigger on `detect_files`, `detect_extensions`, or `detect_folders`. They run shell commands (e.g., `python --version`) only when their trigger conditions match. This keeps the prompt fast — scanning the filesystem for triggers is cheaper than running version commands on every prompt.

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `STARSHIP_CONFIG` | Override config file path |
| `STARSHIP_CACHE` | Override cache directory |
| `STARSHIP_LOG` | Log level: `trace`, `debug`, `info`, `warn`, `error` |
| `STARSHIP_SESSION_KEY` | Session identifier for logs |
| `STARSHIP_SHELL` | Shell override used by custom modules |

---

## 10. Reference Config: Transient Minimal (Fish + Fedora Atomic)

A complete, production-tested config designed for Fish with `enable_transience` on Fedora Atomic (Catppuccin Mocha terminal, JetBrainsMono Nerd Font). Demonstrates multi-line box-drawing layout, right-aligned time, runtime detection, and proper Fish transient wiring.

### ~/.config/starship.toml

```toml
"$schema" = 'https://starship.rs/config-schema.json'

format = """
[┌─](bold bright-white)$directory$git_branch$git_status$fill$time
│  $python$nodejs$bun$cmd_duration
[└─](bold bright-white) ❯
"""

[fill]
symbol = " "

[directory]
truncation_length = 3
truncation_symbol = '…/'
fish_style_pwd_dir_length = 1
style = 'bold cyan'
home_symbol = '~'
format = '[$path]($style)'
read_only = ' '

[git_branch]
format = '[$symbol$branch]($style)'
style = 'bold purple'
symbol = '  '
truncation_length = 20
truncation_symbol = '…'

[git_status]
format = '[$all_status$ahead_behind]($style)'
style = 'bold yellow'
conflicted = '🏳'
up_to_date = ''
ahead = '⇡${count}'
behind = '⇣${count}'
diverged = '⇕${ahead_count}⇣${behind_count}'
staged = '●${count}'
modified = '✎${count}'
deleted = '✗${count}'
renamed = '➜${count}'
stashed = '≡ '
untracked = '?${count}'
ignore_submodules = false

[time]
format = '[$time]($style)'
style = 'bright-black'
time_format = '%l:%M %p'
disabled = false

[nodejs]
format = 'via [$symbol$version]($style) '
style = 'bold green'
symbol = ' '
detect_extensions = ['js', 'ts', 'mjs', 'cjs', 'jsx', 'tsx', 'vue']
detect_files = ['package.json', '.node-version', 'bun.lock']
detect_folders = ['node_modules']

[python]
format = 'via [$symbol$version]($style) '
style = 'bold yellow'
symbol = ' '
detect_extensions = ['py', 'pyw']
detect_files = ['requirements.txt', 'pyproject.toml', 'Pipfile', 'poetry.lock']
detect_folders = ['.venv', 'venv', 'env', '.env']

[bun]
format = 'via [$symbol$version]($style) '
style = 'bold red'
symbol = '🥟 '
detect_files = ['bun.lock', 'bun.lockb', 'bunfig.toml']

[cmd_duration]
format = '  took [$duration]($style)'
style = 'bold yellow'
min_time = 2_000
show_milliseconds = false

[character]
success_symbol = '[❯](bold green)'
error_symbol = '[❯](bold red)'

# Disable unused modules
[package]
disabled = true

[shell]
disabled = true

[line_break]
disabled = true

[golang]
disabled = true

[rust]
disabled = true

[dart]
disabled = true

[elixir]
disabled = true

[helm]
disabled = true

[terraform]
disabled = true
```

### ~/.config/fish/config.fish (Starship section)

```fish
starship init fish | source

# ── Transient prompt ──
enable_transience

function starship_transient_prompt_func
    # Pass $argv so --status is forwarded for red ❯ on errors
    starship module character $argv
end

function starship_transient_rprompt_func
    # Clear right prompt on transient (no leftover time/memory)
end
```

### Expected Visual

```
┌─ ~/src/my-project  main ●1 ⇡2                                         1:15 AM
│  via  v3.14.5   took 3s
└─ ❯
```

After command execution (transient): `❯`

### Verification

```sh
starship explain        # Explain each visible module
starship timings        # Ensure all modules <5ms
starship print-config   # Verify resolved config
```
