# Sump Pump Outage Planner

**When the sump pump dies, you're not fixing an appliance — you're
racing a clock you've never computed.** Gallons per inch of pit rise
÷ storm inflow rate = hours to flooded basement. That number decides
whether you sleep, bail, or hook up a generator.

## The Problem

- Power outages and pump failures happen at night, in storms, when
  inflow is 2–4× normal — the exact worst case.
- Most sump failures aren't even the power: stuck float, failed check
  valve, worn impeller. People replace a $140 pump at 2 AM over a $15
  float or a $20 check valve.
- Backup choices are made in a panic at the hardware store: battery vs
  generator vs water-powered — sized by nothing, tested never.
- Battery backups die silently in 2–4 years; nobody unplugs the main
  pump to test them until the night they're needed.

## What This Skill Does

`scripts/sump_outage.py` computes the countdown from five measurements
(pit diameter, usable rise, pump off-period, on/off gap, storm
multiplier), ranks backup options by real protection hours, sizes the
backup pump to your actual inflow (2× storm), computes battery runtime
at your duty cycle, and prints the 2 AM triage card:

```bash
python3 scripts/sump_outage.py --pit-diameter 18 --usable-rise-in 14 \
  --off-minutes 8 --on-off-gap-in 6 --storm-mult 3

python3 scripts/sump_outage.py --pit-diameter 18 --usable-rise-in 14 \
  --off-minutes 5 --on-off-gap-in 6 --battery-ah 75 --target-hours 8

python3 scripts/sump_outage.py --triage
```

## Who Needs This

- Anyone with a sump pit and a finished (or finishable) basement
- Storm-belt households where outages and rain arrive together
- People buying their first backup pump and unsure which type
- Post-flood: understanding why, before spending $500 on the wrong fix

## Example

18-in pit (1.10 gal/in), 14-in usable rise = 15.4 gal. Measured
off-period 8 min with a 6-in gap = 50 gph baseline; storm ×3 = 150 gph
→ **6 minutes to critical** — bailing is pointless; a backup pump with
its own float plus a high-water alarm is mandatory *before* the next
storm, and this pit needs drainage attention (downspouts, grading).
Even a calmer pit (cycles every 90 min, storm ×2) lands at ~1.8 h:
most real pits live in the minutes-to-few-hours range, which is why
the backup decision is never optional for a wet basement — the only
question is which kind. The script answers that from your five numbers.

## License

MIT — see LICENSE.
