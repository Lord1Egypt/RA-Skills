---
name: Umy Hotel Search
description: An out-of-the-box hotel search skill powered by Umy MCP.
version: 1.0.0
author: Umy
---

# Umy Hotel Search

## Description
An out-of-the-box hotel search skill powered by Umy MCP.

## Credentials
This skill uses a public API key provided by Umy. No user configuration is required.

## Public API Key Declaration
- The built-in key (`umyf1a1e67eae96d612c0d5a09e2d9cdf4f`) is a public access key officially provided by Umy.
- This key is intended for community developers and is not a secret credential.
- The public key is rate-limited. For higher quota, apply for a dedicated key.
- Apply at: https://mcp.umy.com/apply

## MCP Configuration
```json
{
  "mcpServers": {
    "aigohotel-mcp": {
      "url": "https://mcp.umy.com/sse",
      "type": "http",
      "headers": {
        "X-API-Key": "umyf1a1e67eae96d612c0d5a09e2d9cdf4f"
      }
    }
  }
}
```
## Data Transmission Policy

### Allowed data
Only structured hotel search parameters:
- Location, dates, number of guests, star rating, budget

### Prohibited data
- Personal information (name, phone number, email)
- Local files, system information
- Unrelated free-form text

### `query` handling rules
The `query` parameter must contain only the hotel name. The agent must:
- Extract hotel-name-related information
- Remove any personally identifiable information (PII)
- Never forward the user's raw input directly

The agent must filter sensitive information before calling tools.

### Security responsibility statement
This skill is instruction-based and contains no executable code. Data filtering responsibilities:
1. **Agent runtime**: executes PII filtering instructions
2. **MCP server**: performs security validation on requests
3. **User**: avoid entering sensitive personal information in queries

This skill provides reasonable disclosure; actual filtering enforcement depends on the agent platform.

## Tools
- `search_hotel`: search hotels

## Usage Examples
- "Find 5-star hotels in Beijing"
- "Show room types and prices for Beijing Tianlun Dynasty Hotel"
- "Hotels in Shanghai under 1000 CNY"