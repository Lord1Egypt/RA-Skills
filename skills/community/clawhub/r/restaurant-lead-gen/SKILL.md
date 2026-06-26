---
name: restaurant-lead-gen
description: Automated restaurant lead generation and outreach for SMB sales. Use when you need to find restaurant leads, enrich business data (website, phone, address), send automated email/WhatsApp outreach, or manage a restaurant sales pipeline. Includes lead discovery, data enrichment, and multi-channel outreach workflows.
---

# Restaurant Lead Gen

Automated lead generation and outreach for restaurant sales.

## When to Use

- "Find restaurants in [city/region]"
- "Generate leads for restaurant clients"
- "Send outreach emails to restaurants"
- "Enrich restaurant data with website/phone"
- "Build a restaurant sales pipeline"

## Lead Discovery

### Search Methods

1. **Google Maps scraping** - Use SeleniumBase or browser automation
2. **Yelp directory** - Scrape local restaurant listings
3. **Direct Google search** - `restaurants in [location]`

### Data to Collect

| Field | Priority |
|-------|----------|
| Name | Required |
| Address | Required |
| Phone | High |
| Website | High |
| Cuisine type | Medium |
| Hours | Low |

## Outreach Templates

### Email (PAS Formula)

```
Subject: [Problem headline]

Hi [Name],

[Problem]: Many [restaurant type] owners struggle with [issue].

[Agitate]: Without solving this, you're losing [X] per [week/month].

[Solution]: We help restaurants like yours [benefit].

Best,
[Your name]
```

### WhatsApp

```
Hi [Name]! 👋

Saw your spot - love what you're doing at [Restaurant]!

Quick question: are you currently dealing with [pain point]?

Happy to chat if it makes sense. No pressure!
```

## Workflow

### Quick Lead Gen

1. Discover leads via search
2. Enrich with website/contact data
3. Add to outreach list
4. Send personalized outreach
5. Track responses

### Automation Script

```python
# Lead enrichment example
from selenium import webdriver

def enrich_restaurant(name, address):
    driver = webdriver.Chrome()
    search = f"{name} {address} restaurant website"
    # Extract from Google results
    return {"website": ..., "phone": ...}
```

## Regions to Target

- Dominican Republic
- Puerto Rico
- Peru
- Other Latin American markets

## Tools

- **SeleniumBase** - Web scraping
- **Browser automation** - Data enrichment
- **Email** - Outreach (SMTP or API)
- **WhatsApp Business API** - Direct messaging

## Output

Save leads to CSV:

```csv
name,address,phone,website,cuisine,status,notes
Restaurant Name,123 Main St,+1-555-1234,https://...,Italian,new,
```
