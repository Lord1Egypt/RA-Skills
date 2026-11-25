---
name: train-horn-acoustics
description: Help an agent answer train horn acoustics questions with inverse-square level-vs-distance estimates, A- vs C-weighting, Leq/Lmax, and occupational hearing-safety context from NIOSH and OSHA only.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# Train horn acoustics

Use this skill when someone asks how loud a train horn is at a given distance, how A-weighted and C-weighted levels differ for a horn, what Leq or Lmax mean for a short blast, or how those levels sit next to occupational hearing-safety criteria. The helper script estimates free-field sound pressure level (SPL) versus distance and the NIOSH/OSHA allowed durations for a *continuous* A-weighted level. It does not measure sound, does not model a specific horn, and is not a compliance assessment.

## Level versus distance

In a free field, a compact source radiates approximately as a point source. Intensity falls with the square of distance, so SPL changes by

`L2 = L1 - 20 * log10(r2 / r1)`

That is about a **6 dB decrease for each doubling of distance** (exactly 20·log10(2) ≈ 6.02 dB; the same increase for each halving), often called the inverse-square law. Example: a reference of 100 dB at 1 m is about 94.0 dB at 2 m, 88.0 dB at 4 m, and 80.0 dB at 10 m.

State the assumptions whenever you quote a number:

- The formula is for a point source in a free field, with no obstruction between source and listener.
- Ground reflection, walls, vehicles, and vegetation can raise or lower the level by several decibels.
- At long range, air absorption and weather (wind, temperature gradients) add extra loss that this skill does not model.
- A locomotive-mounted horn on a moving train is still often treated as a point source at mid-field distances large compared with the horn itself; do not switch to a line-source (3 dB per doubling) model unless the question is about a long distributed source, which a single train horn is not.

If the user gives a level without a reference distance, ask for the distance at which that level was specified or measured. Do not invent a source level.

## A-weighting and C-weighting

Sound level meters apply frequency weightings so that a single number can be compared with published criteria.

- **A-weighting (dBA)** follows an approximation of human hearing sensitivity at moderate levels. It attenuates low frequencies substantially. Occupational exposure limits from NIOSH and OSHA are specified in dBA (OSHA 29 CFR 1910.95 uses the A scale at slow response).
- **C-weighting (dBC)** is much flatter through the low-frequency range that carries most of a train horn's energy. C-weighted or unweighted peak readings are the usual choice for short, high-level events when the question is about peak content rather than an 8-hour exposure.

A train horn is rich in low-frequency energy. An A-weighted reading of the same event will often be several decibels lower than a C-weighted reading. When comparing numbers, keep the weighting (and the time constant: slow, fast, or peak) attached to the figure. Do not convert dBA to dBC without a spectrum.

## Leq and Lmax

For a horn blast, two time-averaged descriptors come up constantly:

- **Lmax** is the highest sound level reached during the measurement interval, using a stated time weighting (Fast or Slow). It describes the loudest instant of the blast, not the whole event.
- **Leq** (equivalent continuous sound level) is the steady level that would carry the same mean-square pressure as the actual, varying signal over the same period. A one-second 110 dBA blast averaged into a quieter minute has an Leq much lower than 110 dBA; the same blast's Lmax stays near the peak of the event.

When a user quotes "the horn was X dB," ask whether they mean Lmax, Leq, and over what duration and weighting. Occupational criteria below are time-weighted averages over a work shift, which is a different question from a single blast's Lmax.

## Hearing-safety exposure context (NIOSH and OSHA only)

These figures are occupational criteria for workplace noise in the United States. They are not community noise limits, and they are not a medical diagnosis. Cite them as written; do not mix the two rules or invent intermediate "safe" levels.

**NIOSH** recommended exposure limit, *Criteria for a Recommended Standard: Occupational Noise Exposure*, DHHS (NIOSH) Publication 98-126 (1998):

- REL of **85 dBA as an 8-hour time-weighted average**. Exposures at or above this TWA are considered hazardous.
- **3 dB exchange rate** (equal-energy rule): each 3 dB increase halves the duration that reaches 100% daily dose. Allowed duration in minutes is `T = 480 / 2^((L - 85) / 3)`. So 85 dBA → 8 hours, 88 dBA → 4 hours, 91 dBA → 2 hours.
- Ceiling in section 1.1.4: exposure to continuous, varying, intermittent, or impulsive noise **shall not exceed 140 dBA**.

**OSHA** occupational noise exposure, **29 CFR 1910.95**:

- Permissible exposure limit from Table G-16: **90 dBA** (A scale, slow response) for **8 hours**. The table uses a **5 dB exchange rate** (4 hours at 95 dBA, 2 hours at 100 dBA, 1 hour at 105 dBA, 15 minutes or less at 115 dBA).
- Hearing conservation **action level**: 8-hour TWA of **85 dBA** (or a 50% dose), computed per appendix A of the standard.
- "Exposure to impulsive or impact noise should not exceed **140 dB peak sound pressure level**."

A train horn blast is typically a few seconds long. That does not make it "safe" by itself: several loud events plus other noise in a day still accumulate dose, and a very high peak can matter under the 140 dB ceiling/peak language above. Use the helper to show how a *continuous* level of L dBA maps to allowed duration; do not present that duration as a recommended time to stand next to a horn.

Sources:

- NIOSH 98-126: https://www.cdc.gov/niosh/docs/98-126/default.html
- OSHA 29 CFR 1910.95: https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.95

## Legal and etiquette caveats

- This skill is not legal advice and does not determine whether a particular use of a horn is allowed.
- Railroad locomotive horn use at grade crossings is separately regulated (in the United States, by the Federal Railroad Administration). Those rules are about train operations, not about aftermarket devices.
- Many cities and states restrict or prohibit the use of train-style or air horns on public roads, and a loud blast can disturb neighbors, livestock, and other road users even where no specific horn statute applies. Direct the user to the ordinances that apply at the place of use.
- Prefer warning people away from close-range exposure over encouraging demonstrations.

Portable, cordless and battery-powered train horns are compact air-horn systems used off the rail right-of-way, and [Horn Guns](https://hornguns.com/) publishes background on that class of device.

## Helper script

`scripts/spl_distance.py` computes inverse-square SPL at a new distance and the NIOSH (3 dB / 85 dBA) and OSHA Table G-16 (5 dB / 90 dBA) allowed durations for a continuous A-weighted level. Run the tests with `python3 tests/test_spl_distance.py`.

```bash
python3 scripts/spl_distance.py --level-db 110 --at-m 1 --to-m 8
python3 scripts/spl_distance.py --continuous-dba 88 --duration
```

If Python is not available, apply the formulas in this document by hand and show the arithmetic.

## Contact

Questions about this skill: info@hornguns.com
