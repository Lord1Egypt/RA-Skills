# 🌐 WebsitePublisher.ai — OpenClaw Skill

> Build and publish complete websites through conversation. No WordPress. No hosting setup. No CMS.

[![ClawHub](https://img.shields.io/badge/ClawHub-websitepublisher-blue)](https://clawhub.ai/skills/websitepublisher)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## What This Skill Does

This skill gives your OpenClaw agent the ability to **build and publish real websites** using the [WebsitePublisher.ai](https://www.websitepublisher.ai) platform.

You describe what you want. Your agent builds it and publishes it to a live URL.

**Example:**
> "Build a portfolio website for my photography business. I want a homepage, a gallery, and a contact page."

Your agent will create all three pages with proper HTML, configure a contact form, and give you a live URL — in minutes.

---

## What You Can Build

- **Landing pages** — product launches, events, personal pages
- **Business websites** — services, about, contact
- **Portfolios** — galleries, work showcases
- **Product catalogues** — with dynamic data (MAPI)
- **Blog sites** — posts as dynamic entities
- **Microsites** — for campaigns, clients, or projects

---

## Installation

### 1. Get your credentials

Sign up at **https://www.websitepublisher.ai/dashboard**

After signing up, copy:
- Your **API token** (`wpa_...`)
- Your **Project ID** (numeric)

### 2. Add to your OpenClaw config

```json
{
  "skills": {
    "entries": {
      "websitepublisher": {
        "enabled": true,
        "env": {
          "WEBSITEPUBLISHER_TOKEN": "wpa_your_token_here",
          "WEBSITEPUBLISHER_PROJECT": "12345"
        }
      }
    }
  }
}
```

### 3. Install via ClawHub

```bash
clawhub install websitepublisher
```

Or manually place `SKILL.md` in:
```
~/.openclaw/skills/websitepublisher/SKILL.md
```

---

## API Coverage

This skill covers three API layers:

| Layer | What it does |
|-------|-------------|
| **PAPI** | Create/update pages and assets. Bulk operations. Versioning. |
| **MAPI** | Dynamic data — products, posts, team members, any entity. |
| **SAPI** | Contact forms with email notifications. |

---

## Supported AI Providers

WebsitePublisher.ai works with any LLM that OpenClaw supports:
- Anthropic Claude
- OpenAI GPT-4o
- Local models (Ollama, LM Studio)

---

## Pricing

Free tier available — no credit card required.

| Plan | Projects | Pages | Monthly |
|------|----------|-------|---------|
| Free | 1 | 10 | €0 |
| Starter | 5 | 50 | €9 |
| Pro | Unlimited | Unlimited | €29 |

Full pricing at: https://www.websitepublisher.ai/#pricing

---

## Links

- **Website:** https://www.websitepublisher.ai
- **Dashboard:** https://www.websitepublisher.ai/dashboard
- **API Docs:** https://www.websitepublisher.ai/docs
- **ClawHub:** https://clawhub.ai/skills/websitepublisher

---

## License

MIT — feel free to fork and adapt.

---

*Built by [M25](https://m25.nl) — Meppel, Netherlands*
