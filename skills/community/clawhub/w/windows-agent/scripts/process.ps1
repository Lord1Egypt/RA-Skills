# process.ps1 - Process Management for windows-agent
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("list","info","start","kill","monitor","wait","help")]
    [string]$Action,
    [string]$Name = "",
    [int]$ProcId = 0,
    [string]$Path = "",
    [string]$Arguments = "",
    [ValidateSet("memory","cpu","name","pid","")][string]$SortBy = "",
    [int]$Top = 0,
    [int]$Duration = 5,
    [switch]$Force
)
$ErrorActionPreference = "Continue"
try {
    switch ($Action) {
        "help" {
            Write-Output "process.ps1 - list, info, start, kill, monitor, wait"
            Write-Output "  list  [-Name [filter]] [-SortBy memory|cpu|name|pid] [-Top [n]]"
            Write-Output "  info  -ProcId [pid]"
            Write-Output "  start -Path [exe] [-Arguments [args]]"
            Write-Output "  kill  -ProcId [pid] | -Name [name] [-Force]"
            Write-Output "  monitor -ProcId [pid] [-Duration [seconds]]"
            Write-Output "  wait  -ProcId [pid]"
            Write-Output ""
            Write-Output "⚠️ info/monitor/wait 需 -ProcId(进程ID), 不支持 -Name。"
            Write-Output "   先用 list 查到 PID 再调用。"
        }
        "list" {
            $procs = Get-Process -ErrorAction SilentlyContinue
            if ($Name) { $procs = $procs | Where-Object { $_.ProcessName -like "*$Name*" } }
            $data = $procs | Where-Object { $_.Id -ne 0 } | ForEach-Object {
                [PSCustomObject]@{
                    PID=$_.Id; Name=$_.ProcessName
                    MemMB=[math]::Round($_.WorkingSet64/1MB,1)
                    CPU=if($_.CPU){[math]::Round($_.CPU,1)}else{0.0}
                    Title=if($_.MainWindowTitle){$_.MainWindowTitle}else{"-"}
                }
            }
            switch ($SortBy) {
                "memory" { $data = $data | Sort-Object MemMB -Descending }
                "cpu"    { $data = $data | Sort-Object CPU -Descending }
                "name"   { $data = $data | Sort-Object Name }
                "pid"    { $data = $data | Sort-Object PID }
                default  { $data = $data | Sort-Object MemMB -Descending }
            }
            if ($Top -gt 0) { $data = $data | Select-Object -First $Top }
            $data | ForEach-Object {
                $t = if($_.Title -ne "-"){ '  Title="' + $_.Title + '"' } else { "" }
                Write-Output ("PID={0,-6} Mem={1,8}MB  CPU={2,8}s  Name={3}{4}" -f $_.PID,$_.MemMB,$_.CPU,$_.Name,$t)
            }
            Write-Output "`nTotal: $($data.Count) processes$(if($Name){" matching '$Name'"})"
        }
        "info" {
            if ($ProcId -le 0) { Write-Error "Missing -ProcId. 提示: 先 process list 查 PID 再传 -ProcId"; exit 1 }
            $proc = Get-Process -Id $ProcId -EA SilentlyContinue
            if (-not $proc) { Write-Error "Not found: PID=$ProcId"; exit 1 }
            $st = try{$proc.StartTime.ToString("yyyy-MM-dd HH:mm:ss")}catch{"N/A"}
            $ep = try{$proc.Path}catch{"N/A"}
            Write-Output "PID=$ProcId  Name=$($proc.ProcessName)"
            Write-Output "Path: $ep"
            Write-Output "Started: $st"
            Write-Output "Memory: $([math]::Round($proc.WorkingSet64/1MB,1))MB (peak $([math]::Round($proc.PeakWorkingSet64/1MB,1))MB)"
            Write-Output "CPU: $([math]::Round($proc.CPU,2))s  Threads: $($proc.Threads.Count)  Handles: $($proc.HandleCount)"
            Write-Output "Window: $(if($proc.MainWindowTitle){$proc.MainWindowTitle}else{'(none)'})"
            Write-Output "Responding: $($proc.Responding)  Priority: $($proc.PriorityClass)"
        }
        "start" {
            if (-not $Path) { Write-Error "Missing -Path"; exit 1 }
            $p = if($Arguments){Start-Process $Path -ArgumentList $Arguments -PassThru}else{Start-Process $Path -PassThru}
            Start-Sleep -Milliseconds 500
            Write-Output "Started: $Path (PID=$($p.Id))"
        }
        "kill" {
            # 关键系统进程保护名单: 杀了会崩系统/桌面, 一律拒绝(含 -Force)
            $ProtectedNames = @("explorer","winlogon","lsass","services","csrss","smss","wininit","dwm","logonui","taskhost","taskhostw","fontdrvhost","sihost","conhost","System","registry","spoolsv","SearchHost","explorer.exe")
            $targets = @()
            if ($ProcId -gt 0) {
                $chk = Get-Process -Id $ProcId -EA SilentlyContinue
                if ($chk) { $targets += $chk }
            } elseif ($Name) {
                $targets += Get-Process -Name "*$Name*" -EA SilentlyContinue
            }
            foreach($tp in $targets){
                $pn = $tp.ProcessName -replace "\.exe$",""
                if ($ProtectedNames -contains $pn) {
                    Write-Error "拒绝杀死关键系统进程: $($tp.ProcessName) (PID=$($tp.Id)). 此进程是 Windows 关键组件, 强杀会导致桌面/系统崩溃。仅允许杀普通应用进程。"
                    exit 1
                }
            }
            if ($ProcId -gt 0) {
                $p = Get-Process -Id $ProcId -EA SilentlyContinue
                if (-not $p) { Write-Error "Not found: PID=$ProcId"; exit 1 }
                if ($Force) { Stop-Process -Id $ProcId -Force } else { Stop-Process -Id $ProcId }
                Write-Output "Killed: $($p.ProcessName) (PID=$ProcId)"
            } elseif ($Name) {
                $ps = Get-Process -Name "*$Name*" -EA SilentlyContinue
                if (-not $ps) { Write-Error "No match: '$Name'"; exit 1 }
                Write-Output "将杀 $($ps.Count) 个匹配 '$Name' 的进程:"
                $ps | Select-Object -First 8 | ForEach-Object { Write-Output "  PID=$($_.Id) Name=$($_.ProcessName)" }
                if ($ps.Count -gt 8) { Write-Output "  ...共 $($ps.Count) 个" }
                # 杀前先展示匹配进程(防模糊匹配 `*Name*` 误杀, 如 -Name cmd 勿误伤 cmdkey)
                $ps | ForEach-Object { if($Force){Stop-Process -Id $_.Id -Force}else{Stop-Process -Id $_.Id} }
                Write-Output "Killed: $($ps.Count) process(es) matching '$Name'"
            } else { Write-Error "Missing -ProcId or -Name. 提示: 先 process list 查 PID"; exit 1 }
        }
        "monitor" {
            if ($ProcId -le 0) { Write-Error "Missing -ProcId. 提示: 先 process list 查 PID 再传 -ProcId"; exit 1 }
            $proc = Get-Process -Id $ProcId -EA SilentlyContinue
            if (-not $proc) { Write-Error "Not found: PID=$ProcId"; exit 1 }
            Write-Output "Monitoring PID=$ProcId ($($proc.ProcessName)) for ${Duration}s..."
            $prev = $proc.CPU
            for ($i=0; $i -lt $Duration; $i++) {
                Start-Sleep 1
                $proc = Get-Process -Id $ProcId -EA SilentlyContinue
                if (-not $proc) { Write-Output "Process exited."; break }
                $d = [math]::Round($proc.CPU - $prev, 2); $prev = $proc.CPU
                Write-Output "[$((Get-Date).ToString('HH:mm:ss'))] Mem=$([math]::Round($proc.WorkingSet64/1MB,1))MB CPU-delta=${d}s Threads=$($proc.Threads.Count)"
            }
        }
        "wait" {
            if ($ProcId -le 0) { Write-Error "Missing -ProcId. 提示: 先 process list 查 PID 再传 -ProcId"; exit 1 }
            $proc = Get-Process -Id $ProcId -EA SilentlyContinue
            if (-not $proc) { Write-Output "PID=$ProcId already exited."; exit 0 }
            Write-Output "Waiting for PID=$ProcId ($($proc.ProcessName))..."
            $proc.WaitForExit()
            Write-Output "PID=$ProcId exited (code: $($proc.ExitCode))"
        }
    }
    exit 0
} catch { Write-Error "ERROR: $_"; exit 1 }
