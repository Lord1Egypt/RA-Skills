# Child Sleep Data Structure

## Data File
`data/child-sleep-tracker.json`

## Main Structure

### sleep_records (Sleep Records)

| Field | Type | Description |
|------|------|-------------|
| date | string | Sleep date |
| age | string | Age representation |
| age_months | integer | Age in months |

### night_sleep (Night Sleep)

| Field | Type | Description |
|------|------|-------------|
| bedtime | string | Bedtime (HH:MM format) |
| fall_asleep_time | string | Fall asleep time (HH:MM format) |
| wake_time | string | Wake time (HH:MM format) |
| total_sleep_hours | number | Total sleep duration (hours) |
| sleep_efficiency | string | Sleep efficiency: excellent/good/fair/poor |

### night_wakeups (Night Wake-up Records)

| Field | Type | Description |
|------|------|-------------|
| count | integer | Number of night wake-ups |
| durations_minutes | array | Duration of each wake-up (minutes) |
| reasons | array | List of wake-up reasons |
| intervention_required | boolean | Whether intervention required |

### day_sleep (Day Sleep/Naps)

| Field | Type | Description |
|------|------|-------------|
| naps | integer | Number of naps |
| nap_duration_hours | number | Single nap duration |
| total_nap_sleep | number | Total nap duration |

### total_sleep (Overall Sleep)

| Field | Type | Description |
|------|------|-------------|
| hours | number | Total sleep duration (including naps) |
| within_recommended | boolean | Within recommended range |
| recommended_range | string | Recommended range (e.g., "11-14") |

### sleep_quality (Sleep Quality)

| Value | Description |
|-------|-------------|
| excellent | Excellent |
| good | Good |
| fair | Fair |
| poor | Poor |

### sleep_schedule (Sleep Schedule)

| Field | Type | Description |
|------|------|-------------|
| target_bedtime | string | Target bedtime |
| target_wake_time | string | Target wake time |
| nap_time | string | Nap time |

### sleep_problems (Sleep Problems)

| Field | Type | Description |
|------|------|-------------|
| night_terrors | boolean | Night terrors |
| bedwetting | boolean | Bedwetting |
| sleep_walking | boolean | Sleepwalking |
| teeth_grinding | boolean | Teeth grinding |
| snoring | boolean | Snoring |
| mouth_breathing | boolean | Mouth breathing |

### statistics (Statistics)

| Field | Type | Description |
|------|------|-------------|
| total_records | integer | Total records |
| average_sleep_hours | number | Average sleep duration |
| average_bedtime | string | Average bedtime |
| average_wake_time | string | Average wake time |
| sleep_quality_distribution | object | Sleep quality distribution |

## Sleep Reference by Age

| Age | Recommended Total Sleep | Night Sleep | Day Sleep | Naps |
|-----|------------------------|-------------|-----------|------|
| 0-3 months | 14-17 hours | 8-10 hours | 6-7 hours | 3-4 times |
| 4-12 months | 12-16 hours | 9-12 hours | 3-4 hours | 2-3 times |
| 1-2 years | 11-14 hours | 10-12 hours | 1.5-3 hours | 1-2 times |
| 3-5 years | 10-13 hours | 10-12 hours | 0-2 hours | 0-1 times |
| 6-12 years | 9-12 hours | 9-12 hours | 0 | 0 times |
| 13-18 years | 8-10 hours | 8-10 hours | 0 | 0 times |
