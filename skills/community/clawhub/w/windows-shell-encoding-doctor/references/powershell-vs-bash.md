# PowerShell vs Bash quick translation guide

Use this file when a command was clearly written for one shell and pasted into another.

## Common bash -> PowerShell mismatches

### Environment variables

Bash:

```bash
export API_KEY=value
```

PowerShell:

```powershell
$env:API_KEY = 'value'
```

### Heredoc / stdin script blocks

Bash:

```bash
python - <<'PY'
print('hi')
PY
```

PowerShell safer equivalent:

```powershell
@'
print("hi")
'@ | python -
```

If quoting is complex, write a temp file instead.

### Redirect null output

Bash:

```bash
command > /dev/null 2>&1
```

PowerShell:

```powershell
command *> $null
```

### Path style

Bash often tolerates `/` everywhere.
PowerShell usually accepts `/`, but Windows-native tools may prefer `\\` or quoted normal paths.
When in doubt, use quoted Windows paths.

### Command substitution

Bash:

```bash
NAME=$(git branch --show-current)
```

PowerShell:

```powershell
$NAME = git branch --show-current
```

### Grep / sed / awk pipelines

Do not mechanically port token-by-token.
Prefer native PowerShell objects when practical, or keep the external tools if they are installed and the command is simple.

Example:

Bash:

```bash
cat data.json | jq '.name'
```

PowerShell:

```powershell
Get-Content .\data.json -Raw | jq '.name'
```

## Translation policy

- Preserve intent, not exact syntax.
- Reduce escaping complexity where possible.
- Prefer file-based payloads over deeply escaped inline JSON.
- If the user is on PowerShell, return a PowerShell-first answer.
