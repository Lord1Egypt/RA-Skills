# Ubuntu Topic Map

Use this as a quick orientation aid when deciding what authoritative source to look up.

## Core areas

- Package management (`apt`, `apt-get`, `dpkg`, `snap`)
- Services and logs (`systemd`, `systemctl`, `journalctl`)
- Networking (Netplan, NetworkManager, DNS/resolver behavior)
- Storage and filesystem admin (mounts, fstab, disks, permissions)
- Users/groups and admin workflows
- Updates, upgrades, release behavior
- Troubleshooting and repair flows

## Typical lookup prompts

When the task is about...

### Package management
Look for:
- `apt(8)`
- `apt-get(8)`
- `dpkg(1)`
- `dpkg-query(1)`
- relevant Ubuntu packaging docs when broader workflow context is needed

### Services / logs
Look for:
- `systemctl(1)`
- `systemd(1)`
- `journalctl(1)`
- service/unit documentation when relevant

### Networking
Look for:
- Netplan documentation
- NetworkManager documentation
- `resolvectl(1)` / resolver docs when relevant
- `ip(8)` / `ss(8)` / related manpages for command behavior

### Storage / admin
Look for:
- `mount(8)`
- `fstab(5)`
- `lsblk(8)`
- `df(1)`
- `du(1)`
- permissions/user/group manpages as needed

### Updates / upgrades / repair
Look for:
- apt manpages
- release-upgrade docs
- package repair and repository/key guidance in official Ubuntu docs

## Trigger boundary reminder

Use this skill for Ubuntu-specific admin/maintenance/troubleshooting work.
Do not trigger it for generic shell tasks unless Ubuntu-specific semantics materially matter.
