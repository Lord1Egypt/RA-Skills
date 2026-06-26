# Migration Guide: v1.0.0 to v2.0.0

## Overview

**This is a BREAKING CHANGE update.** Version 2.0.0 is a complete rewrite with fundamentally different functionality from v1.0.0.

If you are currently using v1.0.0, please read this guide carefully before upgrading.

---

## What Changed?

### v1.0.0 (Document Analysis Tool)

**Focus:** Local document processing for pitch decks

**Commands:**
- `/vc analyze [file]` - Analyze a pitch deck (PDF/PPT/DOCX)
- `/vc report [file]` - Generate investment report
- `/vc deck [file]` - Extract deck structure
- `/vc compare [file1] [file2]` - Compare two decks
- `/vc extract [file]` - Extract financial data

**Data Flow:**
```
Local Document → PDF Parser → Analysis → Output
```

**Key Features:**
- Fully local processing (no cloud API)
- Document format support (PDF, PPTX, DOCX)
- Privacy-focused (no data leaves your machine)
- No API key required

---

### v2.0.0 (API Client)

**Focus:** Cloud-powered investment analysis via ZhenCap platform

**Tools:**
- `estimate_market_size` - Market sizing (TAM/SAM/SOM)
- `analyze_competitors` - Competitor analysis and SWOT
- `estimate_valuation` - Valuation modeling
- `score_risk` - Multi-dimensional risk assessment
- `analyze_bp` - Business plan analysis (coming soon)

**Data Flow:**
```
Natural Language Query → MCP Tool Call → ZhenCap API → Structured JSON Response
```

**Key Features:**
- Cloud API integration (requires internet)
- Structured data output (JSON)
- Free tier: 50 API calls/month
- Paid tier: 0.10-0.20 CNY per call
- API key optional (for free tier)

---

## Why the Change?

**Original Problem (v1.0.0):**
- Document parsing is error-prone (different formats, OCR quality)
- Limited intelligence (rule-based extraction only)
- No market data or benchmarking
- Maintenance burden (multiple parsers to maintain)

**New Solution (v2.0.0):**
- Focus on API integration (our core competency)
- Leverage ZhenCap's investment data platform
- Provide actionable market intelligence
- Easier to maintain and scale

---

## Should You Upgrade?

### Stay on v1.0.0 If:

- You need fully local/offline document processing
- You work with sensitive documents that cannot leave your machine
- You primarily analyze pitch deck PDFs
- You don't need market data or benchmarking

**How to stay on v1.0.0:**
```bash
clawhub install venture-capitalist@1.0.0
```

---

### Upgrade to v2.0.0 If:

- You need market sizing and competitive analysis
- You want AI-powered valuation suggestions
- You're okay with cloud API calls (free tier available)
- You need structured data output (JSON) for automation

**How to upgrade:**
```bash
clawhub uninstall venture-capitalist
clawhub install venture-capitalist@2.0.0
```

---

## Migration Path

### Option 1: Use Both Versions (Recommended)

Install v2.0.0 alongside local document tools:

```bash
# Install v2.0.0 for market analysis
clawhub install venture-capitalist@2.0.0

# Install separate tools for document processing
clawhub install pdf-parser
clawhub install document-analyzer
```

**Workflow:**
1. Use `pdf-parser` to extract text from pitch decks
2. Use `venture-capitalist` (v2.0.0) for market analysis
3. Combine insights for comprehensive due diligence

---

### Option 2: Replace with v2.0.0

Uninstall v1.0.0 and adopt API-based workflow:

```bash
# Remove old version
clawhub uninstall venture-capitalist

# Install new version
clawhub install venture-capitalist@2.0.0
```

**New Workflow:**
1. Extract key facts manually from pitch decks
2. Use natural language to query ZhenCap tools:
   - "What's the market size for AI healthcare in China?"
   - "Analyze competitors for [company] in [industry]"
   - "Value a Series A company with 5M revenue"
3. Get structured JSON data for reports

---

### Option 3: Stay on v1.0.0

Pin your installation to v1.0.0:

```bash
# In your MCP config file
{
  "mcpServers": {
    "venture-capitalist": {
      "version": "1.0.0",
      "command": "node",
      "args": ["..."]
    }
  }
}
```

**Note:** v1.0.0 will receive critical security patches only. No new features planned.

---

## Feature Comparison

| Feature | v1.0.0 | v2.0.0 |
|---------|--------|--------|
| **Document Analysis** | Yes (PDF, PPTX, DOCX) | No (coming Q2 2026) |
| **Market Sizing** | No | Yes (TAM/SAM/SOM) |
| **Competitor Analysis** | No | Yes (SWOT) |
| **Valuation Modeling** | No | Yes (Comparable Companies) |
| **Risk Scoring** | No | Yes (4 dimensions) |
| **Data Source** | Local files only | ZhenCap API (cloud) |
| **Privacy** | Fully local | API calls to cloud |
| **Pricing** | Free (local) | Free tier + paid |
| **Internet Required** | No | Yes |
| **API Key Required** | No | Optional (for >50 calls/month) |

