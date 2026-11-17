# Windows Remote Host

Use this reference to run a persistent T3 backend on Windows and connect it to a controller over Tailscale or an SSH tunnel.

## Prerequisites

- Run PowerShell as the Windows user who owns the repositories and T3 state.
- Install T3 from the official channels in `updates-and-launchers.md` and confirm that it works in that user's shell.
- Install and authenticate Tailscale when the selected transport uses the Tailnet.
- Use a current-user Scheduled Task. Do not put pairing values, Tailscale auth keys, or SSH private keys in the task arguments.

This workflow starts the backend when that user logs on. Running it without an interactive logon requires a separately reviewed service account or credential strategy.

The skill folder documents the complete T3 configuration path, but it does not ship T3, Tailscale, OpenSSH, credentials, or Tailnet policy. Obtain those prerequisites through their trusted upstream and the local operator's access process.

For the stable Windows desktop application, use the official download page at <https://t3.codes/download> or the upstream package command:

```powershell
winget install T3Tools.T3Code
```

For a headless server or nightly build, follow the npm and GitHub release-channel instructions in `updates-and-launchers.md`. A Scheduled Task still needs an absolute command path that passes `Get-Command t3`.

## 1. Inspect the installed commands

Open PowerShell:

```powershell
$T3Command = Get-Command t3 -ErrorAction Stop
$T3Command.Source
t3 --version
t3 serve --help
```

Record the absolute executable or command-shim path reported by `Get-Command`. Do not assume a global npm path from another machine.

Check Tailscale when it is needed:

```powershell
$Tailscale = Join-Path $env:ProgramFiles 'Tailscale\tailscale.exe'
& $Tailscale status
& $Tailscale ip -4
```

If Tailscale is not installed, install the signed package and complete authentication before continuing:

```powershell
winget install --exact --id Tailscale.Tailscale
```

Use the interactive Tailscale login or an approved secret-management flow. Do not paste reusable auth keys into a public script or command transcript.

## 2. Choose the bind address

Use one of these modes:

- Direct Tailnet: bind T3 to the Windows host's Tailscale IPv4 address.
- Tailscale Serve: bind T3 to `127.0.0.1`, then configure and verify Tailscale Serve using `remote-tailscale.md`.
- SSH tunnel fallback: bind T3 to `127.0.0.1`, then use the controller-side tunnel from `multi-machine.md`.

The launcher should get the direct Tailnet address at runtime. Do not copy a temporary address into a Scheduled Task.

```powershell
$Tailscale = Join-Path $env:ProgramFiles 'Tailscale\tailscale.exe'
$BindAddress = & $Tailscale ip -4 | Select-Object -First 1
if (-not $BindAddress) {
    throw 'Tailscale did not return an IPv4 address.'
}
$BindAddress = $BindAddress.Trim()
```

For Tailscale Serve or SSH tunnel mode, the launcher uses loopback:

```powershell
$BindAddress = '127.0.0.1'
```

Do not use `0.0.0.0` unless broader LAN exposure was explicitly requested and reviewed.

## 3. Create a launcher

Create a user-owned launcher directory:

```powershell
$ServerRoot = Join-Path $env:LOCALAPPDATA 'T3CodeServer'
New-Item -ItemType Directory -Force -Path $ServerRoot | Out-Null
$Launcher = Join-Path $ServerRoot 'run-t3-server.ps1'
```

Save this as `run-t3-server.ps1`. Replace the executable placeholder with the value found on that host. Set `$BindMode` to `tailnet` for direct Tailnet mode or leave it as `loopback` for Tailscale Serve and SSH tunnel modes:

