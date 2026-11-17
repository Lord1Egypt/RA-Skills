# Sleep Debt Calculator 🌙

Track your sleep, calculate accumulated sleep debt, and get evidence-based
recovery schedules. Pure Python — no dependencies, no internet, just you and
better sleep.

## Features

- 📊 **Sleep debt tracking** — cumulative deficit/surplus vs age-based optimal
- ⚖️ **Quality-weighted sleep** — 6h deep sleep counts more than 8h restless
- 📅 **Recovery scheduler** — "Sleep 8.5h for 6 nights to clear 4.5h debt"
- 🦉 **Chronotype detection** — early bird vs night owl from your patterns
- 📈 **ASCII charts** — visualize sleep duration trends with optimal reference line
- 📋 **Weekly/monthly reports** — summaries with quality correlations
- ☕ **Substance impact** — flags caffeine/alcohol in notes, correlates with quality
- 🛌 **Weekend recovery detection** — identifies catch-up sleep patterns
- 🔥 **Consistency streaks** — track your logging habit

## Quick Start

```bash
# No installation required — just Python 3
python3 scripts/sleep_debt.py init          # Set up your profile (age)
python3 scripts/sleep_debt.py log 23:30 07:15 4 "slept well"
python3 scripts/sleep_debt.py debt
```

## Usage

### Initialize your profile

```bash
python3 scripts/sleep_debt.py init
# Enter your age → sets optimal sleep target
```

### Log sleep

```bash
python3 scripts/sleep_debt.py log <bedtime> <wake> [quality] [notes]

# Examples:
python3 scripts/sleep_debt.py log 23:30 07:15 4 "felt rested"
python3 scripts/sleep_debt.py log 01:00 06:30 2 "late night, coffee at 5pm"
python3 scripts/sleep_debt.py log 22:45 06:00 5 "great sleep, one beer with dinner"
```

- **bedtime/wake:** 24-hour format `HH:MM`
- **quality:** 1 (terrible) to 5 (excellent), default 3
- **notes:** free text. Mention caffeine/alcohol for automatic tracking

### Check your debt

```bash
python3 scripts/sleep_debt.py debt
# Shows total debt, recent trends, weekend recovery detection
```

### Plan recovery

```bash
python3 scripts/sleep_debt.py recovery 8.5
# "Current debt: 4.5h → Sleep 8.5h for 6 nights to recover"
```

### See your optimal sleep

```bash
python3 scripts/sleep_debt.py optimal
# Shows recommended hours based on your age
```

### Visualize trends

```bash
python3 scripts/sleep_debt.py chart 14    # Last 14 days
python3 scripts/sleep_debt.py chart 30    # Last 30 days
```

### Tonight's schedule

```bash
python3 scripts/sleep_debt.py schedule
# Suggests bedtimes based on your debt and common wake times
```

### Detect your chronotype

```bash
python3 scripts/sleep_debt.py chronotype
# Analyzes bedtime patterns to classify early bird / night owl
```

### Weekly/monthly report

```bash
python3 scripts/sleep_debt.py report week
python3 scripts/sleep_debt.py report month
```

### Consistency streak

```bash
python3 scripts/sleep_debt.py streak
```

## Data Storage

Sleep data is stored in `~/.sleep_debt.json`. Delete this file to reset.

## The Science

The calculator uses National Sleep Foundation age-based recommendations:

| Age | Optimal Sleep |
|-----|--------------|
| 6–13 | 9.5h |
| 14–17 | 9.0h |
| 18–25 | 8.0h |
| 26–64 | 8.0h |
| 65+ | 7.5h |

Quality weighting reflects that fragmented sleep is less restorative:

| Quality | Weight | Example |
|---------|--------|---------|
| 5 (excellent) | 100% | 8h in bed = 8.0h effective |
| 3 (average) | 80% | 8h in bed = 6.4h effective |
| 1 (terrible) | 45% | 8h in bed = 3.6h effective |

See [`references/sleep-science-basics.md`](references/sleep-science-basics.md)
and [`references/recovery-strategies.md`](references/recovery-strategies.md)
for detailed explanations.

## Requirements

- Python 3.6+ (stdlib only, no pip packages)

## License

MIT © Denis Voronin
