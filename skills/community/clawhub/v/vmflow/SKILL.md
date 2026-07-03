---
name: vmflow
description: Manage your vending machine fleet — send credits, inspect device health, query sales and inventory, and trigger firmware updates via MQTT RPC and Supabase.
version: 1.0.0
metadata:
  openclaw:
    emoji: 🏧
    homepage: https://github.com/nodestark/mdb-esp32-cashless
    primaryEnv: SUPABASE_PASSWORD
    requires:
      env:
        - SUPABASE_EMAIL
        - SUPABASE_PASSWORD
      bins:
        - openssl
        - curl
      anyBins:
        - mosquitto_pub
    envVars:
      - name: SUPABASE_EMAIL
        required: true
        description: Operator account email on supabase.vmflow.xyz
      - name: SUPABASE_PASSWORD
        required: true
        description: Operator account password on supabase.vmflow.xyz
      - name: SUPABASE_URL
        required: false
        description: "Supabase base URL (default: https://supabase.vmflow.xyz)"
      - name: SUPABASE_ANON_KEY
        required: false
        description: "Supabase anon key — public default is embedded in this skill"
      - name: MQTT_HOST
        required: false
        description: "MQTT broker host (default: mqtt.vmflow.xyz)"
    install:
      - kind: brew
        formula: mosquitto
        bins: [mosquitto_pub, mosquitto_sub]
---

# VMflow — Vending Machine Fleet Management

Manage your vending machine fleet with AI. Send credits, inspect device health,
query sales and inventory, and trigger firmware updates — all from a single agent.

**Two control planes:**
- **Supabase REST** — historical data, inventory, sales, device list
- **MQTT RPC** — real-time signed commands directly to each device

---

## Setup

### 1. Get a Bearer Token

The `SUPABASE_ANON_KEY` below is public and safe to embed — row-level security enforces
per-operator data isolation after login.

```bash
SUPABASE_URL="${SUPABASE_URL:-https://supabase.vmflow.xyz}"
SUPABASE_ANON_KEY="${SUPABASE_ANON_KEY:-eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYW5vbiIsImlzcyI6InN1cGFiYXNlLWRlbW8iLCJpYXQiOjE2NDE3NjkyMDAsImV4cCI6MTc5OTUzNTYwMH0.VGEEIztVo-do9cy_Qw2-2sF8bSONckhX71Nvtwj15X4}"

ACCESS_TOKEN=$(curl -s -X POST "$SUPABASE_URL/auth/v1/token?grant_type=password" \
  -H "apikey: $SUPABASE_ANON_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$SUPABASE_EMAIL\",\"password\":\"$SUPABASE_PASSWORD\"}" \
  | jq -r '.access_token')
```

### 2. Fetch Device Credentials

Each device has a `subdomain` (integer) and `passkey` (18-char hex) stored in Supabase.
The agent retrieves them before issuing any RPC command.

```bash
curl -s "$SUPABASE_URL/rest/v1/embedded?select=subdomain,passkey,status,status_at,machine_id" \
  -H "apikey: $SUPABASE_ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

---

## Operations

### Query Sales

```bash
# Latest 50 sales with machine and product name
curl -s "$SUPABASE_URL/rest/v1/sales?select=created_at,item_price,channel,coil_alias,machines(name),products(name)&order=created_at.desc&limit=50" \
  -H "apikey: $SUPABASE_ANON_KEY" -H "Authorization: Bearer $ACCESS_TOKEN"

# Sales today
TODAY=$(date -u +%Y-%m-%dT00:00:00Z)
curl -s "$SUPABASE_URL/rest/v1/sales?select=machine_id,item_price,channel&created_at=gte.$TODAY" \
  -H "apikey: $SUPABASE_ANON_KEY" -H "Authorization: Bearer $ACCESS_TOKEN"
```

### Check Inventory

```bash
# Coils with 2 or fewer units remaining
curl -s "$SUPABASE_URL/rest/v1/machine_coils?select=machine_id,alias,current_stock,capacity,products(name)&current_stock=lte.2" \
  -H "apikey: $SUPABASE_ANON_KEY" -H "Authorization: Bearer $ACCESS_TOKEN"

# All machines with device status
curl -s "$SUPABASE_URL/rest/v1/machines?select=id,name,location_name,monthly_rent,embedded(status,status_at)" \
  -H "apikey: $SUPABASE_ANON_KEY" -H "Authorization: Bearer $ACCESS_TOKEN"
```

### Send Credit (Cashless Payment)

Signs and publishes the MQTT credit RPC, records a sale. Device must be online.

```bash
curl -s -X POST "$SUPABASE_URL/functions/v1/send-credit" \
  -H "apikey: $SUPABASE_ANON_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"subdomain\": $SUB, \"amount\": 5.00}"
