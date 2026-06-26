---
name: windows-shell-syntax
description: Use when giving terminal commands on Windows or when comparing Windows vs Linux shell syntax. Detect whether the shell is PowerShell or cmd.exe before suggesting commands. Prevent Bash-only syntax from being given to Windows users. Covers quoting, escaping, chaining, env vars, line continuation, and safe rewrite patterns for cmd, PowerShell, and Bash.
---

# Windows Shell Syntax

Use this skill whenever the user is on Windows and asks for terminal commands, shell scripts, escaping rules, or asks to compare Windows and Linux terminal syntax.

## First rule: identify the shell

Do **not** say "Windows terminal syntax" as if Windows had one shell.

On Windows, distinguish between:

- **PowerShell** (`powershell`, `pwsh`)
- **cmd.exe** (`cmd`)
- **Git Bash / WSL bash** (Unix-style shell on Windows)

`Windows Terminal` is only the terminal app. It can host multiple shells.

If the shell is unclear:

- Ask which shell they use, **or**
- Give separate `PowerShell:` and `cmd:` variants.

## Hard rule

Never give Bash-only syntax to a Windows user unless they explicitly said they are using:

- Git Bash
- WSL
- MSYS2
- Cygwin
- a Linux remote shell

Examples of Bash-only habits that must not be handed to cmd/PowerShell users without labeling:

- `export NAME=value`
- `$VAR` for environment variables in cmd
- backslash escaping like `\"` as the default Windows answer
- `rm`, `mv`, `cp` as if they were native cmd syntax
- line continuation with `\`

## The `&&` / `||` compatibility rule

Do **not** say "Windows does not support `&&`".

The real compatibility matrix is:

- **cmd.exe**: supports `&`, `&&`, and `||`
- **PowerShell 7+**: supports `&&` and `||`
- **Windows PowerShell 5.1**: does **not** support `&&` and `||`
- **Git Bash / WSL**: supports `&&` and `||`

This means the question is **which shell and which PowerShell version**, not just "Windows or not".

### Safe default for uncertain PowerShell version

If you know only that the user is in PowerShell, but do **not** know whether it is:

- **Windows PowerShell 5.1** (`powershell`), or
- **PowerShell 7+** (`pwsh` / modern PowerShell)

then **avoid** `&&` / `||` in the default answer and use explicit guarded logic instead.

## Quick mapping

### Escaping / quoting

#### cmd.exe

- Escape metacharacters with `^`
- Typical special chars: `& | ( ) < > ^`
- Example literal quote in a cmd snippet for users who need cmd escaping context: `^"`
- Use `"..."` for paths with spaces
- Environment variables: `%USERPROFILE%`
- Line continuation: `^` at end of line
- Chain commands:
  - always run next: `&`
  - next only on success: `&&`
  - next only on failure: `||`

#### PowerShell

- Prefer single quotes `'...'` for literal strings
- Double quotes `"..."` are expandable: variables/interpolation work inside them
- Escape character is the backtick: `` ` ``
- Literal double quote often does **not** need escaping if you wrap the whole string in single quotes
- Environment variables: `$env:USERPROFILE`
- Line continuation: usually avoid; if needed use backtick at end of line, but prefer splatting or parentheses for readability
- **PowerShell 7+** supports `&&` / `||`
- **Windows PowerShell 5.1** does **not** support `&&` / `||`
- When compatibility matters, prefer explicit `if` checks over pipeline chain operators

#### Bash

- Escape character: `\`
- Strong literal quotes: `'...'`
- Expandable quotes: `"..."`
- Environment variables: `$HOME`, `$VAR`
- Line continuation: `\` at end of line

## Safe answer pattern

When the user asks for a command and the shell is not specified, prefer this structure:

```text
PowerShell:
<command>

cmd:
<command>
```

Do **not** provide only one unlabeled command if syntax differs.

If version compatibility matters, prefer this structure:

```text
PowerShell 5.1 compatible:
<command>

PowerShell 7+:
<command>

