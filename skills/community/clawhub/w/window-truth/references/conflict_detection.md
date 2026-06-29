# Window Truth — Local vs Remote Conflict Detection

## The Core Insight

Your camera is at the window. The satellite is 400km away.

When the question is "is it raining at *my house*, right now?", local observation beats remote prediction 75% of the time.

## Signal Orthogonality

Three signals measured:
1. **Brightness** (RGB pixel luminance: 0.299R + 0.587G + 0.114B) — weak rain correlation (r=0.12)
2. **RMS** (audio root-mean-square from RTSP mic) — **only reliable rain signal**
3. **Cloud cover** (Open-Meteo forecast) — moderate correlation

Brightness and RMS are nearly orthogonal (r=-0.026). This means they measure different things. When they disagree, one of them is detecting something the other can't see — and that's exactly where conflicts happen.

## RMS Calibration

| Level | Calibrated RMS | Meaning |
|-------|---------------|---------|
| Silence | < 9 | Baseline quiet (night, empty room) |
| Ambient | 9-30 | Normal background (wind, distant traffic) |
| Activity | 30-80 | Local activity (rain on surfaces, conversation) |
| Loud | 80+ | Heavy rain, thunder, Max's bedtime |

Raw RTSP PCM S16LE 8kHz values ÷ 110 = calibrated RMS.

## Conflict Types

### RAIN_GONE (App says rain, window says no)
- App: precipitation_probability > 30%
- Window: brightness > 100/255 AND RMS < 15
- Win rate: 64% (7/11)
- Typical cause: rain passes 5km away, satellite sees it, but it never reaches your building

### HIDDEN_RAIN (App says clear, window hears rain)
- App: precipitation_probability < 5%
- Window: RMS > 30 (rain on surfaces detected)
- Win rate: 100% (5/5)
- Typical cause: local convective rain too small for satellite resolution

### THIN_CLOUD (App says overcast, window is bright)
- App: cloud_cover > 90%
- Window: brightness > 100/255
- Win rate: not yet measured
- Typical cause: thin cirrus clouds let light through, but satellite can't distinguish thin from thick

## Shenzhen Specifics

Shenzhen's "thin cloud problem": 99.2% of locally-cloudy periods have brightness > 100/255. High thin clouds (cirrus) are transparent to the eye but opaque to satellite cloud detection. This is the #1 source of window-app disagreement.

## IR Night Vision Contamination

IP cameras auto-switch to IR mode when dark. Symptoms:
- File size drops 3-6x
- Pixel variance drops 94%
- R-B color difference drops to ≈0 (normal night: R-B ≈ +5-7)

Detection: sub-stream KB < 20 (daytime) or < 15 (nighttime) = IR mode active.

IR mode data is marked but not deleted — brightness is unreliable but RMS remains valid.
