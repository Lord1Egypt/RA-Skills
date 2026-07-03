---
name: Prevent-WPS-Image-Hijack
description: "Permanently prevent WPS Office from hijacking image file associations, restore user control over default image viewers"
metadata:
  builtin_skill_version: "1.0"
  qwenpaw:
    emoji: "🛡️"
    requires: {}
---

# Prevent WPS Image File Association Hijacking

## Overview

This skill permanently disables WPS Office's image viewing module from hijacking system image file associations, solving the problem where WPS secretly changes image default openers to its own image viewer in the background.

## Execution Steps

### Step 1: Disable WPS Scheduled Tasks

WPS uses scheduled tasks to run in the background and modify file associations. The task names contain user-specific IDs that vary across computers, so we need to detect them dynamically.

**Auto-detect and disable all WPS scheduled tasks:**
```powershell
# Find all WPS-related scheduled tasks
$wpsTasks = Get-ScheduledTask | Where-Object { $_.TaskName -match 'WPS|wps' }
Write-Host "Found $($wpsTasks.Count) WPS scheduled tasks:"
$wpsTasks | Select-Object TaskName, State | Format-Table -AutoSize

# Disable all WPS scheduled tasks
$wpsTasks | ForEach-Object {
    try {
        Disable-ScheduledTask -TaskName $_.TaskName -ErrorAction Stop
        Write-Host "✅ Disabled: $($_.TaskName)"
    } catch {
        Write-Host "⚠️ Failed to disable: $($_.TaskName) - $($_.Exception.Message)"
    }
}
```

**Verification command:**
```powershell
Get-ScheduledTask | Where-Object { $_.TaskName -match 'WPS|wps' } | Select-Object TaskName, State
```

**Expected result:** All WPS scheduled tasks show status "Disabled"

### Step 2: Delete WPS Image Registry Entries

WPS registers numerous image format associations (WPS.PIC.*) in the registry that need to be completely removed.

**Auto-detect and delete HKCU WPS.PIC entries:**
```powershell
$regItems = Get-ChildItem 'HKCU:\SOFTWARE\Classes' | Where-Object { $_.PSChildName -like 'WPS.PIC*' }
Write-Host "Found $($regItems.Count) WPS.PIC registry entries"

$regItems | ForEach-Object {
    try {
        Remove-Item -Path $_.PSPath -Recurse -Force -ErrorAction Stop
        Write-Host "✅ Deleted: $($_.PSChildName)"
    } catch {
        Write-Host "⚠️ Failed to delete: $($_.PSChildName) - $($_.Exception.Message)"
    }
}
```

**Auto-detect and delete HKLM WPS.PIC entries (if present):**
```powershell
$regItemsHKLM = Get-ChildItem 'HKLM:\SOFTWARE\Classes' -ErrorAction SilentlyContinue | Where-Object { $_.PSChildName -like 'WPS.PIC*' }
if ($regItemsHKLM) {
    Write-Host "Found $($regItemsHKLM.Count) WPS.PIC registry entries in HKLM"
    $regItemsHKLM | ForEach-Object {
        try {
            Remove-Item -Path $_.PSPath -Recurse -Force -ErrorAction Stop
            Write-Host "✅ Deleted: $($_.PSChildName)"
        } catch {
            Write-Host "⚠️ Failed to delete: $($_.PSChildName) - $($_.Exception.Message)"
        }
    }
} else {
    Write-Host "No WPS.PIC registry entries found in HKLM"
}
```

**Verification command:**
```powershell
$countHKCU = (Get-ChildItem 'HKCU:\SOFTWARE\Classes' | Where-Object { $_.PSChildName -like 'WPS.PIC*' }).Count
$countHKLM = (Get-ChildItem 'HKLM:\SOFTWARE\Classes' -ErrorAction SilentlyContinue | Where-Object { $_.PSChildName -like 'WPS.PIC*' }).Count
Write-Host "HKCU remaining: $countHKCU, HKLM remaining: $countHKLM"
```

**Expected result:** All WPS.PIC.* registry entries are deleted, counts are 0

### Step 3: Delete photo.dll Plugin

The core plugin file of WPS image module, located in the addons/photo folder of WPS installation directory. WPS may be installed in multiple locations, so we need to search automatically.

**Auto-search and delete all photo.dll files:**
```powershell
# Search common installation paths
$paths = @(
    "${env:ProgramFiles}\WPS",
    "${env:ProgramFiles(x86)}\WPS",
    "${env:LOCALAPPDATA}\WPS",
    "C:\WPS",
    "D:\WPS",
    "E:\WPS"
)

$found = $false
foreach ($basePath in $paths) {
    if (Test-Path $basePath) {
        $dlls = Get-ChildItem $basePath -Recurse -Filter "photo.dll" -ErrorAction SilentlyContinue
        foreach ($dll in $dlls) {
            try {
                Remove-Item -Path $dll.FullName -Force -ErrorAction Stop
                Write-Host "✅ Deleted: $($dll.FullName)"
                $found = $true
            } catch {
                Write-Host "⚠️ Failed to delete: $($dll.FullName) - $($_.Exception.Message)"
            }
        }
    }
}

if (-not $found) {
    Write-Host "No photo.dll files found"
}
```

**Verification command:**
```powershell
$paths | ForEach-Object {
    if (Test-Path $_) {
        Get-ChildItem $_ -Recurse -Filter "photo.dll" -ErrorAction SilentlyContinue | Select-Object FullName
    }
}
```