cmd:
<command>
```

## Rewrite rules

### 1. Command chaining

If you were about to write Bash chaining, rewrite for the actual shell.

- Bash: `cmd1 && cmd2`
- cmd: `cmd1 && cmd2`
- PowerShell 7+: `cmd1 && cmd2`
- PowerShell 5.1 compatible: `cmd1; if ($?) { cmd2 }`

Example:

```text
PowerShell 5.1 compatible:
cmd1
if ($?) { cmd2 }

PowerShell 7+:
cmd1 && cmd2

cmd:
cmd1 && cmd2
```

### 2. How to replace `&&`

When a user says `&&` does not work, first infer the likely shell:

- If they are in **Windows PowerShell 5.1**, replace:
  - `cmd1 && cmd2` → `cmd1; if ($?) { cmd2 }`
  - `cmd1 || cmd2` → `cmd1; if (-not $?) { cmd2 }`
- If they are in **cmd**, keep `&&` / `||`
- If they are in **PowerShell 7+**, `&&` / `||` are valid and usually can stay as-is

For **native executables** in PowerShell, a more explicit form may be safer when exit-code behavior matters:

```powershell
cmd1
if ($LASTEXITCODE -eq 0) { cmd2 }
```

Use this especially when the left-hand side is an `.exe` or external CLI and you want to be precise about process exit codes.

### 3. Environment variables

- Bash: `export NAME=value`
- PowerShell: `$env:NAME = 'value'`
- cmd: `set NAME=value`

For reading values:

- Bash: `$NAME`
- PowerShell: `$env:NAME`
- cmd: `%NAME%`

### 4. Paths with spaces

Always quote Windows paths with spaces.

- PowerShell: `"C:\Program Files\App"`
- cmd: `"C:\Program Files\App"`

### 5. Embedded quotes

If the user is in **cmd**, remember `^` escaping for metacharacters and quote-sensitive cases.
If the user is in **PowerShell**, prefer changing quote style instead of piling on escapes.

Example:

```text
PowerShell:
python -c 'print("hello")'

cmd:
python -c "print(^\"hello^\")"
```

Keep cmd examples minimal and tested-looking; cmd quoting gets messy fast.

### 6. Multi-line commands

Prefer shell-native multi-line styles:

```text
PowerShell:
& python `
  script.py `
  --name test

cmd:
python ^
  script.py ^
  --name test
```

But if a one-line command is acceptable, prefer one line.

### 6.5 Quoting hell: prefer avoiding it

For **cmd** and **PowerShell**, deeply nested quoting can become fragile fast, especially for commands like:

- `python -c "..."`
- JSON passed inline on the command line
- regex patterns with both quotes and backslashes
- commands embedded inside another shell command

If quoting starts getting ugly, prefer a safer rewrite instead of trying to perfectly escape everything.

Preferred escape hatches:

- Put the content in a **script file** and run the file
- Put JSON in a **file** and pass the file path
- In PowerShell, prefer **single quotes outside** and double quotes inside when possible
- In cmd, prefer moving complex logic out of the command line entirely
- If both shells are possible, give a **PowerShell variant** rather than forcing a complicated cmd example

Rule of thumb: if the example needs a paragraph to explain the escaping, rewrite the approach.

### 6.6 Redirection/pipeline pitfalls: prefer simple patterns

Windows shells differ a lot in redirection and pipeline behavior.

- **cmd** pipelines are text-based
- **PowerShell** pipelines pass objects between commands
- stderr/stdout redirection can behave differently across native commands, cmd, and PowerShell

If a command depends on tricky redirection, prefer a simpler pattern:

- Write output to a file first, then read/process the file
- Run commands as separate steps instead of one dense pipeline
- In PowerShell, prefer explicit variables over clever pipeline chaining when clarity matters
- When giving a cross-shell answer, avoid advanced redirection unless you label shell-specific variants clearly

Rule of thumb: if correctness depends on subtle pipe/redirection semantics, choose a more explicit multi-step form.

### 7. Bash → Windows rewrite cheat sheet

Use this section when the user pastes a Bash command and wants the Windows equivalent.

#### `cmd1 && cmd2`

```text
Bash:
cmd1 && cmd2

PowerShell 5.1 compatible:
cmd1
if ($?) { cmd2 }

