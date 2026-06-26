# ZhenCap Investment Analysis Assistant

**AI-powered investment analysis tools for startups and VCs**

Version 2.0.1 - Security patch release fixing authorization header bug and enhancing privacy documentation.

---

## Quick Start

### Installation

```bash
clawhub install venture-capitalist
```

After installation, the tools are automatically available in your MCP-enabled AI assistant (Claude Desktop, Cline, OpenClaw, etc.).

### No Configuration Required

You get **50 free API calls per month** - just install and use. No API key needed.

---

## What's New in v2.0.1?

**Security Fixes:**
- Fixed Authorization header bug (no more "Bearer undefined")
- Enhanced privacy documentation transparency
- Clarified authentication model (optional API key)

**Changes:**
- Removed analyze_bp tool (backend not ready yet - coming Q2 2026)
- Updated privacy section with comprehensive data collection disclosure
- Added detailed free tier documentation

**See:** [CHANGELOG.md](./CHANGELOG.md) for full details.

---

## Authentication

### Free Tier (No API Key)

**50 calls per month** - No registration required

- Just install and use
- No configuration needed
- Quota resets monthly on the 1st
- Anonymous usage tracking by IP

### Paid Tier (API Key Required)

**Unlimited calls** at 0.10-0.20 CNY per call

