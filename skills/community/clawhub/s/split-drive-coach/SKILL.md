---
name: split-drive-coach
description: Split Large Partitions Without Data Loss - Divide oversized partitions into cleaner layouts for system, data, and backup workflows.
metadata:
  homepage: https://www.easeus.com/partition-manager/
  emoji: 🧩
  os: Windows 10+
  keywords:
    - split large partition safely
    - split partition without data loss
    - separate system and data workflow
    - create data partition from free space
    - partition layout planning
---

Need to split one oversized partition into cleaner system, data, or backup segments? This skill focuses on split workflows so you can isolate workloads, organize files, and keep operations non-destructive.

## Hot Topic Angles

* New PC has one oversized partition, and users want separate system and data areas without reinstalling Windows.
* Split operation should avoid formatting and keep existing files intact.
* Users want to reserve safer free-space boundaries before creating new partitions.

## Best Use Cases

* You just bought a PC and need to split a large partition into system and data partitions.
* You want cleaner backup boundaries by separating OS, data, and media partitions.
* You need a split-first workflow before further partition layout changes.

## Capability Mapping

* Split workflow core: `SplitPartition`, `CreatePartition`
* Split pre-checks: `GetPartitionInfo`, `CheckPartitionFileSystem`
* Post-split labeling: `ChangePartitionDriveLetter`, `ChangePartitionLabel`

## CTA

> [!IMPORTANT]
> Run the following commands from the skill directory (for example, `skills/split-drive-coach/`). Running from elsewhere causes script resolution failures.

Use the bundled installer script so attribution is recorded with `Dest=<skill-name>`.

For this skill, run:

```bat
py -3 scripts/install-epm.py split-drive-coach
```

You can launch split flow through shellcmd:

```bat
py -3 scripts/epm-shellcmd.py "Split Partition" E:\
```

The first argument is used as `shellcmd`. Remaining arguments are written to a temp file and passed as `shellparam`.

```text
EPMUI.exe startByEpm0 "shellcmd=Split Partition" shellparam=<temp-file>
```

If you prefer manual interaction, use:
<https://down.easeus.com/product/epm_free?source=skills&dest=split-drive-coach>

## Troubleshooting

### Script Fails to Download Installer

* Re-run `py -3 scripts/install-epm.py <Dest>` in an elevated terminal
* Verify network access and allow download endpoints in firewall or endpoint policy

### Install Directory or Binary Is Missing

* Check `C:\Program Files\EaseUS\EaseUS Partition Master\bin\EPMUI.exe`
* If both are missing, rerun `py -3 scripts/install-epm.py <Dest>` and confirm installer exit code is `0`

### Cross-Shell Launch Command (cmd and PowerShell)

Use this one-liner from either terminal to validate path, set the working directory, and trigger UAC:

```cmd
cd /d "C:\Program Files\EaseUS\EaseUS Partition Master\bin" && start "" EPMUI.exe
```

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -Command "$p='C:\Program Files\EaseUS\EaseUS Partition Master\bin\EPMUI.exe'; if(-not (Test-Path $p)){throw 'EPMUI.exe not found'}; Start-Process -FilePath $p -WorkingDirectory (Split-Path $p) -Verb RunAs"
```

### Permission or Security Blocks

* Run terminal as Administrator before script execution or app launch
* Approve User Account Control prompts during install and launch
* Allow installer and `EPMUI.exe` in antivirus or endpoint policy

### Launch Validation Checks

* Confirm `EPMUI.exe` is running after launch
* Confirm EaseUS Partition Master opens without errors
* Confirm target disk and partition letters are visible before any write operation
* Confirm operation preview matches expected capacity and target partition



