# Skill: Server Audit (Proxmox + Linux)

## Правила
Аудит = тільки читати. НЕ виконувати: apt update/upgrade, systemctl restart, sudo, lshw.
Формат: `exec: ssh [-p PORT] root@<HOST> '<команда>'`

---

## Крок 0 — Визначення типу сервера

```
exec: ssh root@HOST 'pveversion 2>/dev/null && echo TYPE=PROXMOX || echo TYPE=LINUX'
```

Якщо TYPE=PROXMOX → виконуй блоки P1, T, S, E, R, P6, P7, N, P9
Якщо TYPE=LINUX   → виконуй блоки L1, T, S, E, R, L6, L7, N, L9

---

## P1 — Апаратна конфігурація (Proxmox)

```
exec: ssh root@HOST 'lscpu | grep -E "Model name|Socket|Core|Thread|CPU MHz|CPU max"'
exec: ssh root@HOST 'dmidecode -t baseboard | grep -E "Manufacturer|Product|Version"'
exec: ssh root@HOST 'dmidecode -t memory | grep -E "Size|Type:|Speed|Manufacturer|Part Number|Locator" | grep -v "No Module"'
exec: ssh root@HOST 'free -h'
exec: ssh root@HOST 'lsblk -o NAME,SIZE,TYPE,ROTA,MODEL,TRAN,SERIAL'
exec: ssh root@HOST 'fdisk -l 2>/dev/null | grep -E "^Disk /dev/(sd|nvme|vd)"'
exec: ssh root@HOST 'lspci | grep -vE "USB|Audio|SMBus|Serial bus"'
```

## L1 — ОС та апаратна конфігурація (Linux)

```
exec: ssh root@HOST 'uname -a && cat /etc/os-release | grep -E "NAME|VERSION" && uptime'
exec: ssh root@HOST 'lscpu | grep -E "Model name|Socket|Core|Thread|CPU MHz|CPU max"'
exec: ssh root@HOST 'dmidecode -t baseboard | grep -E "Manufacturer|Product|Version"'
exec: ssh root@HOST 'dmidecode -t memory | grep -E "Size|Type:|Speed|Manufacturer|Part Number|Locator" | grep -v "No Module"'
exec: ssh root@HOST 'free -h'
exec: ssh root@HOST 'lsblk -o NAME,SIZE,TYPE,ROTA,MODEL,TRAN,SERIAL'
exec: ssh root@HOST 'fdisk -l 2>/dev/null | grep -E "^Disk /dev/(sd|nvme|vd)"'
exec: ssh root@HOST 'lspci | grep -vE "USB|Audio|SMBus|Serial bus"'
```

---

## T — Температури (обидва типи)

```
exec: ssh root@HOST 'sensors 2>/dev/null || echo "lm-sensors не встановлено"'
exec: ssh root@HOST 'ipmitool sdr type Temperature 2>/dev/null || echo "IPMI недоступний"'
exec: ssh root@HOST 'ipmitool sdr type Fan 2>/dev/null || echo "IPMI недоступний"'
exec: ssh root@HOST 'ipmitool sel elist last 20 2>/dev/null || echo "IPMI SEL недоступний"'
```

## S — SMART всіх дисків (обидва типи)

Спочатку список:
```
exec: ssh root@HOST 'lsblk -dno NAME | grep -E "^(sd|nvme|hd)"'
```

Для КОЖНОГО диска зі списку:
```
exec: ssh root@HOST 'smartctl -i -H /dev/DISK 2>/dev/null | grep -E "Device Model|Model Number|Serial Number|User Capacity|Rotation Rate|SMART overall|SMART Health Status"'
exec: ssh root@HOST 'smartctl -A /dev/DISK 2>/dev/null | grep -E "Reallocated_Sector|Pending_Sector|Uncorrectable|Reported_Uncorrect|Raw_Read_Error|Power_On_Hours|Power_Cycle|Temperature_Celsius|Airflow_Temp|Wear_Leveling|Media_Wearout|UDMA_CRC_Error|Command_Timeout|Spin_Retry|Seek_Error|Percentage Used|Data Units Written|Unsafe Shutdowns|Media and Data Integrity"'
exec: ssh root@HOST 'smartctl -l error /dev/DISK 2>/dev/null | grep -E "Errors Logged|No Errors Logged|Error [0-9]+|at LBA" | head -8'
```