```powershell
$ErrorActionPreference = 'Stop'

$T3 = 'C:\absolute\path\to\t3.cmd'
$BindMode = 'loopback'
$BaseDir = Join-Path $env:USERPROFILE '.t3'

if ($BindMode -eq 'tailnet') {
    $Tailscale = Join-Path $env:ProgramFiles 'Tailscale\tailscale.exe'
    $Deadline = (Get-Date).AddSeconds(60)
    do {
        $AddressLine = & $Tailscale ip -4 2>$null |
            Select-Object -First 1
        $BindAddress = if ($AddressLine) {
            $AddressLine.Trim()
        }
        else {
            $null
        }
        if ($BindAddress) {
            break
        }
        Start-Sleep -Seconds 3
    } while ((Get-Date) -lt $Deadline)

    if (-not $BindAddress) {
        throw 'Tailscale did not return an IPv4 address within 60 seconds.'
    }
}
else {
    $BindAddress = '127.0.0.1'
}

& $T3 serve `
    --no-browser `
    --host $BindAddress `
    --port 3773 `
    --base-dir $BaseDir

exit $LASTEXITCODE
```

The bounded wait handles the normal at-logon race where Task Scheduler starts before Tailscale is connected. Task Scheduler's restart policy handles a later failure. Keep machine-specific paths in the local launcher, not in shared documentation.

Test the launcher in the foreground:

```powershell
powershell.exe -NoProfile -File $Launcher
```

Confirm that T3 prints the intended bind address, port, base directory, and pairing details. Stop the foreground process before registering the task.

If local policy blocks the script, do not bypass a managed execution policy. Use the organization's approved signing or policy process.

## 4. Register the Scheduled Task

Run these commands as the same Windows user:

```powershell
$TaskName = 'T3 Code Server'
$ReplaceExistingTask = $false
$ServerRoot = Join-Path $env:LOCALAPPDATA 'T3CodeServer'
$Launcher = Join-Path $ServerRoot 'run-t3-server.ps1'
$PowerShell = Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'
$PrincipalId = "$env:COMPUTERNAME\$env:USERNAME"

$Action = New-ScheduledTaskAction `
    -Execute $PowerShell `
    -Argument "-NoProfile -File `"$Launcher`""
$Trigger = New-ScheduledTaskTrigger -AtLogOn -User $PrincipalId
$Principal = New-ScheduledTaskPrincipal `
    -UserId $PrincipalId `
    -LogonType Interactive `
    -RunLevel Limited
$Settings = New-ScheduledTaskSettingsSet `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 1) `
    -StartWhenAvailable

$ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($ExistingTask) {
    $ExistingTask | Select-Object TaskName, State, TaskPath
    $ExistingTask.Actions
    $ExistingTask.Triggers
    $ExistingTask.Principal

    $Stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
    $Backup = Join-Path $ServerRoot "t3-code-server-task-backup-$Stamp.xml"
    Export-ScheduledTask -TaskName $TaskName | Set-Content -Path $Backup
    if (-not $ReplaceExistingTask) {
        throw "Task '$TaskName' already exists. Review $Backup and get operator confirmation before replacing it."
    }
}

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger `
    -Principal $Principal `
    -Settings $Settings `
    -Force
```

Use `$env:COMPUTERNAME\$env:USERNAME` for the principal. In an SSH session, `$env:USERDOMAIN` may report `WORKGROUP`, which can produce `No mapping between account names and security IDs was done`.

If the task already exists, the inspection block stops before `-Force`. Review the action, trigger, principal, and XML backup. After the operator confirms replacement, set `$ReplaceExistingTask = $true` for that registration run.

## 5. Start and verify

Start the task and inspect its state:

```powershell
Start-ScheduledTask -TaskName 'T3 Code Server'
Start-Sleep -Seconds 3
Get-ScheduledTask -TaskName 'T3 Code Server'
Get-ScheduledTaskInfo -TaskName 'T3 Code Server'
Get-NetTCPConnection -State Listen -LocalPort 3773
```

Verify the exact URL from the controller. Reboot Windows, log in as the task user, and repeat the task and listener checks.

The task history and `LastTaskResult` should not show a repeating restart loop. A running task without a listener usually means the launcher path, execution policy, T3 path, or arguments are wrong.

From a Linux controller, probe the direct Tailnet URL without relying on SSH:

```bash
curl --connect-timeout 5 --fail --silent --show-error \
  -o /dev/null "http://<windows-tailnet-ip>:3773/"
