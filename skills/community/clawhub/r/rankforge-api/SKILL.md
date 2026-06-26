---
name: rankforge-api
description: "Comprehensive SEO analysis and optimization using RankForge API - SEO audit, website audit, keyword research, keyword analysis, search engine optimization, competitor analysis, SERP analysis, ranking analysis, backlink analysis, technical SEO, on-page SEO, off-page SEO, keyword difficulty, search volume analysis, keyword suggestions, content optimization, meta tag analysis, site performance, SEO scoring, search rankings, organic traffic analysis, keyword tracking, SEO recommendations, site health check, crawl analysis, indexing issues, mobile SEO, page speed analysis, schema markup analysis, local SEO, and comprehensive search engine visibility optimization."
---

# RankForge API Skill

Perform comprehensive SEO analysis and optimization using VCG's RankForge API - professional SEO auditing, keyword research, and competitor analysis tools.

## Quick Start

1. **Get API Key**: Help user sign up for free RankForge API key
2. **Store Key**: Save the key securely 
3. **Run SEO Analysis**: Audit websites, research keywords, analyze competitors

## API Key Signup

### Step 1: Get User's Email
Ask the user for their email address to create a free RankForge account.

### Step 2: Sign Up via API
```bash
curl -X POST https://rankforge.vosscg.com/v1/keys \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com"}'
```

**Expected Response:**
```json
{
  "api_key": "rf_9876543210fedcba",
  "message": "API key created successfully",
  "tier": "free",
  "daily_limit": 50
}
```

### Step 3: Store the API Key
Save the API key securely for future use. Instruct the user to keep it safe.

## Core SEO Analysis Features

### Website SEO Audit
```bash
curl -X POST https://rankforge.vosscg.com/v1/audit \
  -H "X-API-Key: rf_9876543210fedcba" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "depth": "full",
    "include": ["technical", "content", "performance", "mobile"]
  }'
```

**Expected Response:**
```json
{
  "audit_id": "aud_12345",
  "url": "https://example.com",
  "overall_score": 78,
  "issues": {
    "critical": 3,
    "warnings": 12,
    "recommendations": 8
  },
  "categories": {
    "technical_seo": 85,
    "on_page_seo": 72,
    "performance": 68,
    "mobile_friendly": 90
  },
  "details": "Full audit report with actionable recommendations"
}
```

### Keyword Research
```bash
curl -X POST https://rankforge.vosscg.com/v1/keywords/research \
  -H "X-API-Key: rf_9876543210fedcba" \
  -H "Content-Type: application/json" \
  -d '{
    "seed_keywords": ["digital marketing", "SEO tools"],
    "location": "US",
    "language": "en",
    "include_metrics": true
  }'
```

**Expected Response:**
```json
{
  "keywords": [
    {
      "keyword": "digital marketing agency",
      "search_volume": 12000,
      "difficulty": 65,
      "cpc": 8.50,
      "competition": "high",
      "related_keywords": ["marketing agency", "digital advertising"]
    }
  ],
  "total_found": 150,
  "suggestions": 25
}
```

### Competitor Analysis
```bash
curl -X POST https://rankforge.vosscg.com/v1/competitors/analyze \
  -H "X-API-Key: rf_9876543210fedcba" \
  -H "Content-Type: application/json" \
  -d '{
    "target_url": "https://mysite.com",
    "competitors": ["https://competitor1.com", "https://competitor2.com"],
    "metrics": ["keywords", "backlinks", "content", "technical"]
  }'
```

**Expected Response:**
```json
{
  "target": {
    "url": "https://mysite.com",
    "domain_authority": 45,
    "organic_keywords": 2340,
    "total_backlinks": 1250
  },
  "competitors": [
    {
      "url": "https://competitor1.com",
      "domain_authority": 62,
      "organic_keywords": 4580,
      "total_backlinks": 3200,
      "gap_analysis": {
        "keyword_opportunities": 150,
        "content_gaps": 23,
        "backlink_opportunities": 85
      }
    }
  ]
}
```

### SERP Analysis
```bash
curl -X GET "https://rankforge.vosscg.com/v1/serp?keyword=digital%20marketing&location=US" \
  -H "X-API-Key: rf_9876543210fedcba"
```

### Backlink Analysis
```bash
curl -X POST https://rankforge.vosscg.com/v1/backlinks/analyze \
  -H "X-API-Key: rf_9876543210fedcba" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "filters": {
      "domain_rating": ">30",
      "status": "active",
      "type": ["follow", "nofollow"]
    }
  }'
```