## E — Помилки пам'яті ECC (обидва типи)

```
exec: ssh root@HOST 'grep -r "" /sys/devices/system/edac/mc/ 2>/dev/null | grep -v "^Binary" | head -40 || echo "EDAC не підтримується"'
exec: ssh root@HOST 'dmidecode -t memory | grep -i "Error Correction"'
exec: ssh root@HOST 'dmesg | grep -iE "mce|ecc|memory error|corrected|uncorrected" | tail -20'
```

## R — RAID масиви (обидва типи)

```
exec: ssh root@HOST 'cat /proc/mdstat'
exec: ssh root@HOST 'mdadm --detail /dev/md* 2>/dev/null || echo "mdadm RAID не знайдено"'
exec: ssh root@HOST 'zpool list 2>/dev/null && zpool status 2>/dev/null || echo "ZFS не встановлено"'
exec: ssh root@HOST 'storcli /c0 show 2>/dev/null || megacli -AdpAllInfo -aALL 2>/dev/null | grep -E "Product|Memory|BBU|Firmware" || echo "Hardware RAID не знайдено"'
exec: ssh root@HOST 'ssacli ctrl all show status 2>/dev/null || echo "HPE SmartArray не знайдено"'
```

---

## P6 — Диски та файлові системи (Proxmox)

```
exec: ssh root@HOST 'lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINT,LABEL'
exec: ssh root@HOST 'df -h --output=source,size,used,avail,pcent,target | grep -v tmpfs | sort -k5 -rh'
exec: ssh root@HOST 'pvesm status 2>/dev/null || echo "pvesm недоступний"'
exec: ssh root@HOST 'vgs 2>/dev/null; lvs 2>/dev/null'
```

## P7 — Стан Proxmox та VM/CT

```
exec: ssh root@HOST 'pveversion'
exec: ssh root@HOST 'pvecm status 2>/dev/null || echo "Одна нода, кластер відсутній"'
exec: ssh root@HOST 'qm list 2>/dev/null'
exec: ssh root@HOST 'pct list 2>/dev/null'
```

## L6 — Диски та файлові системи (Linux)

```
exec: ssh root@HOST 'lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINT,LABEL'
exec: ssh root@HOST 'df -h --output=source,size,used,avail,pcent,target | grep -v tmpfs | sort -k5 -rh'
exec: ssh root@HOST 'pvs 2>/dev/null; vgs 2>/dev/null; lvs 2>/dev/null'
```

## L7 — Навантаження та сервіси (Linux)

```
exec: ssh root@HOST 'top -bn1 | head -15'
exec: ssh root@HOST 'ps aux --sort=-%cpu | head -10'
exec: ssh root@HOST 'ps aux --sort=-%mem | head -10'
exec: ssh root@HOST 'swapon --show'
exec: ssh root@HOST 'systemctl list-units --type=service --state=failed --no-pager'
exec: ssh root@HOST 'systemctl list-units --type=service --state=running --no-pager'
```

---

## N — Мережа та помилки передачі (обидва типи)

