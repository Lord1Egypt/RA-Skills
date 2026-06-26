# Linux Server Audit — повний промпт

Проведи повну діагностику Linux сервера (Debian/Ubuntu/RHEL/CentOS). Виконуй команди по черзі, показуй вивід, коментуй результат.

## 1. Апаратна конфігурація

```bash
uname -a && cat /etc/os-release | grep -E 'NAME|VERSION' && uptime
lscpu | grep -E 'Model name|Socket|Core|Thread|CPU MHz|CPU max'
dmidecode -t baseboard | grep -E 'Manufacturer|Product|Version'
dmidecode -t memory | grep -E 'Size|Type:|Speed|Manufacturer|Part Number|Locator' | grep -v 'No Module'
free -h
lsblk -o NAME,SIZE,TYPE,ROTA,MODEL,TRAN,SERIAL
fdisk -l 2>/dev/null | grep -E '^Disk /dev/(sd|nvme|vd)'
lspci | grep -vE 'USB|Audio|SMBus|Serial bus'
```

## 2. Температури та стан обладнання

```bash
sensors 2>/dev/null
ipmitool sdr type Temperature 2>/dev/null || echo "IPMI недоступний"
ipmitool sdr type Fan 2>/dev/null
ipmitool sel elist last 20 2>/dev/null
```

## 2б. Повна перевірка SMART всіх дисків

```bash
for disk in $(lsblk -dno NAME | grep -E '^(sd|nvme|hd)'); do
  echo ""
  echo "════════════════════════════════════"
  echo " SMART: /dev/$disk"
  echo "════════════════════════════════════"

  # Модель, серійний номер, ємність, вердикт
  smartctl -i -H /dev/$disk 2>/dev/null | grep -E \
    'Device Model|Model Number|Serial Number|User Capacity|Rotation Rate|SMART overall|SMART Health Status'

  # Ключові SMART атрибути (HDD/SSD)
  echo "--- Атрибути ---"
  smartctl -A /dev/$disk 2>/dev/null | grep -E \
    'Reallocated_Sector|Pending_Sector|Uncorrectable|Reported_Uncorrect|Raw_Read_Error|\
Power_On_Hours|Power_Cycle|Temperature_Celsius|Airflow_Temp|\
Wear_Leveling|Media_Wearout|Percent_Lifetime|SSD_Life|\
UDMA_CRC_Error|Command_Timeout|Spin_Retry|Seek_Error'

  # NVMe специфічні атрибути
  smartctl -A /dev/$disk 2>/dev/null | grep -E \
    'Percentage Used|Data Units Written|Data Units Read|Power Cycles|\
Unsafe Shutdowns|Media and Data Integrity|Temperature Sensor'

  # Лог помилок
  echo "--- Помилки ---"
  smartctl -l error /dev/$disk 2>/dev/null | \
    grep -E 'Errors Logged|No Errors Logged|Error [0-9]+|at LBA' | head -8
done
```

## 3. Помилки пам'яті (ECC)

```bash
grep -r '' /sys/devices/system/edac/mc/ 2>/dev/null | grep -v '^Binary' | head -40
dmidecode -t memory | grep -i 'Error Correction'
ipmitool sel elist 2>/dev/null | grep -iE 'memory|ecc|correctable|uncorrectable' | tail -20
dmesg | grep -iE 'mce|ecc|memory error|corrected|uncorrected' | tail -20
```

## 4. RAID масиви

```bash
cat /proc/mdstat
mdadm --detail /dev/md* 2>/dev/null || echo "mdadm RAID не знайдено"
zpool list 2>/dev/null && zpool status 2>/dev/null && zfs list 2>/dev/null || echo "ZFS не встановлено"
storcli /c0 show 2>/dev/null || megacli -AdpAllInfo -aALL 2>/dev/null | grep -E 'Product|Memory|BBU|Firmware' || echo "MegaRAID не знайдено"
ssacli ctrl all show status 2>/dev/null || echo "HPE SmartArray не знайдено"
```

## 5. Диски та файлові системи

```bash
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINT,LABEL
df -h --output=source,size,used,avail,pcent,target | grep -v tmpfs | sort -k5 -rh
pvs 2>/dev/null && vgs 2>/dev/null && lvs 2>/dev/null
for disk in $(lsblk -dno NAME | grep -E '^(sd|nvme)'); do
  echo "=== /dev/$disk ==="
  parted /dev/$disk print 2>/dev/null
done
```

## 6. Навантаження та ресурси

```bash
top -bn1 | head -15
ps aux --sort=-%cpu | head -15
ps aux --sort=-%mem | head -10
swapon --show
lsof 2>/dev/null | wc -l
```

## 7. Сервіси

```bash
systemctl list-units --type=service --state=running --no-pager
systemctl list-units --type=service --state=failed --no-pager
systemctl list-unit-files --type=service --state=enabled --no-pager
```

## 8. Аналіз логів

```bash
journalctl -p err..emerg --since "7 days ago" --no-pager | tail -60
dmesg --level=err,crit,alert,emerg | tail -40
journalctl --since "7 days ago" | grep -iE 'ata.*error|scsi.*error|I\/O error|smartd' | tail -20
journalctl --since "7 days ago" | grep -iE 'link.*down|carrier.*lost|bond.*fail' | tail -15
journalctl -u ssh --since "7 days ago" --no-pager | grep -iE 'fail|invalid|refused' | tail -20
journalctl --since "7 days ago" | grep -i 'oom\|out of memory\|killed process' | tail -15
```

