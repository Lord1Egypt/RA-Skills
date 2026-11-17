# Symptom Timeline

Track symptoms over time, identify triggers, and generate doctor-ready reports.

## Features

- **Symptom Logging** — Record symptoms with severity (1-10), timestamp, notes, and triggers
- **Timeline View** — Chronological history with severity bars
- **Trigger Correlation** — Detects patterns like "headache correlates with poor sleep (80%)"
- **Cross-Symptom Analysis** — Identifies symptoms that co-occur
- **Flare-Up Detection** — Flags consecutive high-severity episodes and sudden jumps
- **Severity Heatmap** — Visual ASCII heatmap of symptom intensity over time
- **Doctor Report Export** — Clean, chronological plain-text report for appointments

## Quick Start

```bash
# Log a symptom
python3 scripts/symptom_tracker.py log \
  --name headache \
  --severity 7 \
  --triggers "poor sleep,stress"

# See your timeline
python3 scripts/symptom_tracker.py timeline

# Find patterns
python3 scripts/symptom_tracker.py correlate

# Generate a summary
python3 scripts/symptom_tracker.py summary

# Detect flare-ups
python3 scripts/symptom_tracker.py flare-up

# Visualize severity
python3 scripts/symptom_tracker.py heatmap --name headache --days 30

# Export for your doctor
python3 scripts/symptom_tracker.py export --output report.txt
```

## Trigger Categories

Triggers are auto-categorized into: **food, stress, weather, medication, sleep, activity**.

```bash
# Explicit category prefix
python3 scripts/symptom_tracker.py log --name "joint pain" --severity 6 \
  --triggers "weather:high humidity,activity:long walk"

# Auto-categorized
python3 scripts/symptom_tracker.py log --name migraine --severity 8 \
  --triggers "chocolate,deadline,poor sleep"
```

## Requirements

- Python 3.7+ (stdlib only, no pip dependencies)

## Data

All entries are stored in `symptom_db.json`. Use `--db path.json` to customize.

## License

MIT © Denis Voronin
