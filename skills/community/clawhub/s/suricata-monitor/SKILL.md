---
name: suricata-monitor
description: Read and triage Suricata IDS/IPS alerts from eve.json into a structured threat report — severity-ranked findings, attacker IPs, top triggered signatures, and recommended blocks. Use when you want an automated threat intelligence snapshot from your Suricata deployment, after a scan triggers alerts, or as a daily security briefing module. No external API. Reads your local Suricata log only.
---

# Suricata Monitor

Turns raw Suricata `eve.json` alerts into an actionable threat report.

Reads your local Suricata log, ranks findings by severity, surfaces attacker IPs and top
signatures, and delivers a structured brief you can act on or forward to Telegram.

**Privacy:** Reads `/var/log/suricata/eve.json` only. No data leaves your machine.
Single SKILL.md — inspect every line here.

---

## Prerequisites

Suricata must be running and writing to `eve.json`:

```bash
# Verify log exists and is being written
ls -lh /var/log/suricata/eve.json
tail -5 /var/log/suricata/eve.json | python3 -m json.tool
```

If the log is permission-denied:
```bash
sudo chmod 644 /var/log/suricata/eve.json
```

---

## Workflow

### 1. Read recent alerts

```python
import json
from datetime import datetime, timedelta

LOG = "/var/log/suricata/eve.json"
HOURS = 24  # look back window

cutoff = (datetime.now() - timedelta(hours=HOURS)).timestamp()
alerts = []

with open(LOG) as f:
    for line in f:
        try:
            event = json.loads(line)
            if event.get("event_type") != "alert":
                continue
            ts = datetime.fromisoformat(event["timestamp"][:19]).timestamp()
            if ts < cutoff:
                continue
            alerts.append({
                "time":      event["timestamp"][:19],
                "severity":  event["alert"].get("severity", 99),
                "sig":       event["alert"].get("signature", "unknown"),
                "category":  event["alert"].get("category", ""),
                "src_ip":    event.get("src_ip", "?"),
                "dest_ip":   event.get("dest_ip", "?"),
                "dest_port": event.get("dest_port", "?"),
                "proto":     event.get("proto", "?"),
            })
        except (json.JSONDecodeError, KeyError, ValueError):
            continue
```

### 2. Aggregate and rank

```python
from collections import Counter

# Top attacker IPs
attacker_ips = Counter(a["src_ip"] for a in alerts if a["severity"] <= 2)

# Top signatures
top_sigs = Counter(a["sig"] for a in alerts).most_common(5)

# By severity
critical = [a for a in alerts if a["severity"] == 1]
high     = [a for a in alerts if a["severity"] == 2]
medium   = [a for a in alerts if a["severity"] == 3]
low      = [a for a in alerts if a["severity"] >= 4]
```

### 3. Format the report

```
SURICATA THREAT REPORT — YYYY-MM-DD HH:MM  (last Nh)
Alerts: X total  |  Critical: X  High: X  Medium: X  Low: X

TOP ATTACKER IPs
  1. [ip]  — X hits  (Block: sudo ufw deny from [ip])
  2. ...

TOP SIGNATURES
  1. [signature name]  — X times
  2. ...

CRITICAL ALERTS (severity 1)
  [HH:MM] [src_ip] → [dest_ip]:[port]  [signature]

HIGH ALERTS (severity 2) — sample
  [HH:MM] [src_ip] → [dest_ip]:[port]  [signature]

RECOMMENDED ACTIONS
  [ ] Block top attacker IPs:
      sudo ufw deny from [ip1]
      sudo ufw deny from [ip2]
  [ ] Review Suricata rule for: [top signature]
  [ ] If RED posture: run eva-security-audit skill

STATUS: [GREEN/YELLOW/RED]
  GREEN  = 0 critical, <10 high in 24h
  YELLOW = 1–5 critical OR 10–50 high
  RED    = >5 critical OR >50 high OR C2/exploit signatures detected
```

### 4. Deliver

**To Telegram** (use telegram-notifier skill):
```python
# After building the report string above:
import os, requests
requests.post(
    f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}/sendMessage",
    json={"chat_id": os.environ['TELEGRAM_CHAT_ID'], "text": report},
    timeout=10
)
```

**To memory:**
```bash
echo "[report]" >> memory/$(date +%Y-%m-%d).md
```

---

## Schedule daily monitoring

```bash
openclaw cron add \
  --name "suricata-monitor:daily" \
  --cron "0 7 * * *" \
  --prompt "Run the suricata-monitor skill. Look back 24 hours. Send report to Telegram and append to today's memory file."
```

---

## Signature categories to watch

| Category | Severity | Action |
|----------|----------|--------|
| Exploit kit activity | 1 | Block IP immediately |
| Malware C2 | 1 | Isolate affected host |
| Port scanning | 2 | Monitor, consider block |
| Policy violation | 3 | Review, log |
| Informational | 4+ | Log only |

---

## Quick commands

```bash
# Count today's alerts by severity
cat /var/log/suricata/eve.json | python3 -c "
import sys, json
from collections import Counter
sev = Counter()
for line in sys.stdin:
    try:
        e = json.loads(line)
        if e.get('event_type') == 'alert':
            sev[e['alert'].get('severity','?')] += 1
    except: pass
for k,v in sorted(sev.items()): print(f'Severity {k}: {v}')
"

# Top 10 attacker IPs last 24h
cat /var/log/suricata/eve.json | python3 -c "
import sys, json
from collections import Counter
from datetime import datetime, timedelta
cutoff = (datetime.now()-timedelta(hours=24)).timestamp()
ips = []
for line in sys.stdin:
    try:
        e = json.loads(line)
        if e.get('event_type')=='alert':
            ts = datetime.fromisoformat(e['timestamp'][:19]).timestamp()
            if ts > cutoff: ips.append(e.get('src_ip','?'))
    except: pass
for ip,n in Counter(ips).most_common(10): print(f'{n:5}  {ip}')
"
```
