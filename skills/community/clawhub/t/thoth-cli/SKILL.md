---
name: thoth-cli
version: 0.2.26
description: "Hermetic divination CLI: astrology (natal, transits, electional, returns, synastry), tarot (cryptographic random), gematria (Hebrew/Greek/English), numerology (Pythagorean). ALWAYS run CLI first—never fabricate positions or draws."
author: "aklo360"
homepage: "https://thothcli.com"
repository: "https://github.com/aklo360/thoth-cli"
license: "MIT"
metadata:
  openclaw:
    emoji: "𓅝"
    requires:
      bins: ["thoth"]
    install:
      - id: npm
        kind: node
        package: thoth-cli
        bins: ["thoth"]
        label: "Install thoth-cli from npm"
        registry: "https://www.npmjs.com/package/thoth-cli"
---

# thoth-cli — Hermetic Divination Tools

𓅝 **v0.2.26** | Swiss Ephemeris • secrets.SystemRandom • Classical Gematria • Pythagorean Numerology

**Source:** https://github.com/aklo360/thoth-cli  
**npm:** https://www.npmjs.com/package/thoth-cli  
**Website:** https://thothcli.com

## ⚖️ GOLDEN RULE

**NEVER fabricate planetary positions, card draws, or calculated values. Run the CLI first, then interpret.**

```
CLI = DATA (empirical)    →    Agent = INTERPRETATION (Hermetic)
```

---

## Installation

```bash
npm install -g thoth-cli
```

The package is published on npm by `aklo360`. Verify at: https://www.npmjs.com/package/thoth-cli

---

## Astrology

### Natal Chart
```bash
thoth chart --date 1879-03-14 --time 11:30 --city "Ulm" --nation DE
```

### Transits
```bash
thoth transit --natal-date 1879-03-14 --natal-time 11:30 --city "Ulm" --nation DE
```

### Electional (Optimal Timing)
```bash
thoth electional --start 2026-03-15 --end 2026-04-15
thoth electional --start 2026-03-15 --end 2026-04-15 --city "NYC" --nation US --json
```
*Outputs: VOC Moon, retrogrades, aspects, quality scores (excellent/good/challenging)*

### Returns
```bash
thoth solar-return --natal-date 1879-03-14 --natal-time 11:30 --city "Ulm" --nation DE --year 2026
thoth lunar-return --natal-date 1879-03-14 --natal-time 11:30 --city "Ulm" --nation DE --year 2026 --month 3
```

### Relationships
```bash
thoth synastry --date1 ... --date2 ...
thoth composite --date1 ... --date2 ...
thoth score --date1 ... --date2 ...
```

### Other
```bash
thoth horary --question "Should I?" --city "NYC"
thoth moon -e
thoth ephemeris --body pluto
thoth ephemeris-multi --bodies sun,moon,mercury --from 2026-03-01 --to 2026-03-31
thoth transit-scan --natal-date ... --start-year 2026 --end-year 2027
```

---

## Tarot

```bash
thoth tarot                   # Single card
thoth tarot -s 3-card         # Past/Present/Future
thoth tarot -s celtic         # Celtic Cross (10)
thoth tarot -q "Question?"    # With context
thoth tarot-card "The Tower"  # Card lookup
thoth tarot-spreads           # List spreads
```

---

## Gematria

```bash
thoth gematria "THOTH"
thoth gematria "Love" --compare "Will"
thoth gematria-lookup 93
```

---

## Numerology

```bash
thoth numerology --date 1991-07-08 --name "Full Name"
thoth numerology-year --date 1991-07-08
```

---

## Full Documentation

For complete CLI documentation and all commands: https://thothcli.com/skill.md
