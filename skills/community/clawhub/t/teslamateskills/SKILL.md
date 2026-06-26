---
name: teslamate-grafana
description: Query TeslaMate vehicle data via Grafana API. Use when user wants Tesla vehicle status, battery info, drives, charges, statistics, driving score, battery health, or trip data. Requires Grafana running with TeslaMate PostgreSQL datasource.
---

# TeslaMate Grafana API Skill

Query TeslaMate data through Grafana's `/api/ds/query` endpoint using the PostgreSQL datasource.

## Configuration

Grafana address is stored in `~/.openclaw/workspace/memory/teslamate-grafana-config.json`:

```json
{
  "grafana_url": "http://192.168.31.218:3000",
  "datasource_id": 1
}
```

To update address:
```bash
echo '{"grafana_url": "http://YOUR-GRAFANA:3000", "datasource_id": 1}' > ~/.openclaw/workspace/memory/teslamate-grafana-config.json
```

## Usage

### Quick Status
```bash
python3 scripts/query_teslamate.py --status
# Output: Battery: 85% | Range: 420 km | State: online | Today: 45 km
```

### Drives
```bash
python3 scripts/query_teslamate.py --drives 5
# Recent 5 drives with address lookup
```

### Route Planning
```bash
python3 scripts/query_teslamate.py --route "广州珠江新城"
# Output: Distance, duration, energy needed, arrival range
```

## Commands

| Command | Description |
|---------|-------------|
| `--status` | Quick status: battery, range, state, today distance |
| `--drives [N]` | Recent N drives with address lookup |
| `--route <addr>` | Plan route to destination |
| `--report` | Weekly report |
| `--monthly` | Monthly statistics |
| `--trend` | Energy efficiency trend (30 days) |
| `--score` | Driving score based on speed |
| `--milestones` | Achievement milestones |
| `--charging` | Charging statistics (30 days) |
| `--efficiency` | Energy efficiency stats |
| `--cost` | Charging cost (default 1.5 CNY/kWh) |
| `--range` | Range prediction |
| `--health` | Battery health estimation |
| `--places` | Top 10 most visited places |
| `--drain` | Vampire drain analysis |
| `--states` | Vehicle state statistics |
| `--alerts` | Check for anomalies |
| `--temp` | Temperature monitoring |
| `--location` | Current car location |
| `--full` | Complete status dashboard |

## Common Metrics

- **Battery**: `battery_level` (0-100%), `ideal_battery_range_km`
- **Drive**: `distance` (km), `duration_min` (minutes), `speed_max`, `power_max`
- **Charge**: `charge_energy_added` (kWh), `charger_power` (kW), `charger_voltage` (V)
- **States**: `state` = 'online'|'offline'|'driving'|'charging'|'asleep'|'updating'

## API Details

- Endpoint: `{grafana_url}/api/ds/query`
- Method: POST
- Content-Type: application/json
- Datasource: PostgreSQL (TeslaMate)

Request body:
```json
{
  "queries": [{
    "refId": "A",
    "datasourceId": 1,
    "rawSql": "YOUR SQL QUERY",
    "format": "table"
  }]
}
```

Response contains results in `results.A.data.values`.
