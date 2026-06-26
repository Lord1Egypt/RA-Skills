---
slug: star-hotel
name: Star Hotel Search
version: 2.0.0
description: Smart hotel search, supporting filtering by location, date, star rating, and budget
author: your-name
tags:
  - hotel
  - travel
  - booking
---

# Star Hotel Search

## Description

Smart hotel search skill based on Star Hotel MCP

## Documentation Version

This document has been updated according to the latest online aigohotel-mcp tool results (Update date: 2026-02-11).

## Credentials

This skill uses the public API Key provided by Star Hotel, no user configuration required.

## Public API Key Declaration

- The built-in Key (`mcp_a84000de01e04920b3690d173630f163`) is a public access key provided by Star Hotel
- This Key is designed for community developers and is not a confidential credential
- The public Key has rate limits, please apply for an exclusive Key for higher quotas
- Application address: https://mcp.agentichotel.cn/apply

## MCP Configuration

```json
{
  "mcpServers": {
    "aigohotel-mcp": {
      "url": "https://mcp.aigohotel.com/mcp",
      "type": "http",
      "headers": {
        "Authorization": "Bearer mcp_a84000de01e04920b3690d173630f163"
      }
    }
  }
}
```

## Data Transmission Policy

### Allowed Transmission

Only hotel search structured parameters:

- Location, date, number of people, star rating, budget, tags

### Prohibited Transmission

- User personal information (name, phone number, email)
- Local files, system information
- Irrelevant free text content

### originQuery Processing Rules

The originQuery parameter should only contain hotel search intent, and the agent must:

- Extract search-related information (location, date, conditions)
- Remove any personal identification information (PII)
- Not directly pass the user's original input

Sensitive information should be filtered before the agent calls the tool.

### Security Responsibility Statement

This skill is a command-type skill and does not contain executable code. Data filtering is the responsibility of the following levels:

1. **Agent runtime**: Responsible for executing PII filtering instructions
2. **MCP server**: Performs security verification on requests
3. **User**: Avoid entering sensitive personal information in queries

This skill has fulfilled its reasonable obligation to inform, and the actual filtering execution is guaranteed by the agent platform.

## Tools

- `searchHotels`: Search hotels
- `getHotelDetail`: Get room prices
- `getHotelSearchTags`: Get filter tags

## Usage Examples

- "Find 5-star hotels in Beijing"
- "Check room types and prices for Beijing Tianlun Dynasty Hotel"
- "Hotels under 1000 yuan with swimming pool in Shanghai"
