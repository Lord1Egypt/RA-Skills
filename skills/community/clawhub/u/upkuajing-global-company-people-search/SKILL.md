---
name: upkuajing-global-company-people-search
description: Official skill for upkuajing (跨境魔方). Find companies (找公司) and global people (找人) data. Get business registration, background info, and contact details (Email, Phone, WhatsApp). Ideal for customer development, background checks, and talent search.
metadata: {"version":"1.0.6","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"🏢","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# UpKuaJing Company and People Search

Query corporate business information and people data using the UpKuaJing Open Platform API. This skill uses an **entity-driven approach**: finding target entities directly through company attributes (product, industry, size) and people attributes (position, school, experience).

## Overview

This skill provides access to UpKuaJing's global company database and people data through five scripts: two list searches (companies, people) and three enhancement interfaces (company details, people details, contact information).
API key generation and top-up are provided through the `auth.py` script.

## Running Scripts

### Environment Setup

1. **Check Python**: `python --version`
2. **Install dependencies**: `pip install -r requirements.txt`

Script directory: `scripts/*.py`
Run example: `python scripts/*.py`

**Important**: Always use direct script invocation like `python scripts/company_list_search.py`. **Do NOT use** shell compound commands like `cd scripts && python company_list_search.py`.

### Two Search Methods

**Company List Search** (`company_list_search.py`)
- **Return granularity**: Each company as one record
- **Use cases**: Focus on "which companies exist"
- **Examples**:
   - "Find manufacturers producing LED lights"
   - "Find tech companies with 100-500 employees"
- **Parameters**: See [Company List](references/company-list-api.md)

**People List Search** (`human_list_search.py`)
- **Return granularity**: Each person as one record
- **Use cases**: Focus on "which people exist"
- **Examples**:
  - "Find CTOs at XXXX"
  - "Find Sales Directors in China for XXX"
- **Parameters**: See [People List](references/human-list-api.md)

### Three Enhancement Interfaces

After obtaining company or people lists, use these interfaces to enrich information when necessary:

**Company Details** (`company_details.py --pids *`)
- Get company business registration information (excluding contact information)
- **Parameters**: `--pids` List of company IDs (space-separated, obtained from list search), max 20 at a time

**People Details** (`human_details.py --hids *`)
- Get detailed person information (education, work experience, etc.)
- **Parameters**: `--hids` List of people IDs (space-separated, obtained from list search), max 20 at a time

**Contact Information** (`get_contact.py --bus_type * --bus_ids *`)
- Get contact information (email, phone, WhatsApp, social media, website)
- **Parameters**:
  - `--bus_type`: 1=company, 2=person
  - `--bus_ids`: List of company IDs or people IDs (space-separated, obtained from list search), max 20 at a time

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

Choose the appropriate API based on user intent.

### Decision Guide

| User Intent | Use API |
|-------------|---------|
| "Find companies producing XXX" | Company list |
| "Find companies with email/phone" | Company list existEmail=1/existPhone=1 |
| "Find CEO/CTO of XX company" | People list |
| "Find customers purchasing XXX" | Company list |
| "Get person resume" | People details |
| "Get company contact information" | Contact information bus_type=1 |

## Usage Examples

### Scenario 1: Small Query — Search Companies

**User request**: "Find Chinese manufacturers producing LED lights"
```bash
python scripts/company_list_search.py \
  --params '{"products": ["LED lights"], "countryCodes": ["CN"], "existEmail": 1}' \
  --query_count 20
```

### Scenario 2: Search People

**User request**: "Find CTOs at XXXX"
```bash
python scripts/human_list_search.py \
  --params '{"companyNames": ["XXXX"], "titleRoles": ["CTO"]}' \
  --query_count 20
```

### Scenario 3: Large Query — Multiple Script Calls Required

**User request**: "Find 1000 US electronics importers with email addresses"
**Before execution** inform user: ceil(1000/20) = 50 API calls, confirm before executing.
```bash
python scripts/company_list_search.py --params '{"products": ["electronics"], "countryCodes": ["US"], "existEmail": 1}' --query_count 1000
```
**After execution**: Script responds {"task_id":"a1b2-c3d4", "file_url": "xxxxx", ……}
**Continue execution, append data**: Specify task_id, script continues query from last cursor and appends to file
```bash
python scripts/company_list_search.py --task_id 'task-id-here' --query_count 2000
```

## Error Handling

- **API key invalid/non-existent**: Check `UPKUAJING_API_KEY` in `~/.upkuajing/.env` file
- **Insufficient balance**: Guide user to top up
- **Invalid parameters**: **Must first check the corresponding API documentation in references/ directory**, get correct parameter names and formats from documentation, do not guess

## Best Practices

### Choosing the Right Method

1. **Understand user intent**:
   - Find companies? → Use **company list search**
   - Find people? → Use **people list search**

2. **Check API documentation**:
   - **Before executing list queries, must first check the corresponding API reference documentation**
   - Company list: Check [references/company-list-api.md](references/company-list-api.md)
   - People list: Check [references/human-list-api.md](references/human-list-api.md)
   - Do not guess parameter names, get accurate parameter names and formats from documentation

3. **Optimize query parameters**:
   - Use `products` parameter for precise product filtering, translate to English
   - Use `existEmail=1` or `existPhone=1` to filter entities with contact information
   - Use `countryCodes` to limit country scope

### Handling Results

3. **Handle jsonl files carefully**: For large data queries, pay attention to file size
4. **Gradually enrich information**: Only call details/contact interfaces when needed
   - Company IDs returned by both list interfaces can be used for both detail interfaces
   - If user only needs a few companies, don't get details for all companies

## Notes
- Use hids for people search, pids for company search, be careful to distinguish
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

- upkuajing-customs-trade-company-search — Search customs trade companies
- upkuajing-email-tool — Send emails and manage email tasks
- upkuajing-map-merchants-search — Map-based merchant search
- upkuajing-sms-tool — Send SMS and manage SMS tasks
- upkuajing-contact-info-validity-check — Check contact info validity
