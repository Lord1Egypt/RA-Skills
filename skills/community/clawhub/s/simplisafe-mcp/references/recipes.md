# SimpliSafe curl + jq recipes

All examples assume:

```bash
source ~/git/simplisafe-mcp/skills/simplisafe-api/references/ss-helpers.sh
SID=$(ss_sid)
UID_=$(ss_api GET /api/authCheck | jq -r .userId)
```

Every recipe below was run against a live account.

## System

### Full system state

```bash
ss_api GET "/users/$UID_/subscriptions?activeOnly=true" \
  | jq '.subscriptions[] | {
      sid,
      name: .location.locationName,
      state: .location.system.alarmState,
      alarming: .location.system.isAlarming,
      offline: .location.system.isOffline,
      powerOutage: .location.system.powerOutage,
      conn: .location.system.connType,
      version: .location.system.version
    }'
```

### One-line "is the house armed?"

```bash
ss_api GET "/users/$UID_/subscriptions?activeOnly=true" \
  | jq -r '.subscriptions[0].location.system | "\(.alarmState)\(if .isAlarming then "  ** ALARMING **" else "" end)"'
```

### Base-station messages (firmware notices, faults)

```bash
ss_api GET "/users/$UID_/subscriptions?activeOnly=true" \
  | jq -r '.subscriptions[0].location.system.messages[] | "\(.timestamp|todate)  \(.text)"'
```

## Sensors

### All devices, compact

```bash
ss_api GET "/ss3/subscriptions/$SID/sensors?forceUpdate=false" \
  | jq -r '.sensors[] | "\(.type)\t\(.name)\tlowBat=\(.flags.lowBattery)\toffline=\(.flags.offline)"' \
  | column -t
```

### Only devices needing attention

```bash
ss_api GET "/ss3/subscriptions/$SID/sensors?forceUpdate=false" \
  | jq '[.sensors[]
         | select(.flags.offline or .flags.lowBattery or (.status.triggered // false))
         | {name, type, offline: .flags.offline, lowBattery: .flags.lowBattery, triggered: .status.triggered}]'
```

### Currently-open entry sensors (type 5)

```bash
ss_api GET "/ss3/subscriptions/$SID/sensors?forceUpdate=true" \
  | jq -r '.sensors[] | select(.type==5 and .status.triggered==true) | .name'
```

`forceUpdate=true` is warranted here — an open/closed reading is only meaningful
if it is fresh.

### Device type ids

| id | device | | id | device |
| --- | --- | --- | --- | --- |
| 0 | remote | | 13 | siren |
| 1 | keypad | | 14 | smoke + CO |
| 2 | keychain | | 15 | doorbell |
| 3 | panic button | | 16 | **lock** |
| 4 | motion | | 17 | outdoor camera |
| 5 | **entry** | | 20 | motion v2 |
| 6 | glass break | | 22 | outdoor bell box |
| 7 | carbon monoxide | | 253 | lock keypad |
| 8 | smoke | | | |
| 9 | leak | | 21, 23, 24 | seen live, **not in any public enum** |
| 10 | temperature | | | |
| 12 | camera | | | |

Type 24 carries `smokeTriggered` / `coTriggered` / `tamper` / `endOfLife`.

## Locks

### Lock roster with decoded state

`lockState` **1 = locked, 2 = unlocked**; `lockJamState` overrides both.

```bash
ss_api GET "/ss3/subscriptions/$SID/sensors?forceUpdate=false" \
  | jq -r '.sensors[] | select(.type==16) |
      "\(.name)\t\(if .status.lockJamState==1 then "JAMMED"
                   elif .status.lockState==1 then "locked"
                   else "unlocked" end)\tlowBat=\(.status.lockLowBattery)\tpinPadOffline=\(.status.pinPadOffline)"' \
  | column -t
```

### Serials, for the write commands

```bash
ss_api GET "/ss3/subscriptions/$SID/sensors?forceUpdate=false" \
  | jq -r '.sensors[] | select(.type==16) | "\(.name)\t\(.serial)"'
```

