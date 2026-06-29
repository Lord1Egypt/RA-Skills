# ClaWHub — EnsembleData Social Media Scraping Skill

## Overview

ClaWHub wraps the **EnsembleData Social Media Scraping API** (https://ensembledata.com), a real-time data provider active since 2020. It covers **8 platforms** via a simple REST API that returns JSON. All requests are GET and require a `token` query parameter.

**Base URL:** `https://ensembledata.com/apis`

**Authentication:** Every request must include `?token=YOUR_TOKEN`. Tokens are 12–24 characters long and are assigned on signup.

**Pricing unit:** Requests are metered in *units*. Simple calls cost 1 unit; complex or bulk calls cost more. The exact cost per endpoint is documented in each platform file. Failed requests due to internal errors are not charged.

**Rate limits:** None enforced. The platform auto-scales.

**Free trial:** https://dashboard.ensembledata.com/register

**Postman collection:** https://elements.getpostman.com/view/fork?collection=33901342-37bb76fa-5bc5-4342-94b5-3a6f884daabd

---

## Supported Platforms

| Platform  | File            | Endpoint prefix |
|-----------|-----------------|-----------------|
| TikTok    | tiktok.md       | `/tt/`          |
| Instagram | instagram.md    | `/instagram/`   |
| YouTube   | youtube.md      | `/youtube/`     |
| Reddit    | reddit.md       | `/reddit/`      |
| Twitter   | twitter.md      | `/twitter/`     |
| Twitch    | twitch.md       | `/twitch/`      |
| Snapchat  | snapchat.md     | `/snapchat/`    |
| Threads   | threads.md      | `/threads/`     |

---

## Common Error Codes

| Code | Meaning                  |
|------|--------------------------|
| 422  | Validation error (bad params) |
| 491  | Token not found          |
| 492  | Email not verified       |
| 493  | Subscription expired     |
| 495  | Daily unit limit reached |
| 500  | Internal server error    |

---

## Account / Usage APIs

These endpoints are free (0 units) and useful for monitoring consumption.

### GET /customer/get-used-units

Returns total units used on a given date, broken down by platform.

**Params:**
- `date` (required) — Format `YYYY-MM-DD`
- `token` (required)

**Example:**
```python
import requests
res = requests.get("https://ensembledata.com/apis/customer/get-used-units", params={
    "date": "2024-01-15",
    "token": "YOUR-TOKEN"
})
print(res.json())
# {"data": {"tiktok": 2367, "instagram": 802, "reddit": 83, "youtube": 1209, "twitch": 232}}
```

### GET /customer/get-history

Returns daily unit usage for the last N days.

**Params:**
- `days` (required) — integer, e.g. `10`
- `token` (required)

---

## SDK Quick Start

**Python:**
```bash
pip install ensembledata
```
```python
from ensembledata.api import EDClient
client = EDClient("YOUR-TOKEN")
result = client.tiktok.user_info_from_username(username="daviddobrik")
print(result.data)
print("Units charged:", result.units_charged)
```

**Node.js:**
```bash
npm install ensembledata
```

**Async Python:**
```python
from ensembledata.api import EDAsyncClient
import asyncio

async def main():
    client = EDAsyncClient("YOUR-TOKEN")
    result = await client.tiktok.user_info_from_username(username="daviddobrik")

asyncio.run(main())
```

---

## Pagination Pattern

Most list endpoints use a cursor-based pagination:

- Each response contains a `nextCursor` field.
- Pass `nextCursor` value as the `cursor` parameter on the next call.
- When `nextCursor` is absent, there are no more pages.

---

## Compliance

EnsembleData only scrapes **publicly available data** without fake accounts. GDPR-compliant. Does not collect private or sensitive information.

---

## See Also

- [Pricing](https://ensembledata.com/pricing)
- [Official Docs](https://ensembledata.com/apis/docs)
- [Python SDK on GitHub](https://github.com/EnsembleData/ensembledata-python)
- [Node.js SDK on GitHub](https://github.com/EnsembleData/ensembledata-node)
