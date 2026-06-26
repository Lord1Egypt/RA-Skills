# Twelve Data LLM Reference
> Last synced: 2026-03-29 20:21:12 UTC

# Introduction

## Overview

Welcome to Twelve Data developer docs — your gateway to comprehensive financial market data through a powerful and easy-to-use API.
Twelve Data provides access to financial markets across over 50 global countries, covering more than 1 million public instruments, including stocks, forex, ETFs, mutual funds, commodities, and cryptocurrencies.

## Quickstart

To get started, you'll need to sign up for an API key. Once you have your API key, you can start making requests to the API.

### Step 1: Create Twelve Data account

Sign up on the Twelve Data website to create your account [here](https://twelvedata.com/register). This gives you access to the API dashboard and your API key.

### Step 2: Get your API key

After signing in, navigate to your [dashboard](https://twelvedata.com/account/api-keys) to find your unique API key. This key is required to authenticate all API and WebSocket requests.

### Step 3: Make your first request

Try a simple API call with cURL to fetch the latest price for Apple (AAPL):

```
curl "https://api.twelvedata.com/price?symbol=AAPL&apikey=your_api_key"
```

### Step 4: Make a request from Python or Javascript

Use our client libraries or standard HTTP clients to make API calls programmatically. Here’s an example in [Python](https://github.com/twelvedata/twelvedata-python) and JavaScript:

#### Python (using official Twelve Data SDK):

```python
from twelvedata import TDClient

# Initialize client with your API key
td = TDClient(apikey="your_api_key")

# Get latest price for Apple
price = td.price(symbol="AAPL").as_json()

print(price)
```

#### JavaScript (Node.js):

```javascript
const fetch = require('node-fetch');

fetch('https://api.twelvedata.com/price?symbol=AAPL&apikey=your_api_key')
  .then(response => response.json())
  .then(data => console.log(data));
```

### Step 5: Perform correlation analysis between Tesla and Microsoft prices

Fetch historical price data for Tesla (TSLA) and Microsoft (MSFT) and calculate the correlation of their closing prices:

```python
from twelvedata import TDClient
import pandas as pd

# Initialize client with your API key
td = TDClient(apikey="your_api_key")

# Fetch historical price data for Tesla
tsla_ts = td.time_series(
    symbol="TSLA",
    interval="1day",
    outputsize=100
).as_pandas()

# Fetch historical price data for Microsoft
msft_ts = td.time_series(
    symbol="MSFT",
    interval="1day",
    outputsize=100
).as_pandas()

# Align data on datetime index
combined = pd.concat(
    [tsla_ts['close'].astype(float), msft_ts['close'].astype(float)],
    axis=1,
    keys=["TSLA", "MSFT"]
).dropna()

# Calculate correlation
correlation = combined["TSLA"].corr(combined["MSFT"])
print(f"Correlation of closing prices between TSLA and MSFT: {correlation:.2f}")
```

### Authentication

Authenticate your requests using one of these methods:

#### Query parameter method
```
GET https://api.twelvedata.com/endpoint?symbol=AAPL&apikey=your_api_key
```

#### HTTP header method (recommended)
```
Authorization: apikey your_api_key
```

##### API key useful information
- Demo API key (`apikey=demo`) available for demo requests
- Personal API key required for full access
- Premium endpoints and data require higher-tier plans (testable with [trial symbols](https://twelvedata.com/exchanges))

### API endpoints

 Service | Base URL |
---------|----------|
 REST API | `https://api.twelvedata.com` |
 WebSocket | `wss://ws.twelvedata.com` |

### Parameter guidelines
- **Separator:** Use `&` to separate multiple parameters
- **Case sensitivity:** Parameter names are case-insensitive (`symbol=AAPL` = `symbol=aapl`)
- **Multiple values:** Separate with commas where supported

### Response handling

#### Default format
All responses return JSON format by default unless otherwise specified.

#### Null values
**Important:** Some response fields may contain `null` values when data is unavailable for specific metrics. This is expected behavior, not an error.

##### Best Practices:
- Always implement `null` value handling in your application
- Use defensive programming techniques for data processing
- Consider fallback values or error handling for critical metrics

#### Error handling
Structure your code to gracefully handle:
- Network timeouts
- Rate limiting responses
- Invalid parameter errors
- Data unavailability periods

##### Best practices
- **Rate limits:** Adhere to your plan’s rate limits to avoid throttling. Check your dashboard for details.
- **Error handling:** Implement retry logic for transient errors (e.g., `429 Too Many Requests`).
- **Caching:** Cache responses for frequently accessed data to reduce API calls and improve performance.
- **Secure storage:** Store your API key securely and never expose it in client-side code or public repositories.

## Errors

Twelve Data API employs a standardized error response format, delivering a JSON object with `code`, `message`, and `status` keys for clear and consistent error communication.

### Codes

Below is a table of possible error codes, their HTTP status, meanings, and resolution steps:

 Code | status | Meaning | Resolution |
 --- | --- | --- | --- |
 **400** | Bad Request | Invalid or incorrect parameter(s) provided. | Check the `message` in the response for details. Refer to the API Documenta­tion to correct the input. |
 **401** | Unauthor­ized | Invalid or incorrect API key. | Verify your API key is correct. Sign up for a key <a href="https://twelvedata.com/account/api-keys">here</a>. |
 **403** | Forbidden | API key lacks permissions for the requested resource (upgrade required). | Upgrade your plan <a href="https://twelvedata.com/pricing">here</a>. |
 **404** | Not Found | Requested data could not be found. | Adjust parameters to be less strict as they may be too restrictive. |
 **414** | Parameter Too Long | Input parameter array exceeds the allowed length. | Follow the `message` guidance to adjust the parameter length. |
 **429** | Too Many Requests | API request limit reached for your key. | Wait briefly or upgrade your plan <a href="https://twelvedata.com/pricing">here</a>. |
 **500** | Internal Server Error | Server-side issue occurred; retry later. | Contact support <a href="https://twelvedata.com/contact">here</a> for assistance. |

### Example error response

Consider the following invalid request:

```
https://api.twelvedata.com/time_series?symbol=AAPL&interval=0.99min&apikey=your_api_key
```

Due to the incorrect `interval` value, the API returns:

```json
{
  "code": 400,
  "message": "Invalid **interval** provided: 0.99min. Supported intervals: 1min, 5min, 15min, 30min, 45min, 1h, 2h, 4h, 8h, 1day, 1week, 1month",
  "status": "error"
}
```

Refer to the API Documentation for valid parameter values to resolve such errors.

## Libraries

Twelve Data provides a growing ecosystem of libraries and integrations to help you build faster and smarter in your preferred environment. Official libraries are actively maintained by the Twelve Data team, while selected community-built libraries offer additional flexibility.

A full list is available on our [GitHub profile](https://github.com/search?q=twelvedata).

### Official SDKs
- **Python:** [twelvedata-python](https://github.com/twelvedata/twelvedata-python)
- **R:** [twelvedata-r-sdk](https://github.com/twelvedata/twelvedata-r-sdk)

### AI integrations
- **Twelve Data MCP Server:** [Repository](https://github.com/twelvedata/mcp) — Model Context Protocol (MCP) server that provides seamless integration with AI assistants and language models, enabling direct access to Twelve Data's financial market data within conversational interfaces and AI workflows.

### Spreadsheet add-ons
- **Excel:** [Excel Add-in](https://twelvedata.com/excel)
- **Google Sheets:** [Google Sheets Add-on](https://twelvedata.com/google-sheets)

### Community libraries

The community has developed libraries in several popular languages. You can explore more community libraries on [GitHub](https://github.com/search?q=twelvedata).
- **C#:** [TwelveDataSharp](https://github.com/pseudomarkets/TwelveDataSharp)
- **JavaScript:** [twelvedata](https://github.com/evzaboun/twelvedata)
- **PHP:** [twelvedata](https://github.com/ingelby/twelvedata)
- **Go:** [twelvedata](https://github.com/soulgarden/twelvedata)
- **TypeScript:** [twelve-data-wrapper](https://github.com/Clyde-Goodall/twelve-data-wrapper)

### Other Twelve Data repositories
- **searchindex** *(Go)*: [Repository](https://github.com/twelvedata/searchindex) — In-memory search index by strings
- **ws-tools** *(Python)*: [Repository](https://github.com/twelvedata/ws-tools) — Utility tools for WebSocket stream handling

### API specification
- **OpenAPI / Swagger:** Access the [complete API specification](https://api.twelvedata.com/doc/swagger/openapi.json) in OpenAPI format. You can use this file to automatically generate client libraries in your preferred programming language, explore the API interactively via Swagger tools, or integrate Twelve Data seamlessly into your AI and LLM workflows.