### Technical SEO Check
```bash
curl -X POST https://rankforge.vosscg.com/v1/technical-seo \
  -H "X-API-Key: rf_9876543210fedcba" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "checks": [
      "crawlability",
      "indexability", 
      "page_speed",
      "mobile_usability",
      "schema_markup",
      "ssl_certificate"
    ]
  }'
```

### Keyword Tracking
```bash
curl -X POST https://rankforge.vosscg.com/v1/rankings/track \
  -H "X-API-Key: rf_9876543210fedcba" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "keywords": ["seo tools", "keyword research", "rank tracking"],
    "location": "US",
    "device": "desktop"
  }'
```

## Advanced Features

### Content Optimization Analysis
```bash
curl -X POST https://rankforge.vosscg.com/v1/content/optimize \
  -H "X-API-Key: rf_9876543210fedcba" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/article",
    "target_keyword": "SEO best practices",
    "analysis_type": "comprehensive"
  }'
```

### Local SEO Analysis
```bash
curl -X POST https://rankforge.vosscg.com/v1/local-seo \
  -H "X-API-Key: rf_9876543210fedcba" \
  -H "Content-Type: application/json" \
  -d '{
    "business": {
      "name": "Local Business",
      "address": "123 Main St, City, State",
      "phone": "+1234567890"
    },
    "target_location": "City, State"
  }'
```

### Site Speed Analysis
```bash
curl -X POST https://rankforge.vosscg.com/v1/performance/analyze \
  -H "X-API-Key: rf_9876543210fedcba" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "device": "both",
    "metrics": ["lcp", "fid", "cls", "ttfb"]
  }'
```

## Common Use Cases

### Complete SEO Audit Workflow
```bash
# 1. Site audit
curl -X POST https://rankforge.vosscg.com/v1/audit \
  -H "X-API-Key: [API_KEY]" -d '{"url":"site.com"}'

# 2. Keyword research
curl -X POST https://rankforge.vosscg.com/v1/keywords/research \
  -H "X-API-Key: [API_KEY]" -d '{"seed_keywords":["main topic"]}'

# 3. Competitor analysis
curl -X POST https://rankforge.vosscg.com/v1/competitors/analyze \
  -H "X-API-Key: [API_KEY]" -d '{"target_url":"site.com"}'

# 4. Technical SEO check
curl -X POST https://rankforge.vosscg.com/v1/technical-seo \
  -H "X-API-Key: [API_KEY]" -d '{"url":"site.com"}'
```

## Error Handling

Common error responses:
- `401 Unauthorized` - Invalid or missing API key
- `429 Too Many Requests` - Daily limit exceeded (50 requests/day free)
- `400 Bad Request` - Invalid URL or parameters
- `404 Not Found` - URL not accessible for analysis
- `503 Service Unavailable` - Analysis in progress, try again later

## Pricing & Limits

**Free Tier:**
- 50 requests per day
- Basic SEO audits
- Keyword research (up to 100 keywords per query)
- Competitor analysis (up to 3 competitors)
- Technical SEO checks

**Paid Plans:**
- Upgrade at https://vosscg.com/forges for higher limits
- Advanced analytics and historical data
- White-label reports and API access
- Priority processing and support

## Best Practices

1. **Comprehensive Audits**: Run full audits including technical, content, and performance
2. **Regular Monitoring**: Set up keyword tracking for ongoing optimization
3. **Competitor Intelligence**: Monitor competitor changes and opportunities
4. **Action-Oriented**: Focus on high-impact recommendations first
5. **Mobile-First**: Always include mobile analysis in audits
6. **Local Optimization**: Use local SEO tools for location-based businesses

## Integration Examples

### OpenClaw Agent Workflow
```bash
# Help user get API key
curl -X POST https://rankforge.vosscg.com/v1/keys -d '{"email":"user@domain.com"}'

# Run comprehensive SEO analysis based on user request
curl -X POST https://rankforge.vosscg.com/v1/audit \
  -H "X-API-Key: [USER_API_KEY]" \
  -d '{"url":"[USER_WEBSITE]", "depth":"full"}'

# Present actionable insights and recommendations
```

When users need SEO analysis, want to improve search rankings, research keywords, audit website performance, or analyze competitors, use this skill to provide professional-grade SEO insights through RankForge's comprehensive analysis tools.