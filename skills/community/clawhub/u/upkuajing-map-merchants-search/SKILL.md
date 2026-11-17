---
name: upkuajing-map-merchants-search
description: "Pull bulk Google Maps business data with radius‑based filters. Gather merchant contact information, analyze market density and find distributors or overseas buyers for offline business expansion.\n\nTrigger: Google maps business scraper, bulk merchant data download, radius‑based lead search, distributor sourcing, competitor store analysis, regional market research, offline sales‑lead generation"
metadata: {"version":"1.0.6","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"📍","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# UpKuaJing Map Merchants Search

Query merchant information using the UpKuaJing Open Platform API. This skill provides map-based merchant search with two search modes: region search and nearby search.

## Overview

This skill provides access to UpKuaJing's map merchant database through:
- **Merchants Search** (`merchants_search.py`): Search merchants by keywords and location
- **Geography List** (`geography_list.py`): Get country/province/city lists for location parameters

## Running Scripts

### Environment Setup

1. **Check Python**: `python --version`
2. **Install dependencies**: `pip install -r requirements.txt`

Script directory: `scripts/*.py`
Run example: `python scripts/*.py`

**Important**: Always use direct script invocation like `python scripts/merchants_search.py`. **Do NOT use** shell compound commands like `cd scripts && python merchants_search.py`.

## Two Main APIs

### Merchant Search (`merchants_search.py`)

Search merchants by keywords and geographic area.

**Parameters**: See [Merchants Search API](references/merchants-search-api.md)

**Two Search Modes**:
- **Country Search**: Search by country/province/city, keywords, and filters
- **Nearby Search**: Search by latitude/longitude and radius using `geoDistance`

**Examples**:
```bash
# Country search - Find restaurants in Brazil
python scripts/merchants_search.py \
  --params '{"keywords":["restaurant"],"countryCodes":["BR"]}' \
  --query_count 100

# Multi-country search with phone filter - Find restaurants in US or China with phone
python scripts/merchants_search.py \
  --params '{"keywords":["restaurant"],"countryCodes":["US","CN"],"existPhone":true}' \
  --query_count 50

# Industry filter - Find car dealers in Thailand
python scripts/merchants_search.py \
  --params '{"keywords":["car dealer"],"countryCodes":["TH"],"industries":["Cars"]}' \
  --query_count 100

# Nearby search - Find hotels within 5km of a point
python scripts/merchants_search.py \
  --params '{"keywords":["hotel"],"geoDistance":{"location":{"lat":31.1104643,"lon":29.7602221},"distance":"5km"}}'

# Province and city filter - Find restaurants in a specific province/city
python scripts/merchants_search.py \
  --params '{"keywords":["restaurant"],"provinceIds":["2277"],"cityIds":["19975"]}' \
  --query_count 50

# Shop name filter - Find shops by specific name
python scripts/merchants_search.py \
  --params '{"companyNames":["car care"],"countryCodes":["TH"]}' \
  --query_count 100

# Multi-filter search - Combine multiple filters
python scripts/merchants_search.py \
  --params '{"keywords":["restaurant"],"countryCodes":["US"],"provinceIds":["1447"],"industries":["Cars"],"existPhone":true}' \
  --query_count 50
```

**Task Resume**: Use `--task_id` to resume interrupted large queries:
```bash
python scripts/merchants_search.py --task_id 'your-task-id-here' --query_count 2000
```

### Geography List (`geography_list.py`)

Get geographic hierarchy data for building search parameters.

**Examples**:
```bash
# Get country list
python scripts/geography_list.py --type country

# Get province list for a country
python scripts/geography_list.py --type province --country_id 1

# Get city list for a country
python scripts/geography_list.py --type city --country_id 1
```

## API Key and UpKuaJing Account

- **API Key**: Stored in `~/.upkuajing/.env` file as `UPKUAJING_API_KEY`
- **First check**: If not set, prompt user to provide or apply at [UpKuaJing Open Platform](https://developer.upkuajing.com/)

### **API Key Not Set**
First check if the `~/.upkuajing/.env` file has UPKUAJING_API_KEY;
If UPKUAJING_API_KEY is not set, prompt the user to choose:
1. User has one: User provides it (manually add to ~/.upkuajing/.env file)
2. User doesn't have one: Guide user to apply at [UpKuaJing Open Platform](https://developer.upkuajing.com/)
Wait for user selection;

### **Account Top-up**
When API response indicates insufficient balance, explain and guide user to top up:
1. Create top-up order (`auth.py --new_rec_order`)
2. Based on order response, send payment page URL to user, guide user to open URL and pay, user confirms after successful payment;

### **Get Account Information**
Use this script to get account information for UPKUAJING_API_KEY: `auth.py --account_info`

## API Key and UpKuaJing Account

- Newly applied API key: Register and login at [UpKuaJing Open Platform](https://developer.upkuajing.com/), then bind account

### **Report Skill Call Errors**
When an API call fails or returns abnormal data (server error, timeout, malformed response, etc.), explain the anomaly to the user in natural language and ask whether to report it to the platform for troubleshooting. Only run the report after user confirmation:
```bash
python scripts/error_report.py --params '{"requestPath":"/agent/map/search","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"Merchant search failed with a server error"}'
```
- Do not report normal business conditions (insufficient balance, invalid API key, parameter errors) — handle them via their own flows
- Error reporting does not incur query fees
- **Parameters**: See [Error Report API](references/skill-error-report-api.md)

## Fees

**Merchant search API calls incur fees**, different interfaces have different billing methods.
**Latest pricing**: Users can visit [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html)
Or use: `python scripts/auth.py --price_info` (returns complete pricing for all interfaces)

### Merchant Search Billing Rules

Billed by **number of calls**, each call returns up to 100 records:
- Number of calls: `ceil(query_count / 100)` times
- **Whenever query_count > 100, must before execution:**
  1. Inform user of expected number of calls
  2. Stop, wait for explicit user confirmation in a separate message, then execute script

### Geography List Billing Rules

**Free of charge** — No fees for country/province/city list queries.

### Fee Confirmation Principle

**Any operation that incurs fees must first inform and wait for explicit user confirmation. Do not execute in the same message as the notification.**

## Workflow

### Decision Guide

| User Intent | Use API |
|-------------|---------|
| "Find merchants by country/region" | Merchants Search (countryCodes) |
| "Find merchants by province/city" | Merchants Search (provinceIds, cityIds) |
| "Find merchants near a location" | Merchants Search (geoDistance) |
| "Filter by industry or contact info" | Merchants Search (industries, existPhone, existWebsite) |
| "Find shops by name" | Merchants Search (companyNames) |
| "Get country/province/city data" | Geography List |

### Search Flow

1. **For region search**: Use Geography List to get country/province/city IDs first
2. **Build search parameters**: Combine keywords with geographic filters
3. **Execute search**: Use merchants_search.py with appropriate parameters
4. **Handle large queries**: Use task_id to resume interrupted searches

## Error Handling

- **API key invalid/non-existent**: Check `UPKUAJING_API_KEY` in `~/.upkuajing/.env` file
- **Insufficient balance**: Guide user to top up
- **Invalid parameters**: **Must first check the corresponding API documentation in references/ directory**, get correct parameter names and formats from documentation, do not guess
- **Skill call errors / abnormal responses**: Explain to the user and, with user confirmation, report to the platform via `python scripts/error_report.py` (see [Report Skill Call Errors](#report-skill-call-errors))

### API Documentation Reference

- Error Report: Check [references/skill-error-report-api.md](references/skill-error-report-api.md)

## Best Practices

### Choosing the Right Search Mode

1. **Understand user intent**:
   - Find merchants by country/region? → Use **Country Search (countryCodes)**
   - Find merchants by province/city? → Use **provinceIds, cityIds**
   - Find merchants near a location? → Use **Nearby Search (geoDistance)**
   - Filter by industry or contact availability? → Use **industries, existPhone, existWebsite**
   - Find shops by name? → Use **companyNames**

2. **Check API documentation**:
   - **Before executing searches, must first check the corresponding API reference documentation**
   - Merchant search: Check [references/merchants-search-api.md](references/merchants-search-api.md)
   - Geography list: Check corresponding files in references/ directory
   - Do not guess parameter names, get accurate parameter names and formats from documentation

### Location-Based Search

1. **Country search for regional coverage**: Use `countryCodes` with keywords
2. **Nearby search for precise location**: Use `geoDistance` with location and distance

### Parameter Guidelines

- **Keywords**: Use English terms for better results
- **Filters**: Use `existPhone=true` or `existWebsite=true` to filter by contact availability
- **Industry filter**: Use `industries` to filter by business type
- **Province/City filter**: Use `provinceIds` and `cityIds` to filter by specific province or city
- **Shop name filter**: Use `companyNames` to find shops by specific name
- **Nearby search**: distance format like "5km", recommended range 1-10km
- **Search quantity affects API response time**, set reasonable query_count for large queries

### Handling Results

1. **Be mindful of file size for large queries**: jsonl files can grow large
2. **Use task_id to resume interrupted queries**: avoid redundant API calls and fees

## Notes

- Country codes use ISO 3166-1 alpha-2 format (e.g., CN, US, BR)
- File paths use forward slashes on all platforms
- **Do not** guess parameter names, get accurate parameter names and formats from documentation
- **Prohibit outputting technical parameter format**: Do not display code-style parameters in responses, convert to natural language
- **Do not estimate or guess per-call fees** — use `python scripts/auth.py --price_info` to get accurate pricing information

## Related Skills

Other UpKuaJing skills you might find useful:

- linkedin-person-search — Search people from the LinkedIn source
- global-company-person-search — Search people from the global company database
- linkedin-company-search — Search companies from the LinkedIn source
- global-company-search — Search companies from the global company database
- global-company-shareholder — Query shareholder list from the global company database
- global-company-employee — Query employee list from the global company database
- global-company-person-colleague — Query colleague list from the global company database
- global-company-person-alumni — Query alumni list from the global company database
- global-company-person-experience — Query work experience list from the global company database
- global-company-person-education — Query education history list from the global company database
- global-company-person-school-detail — Query school detail from the global company database
- upkuajing-global-company-people-search — Global company and people search
- upkuajing-customs-trade-company-search — Search customs trade companies
- upkuajing-email-tool — Send emails and manage email tasks
- upkuajing-sms-tool — Send SMS and manage SMS tasks
- upkuajing-contact-info-validity-check — Check contact info validity
- phone-validity-check — Check phone number validity
- email-validity-check — Check email address validity
- domain-validity-check — Check domain validity and security