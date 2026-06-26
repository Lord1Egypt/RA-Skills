# TrueCrypt command cookbook

Use these examples as templates. Replace paths, letters, and keyfile locations as needed.

## 1. Check whether TrueCrypt is installed

```powershell
$paths = @(
  'C:\Program Files\TrueCrypt\TrueCrypt.exe',
  'C:\Program Files (x86)\TrueCrypt\TrueCrypt.exe'
) | Where-Object { Test-Path $_ }

if ($paths) {
  $paths
} else {
  (Get-Command TrueCrypt.exe -ErrorAction SilentlyContinue).Source
}
```

## 2. Mount a file container

```bat
"C:\Program Files\TrueCrypt\TrueCrypt.exe" /v "C:\path\secret.tc" /l X /q
```

## 3. Mount with a keyfile

```bat
"C:\Program Files\TrueCrypt\TrueCrypt.exe" /v "C:\path\secret.tc" /l X /k "C:\path\keyfile.bin" /q
```

## 4. Mount read-only

```bat
"C:\Program Files\TrueCrypt\TrueCrypt.exe" /v "C:\path\secret.tc" /l X /m ro /q
```

## 5. Mount as removable media

```bat
"C:\Program Files\TrueCrypt\TrueCrypt.exe" /v "C:\path\secret.tc" /l X /m rm /q
```

## 6. Dismount one mounted volume

```bat
"C:\Program Files\TrueCrypt\TrueCrypt.exe" /d X /q
```

## 7. Dismount all TrueCrypt volumes

```bat
"C:\Program Files\TrueCrypt\TrueCrypt.exe" /d /q
```

## 8. Password on command line

Possible pattern:

```bat
"C:\Program Files\TrueCrypt\TrueCrypt.exe" /v "C:\path\secret.tc" /l X /p "YOUR_PASSWORD" /q
```

Use this only when the user explicitly accepts the risk. The password may be visible in process lists, logs, or history.

## 9. PowerShell wrapper pattern

```powershell
$tc = 'C:\Program Files\TrueCrypt\TrueCrypt.exe'
$volume = 'C:\path\secret.tc'
$letter = 'X'

& $tc /v $volume /l $letter /q
```

## Common switches

- `/v` - volume path
- `/l` - drive letter
- `/d` - dismount one letter or all volumes
- `/q` - quiet mode
- `/k` - keyfile path
- `/m` - mount options such as `ro` or `rm`
- `/p` - password on command line; avoid unless explicitly requested

## Notes

- Some old TrueCrypt GUI switches do not print helpful console output.
- Prefer giving users exact commands over telling them to discover help interactively.
- If a command must be validated safely, start with install checks or dismount commands before attempting a mount.
