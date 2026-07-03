# Automation Recipes

Use this reference for schedule and trigger-action rules in lighting design or automation create/update.

## Repeat And Time Rules

- Daily: `repeat: "daily"`.
- Weekdays: `repeat: "weekdays"`.
- Weekend: `repeat: "weekend"`.
- Once: `repeat: "once"`.
- Custom days: use `repeat: "custom"` plus `repeatDays`, for example `["mon", "wed", "fri"]`.
- Legal holiday/workday repeats are product/platform-specific; use `repeat: "legal_holiday"` or `repeat: "legal_workday"` only when Runtime evidence accepts them.
- Use `HH:mm:ss` clocks. If active window is not specified, use `activeWindow: {"start":"00:00:00","end":"23:59:59"}`.

## Condition Rules

Common scheduled condition:

```json
{
  "trigger": {
    "conditionKind": "alarm",
    "time": "09:00:00"
  }
}
```

- Separate triggers from facts. The first group should be trigger-like (`alarm`, `event`, `fact_change`); fact checks belong in a second group when needed.
- Do not invent event ids, event arguments, properties, or sensor facts from natural language.
- Use `automation.supported.list`, `automation.supported.v2.list`, `automation.detail.get`, or Runtime payloadShape as source evidence.
- Missing light actions may target device slot or group keys in a lighting design import.
- Missing sensor triggers may not be invented as live triggers. Keep them as design notes or recommendations unless product and target evidence exists.
- Non-scheduled automations are supported when Runtime evidence supplies the target and capability details: use `conditionKind: "event"` for device events, `conditionKind: "fact_change"` for property-change triggers, and `conditionKind: "fact"` for state checks. Use clear fields such as `targetType`, `targetKey` or `targetId`, `capabilityPid`, `eventId`, `eventArgs`, `property`, `operation`, and `value`.

## Action Rules

- Use `references/payload-shapes.md` for action rows and light parameters.
- Do not put enable/disable state in `automation.update`; use `automation.enable` or `automation.disable`.
- For updates, read `automation.detail.get` first when possible and resend the complete rule payload.

## Lighting Design Import Automations

```json
{
  "key": "master-9am",
  "name": "主卧每天9点",
  "activeWindow": {"start": "00:00:00", "end": "23:59:59"},
  "repeat": "daily",
  "trigger": {"conditionKind": "alarm", "time": "09:00:00"},
  "actions": [
    {
      "targetType": "group",
      "targetKey": "master-spot-group",
      "targetName": "主卧射灯组",
      "rank": 0,
      "set": {
        "power": true,
        "brightness": 60,
        "colorTemperature": 3000
      }
    }
  ]
}
```
