# Water Reminder Skill - 45-minute Hydration and Movement Reminder

## Function Description
Sends hydration and movement reminders every 45 minutes during working hours (8:00-23:00) to help maintain healthy work habits.

## Configuration Requirements

### 1. Heartbeat Interval Configuration
- **Requirement**: OpenClaw heartbeat interval ≤ 45 minutes
- **Current Status**: High-frequency tasks execute every 15 minutes (meets requirement)
- **Config File**: `~/.openclaw/openclaw.json`
- **If modification needed, inform user of the method**:
  ```bash
  # Backup original config
  cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup.$(date +%Y%m%d_%H%M%S)
  
  # Modify heartbeat config (add to agents.defaults or specific agent)
  # "heartbeat": {
  #   "every": "45m"
  # }
  ```

### 2. State Tracking File
- **File Location**: `/home/${user}/.openclaw/workspace/memory/heartbeat-state.json`
- **Required Fields**:
  ```json
  {
    "lastWaterReminder": 1772681220,
    "chatId": "SESSION_CHAT_ID"
  }
  ```

### 3. User Information File
- **File Location**: USER.md
- **Required Info**: Contains user's channel session ID

## Execution Logic

### Time Check
1. Get current time (Example: GMT+8 timezone) converted to 24-hour format
2. Check if within 8:00-23:00 range
3. If outside working hours, skip reminder

### Interval Check
1. Read `lastWaterReminder` timestamp from `memory/heartbeat-state.json`
2. Calculate time difference between current time and last reminder
3. If difference ≥ 45 minutes (2700 seconds), execute reminder

### Reminder Execution
1. Update `lastWaterReminder` with current timestamp
2. Save back to `memory/heartbeat-state.json`
3. Send reminder message via the agent's configured channel to user's session

## Reminder Message Content
```
💧 Time to hydrate!

Remember to:
- Drink a glass of water 🚰
- Get up and move around 🚶‍♂️
- Rest your eyes 👀

Stay healthy for better productivity! 💪
```

## Error Handling
- **File not found**: Automatically create default state file
- **Time format error**: Use current time as baseline
- **Network issues**: Log error but don't interrupt other tasks
- **User ID missing**: Re-read from USER.md

## Use Cases
- Health reminders during extended work sessions
- Preventing prolonged sitting
- Maintaining proper hydration
- Work rhythm regulation

## Important Notes
- Reminders only sent during working hours (8:00-23:00 GMT+8)
- Respects user rest time, no notifications at night
- Updates state after each reminder for accurate timing
- Supports manual reset of reminder timer

## Maintenance Recommendations
- Regularly check state file integrity
- Adjust reminder frequency based on user feedback
- Monitor reminder effectiveness and optimize user experience