PowerShell 7+:
cmd1 && cmd2

cmd:
cmd1 && cmd2
```

#### `cmd1 || cmd2`

```text
Bash:
cmd1 || cmd2

PowerShell 5.1 compatible:
cmd1
if (-not $?) { cmd2 }

PowerShell 7+:
cmd1 || cmd2

cmd:
cmd1 || cmd2
```

#### `export NAME=value`

```text
Bash:
export NAME=value

PowerShell:
$env:NAME = 'value'

cmd:
set NAME=value
```

#### `echo $NAME`

```text
Bash:
echo $NAME

PowerShell:
echo $env:NAME

cmd:
echo %NAME%
```

#### `~/file.txt`

```text
Bash:
cat ~/file.txt

PowerShell:
Get-Content $HOME\file.txt

cmd:
type %USERPROFILE%\file.txt
```

#### `rm`, `cp`, `mv`

```text
Bash:
rm file.txt
cp a.txt b.txt
mv a.txt b.txt

PowerShell:
Remove-Item file.txt
Copy-Item a.txt b.txt
Move-Item a.txt b.txt

cmd:
del file.txt
copy a.txt b.txt
move a.txt b.txt
```

#### `VAR=value command`

This Bash pattern has no direct same-shape equivalent in PowerShell or cmd.

```text
Bash:
NAME=value mytool

PowerShell:
$env:NAME = 'value'
mytool

cmd:
set NAME=value
mytool
```

If the temporary-only behavior matters, mention that Bash can scope env vars to one command, while PowerShell/cmd examples usually need extra cleanup if true one-command scope is required.

#### `command \
  --flag value`

```text
Bash:
command \
  --flag value

PowerShell:
command `
  --flag value

cmd:
command ^
  --flag value
```

#### `grep pattern file.txt`

```text
Bash:
grep pattern file.txt

PowerShell:
Select-String pattern file.txt

cmd:
findstr pattern file.txt
```

#### `pwd` and `ls`

```text
Bash:
pwd
ls

PowerShell:
Get-Location
Get-ChildItem

cmd:
cd
dir
```

Note: `ls` and `pwd` may appear to work in PowerShell because of aliases, but if you are teaching shell syntax clearly, prefer the native command names.

## Version detection hints

Use these heuristics when deciding whether `&&` is safe in PowerShell:

- If the environment/tooling says `shell=powershell`, that only tells you the shell family, **not always the exact version**
- `pwsh` usually means **PowerShell 7+**
- `powershell` often means **Windows PowerShell 5.1** on older/default Windows setups
- If the user says "Windows PowerShell", assume **5.1** unless they say otherwise
- If the user says just "PowerShell" and compatibility matters, use the **5.1-safe** form

If you need a detection command, give:

```text
PowerShell:
$PSVersionTable.PSVersion
```

## Response policy

When replying to Windows users:

1. Infer shell from context if obvious.
2. If not obvious, label commands by shell.
3. Prefer PowerShell examples when the environment says `shell=powershell`.
4. If the user explicitly mentions `cmd` or says `^"`, answer in cmd syntax.
5. If converting from Linux/Bash to Windows, explain the key syntax changes briefly.
6. Do not call PowerShell syntax "Windows syntax" if the distinction matters.
7. If `&&` is involved, distinguish **cmd**, **PowerShell 7+**, and **PowerShell 5.1** instead of treating all Windows shells the same.

## Minimal explanation to include when helpful

Use short phrasing like:

- `Windows Terminal` is just the terminal app; the real syntax depends on whether you're running PowerShell or cmd.
- In `cmd`, escape special characters with `^`.
- In PowerShell, the escape character is the backtick, and single quotes are usually the easiest literal form.
- `&&` works in `cmd` and PowerShell 7+, but not in Windows PowerShell 5.1.

## Notes

- `cmd` commonly uses `^` for escaping special characters.
- PowerShell quoting rules differ substantially from cmd.
- For maximum compatibility in PowerShell, `cmd1; if ($?) { cmd2 }` is safer than assuming `&&` support.
- When in doubt, provide both variants instead of guessing.
