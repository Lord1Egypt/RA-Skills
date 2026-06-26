# Encoding checklist for Windows shell problems

Use this file when output is garbled, Chinese text turns into mojibake, JSON contains literal `\\uXXXX`, or files look correct in one tool but broken in another.

## Fast triage

1. Check whether the corruption happened:
   - in the terminal
   - in a file written to disk
   - over HTTP payload transport
   - after another tool re-serialized the text
2. Check shell and host:
   - Windows PowerShell 5.x behaves differently from PowerShell 7+
   - old console hosts often show encoding issues more easily
3. Check file encoding explicitly.
4. Prefer moving rich text into UTF-8 files rather than inline command arguments.

## Common failure modes

### A. Bash-style command pasted into PowerShell

Symptoms:
- parser error near `<`
- weird tokenization around quotes
- command never reaches the target program correctly

Fix shell syntax first. Encoding may be a secondary issue.

### B. Unicode was JSON-escaped as literal text

Symptoms:
- server stores `\\u4e2d\\u6587` literally
- resulting page or document shows backslash-u sequences

Safer pattern:
- serialize with real UTF-8 bytes when supported
- avoid transport paths that double-escape JSON
- prefer request files for rich content

### C. File written with the wrong encoding

Prefer:

```powershell
Set-Content -Path .\out.txt -Value $text -Encoding UTF8
```

For BOM control:

```powershell
[System.IO.File]::WriteAllText(
  '.\\out.txt',
  $text,
  [System.Text.UTF8Encoding]::new($false)
)
```

### D. CRLF/LF mismatch

Symptoms:
- shell scripts fail oddly
- parsers complain about invisible characters
- line-based tools behave inconsistently across platforms

Check line endings and normalize when needed.

## Advice patterns

- Prefer UTF-8 file inputs over inline console arguments for large Chinese payloads.
- Prefer `Get-Content -Raw` when passing whole-file content through a pipeline.
- Say whether the issue is display-only or data corruption; these need different fixes.
