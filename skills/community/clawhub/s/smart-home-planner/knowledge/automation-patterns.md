# Automation Scene Templates

## Scene 1: Home Mode (回家模式)

### Effect Description
When you arrive home, the hallway light turns on automatically, the curtains open to let in natural light, the air conditioner adjusts to a comfortable temperature, and your favorite music starts playing. No need to fumble for switches in the dark.

### Trigger Conditions
- Primary: Phone connects to home WiFi / enters geofence
- Alternative: Motion sensor at entrance detects movement
- Alternative: Smart lock is unlocked
- Time-aware: Different behavior for day vs night arrival

### Devices Involved
| Device | Action | Reason |
|--------|--------|--------|
| Hallway light | Turn on | Welcome lighting |
| Living room curtains | Open (if daytime) | Natural light |
| Air conditioner | Set to 24°C | Comfort |
| Speaker | Play playlist | Ambiance |

### Platform Config

**Home Assistant:**
```yaml
automation:
  - alias: "Home Mode"
    trigger:
      - platform: state
        entity_id: device_tracker.phone
        to: "home"
    action:
      - service: light.turn_on
        target:
          area_id: hallway
      - choose:
          - conditions:
              - condition: sun
                after: sunrise
                before: sunset
            sequence:
              - service: cover.open_cover
                target:
                  entity_id: cover.living_room_curtain
      - service: climate.set_temperature
        target:
          entity_id: climate.living_room
        data:
          temperature: 24
```

**米家:**
```
App → Smart → Add Scene
  Trigger: When [Phone] arrives at [Home]
  Action: Turn on [Hallway Light]
  Action: Open [Living Room Curtain]
  Action: Set [AC] to 24°C
```

---

## Scene 2: Away Mode (离家模式)

### Effect Description
When everyone leaves home, all lights turn off, air conditioning shuts down, curtains close, and the security system activates. The robot vacuum starts cleaning. Your home is safe and energy-efficient while you're away.

### Trigger Conditions
- Primary: All phones leave home geofence
- Alternative: No motion detected for 30 minutes + all doors closed
- Manual: Voice command "I'm leaving"

### Devices Involved
| Device | Action | Reason |
|--------|--------|--------|
| All lights | Turn off | Energy saving |
| All ACs | Turn off | Energy saving |
| All curtains | Close | Security + privacy |
| Security cameras | Start recording | Security |
| Door/window sensors | Arm alarm | Security |
| Robot vacuum | Start cleaning | Maintenance |

### Platform Config

**Home Assistant:**
```yaml
automation:
  - alias: "Away Mode"
    trigger:
      - platform: state
        entity_id: group.all_devices
        to: "not_home"
        for: "00:05:00"
    action:
      - service: light.turn_off
        target:
          area_id: all
      - service: climate.turn_off
        target:
          area_id: all
      - service: cover.close_cover
        target:
          area_id: all
      - service: alarm_control_panel.alarm_arm_away
        target:
          entity_id: alarm_control_panel.home
      - service: vacuum.start
        target:
          entity_id: vacuum.robot
```

**米家:**
```
App → Smart → Add Scene
  Trigger: When all family phones leave [Home]
  Action: Turn off all lights
  Action: Turn off all ACs
  Action: Close all curtains
  Action: Start [Robot Vacuum]
```

---

## Scene 3: Sleep Mode (睡眠模式)

### Effect Description
When it's bedtime, the living room lights dim and turn off, bedroom lights warm and dim to 10%, curtains close completely, AC switches to sleep mode with gentle temperature adjustment throughout the night, and the door lock engages.

### Trigger Conditions
- Primary: Voice command "Good night" / "Going to sleep"
- Alternative: Phone placed on charger after 10 PM
- Alternative: Specific scene button pressed

### Devices Involved
| Device | Action | Reason |
|--------|--------|--------|
| Living room lights | Off | Sleep prep |
| Bedroom light | Dim to 10%, warm | Sleep mood |
| All curtains | Close | Block light |
| AC | Sleep mode, 26°C | Comfort through night |
| Door lock | Lock | Security |
| Night light | Auto on if motion | Bathroom trips |

---

## Scene 4: Wake Mode (起床模式)

### Effect Description
In the morning, curtains slowly open over 5 minutes to let natural light wake you gently. Bedroom lights gradually brighten to simulate sunrise. The speaker plays your morning briefing: weather, calendar, and news. Coffee maker starts (if equipped).

### Trigger Conditions
- Primary: Alarm time (weekday/weekend different)
- Alternative: Motion sensor in bedroom detects movement after 6 AM
- Manual: Voice command "Good morning"

### Devices Involved
| Device | Action | Reason |
|--------|--------|--------|
| Bedroom curtains | Open slowly (5 min) | Natural wake |
| Bedroom light | Brighten gradually (5 min) | Simulate sunrise |
| Speaker | Play morning briefing | Information |
| Bathroom light | Turn on | Convenience |
| Water heater | Turn on | Hot water ready |

---

## Scene 5: Security Mode (安防模式)

### Effect Description
When security is armed, any door/window opening triggers an immediate notification. Motion detection in restricted areas activates camera recording and sends alerts. At night, unexpected motion triggers a warning sound and lights.

### Trigger Conditions
- Arm: Away mode activates / Manual arm / Voice command
- Disarm: Arrive home / Smart lock unlock / Manual disarm
- Alert: Door sensor open while armed / Motion in restricted zone

### Devices Involved
| Device | Action | Reason |
|--------|--------|--------|
| Door/window sensors | Monitor | Perimeter security |
| Motion sensors | Monitor | Interior security |
| Cameras | Record on alert | Evidence |
| Indoor siren | Sound on alert | Deterrent |
| All lights | Flash on alert | Visual warning |
| Phone | Push notification | Remote alert |

### Alert Levels
```
Level 1 - Notification only:
  Door sensor triggered → Push notification to phone

Level 2 - Visual alert:
  Motion detected at night → Hallway lights flash + notification

Level 3 - Full alert:
  Multiple sensors triggered → Siren + all lights flash + camera recording + notification
```

### Safety Defaults
- Lock and alarm actions must always have a manual override path.
- Camera alerts should prefer notification-first behavior before loud siren actions.
- Motion-based lights should ignore brief blips and allow a delay before repeat triggers.
- If the house has pets, avoid treating low-height motion as a security trigger without explicit filtering.

### False Trigger Handling
- Add a time window or occupancy check when a scene can be triggered by normal family movement.
- For night alerts, keep visual notification before acoustic escalation when possible.
- If a scene repeatedly misfires, fall back to notification-only until the trigger is adjusted.

---

## Custom Scene Patterns

### Movie Mode (观影模式)
- Living room lights dim to 5%, warm white
- Curtains close
- TV/projector turns on
- AC set to comfortable temperature
- Doorbell notifications silenced (redirect to watch)

### Guest Mode (客人模式)
- All lights bright
- Guest room prepared (lights, AC, fresh towels notification)
- Security relaxed for guest area
- Door lock temporary code generated

### Energy Saving Mode (节能模式)
- All non-essential devices off
- AC limited to 26-28°C range
- Lights auto-off after 5 min no motion
- Standby devices fully powered off via smart plugs

### Pet Mode (宠物模式)
- Camera monitoring active
- AC maintains comfortable temperature
- Feeder schedule active
- Motion alerts for unusual activity
- Curtains partially open for natural light

### Outage / Recovery Pattern
- If cloud control is unavailable, prefer local scene fallback or safe manual state.
- If power returns after an outage, do not auto-arm security scenes without checking state consistency.