---

## Command Mapping

### v1.0.0 Commands (No Longer Work)

```bash
/vc analyze pitch-deck.pdf    # ❌ REMOVED
/vc report pitch-deck.pdf     # ❌ REMOVED
/vc deck pitch-deck.pdf       # ❌ REMOVED
/vc compare deck1.pdf deck2   # ❌ REMOVED
/vc extract pitch-deck.pdf    # ❌ REMOVED
```

### v2.0.0 Natural Language Queries

```bash
# Market Analysis
"What's the market size for AI healthcare in China?"
→ Uses: estimate_market_size

# Competitor Analysis
"Analyze competitors for Tesla in the EV market"
→ Uses: analyze_competitors

# Valuation
"Value a Series A SaaS company with 5M revenue growing at 200%"
→ Uses: estimate_valuation

# Risk Assessment
"Score the investment risk for an early-stage AI startup"
→ Uses: score_risk

# Business Plan Analysis (coming soon)
"Analyze this BP: [text content]"
→ Uses: analyze_bp (Q2 2026)
```

---

## Configuration Changes

### v1.0.0 Configuration

```yaml
# ~/.openclaw/config.yml
skills:
  venture-capitalist:
    pdf_parser: "pdfjs"
    ocr_enabled: true
    local_cache: true
```

### v2.0.0 Configuration

```yaml
# ~/.openclaw/config.yml
skills:
  venture-capitalist:
    api_key: "your_api_key_here"  # Optional
    api_endpoint: "https://www.zhencap.com/api/v1"
```

Or use environment variable:

```bash
export ZHENCAP_API_KEY="your_api_key_here"
```

---

## Troubleshooting

### Issue: "Tool not found" after upgrade

**Cause:** MCP cache not refreshed.

**Solution:**
```bash
# Restart your MCP client (Claude Desktop, Cline, etc.)
# Or manually refresh:
clawhub refresh
```

---

### Issue: "v2.0.0 doesn't analyze my PDFs"

**Cause:** v2.0.0 no longer supports document parsing (it's an API client).

**Solution:**
- Use a dedicated PDF parser tool
- Or wait for `analyze_bp` tool (Q2 2026)
- Or revert to v1.0.0:
  ```bash
  clawhub install venture-capitalist@1.0.0
  ```

---

### Issue: "I need both document analysis AND market data"

**Solution:** Use both v1.0.0 and v2.0.0:

1. Keep v1.0.0 for document parsing
2. Install v2.0.0 as a separate skill
3. Rename one to avoid conflicts:
   ```bash
   clawhub install venture-capitalist@1.0.0 --as vc-docs
   clawhub install venture-capitalist@2.0.0 --as vc-api
   ```

---

## Rollback Instructions

If you upgraded to v2.0.0 and want to go back:

```bash
# Step 1: Uninstall v2.0.0
clawhub uninstall venture-capitalist

# Step 2: Reinstall v1.0.0
clawhub install venture-capitalist@1.0.0

# Step 3: Verify
clawhub list | grep venture-capitalist
# Should show: venture-capitalist v1.0.0
```

---

## Support

If you have migration questions:

- **Email:** support@zhencap.com
- **GitHub Issues:** [github.com/zhencap/mcp-skill/issues](https://github.com/zhencap/mcp-skill/issues)
- **Documentation:** [www.zhencap.com/docs/migration](https://www.zhencap.com/docs/migration)

---

## Timeline

- **v1.0.0 Release:** 2025-12-15
- **v2.0.0 Release:** 2026-03-31
- **v1.0.0 Support End:** 2026-12-31 (security patches only)
- **v2.0.0 `analyze_bp` Tool:** Q2 2026 (expected)

---

## Frequently Asked Questions

### Q: Will v1.0.0 stop working?

**A:** No. v1.0.0 will continue to work, but will only receive security patches. No new features.

### Q: Can I use v2.0.0 without an API key?

**A:** Yes. You get 50 free API calls per month without registration.

### Q: Is my data safe with v2.0.0?

**A:** Yes. API calls are encrypted (HTTPS/TLS 1.3). We don't store sensitive business data. See [SKILL.md Privacy section](./SKILL.md#privacy--data-security).

### Q: When will `analyze_bp` tool be available?

**A:** Expected Q2 2026. It will process business plans through the ZhenCap API.

### Q: Can I contribute to v2.0.0 development?

**A:** Yes! We welcome contributions. See [CONTRIBUTING.md](./CONTRIBUTING.md).

---

## Acknowledgments

Thank you to all v1.0.0 users for your feedback. Your input shaped v2.0.0's design.

If you have suggestions for v2.1.0, please open a GitHub issue or email us.

---

**Last Updated:** 2026-03-31
