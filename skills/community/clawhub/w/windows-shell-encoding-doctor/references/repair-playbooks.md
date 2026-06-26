# Repair playbooks

Read this file when the user says “it broke, how do I fix it?” rather than naming a precise technical category.

Every playbook follows the same sequence:

1. Identify the current shell.
2. Classify the issue as shell / quoting / encoding / path / line ending.
3. Give the lowest-risk fix first.
4. If needed, provide a safer file-based variant.

## Playbook 1: Bash heredoc pasted into PowerShell

### Typical input

- `python - <<'PY'` fails on Windows
- `Missing file specification after redirection operator`
- parser error near `<`

### Diagnostic path

- Confirm whether the shell is PowerShell.
- If yes, strongly suspect bash heredoc syntax pasted directly into PowerShell.
- Do not blame Python / Node / curl first.

### Fix strategy

Prefer here-string + stdin:

```powershell
@'
print("hello")
'@ | python -
```

If the content is longer or more deeply nested, write a temporary file instead.

### Response shape

- State clearly that the original command is bash syntax, not PowerShell syntax.
- Then provide a PowerShell-native equivalent.
- If Chinese text or JSON is involved, prefer a file-based fix.

## Playbook 2: JSON argument passing explodes in PowerShell

### Typical input

- curl / Invoke-RestMethod / another CLI rejects the JSON body
- quotes disappear
- payload structure breaks
- Chinese text is mixed in as well

### Diagnostic path

- Check whether the inline JSON is too long or too heavily escaped.
- Then check whether Chinese text makes encoding a second risk factor.

### Fix strategy

Preferred order:

1. Hashtable + `ConvertTo-Json`
2. Write a UTF-8 request file
3. Only keep a complex inline one-liner as a last resort

### Safer template

```powershell
$body = @{
  title = '中文标题'
  content = '<p>内容</p>'
} | ConvertTo-Json -Depth 10

$path = Join-Path (Get-Location) 'request.json'
[System.IO.File]::WriteAllText($path, $body, [System.Text.UTF8Encoding]::new($false))
```

## Playbook 3: Chinese looks garbled, but it is unclear whether the data is actually corrupted

### Typical input

- terminal output is garbled
- the file opens correctly in an editor
- API output looks wrong, but the server may not have stored bad data

### Diagnostic path

Separate two cases first:

1. display-only console garbling
2. real corruption on disk or in transport

### Fix strategy

- Do not rebuild the whole pipeline immediately.
- Check file encoding, console encoding, and whether literal `\\uXXXX` sequences are present.
- Inspect the file bytes / BOM / line endings before changing the pipeline.
- Prefer UTF-8 files for Chinese rich text and payload transport.

### Response priority

Tell the user clearly whether the problem is display-only or real data corruption.

## Playbook 4: The path exists, but the tool still says file not found

### Typical input

- the file is visible in `dir` / Explorer
- the tool says `file not found`
- paths with spaces fail especially often

### Diagnostic path

Check, in order:

- whether the path is quoted as a whole
- whether the current working directory is correct
- whether PowerShell, cmd, or the external Windows tool is interpreting the path differently

### Fix strategy

Prefer:

```powershell
python ".\scripts\tool.py"
Get-Content ".\data\input file.json"
```

Use absolute paths when needed.

## Playbook 5: A script edited on Windows breaks on Linux

### Typical input

- shebang stops working
- `^M` appears
- parser errors appear on Linux but not on Windows

### Diagnostic path

Suspect CRLF / LF mismatch before blaming the script language itself.

### Fix strategy

- Inspect the file's line endings.
- Then normalize the file to LF with a safe editor or line-ending conversion step.

### Response priority

Tell the user this is a cross-platform line-ending issue, not that the script logic suddenly broke.

## General rules

- Prefer the smallest safe change that fixes the issue.
- Explain underlying theory only when needed.
- If JSON, multiline payloads, and Chinese text appear together, strongly prefer a file-based approach.
- If the error points near `<`, check for bash heredoc misuse first.