1. Register at [www.zhencap.com/register](https://www.zhencap.com/register)
2. Generate API key in dashboard
3. Set environment variable:

```bash
export ZHENCAP_API_KEY="your_api_key_here"
```

Or configure in your MCP client:

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

## Tools

### 1. Estimate Market Size

```bash
claw "What's the market size for AI healthcare in China?"
```

**Output:**
- TAM (Total Addressable Market)
- SAM (Serviceable Addressable Market)
- SOM (Serviceable Obtainable Market)
- Growth rate and trends
- Data sources

---

### 2. Analyze Competitors

```bash
claw "Analyze competitors for ByteDance in the short video market"
```

**Output:**
- List of main competitors
- Market share distribution
- SWOT analysis
- Competitive positioning

---

### 3. Estimate Valuation

```bash
claw "Value a Series A SaaS company with 5M revenue growing at 200%"
```

**Output:**
- Valuation range (low/mid/high)
- Revenue multiples
- Industry benchmarks
- Key assumptions

---

### 4. Score Risk

```bash
claw "Score the investment risk for an early-stage AI startup with 15 people"
```

**Output:**
- Overall risk score (0-100)
- Risk level (Low/Medium/High)
- Dimension breakdown (market, team, technology, financial)
- Red flags and recommendations

---

## Privacy & Security

### What Data We Collect

**API Request Parameters:**
- Industry names (e.g., "AI healthcare")
- Company names (e.g., "ByteDance")
- Geographic regions (e.g., "China")
- Financial figures (revenue, growth rate)
- Query timestamps

**Usage Tracking:**
- API call counts (for quota enforcement)
- Error logs (30-day retention for debugging)
- Aggregated statistics (anonymous, 1-year retention)

### What We DON'T Permanently Store

- User identities (for free tier)
- Proprietary business strategies
- Full analysis results
- Personal information

### How Your Data is Used

- **Query parameters** are sent to www.zhencap.com/api/v1 to generate market intelligence
- **IP addresses** are used for rate limiting only (not stored permanently)
- **Error logs** help us debug and improve service quality
- **Statistics** help us understand usage patterns (anonymous)

### Security Measures

- **HTTPS/TLS 1.3** encryption for all API calls
- **JWT authentication** for paid tier
- **API key hashing** in database
- **GDPR compliant** data handling
- **SOC 2 Type II** certification in progress

### Your Rights

- **Data export:** support@zhencap.com
- **Data deletion:** support@zhencap.com
- **Privacy questions:** privacy@zhencap.com

**Full Privacy Policy:** [www.zhencap.com/privacy](https://www.zhencap.com/privacy)

**Terms of Service:** [www.zhencap.com/terms](https://www.zhencap.com/terms)

---

## Pricing

| Tier | Quota | Price | Registration |
|------|-------|-------|--------------|
| **Free** | 50 calls/month | Free | Not required |
| **Paid** | Unlimited | 0.10-0.20 CNY/call | Required |

Get your API key at [www.zhencap.com/register](https://www.zhencap.com/register)

---

## Migration from v2.0.0

This is a security patch release. No breaking changes.

**To update:**
```bash
clawhub update venture-capitalist
```

**What changed:**
- Authorization header fix (internal improvement)
- Documentation improvements
- analyze_bp tool removed (was not working)

---

## Troubleshooting

### Error: "Network connection failed"

**Solution:**
- Check internet connection
- Verify firewall allows HTTPS to www.zhencap.com
- Try again in a few minutes

### Error: "API quota exceeded"

**Solution:**
- Wait until next month (quota resets on 1st)
- Register for paid account at [www.zhencap.com](https://www.zhencap.com)

### Error: "Invalid API key"

**Solution:**
- Re-generate API key in dashboard
- Check for extra spaces: `echo "$ZHENCAP_API_KEY"`
- Ensure correct API key is copied

More troubleshooting: [SKILL.md Troubleshooting section](./SKILL.md#troubleshooting)

---

## Tools Reference

| Tool Name | Description | Key Parameters |
|-----------|-------------|----------------|
| `estimate_market_size` | Market sizing (TAM/SAM/SOM) | industry, geography, year |
| `analyze_competitors` | Competitor analysis & SWOT | company, industry |
| `estimate_valuation` | Valuation modeling | revenue, growth_rate, industry, stage |
| `score_risk` | Multi-dimensional risk scoring | company_data (name, industry, stage, team_size) |

Full documentation: [SKILL.md](./SKILL.md)

---

## Development

### Local Testing

```bash
# Install dependencies
npm install

# Test without API key (free tier simulation)
unset ZHENCAP_API_KEY
node -e "
const ZhenCapSkill = require('./index.js');
const skill = new ZhenCapSkill();
console.log('Headers:', skill.client.defaults.headers);
"

# Test with API key
export ZHENCAP_API_KEY="test_key_123"
node -e "
const ZhenCapSkill = require('./index.js');
const skill = new ZhenCapSkill();
console.log('Headers:', skill.client.defaults.headers);
"
```

### Project Structure

```
venture-capitalist/
├── index.js          # Main skill implementation
├── manifest.json     # MCP skill manifest
├── package.json      # NPM package definition
├── CHANGELOG.md      # Version history
├── README.md         # This file
├── SKILL.md          # Detailed documentation
├── MIGRATION-v1-to-v2.md  # Migration guide
├── LICENSE           # MIT license
└── .gitignore        # Git ignore rules
```

---

## Support

- **Documentation:** [www.zhencap.com/docs](https://www.zhencap.com/docs)
- **Email:** support@zhencap.com
- **GitHub Issues:** [github.com/zhencap/mcp-skill/issues](https://github.com/zhencap/mcp-skill/issues)
- **Community:** [Discord](https://discord.gg/zhencap) (coming soon)

---

## About v2.0.0 Breaking Changes

v2.0.0 was a complete rewrite from v1.0.0:

**v1.0.0:** Local document analysis tool
**v2.0.0:** Cloud API client for market intelligence

**Should you upgrade from v1.0.0?**
- Stay on v1.0.0 if you need local document processing
- Upgrade to v2.0.0+ if you need market intelligence and API integration

**See:** [MIGRATION-v1-to-v2.md](./MIGRATION-v1-to-v2.md) for full migration guide.

---

## License

MIT License - See [LICENSE](./LICENSE) file for details.

---

## About ZhenCap

ZhenCap (真资本) is an AI-powered investment analysis platform serving startups and VCs in China.

**Platform Features:**
- Market intelligence dashboard
- Investment pipeline management
- LP reporting automation
- Deal flow analytics

**Website:** [www.zhencap.com](https://www.zhencap.com)

---

## Changelog

### v2.0.1 (2026-04-01)

**Security Fixes:**
- Fixed Authorization header bug
- Enhanced privacy documentation

**Changes:**
- Removed analyze_bp tool (backend not ready)
- Updated manifest.json requiresAuth: false
- Added comprehensive privacy section

See [CHANGELOG.md](./CHANGELOG.md) for full history.

### v2.0.0 (2026-03-31)

**BREAKING CHANGES:** Complete rewrite - API client for cloud intelligence

**New Features:**
- Market size estimation
- Competitor analysis
- Valuation modeling
- Risk scoring

---

Built with [Model Context Protocol](https://modelcontextprotocol.io)
