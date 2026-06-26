# ZhenCap Investment Analysis Assistant

**AI-powered investment analysis tools for startups and VCs**

Version 2.0.1

---

## Overview

ZhenCap MCP Skill provides cloud-powered investment analysis capabilities through the Model Context Protocol. It connects to the ZhenCap platform to deliver:

- Market size estimation (TAM/SAM/SOM)
- Competitor analysis and SWOT mapping
- Valuation modeling (Comparable Companies, DCF)
- Risk scoring across multiple dimensions

Perfect for startup founders preparing pitches and investors conducting due diligence.

---

## Quick Start

### Installation

```bash
clawhub install venture-capitalist
```

After installation, the tools are automatically available in your MCP-enabled AI assistant (Claude Desktop, Cline, OpenClaw, etc.).

### No Configuration Required (Free Tier)

You get 50 free API calls per month - just install and use. No API key needed.

---

## Authentication

### Free Tier (No API Key)

**50 calls per month** - No registration required

- API calls are anonymous
- Quota resets on the 1st of each month
- No configuration needed - just install and use
- Backend tracks usage by IP address and user-agent fingerprint

### Paid Tier (API Key Required)

**Unlimited calls** at 0.10-0.20 CNY per call

1. Register at [www.zhencap.com/register](https://www.zhencap.com/register)
2. Generate API key in dashboard
3. Set environment variable: `export ZHENCAP_API_KEY="your_key"`

**Configuration Options:**

Option A - Environment Variable:
```bash
export ZHENCAP_API_KEY="your_api_key_here"
```

Option B - MCP Client Config:
```json
{
  "mcpServers": {
    "venture-capitalist": {
      "command": "node",
      "args": ["/path/to/mcp-skill/index.js"],
      "env": {
        "ZHENCAP_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

---

## How Free Tier Works

**Without API Key:**
1. Install skill: `clawhub install venture-capitalist`
2. Use directly - no configuration needed
3. Backend tracks usage by:
   - IP address
   - User-Agent fingerprint
   - Rate limited to 50 calls/month
   - Resets monthly on the 1st

**Quota Exceeded Response:**
```json
{
  "success": false,
  "error": "Free quota exceeded",
  "message": "You've used all 50 free calls this month. Register at www.zhencap.com for unlimited access.",
  "quotaUsed": 50,
  "quotaLimit": 50,
  "resetDate": "2026-05-01T00:00:00Z"
}
```

**To get more quota:**
- Register: [www.zhencap.com/register](https://www.zhencap.com/register)
- Add balance: 100 CNY = ~500-1000 calls
- Generate API key
- Configure: `export ZHENCAP_API_KEY="your_key"`

---

## Tools

### 1. Estimate Market Size

**Tool Name:** `estimate_market_size`

Estimate market size (TAM/SAM/SOM) for a specific industry and geography.

**Parameters:**
- `industry` (required): Industry name (e.g., "AI healthcare", "E-commerce")
- `geography` (optional): Geographic scope (default: "China")
- `year` (optional): Target year (default: 2024)

**Example Usage:**
```
"What's the market size for AI healthcare in China?"
"Estimate the TAM for electric vehicles globally in 2025"
```

**Output:**
```json
{
  "success": true,
  "data": {
    "tam": 500000000000,
    "sam": 100000000000,
    "som": 5000000000,
    "growth_rate": 35.2,
    "trends": ["AI-powered diagnostics growing rapidly"],
    "sources": ["IDC", "Gartner", "McKinsey"]
  }
}
```

---

### 2. Analyze Competitors

**Tool Name:** `analyze_competitors`

Identify main competitors and generate SWOT analysis for competitive positioning.

**Parameters:**
- `company` (required): Company name
- `industry` (required): Industry sector

**Example Usage:**
```
"Analyze competitors for ByteDance in short video"
"Who are the main competitors for Tesla in the EV market?"
```

**Output:**
```json
{
  "success": true,
  "data": {
    "competitors": [
      {
        "name": "Competitor A",
        "market_share": 25,
        "funding": "Series C",
        "differentiation": "Strong in enterprise segment"
      }
    ],
    "swot": {
      "strengths": ["..."],
      "weaknesses": ["..."],
      "opportunities": ["..."],
      "threats": ["..."]
    },
    "market_position": "Top 3 in China"
  }
}
```

---

### 3. Estimate Valuation

**Tool Name:** `estimate_valuation`

Provide valuation range based on comparable companies and DCF models.

**Parameters:**
- `revenue` (required): Annual revenue (in 10,000 CNY)
- `growth_rate` (optional): Annual growth rate (%)
- `industry` (required): Industry sector
- `stage` (required): Funding stage ("seed", "angel", "a", "b", "c", "pre-ipo")

**Example Usage:**
```
"Value a Series A SaaS company with 5M revenue growing at 200%"
"What's the fair valuation for a B2B AI company at Series B?"
```

**Output:**
```json
{
  "success": true,
  "data": {
    "valuation_range": {
      "low": 200000000,
      "mid": 350000000,
      "high": 500000000
    },
    "method": "Comparable Companies",
    "comparable_multiples": {
      "revenue_multiple": "15-25x",
      "industry_avg": "20x"
    },
    "assumptions": ["..."]
  }
}
```

---

### 4. Score Risk

**Tool Name:** `score_risk`

Assess investment risk across market, team, technology, and financial dimensions.

**Parameters:**
- `company_data` (required): Object containing:
  - `name`: Company name
  - `industry`: Industry sector
  - `stage`: Funding stage
  - `team_size`: Number of employees

**Example Usage:**
```
"Assess the investment risk for an early-stage AI startup with 15 people"
"Score the risk for a pre-IPO fintech company"
```

**Output:**
```json
{
  "success": true,
  "data": {
    "overall_score": 65,
    "risk_level": "Medium",
    "dimensions": {
      "market_risk": 70,
      "team_risk": 60,
      "technology_risk": 55,
      "financial_risk": 75
    },
    "red_flags": ["Limited runway", "Single customer dependency"],
    "recommendations": ["Diversify customer base", "Secure bridge funding"]
  }
}
```

---

## Privacy & Security

### Data Collection & Retention

**What we collect:**
- API request parameters (industry, company name, geography, year, etc.)
- Request timestamps and response times
- Error logs (for debugging only, retained 30 days)
- Usage statistics (aggregated and anonymous, retained 1 year)
- IP addresses (for rate limiting only, not permanently stored)

**What we DON'T permanently store:**
- User identities (for free tier users)
- Business strategies or proprietary analysis results
- Personal information beyond API usage patterns

**Data Transmission:**
- All tools send query parameters to www.zhencap.com/api/v1
- Parameters include: industry names, company names, geography, revenue figures, growth rates
- This data is necessary to provide market intelligence and analysis
- Data is transmitted over HTTPS/TLS 1.3 encrypted connections

**Data Retention Policy:**
- Query parameters: 90 days (for service improvement)
- Usage statistics: 1 year (aggregated, anonymous)
- Error logs: 30 days (for debugging)
- API keys: Until user deletes account

### Security Measures

- **Encryption:** All API calls use HTTPS/TLS 1.3
- **Authentication:** JWT-based authentication for paid tier
- **Rate Limiting:** IP-based rate limiting for free tier
- **API Key Security:** Keys are hashed and encrypted in database
- **Access Control:** Role-based access control for internal systems

### Compliance

- GDPR compliant (EU data protection regulation)
- Data processing agreement available upon request
- SOC 2 Type II certification in progress (expected Q3 2026)
- Privacy-by-design architecture

### Your Rights

You have the right to:
- **Data Export:** Request a copy of your data (support@zhencap.com)
- **Data Deletion:** Request deletion of your data (support@zhencap.com)
- **Opt-Out:** Stop using the service at any time
- **Transparency:** Ask questions about data handling (privacy@zhencap.com)

### Contact

- **Privacy Questions:** privacy@zhencap.com
- **Security Issues:** security@zhencap.com
- **Full Privacy Policy:** [www.zhencap.com/privacy](https://www.zhencap.com/privacy)
- **Terms of Service:** [www.zhencap.com/terms](https://www.zhencap.com/terms)

---

## Pricing

| Tier | Quota | Price | Registration |
|------|-------|-------|--------------|
| **Free** | 50 calls/month | Free | Not required |
| **Paid** | Unlimited | 0.10-0.20 CNY/call | Required |

**Paid Tier Details:**
- Pay-per-call billing (charged monthly)
- Volume discounts available for >10,000 calls/month
- Enterprise plans with SLA available

**Get your API key:**
1. Register at [www.zhencap.com/register](https://www.zhencap.com/register)
2. Add balance to account (100 CNY minimum)
3. Generate API key in dashboard
4. Configure environment variable

---

## Troubleshooting

### Error: "Network connection failed"

**Cause:** Cannot reach ZhenCap API servers.

**Solution:**
- Check internet connection
- Verify firewall allows HTTPS to www.zhencap.com
- Check if www.zhencap.com is accessible: `curl https://www.zhencap.com/api/v1/health`
- Try again in a few minutes (may be temporary outage)

### Error: "API quota exceeded"

**Cause:** You've used all 50 free calls this month.

**Solution:**
- Wait until next month for quota reset (1st of the month)
- Register for a paid account at [www.zhencap.com](https://www.zhencap.com)
- Check current usage: Contact support@zhencap.com

### Error: "Invalid API key"

**Cause:** API key is incorrect, expired, or has insufficient balance.

**Solution:**
- Re-generate API key in dashboard
- Check for extra spaces in environment variable: `echo "$ZHENCAP_API_KEY"`
- Ensure API key is copied correctly (no line breaks)
- Verify account has sufficient balance

### Error: "Tool not found"

**Cause:** MCP client hasn't loaded the skill properly.

**Solution:**
- Restart your MCP client (Claude Desktop, etc.)
- Reinstall the skill: `clawhub install venture-capitalist`
- Check MCP server logs for errors

---

## Migration from v2.0.0 to v2.0.1

This is a security patch release. No breaking changes.

**What changed:**
- Fixed Authorization header bug (internal improvement)
- Removed analyze_bp tool (backend not ready yet)
- Enhanced privacy documentation

**Do I need to update?**
- Recommended for all users (security fix)
- No configuration changes required

**How to update:**
```bash
clawhub update venture-capitalist
```

---

## Support

- **Documentation:** [www.zhencap.com/docs](https://www.zhencap.com/docs)
- **Email Support:** support@zhencap.com
- **GitHub Issues:** [github.com/zhencap/mcp-skill/issues](https://github.com/zhencap/mcp-skill/issues)
- **Community Forum:** [forum.zhencap.com](https://forum.zhencap.com) (coming soon)
- **Discord:** [discord.gg/zhencap](https://discord.gg/zhencap) (coming soon)

**Response Times:**
- Free tier: Best effort (24-48 hours)
- Paid tier: Within 12 hours
- Enterprise: SLA-based (4-hour response)

---

## About ZhenCap

ZhenCap (真资本) is an AI-powered investment analysis platform serving startups and VCs in China. Our mission is to democratize access to institutional-grade investment analysis tools.

**Website:** [www.zhencap.com](https://www.zhencap.com)

**Platform Features:**
- Market intelligence dashboard
- Investment pipeline management
- LP reporting automation
- Deal flow analytics
- Founder directory
- Investor matching

---

## License

MIT License - See [LICENSE](./LICENSE) file for details.

---

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for version history and release notes.

---

Built with [Model Context Protocol](https://modelcontextprotocol.io) - Learn more about building MCP skills at [github.com/modelcontextprotocol](https://github.com/modelcontextprotocol)