```

### Device Health Snapshot (RPC `info`)

```bash
MQTT_HOST="${MQTT_HOST:-mqtt.vmflow.xyz}"
TS=$(date +%s)
SIG=$(printf '%s' "info:-:$TS" | openssl dgst -sha256 -hmac "$PASSKEY" -hex | awk '{print $NF}')
# publish; listen for reply on domain.vmflow.xyz/$SUB/rpc/info
mosquitto_pub -h "$MQTT_HOST" -t "$SUB.vmflow.xyz/rpc" -m "info:-:$TS:$SIG" -q 1
```

Reply JSON:
```json
{
  "version": "fw-version",
  "uptime_s": 86400,
  "reset_reason": 1,
  "free_heap": 182000,
  "min_free_heap": 145000,
  "machine_state": 3,
  "last_sale_price": 150,
  "last_sale_item": 7,
  "last_vend_success_time": 1751000000,
  "vend_fail_count": 2
}
```

`machine_state`: `0=INACTIVE` `1=DISABLED` `2=ENABLED` `3=IDLE` `4=VEND`

`reset_reason`: `1=POWERON` `2=EXT` `3=SW` `4=PANIC` `5=INT_WDT` `6=TASK_WDT` `7=WDT`

### Other RPC Commands

All RPC envelopes: `<cmd>:<args>:<ts>:<hmac>` where `hmac = HMAC-SHA256(passkey, "<cmd>:<args>:<ts>")`.
Commands with no argument use `-` as `<args>`. Messages expire after 10 seconds — sign at send time.

```bash
_rpc() {
  local CMD=$1 ARGS=${2:--}
  local TS SIG
  TS=$(date +%s)
  SIG=$(printf '%s' "$CMD:$ARGS:$TS" | openssl dgst -sha256 -hmac "$PASSKEY" -hex | awk '{print $NF}')
  mosquitto_pub -h "${MQTT_HOST:-mqtt.vmflow.xyz}" -t "$SUB.vmflow.xyz/rpc" -m "$CMD:$ARGS:$TS:$SIG" -q 1
}

_rpc echo          # liveness probe — reply on domain.vmflow.xyz/$SUB/rpc/echo
_rpc buzzer        # 1s beep (physical locate)
_rpc oos           # send MDB "out of sequence" to recover stuck VMC
_rpc restart       # reboot device — ack on .../rpc/restart then disconnects
_rpc dex           # pull EVA-DTS DEX telemetry — raw bytes on .../rpc/dex
_rpc ota -         # OTA to latest firmware release
_rpc ota v1.2.3    # OTA pinned to specific tag
```

### Foot-Traffic (PAX Counter)

```bash
curl -s "$SUPABASE_URL/rest/v1/metrics?name=eq.paxcounter&select=created_at,value,machine_id&order=created_at.desc&limit=100" \
  -H "apikey: $SUPABASE_ANON_KEY" -H "Authorization: Bearer $ACCESS_TOKEN"
```

Each row is a BLE scan count (nearby devices detected) timestamped at scan completion.

---

## Agent Playbooks

### Fleet health sweep
1. `GET /rest/v1/embedded` → list all devices with `subdomain`, `passkey`, `status`
2. For each device send `info` RPC, collect reply JSON
3. Flag: `machine_state=0` (MDB lost), `vend_fail_count > 0`, `min_free_heap < 50000`, `reset_reason >= 4` (crash/watchdog)

### Restocking priority list
1. `GET /rest/v1/machine_coils?current_stock=lte.2` → critical coils
2. Join `machines` → group by `location_name`
3. Return ordered list by most critical location first

### Revenue report
1. `GET /rest/v1/sales?created_at=gte.{start}` → all sales in period
2. Aggregate by `machine_id`, sum `item_price`, count rows
3. Join `machines.monthly_rent` → compute `revenue - rent` per machine

### Recover unresponsive device
1. Send `echo` RPC, subscribe to `domain.vmflow.xyz/$SUB/rpc/echo`, wait 15s
2. No reply → device offline or MQTT unreachable
3. Try `restart` RPC; if no ack within 15s → escalate to physical inspection

---

## Data Model

| Table | Key columns |
|---|---|
| `machines` | `id`, `name`, `location_name`, `lat`, `lng`, `monthly_rent`, `category` |
| `embedded` | `subdomain`, `passkey`, `status` (online/offline), `status_at`, `machine_id` |
| `sales` | `created_at`, `machine_id`, `product_id`, `item_price`, `channel` (ble/mqtt/cash), `coil_alias` |
| `machine_coils` | `machine_id`, `product_id`, `alias`, `current_stock`, `capacity`, `item_price` |
| `products` | `name`, `barcode`, `price`, `current_stock` |
| `metrics` | `machine_id`, `name` (paxcounter), `value`, `created_at` |

---

## Known Limitations

- `sales.product_id` is NULL for MercadoPago/Stripe webhook payments — product-level analytics only available for cash and BLE sales.
- `vend_fail_count` resets on device reboot — not a reliable all-time counter.
- `embedded.status_at` is the last status change only — no downtime history table.
- `dex` RPC result is raw EVA-DTS binary on the MQTT reply topic — no Supabase table persists DEX data today.

---

## References

- Full agent context + BLE payload spec: [`AGENTS.md`](./AGENTS.md)
- RPC helper script: [`tools/rpc.sh`](./tools/rpc.sh)
- Firmware RPC handler: [mdb-slave-esp32s3/main/mdb-slave-esp32s3.c](https://github.com/nodestark/mdb-esp32-cashless/blob/main/mdb-slave-esp32s3/main/mdb-slave-esp32s3.c)
- Supabase schema: [docker/supabase/migrations/](https://github.com/nodestark/mdb-esp32-cashless/tree/main/docker/supabase/migrations)
- Web dashboard: <https://vmflow.xyz/dashboard>
- GitHub: <https://github.com/nodestark/mdb-esp32-cashless>
