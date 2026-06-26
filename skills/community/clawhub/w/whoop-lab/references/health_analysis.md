# WHOOP Health Analysis Guide

> **Core principle:** Track *your* trends vs *your* personal baseline — not population averages. WHOOP's value is in deviation detection, not absolute benchmarking.

---

## HRV (Heart Rate Variability — RMSSD)

HRV measures beat-to-beat variation in milliseconds. Higher generally = better autonomic nervous system recovery.

### Population Ranges by Age (RMSSD, ms)
| Age | Low | Average | High |
|-----|-----|---------|------|
| 20–29 | <40 | 55–75 | >90 |
| 30–39 | <35 | 45–65 | >80 |
| 40–49 | <28 | 35–55 | >70 |
| 50–59 | <22 | 28–45 | >60 |
| 60+ | <18 | 22–35 | >50 |

**Important:** Athletes often run 20–30ms above these ranges. Fit people in their 40s can easily match a sedentary 20-year-old's numbers, and that's fine.

### What Trends Mean
- **Rising week-over-week:** Adapting well to training load, good recovery, positive stress response
- **Stable:** Baseline maintenance — sustainable if strain is also stable
- **Dropping 5–10ms over a week:** Emerging fatigue, inadequate recovery, possible illness onset
- **Sudden single-day drop >10ms:** Acute stressor (alcohol, illness, poor sleep, emotional stress)
- **Chronically suppressed (>2 weeks below baseline):** Overtraining or systemic stress — reduce load

### Red Flags
- HRV drops >20% from personal baseline and stays low for 5+ days
- HRV low + RHR elevated + recovery red for 3+ consecutive days (overtraining pattern)
- Erratic swings (high one day, low next) with no clear cause — can indicate irregular sleep, arrhythmia

---

## Resting Heart Rate (RHR)

Measured during sleep (most accurate window). Lower = more efficient cardiovascular system.

### Ranges by Fitness Level
| Level | RHR (bpm) |
|-------|-----------|
| Elite athlete | 30–45 |
| Fit / active | 45–60 |
| Average healthy adult | 60–75 |
| Below average | 75–85 |
| Medical concern | >85 consistently |

### Interpretation
- **Trending down over months:** Improving cardiovascular fitness
- **+3–5 bpm above baseline:** Fatigue, dehydration, illness starting, heavy alcohol the night before
- **+8–10 bpm above baseline:** Significant stressor — illness, very hard training, extreme stress
- **Consistently elevated (>2 weeks):** Chronic overtraining, illness, thyroid issue, medication effect

### RHR + HRV Together
These two metrics are inversely correlated. RHR up + HRV down = sympathetic nervous system dominance = your body is stressed. When both trend favorably (RHR down, HRV up), you're adapting well.

---

## Sleep Stage Breakdown

WHOOP tracks sleep via heart rate and respiratory rate. Not as precise as PSG (lab sleep study) but good for trend tracking.

### Target Stage Percentages
| Stage | Target | What It Does |
|-------|--------|--------------|
| Deep (SWS) | 15–20% | Physical repair, hormone release (HGH), immune function |
| REM | 20–25% | Memory consolidation, emotional regulation, creativity |
| Light | 50–60% | Transition stage, still restorative |
| Awake | <5% | Normal to wake briefly; more = fragmented sleep |

### Stage Deficits and Their Consequences
- **Low deep sleep (<10%):** Physical fatigue, reduced muscle recovery, immune suppression, blunted HGH release
- **Low REM (<15%):** Brain fog, emotional reactivity, poor learning consolidation, impaired decision-making
- **High awake %:** Fragmented sleep — often caused by alcohol, caffeine late in day, sleep apnea, stress
- **Short total sleep:** Everything degrades — prioritize duration first, then stage quality

### Sleep Performance Score
WHOOP's composite score. Targets:
- **85–100%:** Optimal
- **70–84%:** Adequate
- **<70%:** Insufficient — expect impaired recovery

### Sleep Debt
WHOOP tracks cumulative sleep need. Each hour of debt compounds cognitive and physical impairment. 1 hour of debt ≠ 1 hour of makeup sleep — it takes ~4 nights of full sleep to fully repay significant debt.

---

## Recovery Score

WHOOP's proprietary 0–100% score combining HRV, RHR, sleep performance, and respiratory rate vs your personal baseline.

### Zones
| Score | Zone | Color | Recommended Action |
|-------|------|-------|-------------------|
| 67–100% | Green | 💚 | Take on high strain; push hard in training |
| 34–66% | Yellow | 💛 | Moderate effort; listen to body; don't force it |
| 0–33% | Red | 🔴 | Recovery day; light movement only; prioritize sleep |

### What to Do in Each Zone
**Green:** Schedule hard workouts, new PRs, demanding cognitive work here. Your body is primed.

**Yellow:** Tempo runs, moderate lifting, steady-state cardio are fine. Avoid max efforts. Monitor how you feel vs the score.

**Red:** Don't override red for consecutive days. Walk, stretch, sleep more. One red day is fine; 3+ consecutive reds = something systemic is wrong.