```
exec: ssh root@HOST 'ip -br link && ip -br addr'
exec: ssh root@HOST 'for iface in $(ip -br link | awk "{print \$1}" | grep -v lo); do echo -n "$iface: "; ethtool $iface 2>/dev/null | grep -E "Speed|Duplex|Link detected"; done'
exec: ssh root@HOST 'for iface in $(ip -br link | awk "{print \$1}" | grep -v lo); do rx_drop=$(cat /sys/class/net/$iface/statistics/rx_dropped 2>/dev/null||echo 0); tx_drop=$(cat /sys/class/net/$iface/statistics/tx_dropped 2>/dev/null||echo 0); rx_err=$(cat /sys/class/net/$iface/statistics/rx_errors 2>/dev/null||echo 0); tx_err=$(cat /sys/class/net/$iface/statistics/tx_errors 2>/dev/null||echo 0); echo "$iface: rx_drop=$rx_drop tx_drop=$tx_drop rx_err=$rx_err tx_err=$tx_err"; done'
exec: ssh root@HOST 'for iface in $(ip -br link | awk "{print \$1}" | grep -vE "^lo|^veth|^tap|^fwbr|^fwpr"); do stats=$(ethtool -S $iface 2>/dev/null | grep -iE "drop|error|miss|discard|bad|crc" | grep -v " 0$"); if [ -n "$stats" ]; then echo "--- $iface ---"; echo "$stats"; fi; done'
exec: ssh root@HOST 'ip route && ss -tlnp'
exec: ssh root@HOST 'cat /proc/net/bonding/bond* 2>/dev/null | grep -E "Bonding Mode|MII Status|Active Slave" || echo "Bonding не знайдено"'
```

---

## P9 — Аналіз логів (Proxmox)

```
exec: ssh root@HOST 'journalctl -p err..emerg --since "7 days ago" --no-pager | tail -40'
exec: ssh root@HOST 'dmesg --level=err,crit,alert,emerg | tail -30'
exec: ssh root@HOST 'journalctl -u pvedaemon --since "7 days ago" --no-pager | grep -iE "error|fail|warn" | tail -20'
exec: ssh root@HOST 'journalctl --since "7 days ago" | grep -iE "ata.*error|scsi.*error|I\/O error|smartd" | tail -15'
exec: ssh root@HOST 'journalctl --since "7 days ago" | grep -iE "link.*down|carrier.*lost|bond.*fail" | tail -10'
```

## L9 — Безпека та логи (Linux)

```
exec: ssh root@HOST 'last | head -15'
exec: ssh root@HOST 'lastb 2>/dev/null | head -10'
exec: ssh root@HOST 'journalctl -p err..emerg --since "7 days ago" --no-pager | tail -40'
exec: ssh root@HOST 'dmesg --level=err,crit,alert,emerg | tail -30'
exec: ssh root@HOST 'journalctl --since "7 days ago" | grep -iE "ata.*error|scsi.*error|I\/O error|smartd" | tail -15'
exec: ssh root@HOST 'journalctl --since "7 days ago" | grep -iE "link.*down|carrier.*lost|bond.*fail" | tail -10'
exec: ssh root@HOST 'journalctl -u ssh --since "7 days ago" --no-pager | grep -iE "fail|invalid|refused" | tail -15'
exec: ssh root@HOST 'journalctl --since "7 days ago" | grep -i "oom\|out of memory\|killed process" | tail -10'
exec: ssh root@HOST 'apt list --upgradable 2>/dev/null | grep -i security | head -15 || yum check-update --security 2>/dev/null | head -15'
```

---

## Підсумок

1. **Конфігурація** — ОС/Proxmox версія, CPU, RAM (модулі, тип, частота), плата, диски
2. **SMART** — статус і ключові атрибути кожного диску
3. **RAID/Storage** — тип, режим, стан
4. **Температури** — CPU і диски, перегрів?
5. **ECC** — помилки пам'яті є чи ні
6. **Ресурси** — CPU/RAM навантаження (Linux) / VM/CT стан (Proxmox)
7. **Мережа** — dropped packets та помилки
8. **Сервіси** — що впало або з помилками
9. **Логи** — найважливіші знахідки за 7 днів
10. **Вердикт** — 🟢 все добре / 🟡 є попередження / 🔴 критичні проблеми
