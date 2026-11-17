---
name: tire-chain-law-navigator
description: Use when driving mountain passes in snow season and unsure about chain requirements — coverage-based verdicts (R1/R2/R3, traction-device, conditional closure) for US/Canada/EU-Alps routes by date, vehicle class and AWD/4WD status, chain-up zone finder, carry-requirement vs must-install rules, and printable dash-card for the drive.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [winter-driving, tire-chains, mountain-passes, road-trip, snow, traction-law, chain-law]
---

# Tire Chain Law Navigator

## Overview

Winter mountain driving has a legal layer most drivers discover only at a
checkpoint or in a ditch: **chain law**. California posts R1/R2/R3, Colorado
alternates a **Traction Law** and **Passenger Vehicle Chain Law**, Washington
and Oregon have their own codes, BC requires chains Nov 1–Mar 31 on many
routes, and Alpine countries post snow-chain *signs* (267/268) that are
legally binding. Drivers from out of region routinely get fined or turned
around — or worse, drive unchained in conditions where chains were required.

This skill gives you:

1. **Verdict by route + date + vehicle** — which requirement class applies
   on a given pass/corridor in snow season, for your vehicle class
   (passenger / 4WD-AWD / CMV truck), with fine ranges.
2. **Carry vs install rules** — where chains must merely be *carried*
   (e.g. BC commercial vehicles, some park roads) vs *installed*, and the
   AWD-with-snow-tires exemptions (they exist — but not in R2 for 2WD, not
   at R3 for anyone).
3. **Chain-up zone finder** — how to locate the signed chain-up areas
   before a checkpoint (US: "Chain Up Ahead" signs; EU: panneau zones
   chaînes), and why you must never install on a live lane.
4. **Sizing guide** — cable vs link chains vs socks: what your clearance
   allows, what is legal where (socks are not legal substitutes in some
   jurisdictions/states for R2), speed limits with chains (typically
   25–30 mph / 30–50 km/h).
5. **Dash-card** — a printable one-pager for the glovebox: your route's
   requirement classes, phone numbers (road conditions), checkpoint behavior.

The script holds a curated corridor database (I-70 Colorado, Donner Pass
I-80, Snoqualmie I-90, BC Coquihalla, Alpine crossings) and computes
seasonal requirements by date.

## When to Use

- Planning a ski / mountain trip in snow season (Nov–Apr in most ranges)
- "Do I need chains for I-70 to Denver if it's snowing?" → verdict + exemptions
- Driving a rental or a new AWD vehicle into the mountains first time
- CMV/truck routing decisions in winter (chain requirements differ)
- Alpine driving (France/Italy/Switzerland/Austria): panel 267/268 meaning

**Don't use for:** real-time road status — always confirm with the live
phone line/website listed on the dash-card the day of travel. This skill is
the legal/rule layer, not a live feed.

## Quick Start

```bash
# What applies on I-70 mountain corridor, Jan 15, passenger AWD with snow tires?
python3 scripts/chainlaw.py check --route i70-co --date 2027-01-15 \
    --vehicle awd-snows --conditions active

# Same corridor, 2WD all-seasons in active snow (what changes?)
python3 scripts/chainlaw.py check --route i70-co --date 2027-01-15 \
    --vehicle rwd-allseason --conditions active

# List every known corridor with its jurisdiction + season
python3 scripts/chainlaw.py routes

# Chain sizing / equipment legality primer
python3 scripts/chainlaw.py equipment --vehicle passenger --clearance tight

# Printable dash-card for the trip
python3 scripts/chainlaw.py dashcard --routes i70-co,donner-i80 --vehicle awd-snows --out card.md
```

## Requirement Classes (core knowledge)

| Code | Meaning | Who may proceed | Typical fine if ignored |
|---|---|---|---|
| **R1** (CA) / Traction Law (CO) | Snow/mud on roadway | Chains OR snow tires (M+S), MUD/SNOW rated; AWD exempt from chains in CO traction law if tread ≥ 3/16" | $130+ (CO ~$650 if blocking road) |
| **R2** (CA) | Snow, deeper | 4WD/AWD with snow-rated tires OR chains on drive axle of 2WD | ~$100–1,000 + turnaround |
| **R3** (CA) / PV Chain Law (CO) | Severe | CHAINS ON EVERYTHING — no exemptions | fine + closure |
| BC (Canada) | Nov 1–Mar 31 many highways | Carry required (commercial); install when signed/posted | $157–$595 |
| EU Alpine sign 267 | Snow-covered road | Chains on drive axle for the signed stretch | on-the-spot fines (e.g. France ~135 €) |

Key nuance the script encodes: **AWD is not a chain exemption at R3 or CO's
Passenger Vehicle Chain Law** — and "snow tires" means 3PMSF or M+S *with
adequate tread*, not all-seasons with highway tread.

## How the Verdict Is Computed

1. Date → is it in the corridor's chain-law season? (Most: Nov 1–Mar 31;
   some passes Oct 1–May 31 — see `routes` output.)
2. Route → jurisdiction + default requirement class for that date
   (base = carry advisory; `--conditions active` escalates per the
   jurisdiction's escalation ladder).
3. Vehicle → exemptions applied (AWD+snows at R1/traction-law; none at R3).
4. Output: requirement class, whether YOU may pass, what to install,
   fine exposure, and the corridor's info line.

## Common Pitfalls

1. **"I have AWD, I don't need chains."** True at R1/Traction Law with
   proper snow tires; FALSE at R2 in some states for 2WD (chains on drive
   axle), always FALSE at R3 and Colorado's PV Chain Law. AWD helps you
   go; it does not help you *stop*, and law is about control.
2. **Socks vs chains.** Auto socks are accepted in some jurisdictions as
   "traction devices" and not in others (CA accepts cables; some EU states
   accept textile; BC distinguishes). Check `equipment` output before
   relying on socks.
3. **Speed with chains.** 25–30 mph max — chains destroy tires/fenders and
   can wrap drivelines at speed. It's also the law in most jurisdictions.
4. **Installing on the shoulder of a live lane.** Use signed chain-up
   zones; they're flat, wide, and visible to trucks. People die doing this
   on live shoulders.
5. **All-seasons ≠ snow tires.** M+S marking with 4/32" tread may fail a
   checkpoint's tread check. CO traction law: ≥3/16" (≈5/32") tread.

## Verification Checklist

- [ ] Route + date checked against the corridor season table
- [ ] Vehicle class + tire type entered honestly (tread depth matters)
- [ ] Live status confirmed via the corridor's info line on travel day
- [ ] Chains tried on the vehicle BEFORE the trip (fitting practice)
- [ ] Dash-card printed with phone numbers for every corridor on the route

## One-Shot Recipes

**Ski trip, Denver→Vail, AWD SUV with new snow tires:**
```bash
python3 scripts/chainlaw.py check --route i70-co --date 2027-02-20 \
    --vehicle awd-snows --conditions active
python3 scripts/chainlaw.py dashcard --routes i70-co --vehicle awd-snows --out card.md
```

**Rear-wheel-drive rental, Tahoe weekend:**
```bash
python3 scripts/chainlaw.py check --route donner-i80 --date 2027-01-09 \
    --vehicle rwd-allseason --conditions severe
# → expect: at R2 you install chains on drive axle; carry them regardless.
```

**Alps rental in January:**
```bash
python3 scripts/chainlaw.py check --route alps-fr-it --date 2027-01-12 \
    --vehicle fwd-snows --conditions sign267
```
