---
title: metrics_glossary.md
description: Definitions and units for Ultrahuman metric types.
created: 2026-03-16
updated: 2026-03-16
---

# Ultrahuman metrics – glossary

Short definitions and units for metrics returned by the Ultrahuman Partner API. Use this when the user asks what a metric means or which unit applies.

## Sleep

- **Sleep Score** – Overall sleep quality score (typically 0–10). Combines duration, efficiency, restfulness, and other factors.
- **Total Sleep** – Total time asleep (e.g. displayed as "7h 5m").
- **Sleep Efficiency** – Percentage of time in bed spent asleep (e.g. 93%).
- **Sleep stages** – Deep, Light, REM, Awake (percentages). From the ring’s sleep staging.

## Recovery and cardiovascular

- **Recovery Score** – Readiness/recovery score (e.g. 0–10). Often derived from overnight HR/HRV and sleep.
- **Recovery Index** – Numeric index (e.g. 0–100) indicating recovery state; higher often means better recovered.
- **Heart Rate (HR)** – Beats per minute (BPM). Can be daytime or overnight.
- **Resting HR (night_rhr)** – Resting heart rate during sleep (BPM). Lower can indicate better recovery.
- **HRV** – Heart rate variability (often in ms or a normalized unit). Higher HRV often indicates better recovery/adaptation; values and units depend on the device.

## Activity

- **Steps** – Step count for the day.
- **Movement Index** – Index of movement/activity (e.g. 0–100).
- **VO2 Max** – Estimated maximal oxygen uptake (e.g. ml/kg/min). From ring/activity data.

## Metabolic (CGM / glucose)

- **Metabolic Score** – Overall metabolic health score (e.g. 0–100).
- **Glucose** – Blood glucose readings (mg/dL). From CGM if linked.
- **Average Glucose** – Average glucose in mg/dL for the day.
- **Glucose Variability** – Variability of glucose (often %). Lower variability is often associated with more stable metabolism.
- **Time in Target** – Percentage of time glucose stayed within a target range (%).
- **HbA1c** – Estimated or measured glycated hemoglobin (%). Long-term glucose marker.

## Other

- **Skin Temperature (temp)** – From the ring (°C). Can reflect circadian and recovery state.
- **Motion** – Movement metric during sleep or day (device-specific scale).

All metrics are from Ultrahuman’s systems and are not a substitute for medical advice.
