---
name: upkuajing-trade-company-search
description: Official skill for upkuajing (跨境魔方). Find companies (找公司) and global buyers using customs trade data. Get trade order details, business contact info, and lead generation tools for import/export market research and supply chain analysis.
metadata: {"version":"1.0.6","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"🏢","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# UpKuaJing Customs Trade Company Search

Search for companies through customs trade data using the UpKuaJing Open Platform API. This skill uses a **data-driven approach**: finding companies by analyzing trade records and transaction patterns.

## Overview

This skill provides access to UpKuaJing's customs trade data API through four scripts: two search methods (trade list, company list) and two enhancement interfaces (company details, contact information).
API key generation and top-up are provided through the `auth.py` script.

## Running Scripts

### Environment Setup

1. **Check Python**: `python --version`
2. **Install dependencies**: `pip install -r requirements.txt`

Script directory: `scripts/*.py`
Run example: `python scripts/*.py`

**Important**: Always use direct script invocation like `python scripts/trade_list_search.py`. **Do NOT use** shell compound commands like `cd scripts && python trade_list_search.py`.

### Two Search Methods

**Trade List Search** (`trade_list_search.py`)
- **Return granularity**: Each trade order as one record
- **Use cases**: Focus on "what transactions occurred"
- **Examples**:
   - "Show all orders where Company A purchased LED"
   - "Find soybean trade records imported/exported to US"
   - "View specific transaction details within a time period"
- **Parameters**: See [Trade List](references/trade-list-api.md)


**Company List Search** (`company_list_search.py`)
- **Return granularity**: Trade orders aggregated by company, each company as one row
- **Use cases**: Focus on "which companies exist"
- **Examples**:
  - "Find companies that purchased LED"
  - "Find US companies with electronics import/export business with China"
  - "Find companies with China-US trade" (logistics industry customer development)
- **Parameters**: See [Company List](references/company-list-api.md)


### Two Enhancement Features

After obtaining trade list or company list, use these interfaces to enrich company IDs in the results when necessary:
**Company Details** (`company_get_details.py --companyIds *`)
- Get company information (excluding contact information)
- **Parameters**: `--companyIds` List of company IDs (space-separated), max 20 at a time
- **API business parameters**: [Company Details](references/company-detail-api.md)

**Contact Information** (`company_get_contact.py --companyIds *`)
- Get contact details: email, phone, social media, website
- **Parameters**: `--companyIds` List of company IDs (space-separated), max 20 at a time
- **API business parameters**: [Get Contact Information](references/contact-fetch-api.md)

## API Key and Top-up

This skill requires an API key. The API key is stored in the `~/.upkuajing/.env` file:
```bash
cat ~/.upkuajing/.env
```
**Example file content**:
```
UPKUAJING_API_KEY=your_api_key_here
```
### **API Key Not Set**
First check if the `~/.upkuajing/.env` file has UPKUAJING_API_KEY;
If UPKUAJING_API_KEY is not set, prompt the user to choose:
1. User has one: User provides it (manually add to ~/.upkuajing/.env file)
2. User doesn't have one: You can apply using the interface (`auth.py --new_key`), the new key will be automatically saved to ~/.upkuajing/.env
Wait for user selection;

### **Account Top-up**
When API response indicates insufficient balance, explain and guide user to top up:
1. Create top-up order (`auth.py --new_rec_order`)
2. Based on order response, send payment page URL to user, guide user to open URL and pay, user confirms after successful payment;

### **Get Account Information**
Use this script to get account information for UPKUAJING_API_KEY: `auth.py --account_info`

## API Key and UpKuaJing Account
- Newly applied API key: Register and login at [UpKuaJing Open Platform](https://developer.upkuajing.com/), then bind account

## Fees

**All API calls incur fees**, different interfaces have different billing methods.
**Latest pricing**: Users can visit [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html)
Or use: `python scripts/auth.py --price_info` (returns complete pricing for all interfaces)

### List Search Billing Rules

Billed by **number of calls**, each call returns up to 20 records:
- Number of calls: `ceil(query_count / 20)` times
- **Whenever query_count > 20, must before execution:**
  1. Inform user of expected number of calls
  2. Stop, wait for explicit user confirmation in a separate message, then execute script

### Enhancement Interface Billing Rules

Billed by **number of IDs passed**, max 20 IDs per call:
- Pass 1 ID = billed 1 time
- Pass 20 IDs = billed 20 times (single call limit)
- **Before batch retrieval must:**
  1. Inform user of number of IDs passed and corresponding fee count
  2. Stop, wait for explicit user confirmation in a separate message, then execute script

### Fee Confirmation Principle

**Any operation that incurs fees must first inform and wait for explicit user confirmation. Do not execute in the same message as the notification.**


## Workflow

Choose the appropriate API based on user intent

### Decision Guide

| User Intent | Use API |
|-------------|---------|
| "Analyze trade patterns/order data" | Trade list |
| "Find companies purchasing XXX" | Company list |
| "Find suppliers for XXX with email" | Company list existEmail=1 |
| "Get company detailed information" | Company details |
| "Get contact information" | Contact information |

## Usage Examples

### Scenario 1: Small Query — Trade Data Analysis

**User request**: "Show 2024 LED lighting fixture trade data exported to US"
```bash
python scripts/trade_list_search.py \
  --params '{"products": ["LED lights"], "buyerCountryCodes": ["US"], "dateStart": 1704067200000, "dateEnd": 1735689599999}' \
  --query_count 20
```

To further get supplier details (supports batch queries):
```bash
python scripts/company_get_details.py --companyIds 123456 789012 ...
```

### Scenario 2: Large Query — Big Data Analysis

**User request**: "Analyze 100 soybean trade records from 2024"
**Before execution** inform user: ceil(100/20) = 5 API calls, confirm before executing;
```bash
python scripts/trade_list_search.py --params '{"products": ["soybean"], "dateStart": 1704067200000, "dateEnd": 1735689599999}' --query_count 100
```

### Scenario 3: Ultra Large Query - Multiple Script Calls Required

**User request**: "Find 2000 companies importing electronics from China, with email addresses"
**Before execution** inform user: ceil(2000/20) = 100 API calls, confirm before executing;
```bash
python scripts/company_list_search.py --params '{"companyType": 2, "sellerCountryCodes": ["CN"], "existEmail": 1}' --query_count 1000
```
**After execution**: Script responds {"task_id":"a1b2-c3d4", "file_url": "xxxxx", ……}
**Continue execution, append data**: Specify task_id, script continues query from last cursor and appends to file
```bash
python scripts/company_list_search.py --task_id 'a1b2-c3d4' --query_count 1000
```

## Error Handling

- **API key invalid/non-existent**: Check `UPKUAJING_API_KEY` in `~/.upkuajing/.env` file
- **Insufficient balance**: Guide user to top up according to **Account Top-up** steps
- **Invalid parameters**: **Must first check the corresponding API documentation in references/ directory**, check parameter names and formats, do not guess

## Best Practices

### Choosing the Right Method

1. **Understand user intent**:
   - Analyze trade data? → Use **trade list search**
   - Find customers/partners? → Use **company list search**

2. **Check API documentation**:
   - **Before executing list queries, must first check the corresponding API reference documentation**
   - Trade list: Check [references/trade-list-api.md](references/trade-list-api.md)
   - Company list: Check [references/company-list-api.md](references/company-list-api.md)

3. **Identify parameter conditions**:
   - Set date range
   - HS codes are usually more precise than product names for filtering
   - Reduce noise by filtering specific countries
   - Use ISO country codes: CN, US, JP, etc.
   - Use filters to find companies with contact information

### Handling Results

3. **Handle jsonl files carefully**: For large data queries, pay attention to file size

4. **Gradually enrich information**: Only call details/contact interfaces when needed
   - Company IDs returned by both list interfaces can be used for both detail interfaces
   - If user only needs a few companies, don't get details for all companies

## Notes
- All timestamps are in milliseconds
- Country codes use ISO 3166-1 alpha-2 format (e.g., CN, US, JP)
- File paths use forward slashes on all platforms
- Product names and industry names must be in **English**
- Search quantity affects API response time, recommend setting timeout:120
- **Prohibit outputting technical parameter format**: Do not display code-style parameters in responses, convert to natural language
- **Do not estimate or guess per-call fees** — use `python scripts/auth.py --price_info` to get accurate pricing information
- **Do not** guess parameter names, get accurate parameter names and formats from documentation

## Related Skills

Other UpKuaJing skills you might find useful:

- upkuajing-global-company-people-search — Global company and people search
- upkuajing-email-tool — Send emails and manage email tasks
- upkuajing-map-merchants-search — Map-based merchant search
- upkuajing-sms-tool — Send SMS and manage SMS tasks
- upkuajing-contact-info-validity-check — Check contact info validity
