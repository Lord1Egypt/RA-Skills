# Common Windows shell failures

Use this file when the user pasted a failing command or error message and the likely cause is not obvious at first glance.

## 1) Bash heredoc pasted into PowerShell

### Symptom

- parser error near `<`
- `Missing file specification after redirection operator`
- multiline script never reaches Python / Node / curl

### Likely cause

Bash heredoc syntax like `<<'EOF'` or `<<'PY'` was pasted into PowerShell.

### Safer fix

- Replace with a PowerShell here-string piped into stdin, or
- write a temp file and run it

### Preferred response shape

- state that the command is bash syntax
- give a PowerShell-native equivalent
- prefer temp files if JSON or Chinese text is involved

## 2) `export VAR=value` used in PowerShell

### Symptom

- `export` not recognized
- environment variable appears unset in the child process

### Likely cause

Bash environment variable syntax used in PowerShell.

### Safer fix

```powershell
$env:VAR = 'value'
```

## 3) JSON body breaks only on Windows

### Symptom

- API rejects JSON
- quotes disappear or double-escape
- Chinese text becomes mojibake or literal `\\uXXXX`

### Likely cause

Inline JSON was over-escaped in the shell, or the shell / tool wrote text with the wrong encoding.

### Safer fix

- build JSON as a PowerShell object and `ConvertTo-Json`, or
- write a UTF-8 request file and submit `@file`

See `references/json-and-stdin-patterns.md`.

## 4) `Get-Content` pipeline corrupts structured payloads

### Symptom

- line breaks inserted unexpectedly
- hash/signature mismatch
- file content arrives fragmented downstream

### Likely cause

`Get-Content` without `-Raw` returns an array of lines instead of one whole string.

### Safer fix

```powershell
Get-Content .\payload.json -Raw
```

## 5) Path exists but command says file not found

### Symptom

- file is visible in Explorer / `dir`
- tool says file not found or reads only part of the path

### Likely cause

Unquoted path with spaces, wrong working directory, or tool-specific path parsing.

### Safer fix

- quote the full path
- check the current working directory
- prefer relative paths only when the current directory is explicit

## 6) Script works in Git Bash but not in PowerShell

### Symptom

- pipelines or redirection behave differently
- `/dev/null`, `&&`, `grep`, `xargs`, `sed -i`, or command substitution breaks

### Likely cause

The command depends on bash semantics or Unix tool behavior.

### Safer fix

Translate intent, not token-by-token syntax. See `references/powershell-vs-bash.md`.

## 7) Chinese displays as garbage but file is actually fine

### Symptom

- terminal output is garbled
- file content opens correctly in a UTF-8-aware editor

### Likely cause

Display-only console encoding mismatch.

### Safer fix

Say clearly that the underlying data may be intact. Distinguish display problems from on-disk corruption before rewriting the pipeline.

## 8) Shell script fails due to invisible characters

### Symptom

- parser errors on Linux after editing on Windows
- shebang not respected
- odd `^M` behavior

### Likely cause

CRLF / LF mismatch.

### Safer fix

Normalize line endings deliberately: editor set to LF, `core.autocrlf` / `.gitattributes`, `dos2unix`, or another safe conversion path.
