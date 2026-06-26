# WSL-PowerShell Controller

Call Windows PowerShell from WSL to control Windows host from Linux environment.

## How It Works

WSL mounts Windows drives to `/mnt/`, allowing direct execution of Windows binaries:
- PowerShell: `/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe`
- CMD: `/mnt/c/Windows/System32/cmd.exe`

## Usage

### Execute PowerShell Commands

```bash
/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -Command "Your-Command"
```

### Execute PowerShell Scripts

```bash
/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -File "/mnt/c/path/to/script.ps1"
```

## Common Examples

### System Information
```bash
# Get system info
powershell.exe -Command "Get-ComputerInfo"

# Get process list
powershell.exe -Command "Get-Process | Select-Object -First 10 Name,Id,CPU"

# Get service status
powershell.exe -Command "Get-Service | Where-Object {$_.Status -eq 'Running'} | Select-Object -First 10 Name,DisplayName"
```

### File Operations
```bash
# List directory
powershell.exe -Command "Get-ChildItem C:\\Users"

# Copy file
powershell.exe -Command "Copy-Item C:\\source\\file.txt C:\\dest\\file.txt"

# Create file
powershell.exe -Command "New-Item -Path C:\\test.txt -ItemType File -Force"
```

### Process Management
```bash
# Start program
powershell.exe -Command "Start-Process notepad.exe"

# Stop process
powershell.exe -Command "Stop-Process -Name notepad -Force"
```

### Network Operations
```bash
# Get network config
powershell.exe -Command "Get-NetIPConfiguration"

# Ping test
powershell.exe -Command "Test-Connection -ComputerName google.com -Count 2"
```

## Path Conversion

WSL Path ↔ Windows Path:
- WSL: `/mnt/c/Users/Tao` ↔ Windows: `C:\Users\Tao`
- Use `wslpath` command:
  ```bash
  wslpath -w /mnt/c/Users  # Output: C:\Users
  wslpath -u C:\\Users     # Output: /mnt/c/Users
  ```

## Notes

1. **Permissions**: Some operations require administrator privileges, use `-Verb RunAs` for elevated PowerShell
2. **Path Escaping**: Backslashes `\` in Windows paths must be escaped as `\\`
3. **Encoding**: PowerShell outputs UTF-16 by default, may need conversion
4. **Execution Policy**: Running scripts may require `Set-ExecutionPolicy`

## Security Tips

- Use caution with system-level commands
- Avoid deleting critical system files
- Test commands before executing in production
