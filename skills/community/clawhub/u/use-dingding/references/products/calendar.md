# Calendar Reference

## Event Operations

### List Events

```bash
dws calendar event list [--start <date>] [--end <date>] [--limit <N>]
```

**Parameters:**
- `--start`: Start date (ISO 8601, e.g., "2024-03-29T00:00:00Z")
- `--end`: End date (ISO 8601)
- `--limit`: Max results

**Example:**
```bash
# Today's events
dws calendar event list --start "2024-03-29T00:00:00Z" --end "2024-03-29T23:59:59Z"

# This week
dws calendar event list --start "2024-03-29" --end "2024-04-05" --jq '.result[] | {title: .title, start: .startTime}'
```

### Create Event

```bash
dws calendar event create --title "<title>" --start "<startTime>" --end "<endTime>" [--participants <userIds>] [--location "<location>"]
```

**Example:**
```bash
dws calendar event create \
  --title "Team Meeting" \
  --start "2024-03-29T14:00:00Z" \
  --end "2024-03-29T15:00:00Z" \
  --participants "user1,user2,user3" \
  --location "Conference Room A"
```

### Update Event

```bash
dws calendar event update --event-id <eventId> --title "<new-title>" [--start <new-start>] [--end <new-end>]
```

### Delete Event

```bash
dws calendar event delete --event-id <eventId>
```

### Get Event Detail

```bash
dws calendar event get --event-id <eventId>
```

## Participant Operations

### Add Participants

```bash
dws calendar participant add --event-id <eventId> --user-ids <userId1,userId2>
```

### Remove Participants

```bash
dws calendar participant remove --event-id <eventId> --user-ids <userId1,userId2>
```

### Check Participant Availability

```bash
dws calendar participant busy --user-ids <userId1,userId2> --start "<start>" --end "<end>"
```

**Example:**
```bash
# Find when everyone is free
dws calendar participant busy \
  --user-ids "user1,user2,user3" \
  --start "2024-03-29T09:00:00Z" \
  --end "2024-03-29T18:00:00Z" \
  --jq '.result.busySlots[] | {start: .startTime, end: .endTime}'
```

## Meeting Room Operations

### Search Meeting Rooms

```bash
dws calendar room search --keyword "<room-name>" [--city "<city>"]
```

**Example:**
```bash
dws calendar room search --keyword "Conference Room" --jq '.result[] | {name: .name, roomId: .roomId, capacity: .capacity}'
```

### Book Meeting Room

```bash
dws calendar room book --room-id <roomId> --start "<start>" --end "<end>" --title "<title>"
```

### Get Room Availability

```bash
dws calendar room get --room-id <roomId> --start "<start>" --end "<end>"
```

## Common Patterns

### Schedule Meeting with Room

```bash
# 1. Find free slot
dws calendar participant busy --user-ids "user1,user2" --start "2024-03-29T09:00:00Z" --end "2024-03-29T18:00:00Z"

# 2. Find available room
dws calendar room search --keyword "Conference Room" --jq '.result[0].roomId'

# 3. Create event with room
dws calendar event create --title "Meeting" --start "2024-03-29T14:00:00Z" --end "2024-03-29T15:00:00Z" --participants "user1,user2"
```

### Find Common Free Slots

See bundled script: `scripts/calendar_free_slot_finder.py`

### View Today's Agenda

```bash
dws calendar event list --start "$(date -I)T00:00:00Z" --end "$(date -I)T23:59:59Z" --jq '.result[] | "\(.startTime) - \(.title)"'
```
