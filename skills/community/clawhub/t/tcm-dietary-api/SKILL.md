---
name: tcm-dietary
description: TCM dietary therapy & syndrome differentiation. Pattern diagnosis, ingredient properties, food therapy plans, and tea recipes via HTTPS API. Free tier: 10 calls/day, no registration. All queries are transmitted to api.tcmplate.com for processing — this is a remote API client, not a local knowledge base. Reference only, not medical advice.
version: 1.0.1
author: 饭去病 (Fan Qu Bing)
license: MIT-0
tags: [tcm, chinese-medicine, dietary-therapy, syndrome-differentiation, wellness, tea, herbs, constitution]
---

# tcm-dietary

**Remote API client, not a local knowledge base.** All queries are sent via HTTPS to the `api.tcmplate.com` cloud diagnosis engine for processing. Free tier: 10 calls/day, no registration required.

> [中文文档 / Chinese docs](SKILL.zh.md)

---

## 🔒 Privacy & Data Handling

**This Skill transmits your queries (symptoms, constitution types, disease names, ingredient keywords) over HTTPS to api.tcmplate.com for cloud processing. Review this table before use.**

| Item | Detail |
|------|--------|
| Transport | HTTPS encrypted (TLS 1.2+) |
| Data sent | **Only symptom descriptions, constitution types, disease terms, and ingredient names.** A field whitelist at the code level automatically filters out accidentally included personal information (names, ID numbers, addresses, phone numbers, etc.) — these are stripped client-side and never reach the server |
| Data storage | Query content (symptoms, keywords) is processed in-memory and **not persisted to disk**. No query database exists |
| Server logs | IP address and timestamp retained in access logs for **14 days** (rate limiting + abuse prevention). Query content is **never written to logs** |
| Data use | Solely for generating dietary therapy suggestions in the current request. **Not used for model training, analytics, profiling, or any secondary purpose** |
| Third-party sharing | **None.** Query data is never shared, sold, or disclosed to any third party |
| Data deletion | Since query content is not persisted, there is no stored data to delete. Access log entries (IP + timestamp only) auto-expire after 14 days |
| Payments | Paid subscriptions are handled independently by PayPal. The API never receives or stores payment card information |
| Consent | By using this Skill, you confirm you have read this table and consent to your queries being transmitted via HTTPS to api.tcmplate.com for real-time processing. **Do not include names, ID numbers, addresses, or phone numbers in your queries** |

📧 Privacy inquiries / data access requests: privacy@tcmplate.com
📄 Full privacy policy: https://tcmplate.com/privacy

---

## ⚡ Zero-Step Start (Free — 10 calls/day, no API key)

> ⚠️ **Heads-up:** Your query data (symptoms, diseases, constitution types) leaves your machine and is sent over HTTPS to api.tcmplate.com for cloud processing. Do not include personal identifiers. Read the [Privacy & Data Handling](#-privacy--data-handling) section above.

```bash
# Syndrome diagnosis — symptoms sent via HTTPS to api.tcmplate.com
# ⚠️ Do not include names, ID numbers, or addresses in symptoms
curl -X POST https://api.tcmplate.com/api/diagnose \
  -H "Content-Type: application/json" \
  -d '{"symptoms":["dry mouth","insomnia","irritability"]}'

# Knowledge search — keywords sent via HTTPS to api.tcmplate.com
curl -X POST https://api.tcmplate.com/api/search \
  -H "Content-Type: application/json" \
  -d '{"category":"ingredients","keywords":["ginger"]}'
```

Rate limit: 10 calls/day per IP. Exceeded? Returns HTTP 429.

---

## Python Client

```python
# No installation — just copy the core/ directory into your project
# All calls transmit queries via HTTPS to api.tcmplate.com
import sys; sys.path.insert(0, "path/to/tcm-dietary")
from core.diagnose import diagnose
from core.search import search

# Free: no API key needed
result = diagnose(["insomnia", "palpitations", "poor appetite"])
print(result["syndrome"]["pattern"])
print(result["recommended_foods"][:5])

# Paid: $5/month, unlimited
# core.set_api_key("tcm_xxxx")
```

This client sends every query you provide over HTTPS to `api.tcmplate.com`. Do not include personal identifiers in your queries.

---

## API Endpoints

| Endpoint | Free | Description |
|----------|:----:|-------------|
| `/api/diagnose` | ✅ | Symptoms → pattern diagnosis + food therapy plan |
| `/api/search` | ✅ | Full-text search across 9 knowledge bases |
| `/api/health` | ✅ | Health check |

### Pricing

| Plan | Quota | Price |
|------|-------|-------|
| Free | 10 calls/day | $0 |
| Paid | Unlimited | $5/month |

📖 Full docs: https://tcmplate.com/docs
🛒 Subscribe: https://api.tcmplate.com/subscribe

---

## 🆘 Support & Contact

**Paid subscribers — we respond within 24 hours:**

| Channel | Address |
|---|---|
| 📧 Email | **[support@tcmplate.com](mailto:support@tcmplate.com)** — fastest for billing, API key, and technical issues |
| 🌐 Web | **[tcmplate.com/support](https://tcmplate.com/support)** — contact form + FAQ |
| 🐛 Bug reports | Include your API key prefix (first 4 chars) + the error you saw |

### Quick Self-Help

| Problem | Likely Cause | Fix |
|---|---|---|
| `invalid_api_key` | Key not set or not yet activated | Call `core.set_api_key("tcm_xxxx")` before queries. New keys may take 5 min to activate |
| HTTP 429 | Free tier limit (10/day) | Upgrade at [api.tcmplate.com/subscribe](https://api.tcmplate.com/subscribe) |
| HTTP 500 / timeout | Temporary server issue | Check [api.tcmplate.com/health](https://api.tcmplate.com/health). If down, email us immediately |
| Skill not loading | OpenClaw version mismatch | `openclaw --version`; requires OpenClaw ≥0.16. Update: `openclaw update` |

---

## ⚠️ Disclaimer

**This Skill is an informational reference tool. It does not provide medical services.**

- All output is for learning and informational reference only. It does not constitute medical diagnosis, prescription, or treatment advice
- If you have health concerns, consult a licensed medical practitioner
- This Skill is a remote API client: the symptom descriptions you submit will be transmitted over the network to api.tcmplate.com for processing
- Do not include names, ID numbers, home addresses, or other personal identifiers in your queries
- By using this Skill, you confirm that you have read and agree to the Privacy & Data Handling terms above
