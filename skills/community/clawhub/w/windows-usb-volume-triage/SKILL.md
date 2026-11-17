---
name: "windows-usb-volume-triage"
description: "Diagnose missing Windows USB volumes or mount paths safely with read-only disk, partition, volume, and PnP correlation."
---

# Windows USB Volume Triage

Use when Windows detects a USB disk or enclosure but an expected drive letter or directory mount is missing.

## Procedure

1. Keep diagnosis read-only. Do not initialize, format, create partitions, or assign mounts while existing data may be present.
2. Inventory disks with `Get-Disk`. Capture `Number`, `FriendlyName`, `SerialNumber`, `UniqueId`, `Guid`, `Size`, `PartitionStyle`, `NumberOfPartitions`, `LargestFreeExtent`, `OperationalStatus`, and `HealthStatus`.
3. Inventory partitions with `Get-Partition`. Capture `DiskNumber`, `PartitionNumber`, `Type`, `Size`, `Guid`, and `AccessPaths`.
4. Check each expected directory mount with `Get-Volume -FilePath <path>`. Record volume path, label, filesystem, and health. Treat `Test-Path` only as a directory/reparse-point check; it can succeed when no volume resolves there.
5. Correlate the missing mount to a disk using multiple fields: expected capacity, partition/access-path mapping, serial, device path, and location. Do not trust `UniqueId` alone when several enclosure disks expose the same value or Windows logs duplicate-identifier events.
6. Inspect the candidate with `Get-Disk -Number <n>` and `Get-Partition -DiskNumber <n>`. A physical disk marked `Healthy` does not prove its partitions or mounted volume are visible.
7. Map the candidate to enclosure hardware with `Get-PnpDevice` and `Get-PnpDeviceProperty`. Capture the disk instance ID, parent USB instance, location, and bus-reported description.
8. If needed, perform one non-destructive refresh: run `Update-HostStorageCache`, then `Update-Disk -Number <n>`. Re-run the exact disk, partition, and mount checks.
9. If the state is unchanged, report the affected disk and enclosure channel evidence. Recommend reseating or power-cycling only the affected bay when hardware supports it; leave broader shutdown or recovery actions to the user.

## Output discipline

- Start with compact selected fields; broad formatted inventories can be truncated and hide the relevant disk.
- Narrow subsequent queries to the candidate disk and exact mount path.
- In PowerShell, collect `foreach` output before piping to `Format-Table`; piping a statement directly can produce `ParserError: EmptyPipeElement`.

## Verification

Compare before and after refresh:

- `Get-Disk -Number <n>`: `NumberOfPartitions` and `LargestFreeExtent`.
- `Get-Partition -DiskNumber <n>`: expected partition presence and access paths.
- `Get-Volume -FilePath <path>`: resolved volume path, filesystem, and health.

Call recovery successful only when the expected partition and exact mount resolve. Otherwise state that refresh did not restore visibility and preserve the no-initialize/no-format warning.