**Expected result:** No photo.dll files found

### Step 4: Rename photolaunch.exe Files

WPS image viewer executable file, may exist in multiple versions, needs to be automatically searched and renamed.

**Auto-search and rename all photolaunch.exe files:**
```powershell
$paths = @(
    "${env:ProgramFiles}\WPS",
    "${env:ProgramFiles(x86)}\WPS",
    "${env:LOCALAPPDATA}\WPS",
    "C:\WPS",
    "D:\WPS",
    "E:\WPS"
)

$found = $false
foreach ($basePath in $paths) {
    if (Test-Path $basePath) {
        $exes = Get-ChildItem $basePath -Recurse -Filter "photolaunch.exe" -ErrorAction SilentlyContinue
        foreach ($exe in $exes) {
            try {
                $newName = $exe.FullName + ".bak"
                Rename-Item -Path $exe.FullName -NewName $newName -Force -ErrorAction Stop
                Write-Host "✅ Renamed: $($exe.FullName)"
                $found = $true
            } catch {
                Write-Host "⚠️ Failed to rename: $($exe.FullName) - $($_.Exception.Message)"
            }
        }
    }
}

if (-not $found) {
    Write-Host "No photolaunch.exe files found"
}
```

**Verification command:**
```powershell
$paths | ForEach-Object {
    if (Test-Path $_) {
        Get-ChildItem $_ -Recurse -Filter "photolaunch.exe" -ErrorAction SilentlyContinue | Select-Object FullName
    }
}
```

**Expected result:** No photolaunch.exe files found, only photolaunch.exe.bak

### Step 5: Remind User to Manually Set Default Applications

Due to Windows UserChoice registry key hash protection, scripts cannot directly modify it. Users need to manually change through the system settings interface.

**Reminder content:**
1. Press **Win + I** to open Settings
2. Go to **Apps → Default apps**
3. Enter file extension in search box (e.g., .jpg)
4. Or click "Choose defaults by file type"
5. Change the default application for the following extensions to desired program (e.g., Windows Photo Viewer):
   - .jpg, .jpeg, .png, .gif, .bmp, .tiff, .ico

**Optional: Restore Windows Photo Viewer**
If Windows Photo Viewer is not in the settings list, it may need to be restored through registry. But it's recommended to prioritize using the system settings interface.

## Verify Overall Effect

After completion, run the following command to verify all operations have taken effect:

```powershell
Write-Host "=== 1. Scheduled Tasks ===" 
Get-ScheduledTask | Where-Object { $_.TaskName -match 'WPS|wps' } | Select-Object TaskName, State | Format-Table -AutoSize

Write-Host "=== 2. WPS.PIC Registry Entries ===" 
$countHKCU = (Get-ChildItem 'HKCU:\SOFTWARE\Classes' | Where-Object { $_.PSChildName -like 'WPS.PIC*' }).Count
$countHKLM = (Get-ChildItem 'HKLM:\SOFTWARE\Classes' -ErrorAction SilentlyContinue | Where-Object { $_.PSChildName -like 'WPS.PIC*' }).Count
Write-Host "HKCU: $countHKCU, HKLM: $countHKLM"

Write-Host "=== 3. photo.dll ===" 
@("${env:ProgramFiles}\WPS", "${env:ProgramFiles(x86)}\WPS", "${env:LOCALAPPDATA}\WPS", "C:\WPS", "D:\WPS", "E:\WPS") | ForEach-Object {
    if (Test-Path $_) {
        $dlls = Get-ChildItem $_ -Recurse -Filter "photo.dll" -ErrorAction SilentlyContinue
        if ($dlls) { $dlls | Select-Object FullName }
    }
}

Write-Host "=== 4. photolaunch.exe ===" 
@("${env:ProgramFiles}\WPS", "${env:ProgramFiles(x86)}\WPS", "${env:LOCALAPPDATA}\WPS", "C:\WPS", "D:\WPS", "E:\WPS") | ForEach-Object {
    if (Test-Path $_) {
        $exes = Get-ChildItem $_ -Recurse -Filter "photolaunch.exe" -ErrorAction SilentlyContinue
        if ($exes) { $exes | Select-Object FullName }
    }
}
```

**Expected verification results:**
1. All WPS scheduled tasks status is "Disabled"
2. WPS.PIC registry entries count is 0
3. No photo.dll files found
4. No photolaunch.exe files found

## Important Notes

1. **May restore after WPS update**: WPS may re-register these components after updates. If you find file associations hijacked again, you need to re-execute this skill's operations.

2. **WPS other functions unaffected**: This skill only disables WPS's image viewing module. WPS's word processing, spreadsheet, presentation and other core functions are not affected.

3. **Administrator privileges required**: Some operations (especially modifying HKLM registry entries) may require administrator privileges. If you encounter permission errors, please run PowerShell as administrator.

4. **Backup recommendation**: It's recommended to record current file association settings before executing operations, so you can restore when needed.

5. **Multiple WPS versions**: WPS may install multiple versions, need to process all versions of related files.

## Working Principle

WPS uses the following mechanisms to hijack file associations:
1. **Scheduled tasks**: Periodically run background processes to check and modify file associations
2. **Registry entries**: Register WPS.PIC.* format file associations in HKLM and HKCU
3. **photo.dll plugin**: Core component of the image module
4. **photolaunch.exe**: Image viewer executable file

This skill completely blocks WPS's file association hijacking by disabling scheduled tasks, deleting registry entries, removing plugins and executable files.
