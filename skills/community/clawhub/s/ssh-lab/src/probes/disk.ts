// Disk probe — parses `df -h` output

import type { Probe, DiskProbeData, DiskInfo } from '../types/index.js';

// Filter to real filesystems, skip tmpfs/devtmpfs/squashfs etc
const DISK_COMMAND = "df -h --output=source,size,used,avail,pcent,target 2>/dev/null || df -h 2>/dev/null";

function parseDfLine(line: string): DiskInfo | null {
  // df output: Filesystem  Size  Used  Avail  Use%  Mounted on
  const parts = line.trim().split(/\s+/);
  if (parts.length < 6) return null;

  const filesystem = parts[0];
  // Skip pseudo filesystems
  if (/^(tmpfs|devtmpfs|squashfs|overlay|shm|udev|none)$/i.test(filesystem)) return null;
  if (filesystem === 'Filesystem') return null; // header

  const usedPctStr = parts[4].replace('%', '');
  const usedPct = parseInt(usedPctStr, 10);
  if (isNaN(usedPct)) return null;

  return {
    filesystem,
    size: parts[1],
    used: parts[2],
    available: parts[3],
    usedPct,
    mountpoint: parts.slice(5).join(' '),
  };
}

export const diskProbe: Probe = {
  name: 'disk',
  command: DISK_COMMAND,

  parse(stdout: string): DiskProbeData {
    const disks: DiskInfo[] = [];

    for (const line of stdout.split('\n')) {
      const disk = parseDfLine(line);
      if (disk) disks.push(disk);
    }

    // Sort by used percentage descending (most critical first)
    disks.sort((a, b) => b.usedPct - a.usedPct);

    return { probe: 'disk', disks };
  },
};
