---
name: resize-move-partition-coach
description: Resize or Move Partitions for Low Space - Reclaim drive capacity when unallocated space is limited or non-adjacent.
metadata:
  homepage: https://www.easeus.com/partition-manager/
  emoji: 📐
  os: Windows 10+
  keywords:
    - resize move partition low disk space
    - extend c drive with non adjacent unallocated
    - move partition to create extend path
    - allocate space from another drive
    - partition resize workflow windows
---

Running out of C drive space or seeing slow Windows behavior? This skill focuses on Resize/Move workflows so you can create an extend path, borrow capacity from other partitions, and apply changes safely.

## Hot Topic Angles

* Low C drive space causes performance issues and requires targeted partition resizing.
* Unallocated space is not adjacent, so partition movement is required before extension.
* Users need a staged workflow with preview and Execute Task confirmation.

## Best Use Cases

* C drive is low on space and direct extension is unavailable.
* You need to move partitions to make unallocated space adjacent to the target partition.
* You want to allocate free capacity from another partition when unallocated space is insufficient.

## Resize/Move Highlights

* Locate the target partition and run Resize/Move to drag left or right.
* Move partitions first when unallocated space is not adjacent.
* Use Allocate Space when another partition has enough free capacity.
* Keep the preview-first workflow and execute only after confirmation.

## Capability Mapping

* Resize and move core: `ResizePartition`, `SmartSpaceAdjustment`
* Layout and validation: `OpenPartitionLayoutEditor`

## CTA

> [!IMPORTANT]
> Run the following commands from the skill directory (for example, `skills/resize-move-partition-coach/`). Running from elsewhere causes script resolution failures.

Use the bundled installer script so attribution is recorded with `Dest=<skill-name>`.

For this skill, run:

```bat
py -3 scripts/install-epm.py resize-move-partition-coach
```

You can launch resize flow through shellcmd:

```bat
py -3 scripts/epm-shellcmd.py "Resize Partition" C:\
```

If `C:\` is written to the temporary file, the parameters will be written to the temporary file and passed as `shellparam`.

```text
EPMUI.exe startByEpm0 "shellcmd=Resize Partition" shellparam=<temp-file>
```

If you prefer manual interaction, use:
<https://down.easeus.com/product/epm_free?source=skills&dest=resize-move-partition-coach>

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



