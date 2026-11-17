# windows-health · PowerShell 扫描命令

## 性能诊断（只读）

```powershell
Get-PSDrive C | Select-Object Used,Free,@{n='UsedGB';e={[math]::Round($_.Used/1GB,1)}},@{n='FreeGB';e={[math]::Round($_.Free/1GB,1)}}
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10 Name,CPU,WorkingSet
Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 10 Name,WorkingSet
Get-CimInstance Win32_OperatingSystem | Select-Object TotalVisibleMemorySize,FreePhysicalMemory
Get-CimInstance Win32_StartupCommand | Select-Object Name,Command,Location
```

## 磁盘与目录

```powershell
Get-Volume | Select-Object DriveLetter,Size,SizeRemaining
Get-ChildItem $env:USERPROFILE -Directory | ForEach-Object { [PSCustomObject]@{Name=$_.Name; Size=(Get-ChildItem $_.FullName -Recurse -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum} } | Sort-Object Size -Descending | Select-Object -First 10
```

## 缓存（TIER 1）

```powershell
$caches = @($env:TEMP, "$env:LOCALAPPDATA\Temp", "$env:LOCALAPPDATA\npm-cache", "$env:APPDATA\npm-cache", "$env:LOCALAPPDATA\pip\Cache")
$caches | Where-Object { Test-Path $_ } | ForEach-Object { [PSCustomObject]@{Path=$_; Size=(Get-ChildItem $_ -Recurse -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum} }
```

## 大文件与 node_modules

```powershell
Get-ChildItem $env:USERPROFILE -Recurse -File -ErrorAction SilentlyContinue | Where-Object { $_.Length -gt 200MB -and $_.FullName -notmatch '\\AppData\\Roaming' } | Sort-Object Length -Descending | Select-Object -First 20 FullName,@{n='GB';e={[math]::Round($_.Length/1GB,2)}}
Get-ChildItem $env:USERPROFILE -Recurse -Directory -Filter node_modules -ErrorAction SilentlyContinue | ForEach-Object { [PSCustomObject]@{Path=$_.FullName; Size=(Get-ChildItem $_.FullName -Recurse -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum} } | Sort-Object Size -Descending | Select-Object -First 10
```

## 重复候选（先候选后 SHA256）

```powershell
Get-FileHash -Algorithm SHA256 '候选A','候选B'
```

只有哈希完全一致才能进入 `DELETE_DUPLICATE`。

## 启动项

```powershell
Get-CimInstance Win32_StartupCommand | Select-Object Name,Command,Location
Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run' | Format-List
```

注意：HKCU 为用户级（普通权限可管理）；HKLM 与系统服务需管理员。