### Score Can Lie
- New illness (score may be green before you feel sick)
- Alcohol consumed — HRV is artificially suppressed, so score drops
- Mental stress without physical load — often under-represented
- Pregnancy and hormonal cycles affect baseline

---

## Strain Scale (0–21)

WHOOP strain measures cardiovascular load using time-in-heart-rate-zones. Higher ≠ better.

### Scale Breakdown
| Range | Level | Description |
|-------|-------|-------------|
| 0–9 | Light | Daily living, walking, gentle yoga |
| 10–13 | Moderate | Brisk walking, casual cycling, light lifting |
| 14–17 | Strenuous | Running, moderate lifting, sports |
| 18–20 | Very Strenuous | Hard interval training, intense CrossFit |
| 21 | Max Effort | Rare — race day, extreme physical output |

### Matching Strain to Recovery
| Recovery | Suggested Max Strain |
|----------|---------------------|
| Green (67–100%) | 14–21 — push as hard as goal demands |
| Yellow (34–66%) | 10–14 — moderate effort |
| Red (0–33%) | 0–10 — light only |

**Rule of thumb:** Don't chase high strain on red recovery. This compounds debt. The best athletes train hard when ready and recover hard when not.

### Strain Without Adequate Recovery = Injury Risk
3+ consecutive days of strain >16 without a green recovery day is a red flag pattern.

---

## SpO2 (Blood Oxygen Saturation)

Measured during sleep by WHOOP (4.0+).

### Ranges
| SpO2 | Interpretation |
|------|---------------|
| 95–100% | Normal |
| 90–94% | Mild hypoxemia — worth monitoring |
| <90% | Significant — investigate (altitude, sleep apnea, illness) |

### Context
- **Altitude:** SpO2 naturally drops at elevation (90–93% common above 8,000 ft)
- **Sleep apnea signal:** Dips below 90% repeatedly throughout the night — consult a doctor
- **COVID/respiratory illness:** Watch for sustained drops even at sea level
- WHOOP SpO2 is a trend indicator, not medical-grade oximetry

---

## Skin Temperature

WHOOP 4.0 measures skin temp during sleep vs your personal baseline.

### What Deviations Mean
| Deviation | Likely Cause |
|-----------|-------------|
| +0.5–1.0°C | Mild inflammation, increased exertion, warm environment |
| +1.0–2.0°C | Emerging illness, significant alcohol, acute inflammation |
| >+2.0°C | Active illness — expect reduced recovery |
| Negative deviation | Unusual; may indicate cold environment or lower metabolic activity |

**Use it as an early warning system.** Elevated skin temp before you feel sick often shows up 1–2 days before subjective symptoms.

---

## Overtraining Signals (Combo Patterns)

Single metrics are noisy. Combinations are diagnostic.

### Pattern: Classic Overtraining
- HRV: 10–15% below personal baseline for 7+ days
- RHR: 5+ bpm above baseline consistently
- Recovery: Yellow/red for 5+ consecutive days
- Sleep: Performance declining despite adequate duration
- **Action:** Take 3–5 full rest days. Reassess. If no improvement, see a sports medicine doctor.

### Pattern: Lifestyle Stress (Not Training)
- HRV: Suppressed
- RHR: Elevated
- Recovery: Red
- Strain: Low (not training hard)
- Sleep: Short or fragmented
- **Action:** Sleep, stress management, nutrition. This isn't a fitness problem.

### Pattern: Illness Onset
- Skin temp: +1°C above baseline
- RHR: +5–8 bpm
- HRV: Dropping
- Recovery: Sudden red from baseline green
- **Action:** Rest. Don't train through it. One sick day of rest beats a week-long setback.

### Pattern: Alcohol Effect
- HRV: Suppressed night of consumption
- RHR: Elevated
- Sleep: REM severely reduced
- Recovery: Often 20–30% below normal
- **Action:** Expected — factor this in. Avoid hard training next day.

---

## Red Flags — When to See a Doctor

These patterns in WHOOP data warrant medical attention:

1. **Resting HR consistently >85 bpm** with no clear cause
2. **SpO2 regularly dipping below 90%** during sleep (possible sleep apnea)
3. **HRV chronically <20ms** (for adults under 60) with no improvement after rest
4. **Respiratory rate elevated >20 breaths/min** consistently during sleep (normal: 12–18)
5. **3+ weeks of red recovery** despite adequate sleep and reduced training
6. **Sudden persistent elevation in RHR (+10 bpm)** with no training explanation — cardiac screening warranted
7. **Skin temp deviation >3°C** sustained — high fever, seek evaluation

---

## Using WHOOP Data Effectively

### Do
- Track 4–6 week trends, not day-to-day numbers
- Correlate metrics with lifestyle events (alcohol, stress, travel, illness)
- Use green days strategically for peak performance demands
- Build a personal baseline awareness — know *your* normal ranges

### Don't
- Chase high strain scores for their own sake
- Override red recovery for non-essential hard training
- Compare your HRV to others' — it's not a competition metric
- Rely solely on WHOOP for medical decisions

### The Baseline Window
WHOOP uses a rolling 90-day window to calculate your personal baselines. It takes ~30 days of consistent wear for meaningful personalization. Trust your trends after 60+ days of data.
