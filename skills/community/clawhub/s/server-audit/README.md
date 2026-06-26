# server-audit — Server Audit Skill for AI Agents

Skill для повної діагностики серверів. Підтримує два типи:
- **Proxmox VE** — з перевіркою VM/CT, storage, кластеру
- **Linux Server** — Debian / Ubuntu / RHEL / CentOS

## Що перевіряє

| Категорія | Деталі |
|-----------|--------|
| Апаратура | CPU, RAM (тип, кількість модулів, частота), материнська плата |
| Диски | Моделі, типи (SSD/HDD/NVMe), SMART статус |
| RAID | Software (mdadm), ZFS, Hardware (MegaRAID, HPE SmartArray) |
| Температури | CPU, диски, IPMI датчики |
| Пам'ять (ECC) | EDAC помилки, IPMI SEL, mcelog |
| Файлові системи | Розбивка, завантаженість, LVM |
| Логи | Помилки за 7 днів: I/O, OOM, мережа, auth |
| Мережа | Інтерфейси, швидкість, bonding |
| Proxmox | VM/CT список, storage пули, стан кластеру |
| Безпека | Останні входи, підозрілі події, оновлення |

## Використання

Промпти зберігаються у `references/`:
- `proxmox-audit.md` — повний промпт для Proxmox сервера
- `linux-audit.md` — повний промпт для Linux сервера

## Тригери (коли Софійка використовує цей skill)

Див. `SKILL.md` — там описані ключові слова і алгоритм виконання.