```

Replace the placeholder with the address reported by Tailscale on Windows. A successful exit proves that the controller reached a valid application response without printing the response body. Complete T3 pairing in the controller using the fields shown by the installed build.

## 6. Scope the Windows firewall

Loopback-only Tailscale Serve and SSH tunnel modes do not need an inbound T3 firewall rule.

For direct Tailnet mode, first test whether the controller reaches the T3 URL. If Windows Firewall blocks the connection, add a narrowly scoped rule from an elevated PowerShell window:

```powershell
$Tailscale = Join-Path $env:ProgramFiles 'Tailscale\tailscale.exe'
$BindAddress = & $Tailscale ip -4 | Select-Object -First 1
if (-not $BindAddress) {
    throw 'Tailscale did not return an IPv4 address.'
}
$BindAddress = $BindAddress.Trim()

New-NetFirewallRule `
    -DisplayName 'T3 Code Tailnet' `
    -Direction Inbound `
    -Action Allow `
    -Protocol TCP `
    -LocalAddress $BindAddress `
    -LocalPort 3773 `
    -RemoteAddress '<controller-tailnet-ip>'
```

Replace the placeholder with the controller's Tailnet address. Do not open the port to every remote address. If Tailnet ping works but the T3 port remains unreachable, inspect VPN policy and routing before widening the firewall rule. Use the SSH tunnel fallback when policy intentionally blocks direct inbound TCP.

## 7. Verify SSH fallback prerequisites

The Windows host needs an authorized, noninteractive OpenSSH Server route. From an approved administrative PowerShell session on Windows, record the host-key fingerprint:

```powershell
Get-Service sshd
Get-NetTCPConnection -State Listen -LocalPort 22
ssh-keygen -lf "$env:ProgramData\ssh\ssh_host_ed25519_key.pub"
```

On the Linux controller, obtain the offered key and compare its fingerprint with the Windows value over a separate trusted channel:

```bash
ssh-keyscan -t ed25519 windows-host 2>/dev/null | ssh-keygen -lf -
```

Do not continue when the fingerprints differ. After they match, establish host-key trust interactively, then verify key authentication without prompts:

```bash
ssh -o BatchMode=yes windows-user@windows-host true
```

The approved route must include a running Windows OpenSSH Server, authorized keys, trusted host keys, and any required Tailnet SSH policy. Do not disable host-key checking, put passwords in a unit file, or reconfigure SSH solely to bypass an access policy. If this preflight fails, stop and fix the approved SSH route or choose another transport.

Once SSH is approved and verified, keep T3 on loopback and create the controller-side local forward documented in `multi-machine.md`. Use the same `windows-user@windows-host` target in the foreground tunnel and persistent service, or use an SSH config alias that pins the intended user, key, and host.

## 8. Stop or update safely

Stopping a Scheduled Task may leave its child `node.exe` process listening. Inspect exact command lines before ending anything:

```powershell
Get-CimInstance Win32_Process |
    Where-Object {
        $_.Name -eq 'node.exe' -and
        $_.CommandLine -match 't3' -and
        $_.CommandLine -match 'serve' -and
        $_.CommandLine -match '3773'
    } |
    Select-Object ProcessId, CommandLine
```

Do not stop every Node.js process. After confirming the exact T3 server command and process ID, stop only that process:

```powershell
Stop-Process -Id <confirmed-process-id>
```

Then verify that port 3773 is free before updating or restarting:

```powershell
Get-NetTCPConnection -State Listen -LocalPort 3773 -ErrorAction SilentlyContinue
```

## Failure patterns

- Task registration fails with an account-mapping error: rebuild the principal with `$env:COMPUTERNAME\$env:USERNAME`.
- Task reports `Running`, but no listener exists: run the launcher interactively and inspect the absolute T3 path and arguments.
- Task stops, but port 3773 remains occupied: inspect exact `node.exe` command lines and stop only the confirmed T3 child.
- Tailnet ping succeeds, but the T3 URL fails: test TCP, then inspect the bind address, Windows Firewall, VPN, Tailnet policy, and routing.
- Controller opens the wrong machine: use a unique saved environment label and pairing record for every Windows host.
