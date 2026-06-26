# get-profile Skill Examples

## Example 1: Complete Data Display

```
Invoke: get-profile

Output:
╔══════════════════════════════════════════════════╗
║                 👤 Personal Health Profile       ║
╠══════════════════════════════════════════════════╣
║  📋 Basic Information                           ║
║  Height:      ████ 175 cm                       ║
║  Weight:      ██████ 70 kg                      ║
║  Age:         35 years                         ║
╠══════════════════════════════════════════════════╣
║  📊 Health Indicators                          ║
║  BMI Index: 22.9 [Normal]✅                     ║
║  Body Surface Area: 1.85 m²                     ║
╚══════════════════════════════════════════════════╝
```

## Example 2: Overweight Status Display

```
Invoke: get-profile (BMI=25.5)

Output:
║  BMI Index: 25.5 [Overweight]⚠️               ║
║                                                  ║
║  💡 Recommendation: Control diet, increase exercise ║
```

## Example 3: Data Not Set

```
Invoke: get-profile (no data)

Output:
┌────────────────────────────────────┐
│       ⚠️  Data Not Set              │
├────────────────────────────────────┤
│  Personal health profile not set   │
│                                    │
│  Please use: /profile set 175 70 1990-01-01 │
└────────────────────────────────────┘
```

## Example 4: With Weight Trend

```
Invoke: get-profile (with history)

Output:
📈 Weight History Trend (Last 5)
2025-12-31  →  70.0 kg
2025-11-15  →  71.5 kg
...
📊 Change: -4.0 kg (-5.4%)
```
