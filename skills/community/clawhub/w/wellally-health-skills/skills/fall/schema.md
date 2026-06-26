# FallRiskAssessment Schema

Complete data structure definition for fall risk assessment.

## Field Quick Reference

### Core Fields

| Field | Type | Description |
|-----|------|-------------|
| `fall_history` | array | Fall history records |
| `balance_tests` | object | Balance function tests |
| `gait_analysis` | array | Gait analysis records |
| `home_safety` | object | Home environment safety assessment |
| `risk_factors` | object | Risk factors |
| `overall_risk` | enum | Overall risk level |
| `interventions` | array | Intervention recommendations |

## fall_history Array Item

| Field | Type | Description |
|-----|------|-------------|
| `id` | string | Record ID |
| `date` | string | Fall date |
| `time` | string | Fall time |
| `location` | enum | Location: bathroom/bedroom/living_room/kitchen/stairs/other |
| `cause` | enum | Cause: slippery_floor/trip/loss_balance/dizziness/weak, etc. |
| `injury_level` | enum | Injury: none/bruise/cut/fracture/head_injury/other |
| `required_medical_attention` | boolean | Whether medical attention needed |

## balance_tests Object

### tug_test (Timed Up and Go Test)
| Field | Type | Description |
|-----|------|-------------|
| `time_seconds` | number | Test time (seconds) |
| `interpretation` | string | Result interpretation |
| `fall_risk` | enum | Fall risk level |

### berg_balance_scale (Berg Balance Scale)
| Field | Type | Description |
|-----|------|-------------|
| `score` | integer | Score (0-56) |
| `interpretation` | string | Result interpretation |

### single_leg_stance (Single Leg Stance)
| Field | Type | Description |
|-----|------|-------------|
| `eyes_open_seconds` | number | Eyes open time |
| `eyes_closed_seconds` | number | Eyes closed time |

## gait_analysis Array Item

| Field | Type | Description |
|-----|------|-------------|
| `speed_m_per_s` | number | Walking speed (m/second) |
| `abnormalities` | array | Abnormality types |
| `interpretation` | string | Result interpretation |

## home_safety Object

### Room Assessment Items

| Room | Assessment Items |
|------|------------------|
| living_room | floor_slippery, adequate_lighting, obstacles_removed, rugs_secure |
| bedroom | bedside_light, night_light, bed_height_appropriate, clutter_free |
| bathroom | non_slip_mat, grab_bars, shower_chair, easy_access |
| stairs | handrails, non_slip_treads, adequate_lighting, clutter_free |

## risk_factors Object

| Field | Description |
|-----|-------------|
| `age_over_75` | Age > 75 years |
| `previous_falls` | History of falls |
| `balance_problems` | Balance problems |
| `gait_abnormalities` | Gait abnormalities |
| `muscle_weakness` | Muscle weakness |
| `vision_problems` | Vision problems |
| `cognitive_impairment` | Cognitive impairment |
| `multiple_medications` | Multiple medications |
| `chronic_conditions` | Chronic conditions |
| `home_hazards` | Home environmental hazards |

## overall_risk Enum Values

- `low_risk`: 0-5 points
- `moderate_risk`: 6-12 points
- `high_risk`: 13-18 points

## Data Storage

- Location: `data/fall-risk-assessment.json`