## Events

### Recent activity, human-readable

```bash
ss_api GET "/subscriptions/$SID/events?numEvents=20" \
  | jq -r '.events[] | "\(.eventTimestamp|todate)  [\(.eventType)]  \(.info)  \(.sensorName // "")"'
```

Note: **no `ss3/` prefix** on this route, and `eventTimestamp` is in seconds.

> **`numEvents` maxes out at 50.** Verified by bisection against the live API:
> 50 succeeds, 51 and above return `400 InvalidParameter`. To reach further back,
> page with `fromTimestamp` rather than asking for more at once.

### Only alarms

```bash
ss_api GET "/subscriptions/$SID/events?numEvents=50" \
  | jq -r '.events[] | select(.eventType=="alarm") | "\(.eventTimestamp|todate)  \(.info)"'
```

### Since a point in time

```bash
SINCE=$(date -v-24H +%s)     # macOS; GNU: date -d '24 hours ago' +%s
ss_api GET "/subscriptions/$SID/events?fromTimestamp=$SINCE&numEvents=50" \
  | jq -r '.events[] | "\(.eventTimestamp|todate)  \(.info)"'
```

### Who disarmed it, and when

```bash
ss_api GET "/subscriptions/$SID/events?numEvents=50" \
  | jq -r '.events[] | select(.info | test("Disarm"; "i")) | "\(.eventTimestamp|todate)  \(.info)  by \(.pinName // "unknown")"'
```

## Settings and health

### Delays and volumes (PIN block excluded)

```bash
ss_api GET "/ss3/subscriptions/$SID/settings/normal?forceUpdate=false" \
  | jq '.settings.normal | {entryDelayHome, entryDelayAway, exitDelayHome, exitDelayAway,
                            alarmVolume, alarmDuration, doorChime, voicePrompts}'
```

### Base-station health

```bash
ss_api GET "/ss3/subscriptions/$SID/settings/normal?forceUpdate=false" \
  | jq '.basestationStatus | {wifiStatus, wifiRssi, wallPower, backupBattery,
                              gsmStatus, gsmRssi, rfJamming, cellCarrier}'
```

### PINs — cleartext, ask first

```bash
ss_api GET "/ss3/subscriptions/$SID/settings/normal?forceUpdate=false" | jq '.settings.pins'
```

Returns the master and duress codes and every named user PIN in the clear. Only
run it if the user actually wants the codes; `.settings.normal` above is the
safe projection for everything else.

## Writes

Confirm with the user first — these move real hardware.

```bash
# Arm / disarm (no request body)
ss_api POST "/ss3/subscriptions/$SID/state/away"
ss_api POST "/ss3/subscriptions/$SID/state/home"
ss_api POST "/ss3/subscriptions/$SID/state/off"

# Locks (serial from the roster above)
ss_api POST "/doorlock/$SID/<serial>/state" '{"state":"lock"}'
ss_api POST "/doorlock/$SID/<serial>/state" '{"state":"unlock"}'
```

### Verify, don't assume

```bash
arm_and_verify() {
  local want="$1"
  ss_api POST "/ss3/subscriptions/$SID/state/$want" >/dev/null || return 1
  sleep 3
  local got
  got=$(ss_api GET "/users/$UID_/subscriptions?activeOnly=true" \
        | jq -r '.subscriptions[0].location.system.alarmState')
  case "$got" in
    "$(echo "$want" | tr '[:lower:]' '[:upper:]')")       echo "confirmed: $got" ;;
    "$(echo "$want" | tr '[:lower:]' '[:upper:]')_COUNT") echo "in progress (exit delay): $got" ;;
    *) echo "UNCONFIRMED: wanted $want, system reports $got" >&2; return 1 ;;
  esac
}
```

The `_COUNT` case is the exit delay counting down — a success, not a failure.
Comparing whole objects instead of this one field would report success
unconditionally, because the timestamps advance on their own.