## 9. Мережа та помилки передачі

```bash
# Інтерфейси, адреси, стан
ip -br link && ip -br addr

# Швидкість і дуплекс
for iface in $(ip -br link | awk '{print $1}' | grep -v lo); do
  echo -n "$iface: "; ethtool $iface 2>/dev/null | grep -E 'Speed|Duplex|Link detected'
done

# Dropped packets та помилки по кожному інтерфейсу
echo ""
echo "=== Errors / Drops / Missed ==="
for iface in $(ip -br link | awk '{print $1}' | grep -v lo); do
  rx_drop=$(cat /sys/class/net/$iface/statistics/rx_dropped 2>/dev/null || echo 0)
  tx_drop=$(cat /sys/class/net/$iface/statistics/tx_dropped 2>/dev/null || echo 0)
  rx_err=$(cat /sys/class/net/$iface/statistics/rx_errors 2>/dev/null || echo 0)
  tx_err=$(cat /sys/class/net/$iface/statistics/tx_errors 2>/dev/null || echo 0)
  rx_miss=$(cat /sys/class/net/$iface/statistics/rx_missed_errors 2>/dev/null || echo 0)
  rx_over=$(cat /sys/class/net/$iface/statistics/rx_over_errors 2>/dev/null || echo 0)
  echo "$iface: rx_drop=$rx_drop tx_drop=$tx_drop rx_err=$rx_err tx_err=$tx_err rx_missed=$rx_miss rx_overrun=$rx_over"
done

# Детальна статистика через ip (collisions, errors)
ip -s link | grep -A 4 -E '^[0-9]+: (eth|ens|eno|enp|bond|br)' | grep -v '^--$'

# Помилки через ethtool (апаратні лічильники NIC)
for iface in $(ip -br link | awk '{print $1}' | grep -vE '^lo|^veth|^tap'); do
  stats=$(ethtool -S $iface 2>/dev/null | grep -iE 'drop|error|miss|discard|fail|bad|crc|abort' | grep -v ' 0$')
  if [ -n "$stats" ]; then
    echo "--- ethtool $iface ---"
    echo "$stats"
  fi
done

# Bonding (якщо є)
cat /proc/net/bonding/bond* 2>/dev/null | grep -E 'Bonding Mode|MII Status|Active Slave' || echo "Bonding не знайдено"

# Маршрутизація та відкриті порти
ip route
ss -tlnp
```

## 10. Безпека та оновлення

```bash
last | head -20
lastb 2>/dev/null | head -10
apt list --upgradable 2>/dev/null | grep -i security | head -20 || yum check-update --security 2>/dev/null | head -20
```

## Підсумок

1. **Конфігурація** — ОС, CPU, RAM (модулі, тип, частота), материнська плата, диски
2. **SMART** — статус кожного диску, помилки
3. **RAID** — тип, режим, стан, диски
4. **Температури** — CPU і диски, перегрів?
5. **ECC** — помилки пам'яті є чи ні
6. **Ресурси** — CPU/RAM/диск навантаження
7. **Мережа** — dropped packets, помилки на інтерфейсах (ненульові значення — привід для уваги)
8. **Сервіси** — що впало або з помилками
9. **Логи** — I/O помилки, OOM, мережа, підозрілі входи
10. **Безпека** — підозрілі входи, незакриті вразливості безпеки
11. **Вердикт** — 🟢 все добре / 🟡 є попередження / 🔴 критичні проблеми

---

## Після аудиту: збереження документації

**Перед збереженням запитай у Сергія назву проєкту** (наприклад: Halfnet, Infrastructure тощо).

Документація зберігається в Obsidian vault:
```
/DATA/local_database/<project>/Servers/<hostname>/server-info.md
```

```bash
# Визначаємо hostname та IP сервера (виконати на цільовому сервері)
HOSTNAME=$(hostname)
SERVER_IP=$(hostname -I | awk '{print $1}')
echo "hostname=$HOSTNAME ip=$SERVER_IP"
```

Потім на сервері Софійки створи файл:
```bash
PROJECT="<назва проєкту від Сергія>"
DOC_DIR="/DATA/local_database/${PROJECT}/Servers/${HOSTNAME}"
mkdir -p "$DOC_DIR"
```

Збережи `$DOC_DIR/server-info.md` з наступним вмістом:

```markdown
# Сервер: <hostname> (<IP>)

> Аудит проведено: <дата>
> ОС: <дистрибутив, версія ядра>

## Апаратна конфігурація

**CPU:** <модель, кількість ядер>
**RAM:** <обсяг, тип, кількість модулів, частота>
**Материнська плата:** <виробник, модель>

## Диски

| Пристрій | Модель | Розмір | Тип | SMART | Напрацювання |
|----------|--------|--------|-----|-------|--------------|
| /dev/sdX | ...    | ...    | HDD/SSD | PASSED/FAILED | X годин |

## RAID / Storage

<опис масивів: тип, диски, стан>

## Мережа

| Інтерфейс | IP | Швидкість | Errors | Drops |
|-----------|-----|-----------|--------|-------|
| ethX | ... | 1Gb | 0 | 0 |

## Ключові сервіси

<список важливих запущених сервісів>

## Проблеми та попередження

<знайдені під час аудиту проблеми — SMART попередження, помилки в логах, dropped packets тощо>

## Вердикт

🟢 / 🟡 / 🔴 — <пояснення>
```
