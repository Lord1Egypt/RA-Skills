# macOS System Sounds Reference

## Sound Duration Rankings (Measured 2026-02-12)

Only sounds >= 1.4 seconds are acceptable. Short sounds get ignored/missed.

### APPROVED Sounds (Long - >= 1.4s)

| Sound     | Duration | Character         | Recommended Use           |
| --------- | -------- | ----------------- | ------------------------- |
| Funk      | 2.16s    | Attention-getter  | Urgent / imminent alerts  |
| Glass     | 1.65s    | Crisp, clear ding | Event start time          |
| Pop       | 1.63s    | Distinct pop      | Morning-of reminder       |
| Sosumi    | 1.54s    | Classic Mac chime | Day-before reminder       |
| Ping      | 1.50s    | Clean ping        | Alternative general alert |
| Submarine | 1.49s    | Sonar ping        | Alternative general alert |
| Blow      | 1.40s    | Soft whoosh       | Gentle early reminder     |

### REJECTED Sounds (Too Short - < 1.4s)

| Sound  | Duration | Reason        |
| ------ | -------- | ------------- |
| Hero   | 1.06s    | Too short     |
| Basso  | 0.77s    | Too short     |
| Bottle | 0.77s    | Too short     |
| Purr   | 0.76s    | Too short     |
| Frog   | 0.72s    | Too short     |
| Morse  | 0.70s    | Too short     |
| Tink   | 0.56s    | Far too short |

## Default Sound Assignment by Reminder Tier

| Tier              | Trigger       | Sound  | Duration | Rationale                       |
| ----------------- | ------------- | ------ | -------- | ------------------------------- |
| 1 day before      | -1440 min     | Blow   | 1.40s    | Gentle advance notice           |
| Morning-of (9 AM) | Absolute time | Sosumi | 1.54s    | Distinct "remember today" chime |
| 3 hours before    | -180 min      | Pop    | 1.63s    | Getting closer, more noticeable |
| 1 hour before     | -60 min       | Glass  | 1.65s    | Clear "prepare now" signal      |
| 30 min before     | -30 min       | Ping   | 1.50s    | Time to leave                   |
| At event time     | 0 min         | Funk   | 2.16s    | Loudest/longest - it's NOW      |

## Hard-Learned Truths (2026-02-12)

1. **Use `sound alarm`, NOT `display alarm`** for audible alerts
   - `make new sound alarm at end of sound alarms with properties {trigger interval:-5, sound name:"Sosumi"}`
   - `display alarm` only shows a visual banner, no guaranteed sound
2. **Each alarm can have its own sound** - use `sound name` property
3. **macOS notification settings must be enabled** for Calendar to show banners
   - System Settings > Notifications > Calendar > Allow Notifications + Banners/Alerts + Play Sound
4. **Reminders app does NOT support per-reminder custom sounds** via AppleScript
   - Reminders use the system notification sound globally
   - Calendar `sound alarm` is the ONLY way to get per-event custom sounds
5. **Always create BOTH Calendar event AND Reminders** for maximum coverage
   - Calendar = custom sounds per alarm tier
   - Reminders = separate notification channel, syncs to iPhone/iPad
6. **Never use short sounds** - they get missed/ignored in real life

## AppleScript Syntax Reference

### Sound Alarm (per-event custom sound)

```applescript
tell testEvent
    make new sound alarm at end of sound alarms with properties {trigger interval:-60, sound name:"Glass"}
    make new sound alarm at end of sound alarms with properties {trigger interval:-30, sound name:"Funk"}
end tell
```

### Display Alarm (visual banner only)

```applescript
make new display alarm at end of display alarms with properties {trigger interval:-60}
```

### Source

- [Apple Calendar Scripting Guide](https://developer.apple.com/library/archive/documentation/AppleApplications/Conceptual/CalendarScriptingGuide/Calendar-AddanAlarmtoanEvent.html)
