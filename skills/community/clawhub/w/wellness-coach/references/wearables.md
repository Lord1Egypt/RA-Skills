# Wearable Integration Guide

## Current State
`backend/health_mock.py` returns mock data by default. Swap `get_health_data()` to use a real provider.

## Oura Ring
```python
import requests
def get_oura_health_data(api_token: str) -> dict:
    headers = {"Authorization": f"Bearer {api_token}"}
    sleep = requests.get("https://api.ouraring.com/v2/usercollection/daily_sleep", headers=headers).json()
    readiness = requests.get("https://api.ouraring.com/v2/usercollection/daily_readiness", headers=headers).json()
    # Map to standard format: sleep_score, hrv_ms, recovery_score etc.
```
Get token: https://cloud.ouraring.com/personal-access-tokens
Add to .env: `OURA_API_TOKEN=...`

## Fitbit
```python
def get_fitbit_health_data(access_token: str) -> dict:
    headers = {"Authorization": f"Bearer {access_token}"}
    sleep = requests.get("https://api.fitbit.com/1.2/user/-/sleep/date/today.json", headers=headers).json()
    hrv = requests.get("https://api.fitbit.com/1/user/-/hrv/date/today.json", headers=headers).json()
```
Get token: https://dev.fitbit.com (OAuth2 flow)

## Apple Health
No direct API. Options:
1. **Health Auto Export** app → exports JSON → parse in `health_mock.py`
2. **Terra API** (https://tryterra.co) — unified bridge for Apple Health, Garmin, Whoop, etc.
3. **HealthKit** via companion iOS app

## Standard Health Data Format
All providers should return this shape:
```python
{
    "date": "2026-04-11",
    "sleep_hours": 6.2,
    "sleep_score": 71,       # 0-100
    "hrv_ms": 42,            # milliseconds
    "hrv_7day_avg": 56,
    "resting_hr": 68,        # bpm
    "recovery_score": 65,    # 0-100
    "steps_yesterday": 4200,
    "source": "oura"         # or "fitbit", "apple", "mock"
}
```
