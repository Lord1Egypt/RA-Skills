---
description: Calendar Event Tracking Workflow - Track important market events from financial calendars
---

# Calendar Event Tracking Workflow

Track important market events from financial calendars, including earnings releases, dividend distributions, IPO listings, economic data releases, etc.

## Execution Steps

### Step 1: Determine Calendar Type

Determine the calendar type based on user needs:
- **economic**: Economic calendar (GDP, CPI, employment data, etc.)
- **earnings**: Earnings calendar (company earnings release dates)
- **revenue**: Dividend calendar (dividend distribution dates)
- **ipo**: IPO calendar (new stock listing dates)

### Step 2: Determine Time Range

Calculate the query time range (Unix timestamp):
- Default query: next 7-14 days
- User can specify specific date range
- Note: Time span cannot exceed 40 days

### Step 3: Determine Market Scope

Select market based on calendar type:
- Economic calendar: Supports multiple countries (america, china, japan, etc.)
- Earnings/Dividend/IPO: Default is america, can specify other markets

### Step 4: Call Calendar Tool

Call `tradingview_get_calendar` to retrieve calendar data:

```
Parameter description:
- type: Calendar type (required)
  - economic: Economic events
  - earnings: Earnings releases
  - revenue: Dividend distributions
  - ipo: New stock listings
- from: Start time (required, Unix timestamp)
- to: End time (required, Unix timestamp)
- market: Market code (optional, comma-separated)
```

### Step 5: Filter and Sort Events

Filter based on user focus:
- Sort by importance
- Filter by industry/sector
- Filter by specific securities

### Step 6: Generate Calendar Report

Output formatted calendar report:
- Event list (time, event name, expected value, actual value)
- Highlight important events
- Potential impact analysis
- Recommended securities to watch

## Example Conversations

**User**: "What important earnings are coming next week?"

**Execution**:
1. Calculate next week's time range (from/to timestamps)
2. Call `tradingview_get_calendar` with type="earnings"
3. Return earnings list, highlighting companies with high market attention
4. Suggest securities that may exceed expectations

---

**User**: "Check US economic data releases for the next two weeks"

**Execution**:
1. Calculate time range for next two weeks
2. Call `tradingview_get_calendar` with type="economic", market="america"
3. Return important data release times like CPI, non-farm payrolls, GDP, etc.
4. Analyze potential market impact of the data

---

**User**: "Check which new stocks are listing this month"

**Execution**:
1. Calculate time range for this month
2. Call `tradingview_get_calendar` with type="ipo"
3. Return new stock list including offering price, listing date, etc.
4. Analyze industry distribution of new stocks and IPO recommendations

---

**User**: "Are any of my holdings paying dividends soon?"

**Execution**:
1. Get user's stock holdings list
2. Call `tradingview_get_calendar` with type="revenue"
3. Filter dividend information for user's holdings
4. Return ex-dividend date, payment date, dividend amount, etc.
