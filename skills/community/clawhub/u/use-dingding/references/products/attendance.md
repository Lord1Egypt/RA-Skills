# Attendance Reference

## Record Operations

### List Attendance Records

```bash
dws attendance record list --user-id <userId> [--start <date>] [--end <date>]
```

**Parameters:**
- `--user-id`: User ID (required)
- `--start`: Start date (YYYY-MM-DD)
- `--end`: End date (YYYY-MM-DD)

**Example:**
```bash
# Today's records
dws attendance record list --user-id "user123" --start "2024-03-29" --end "2024-03-29"

# This week
dws attendance record list --user-id "user123" --start "2024-03-25" --end "2024-03-31" --jq '.result[] | {date: .workDate, checkIn: .checkInTime, checkOut: .checkOutTime}'
```

### Get My Records

```bash
# First get your userId
dws contact user get-self --jq '.result[0].userId'

# Then get records
dws attendance record list --user-id "<your-userId>" --start "2024-03-29" --end "2024-03-29"
```

See bundled script: `scripts/attendance_my_record.py`

## Shift Operations

### List Shift Schedules

```bash
dws attendance shift list --dept-id <deptId> [--start <date>] [--end <date>]
```

**Example:**
```bash
dws attendance shift list --dept-id "dept123" --start "2024-03-29" --end "2024-04-05"
```

See bundled script: `scripts/attendance_team_shift.py`

### Get Shift Detail

```bash
dws attendance shift get --shift-id <shiftId>
```

## Summary Operations

### Get Attendance Summary

```bash
dws attendance summary get --user-id <userId> --start <date> --end <date>
```

**Example:**
```bash
dws attendance summary get --user-id "user123" --start "2024-03-01" --end "2024-03-31" --jq '.result | {workDays: .workDays, attendanceDays: .attendanceDays, lateDays: .lateDays}'
```

### Get Team Summary

```bash
dws attendance summary team --dept-id <deptId> --start <date> --end <date>
```

## Group Rules

### List Attendance Rules

```bash
dws attendance rules list --dept-id <deptId>
```

### Get Rule Detail

```bash
dws attendance rules get --rule-id <ruleId>
```

## Common Patterns

### Check If Someone Clock In Today

```bash
dws attendance record list --user-id "user123" --start "$(date -I)" --end "$(date -I)" --jq '.result | length > 0'
```

### Get Team Attendance Rate

```bash
# Get department members
dws contact dept members --dept-id "dept123" --jq '.result[] | .userId'

# Get summary for each
for user in $USERS; do
  dws attendance summary get --user-id "$user" --start "2024-03-01" --end "2024-03-31" --jq '.result.attendanceRate'
done
```

### Find Late Arrivals

```bash
dws attendance summary get --user-id "user123" --start "2024-03-01" --end "2024-03-31" --jq '.result.lateDays'
```
