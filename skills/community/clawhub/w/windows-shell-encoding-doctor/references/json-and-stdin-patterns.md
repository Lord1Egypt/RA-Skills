# JSON and stdin patterns on Windows

Use this file when the user needs to send structured payloads, multiline text, code snippets, or Chinese content through PowerShell without fighting escaping.

## Preferred patterns

### Pattern 1: Build JSON as an object

Use when the payload is moderate in size and values are already available as variables.

```powershell
$body = @{
  title = '中文标题'
  tags = @('a', 'b')
  nested = @{ enabled = $true }
} | ConvertTo-Json -Depth 5
```

Then pass `$body` to the client in the safest supported way.

### Pattern 2: Write UTF-8 request file

Use when:
- the payload contains lots of quotes
- the payload contains Chinese text
- the target tool supports `@file`
- reproducibility matters

```powershell
$body = @{
  title = '中文标题'
  content = '<p>内容</p>'
} | ConvertTo-Json -Depth 10

$path = Join-Path (Get-Location) 'request.json'
[System.IO.File]::WriteAllText($path, $body, [System.Text.UTF8Encoding]::new($false))
```

Then submit `@request.json` if the target tool supports it.

### Pattern 3: Pipe here-string into stdin

Use for short scripts or text blocks.

```powershell
@'
print("hello")
'@ | python -
```

If the content is long or contains multiple layers of quoting, prefer a file.

## Anti-patterns

- giant inline JSON one-liners with many escaped quotes
- bash heredocs pasted directly into PowerShell
- relying on terminal encoding for rich Chinese payloads
- using `Get-Content` without `-Raw` for whole-file transport

## Rule of thumb

If you see JSON + Chinese + PowerShell in the same command, strongly consider writing a UTF-8 file first.
