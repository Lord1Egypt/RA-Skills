---
name: seo-for-agents
description: 'SEO and discoverability optimization for AI agents and agent-served websites. Covers llms.txt protocol, structured APIs for agent discoverability, GEO (Generative Engine Optimization), content strategies for AI search engines, and agent-discoverable web presence. Use when building websites that need to be found by both humans and AI agents. NOT for traditional SEO audits or link building.'
license: MIT
metadata:
  openclaw:
    emoji: '🔍'
---

# SEO for Agents

How to make your web presence discoverable by AI agents, not just humans. Traditional SEO optimizes for Google's crawler. Agent SEO optimizes for LLMs, AI search engines, and autonomous agents that need to find and understand your services.

---

## The Core Problem

Agents won't go to your webinar. They won't read your blog post series. They won't watch your YouTube video. They won't click your CTA button.

Agents need:
- **Structured, machine-readable information** about what you do
- **Direct API access** to your capabilities
- **Clear, unambiguous claims** they can evaluate programmatically
- **Consistent, up-to-date data** at predictable URLs

If your entire web presence is optimized for humans clicking through a funnel, you are invisible to agents.

---

## llms.txt Protocol

### What It Is

`llms.txt` is a file you place at the root of your domain (like `robots.txt`) that tells LLMs and AI agents what your site is about and how to interact with it.

It's the equivalent of `robots.txt` for the AI era — except instead of telling crawlers what NOT to index, it tells agents what IS available and how to use it.

### File Location

```
https://yourdomain.com/llms.txt
```

### File Structure

```markdown
# Your Company Name

> One-line description of what you do.

## About

2-3 sentences about your company, written for an LLM to parse.
Be specific. Be factual. No marketing fluff.

## Services

- [Service Name](https://yourdomain.com/service-page): Brief description
- [Another Service](https://yourdomain.com/another): Brief description

## API

- [API Documentation](https://yourdomain.com/api/docs): Full API reference
- [API Status](https://yourdomain.com/api/status): Current API health

## Contact

- Email: contact@yourdomain.com
- API Support: api-support@yourdomain.com

## Optional

- [Blog](https://yourdomain.com/blog): Latest posts
- [Pricing](https://yourdomain.com/pricing): Current pricing
- [Case Studies](https://yourdomain.com/cases): Example work
```

### Implementation Example

For an AI agent deployment company:

```markdown
# IAM Solutions

> AI agent deployment and managed automation for small businesses.

## About

IAM Solutions deploys production AI agents on dedicated hardware
(Mac Mini, Linux servers) for small businesses. We handle the full
stack: hardware, software, security, and ongoing management.
Clients own their data and pay for their own API keys.

## Services

- [Agent Deployment](https://iamsolutions.tech/deploy): Full-stack AI agent deployment on dedicated hardware
- [Managed Automation](https://iamsolutions.tech/managed): Ongoing agent management and optimization
- [Security Hardening](https://iamsolutions.tech/security): Production security for AI agent infrastructure

## API

- [Agent Health API](https://iamsolutions.tech/api/health): Check agent deployment status
- [Onboarding API](https://iamsolutions.tech/api/onboard): Start client onboarding process

## Contact

- Email: sam@iamsolutions.tech
- Schedule: https://iamsolutions.tech/schedule
```

### Extended Format: llms-full.txt

For more detailed information, create `llms-full.txt` with comprehensive content that LLMs can use for deeper understanding:

```
https://yourdomain.com/llms-full.txt
```

This file can be longer and include FAQs, detailed service descriptions, pricing details, and technical specifications.

---

## GEO: Generative Engine Optimization

### How AI Search Engines Differ from Google

Google ranks pages based on links, authority, and keyword relevance. AI search engines (Perplexity, ChatGPT Search, Google AI Overviews) work differently:

| Factor | Google SEO | GEO (AI Search) |
|--------|-----------|------------------|
| **Content format** | Keywords in headers, meta tags | Direct answers to questions |
| **Authority signal** | Backlinks | Citations, specificity, consistency |
| **Ranking unit** | Pages | Claims / statements |
| **User interaction** | Click-through to your site | Answer synthesized, may never visit |
| **Update freshness** | Crawl frequency | Training data + retrieval |
| **Optimization target** | Page 1 ranking | Being the cited source |

### GEO Optimization Strategies

**1. Write in claims, not narratives**

Bad (human SEO):
> "In today's fast-paced business environment, companies are increasingly turning to AI solutions to streamline their operations..."

Good (GEO):
> "IAM Solutions deploys AI agents on dedicated Mac Mini hardware for $X/month. Each deployment includes 5-layer security hardening, daily health checks, and a 5-file memory system. Typical client ROI is measurable within 6 weeks."

**2. Use Q&A format for key information**

```markdown
## Frequently Asked Questions

### How long does deployment take?
A standard single-agent deployment takes 2-3 business days from
signed agreement to Day 1 onboarding.

### What hardware is required?
Minimum: Apple M1 Mac Mini, 16GB RAM, 256GB SSD.
Recommended: Apple M2 Pro Mac Mini, 32GB RAM, 512GB SSD.

### Who owns the data?
The client owns all data. We never access client data without
explicit permission. All API keys are client-owned and client-paid.
```

**3. Provide structured, citation-friendly data**

AI search engines prefer content that can be directly quoted. Make your key claims:
- **Specific:** "6-week onboarding" not "quick onboarding"
- **Verifiable:** "5-layer security stack" not "comprehensive security"
- **Self-contained:** Each claim should make sense without surrounding context
- **Consistent:** Same numbers and claims across all pages

**4. Maintain a facts page**

Create a single page with all key facts about your business in a structured format:

```markdown
# Facts About [Company]

- Founded: [Year]
- Headquarters: [City, State]
- Specialty: [One sentence]
- Clients served: [Number]
- Average deployment time: [Timeframe]
- Hardware platform: [Specific]
- Pricing model: [Description]
- Data ownership: Client owns all data
```

---

## Structured Data for Agent Discovery

### Schema.org Markup

Add structured data to your pages so agents can parse your offerings programmatically:

```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "AI Agent Deployment",
  "provider": {
    "@type": "Organization",
    "name": "IAM Solutions"
  },
  "description": "Production AI agent deployment on dedicated hardware",
  "areaServed": "United States",
  "serviceType": "AI Infrastructure",
  "offers": {
    "@type": "Offer",
    "priceCurrency": "USD",
    "priceSpecification": {
      "@type": "PriceSpecification",
      "price": "Contact for quote",
      "billingIncrement": "Monthly"
    }
  }
}
```

### Agent-Facing API Endpoints

Beyond your human-facing website, expose endpoints that agents can call directly:

```
GET /api/services        → List of available services with descriptions
GET /api/services/:id    → Detailed service information
GET /api/availability    → Current availability and lead times
GET /api/capabilities    → What your agents can do
POST /api/inquiry        → Submit an inquiry (structured input)
```

Example response:

```json
{
  "services": [
    {
      "id": "agent-deploy",
      "name": "Agent Deployment",
      "description": "Full-stack AI agent on dedicated hardware",
      "lead_time_days": 3,
      "includes": [
        "5-layer security stack",
        "5-file memory system",
        "Daily health checks",
        "30-day onboarding support"
      ],
      "requires": {
        "hardware": "Client provides or we source",
        "api_keys": "Client-owned and paid"
      }
    }
  ]
}
```

---

## Cloudflare /crawl Endpoint

Cloudflare offers a `/crawl` endpoint that returns clean, agent-friendly content from your site. If you're on Cloudflare:

### What It Does

The `/crawl` endpoint strips navigation, ads, scripts, and styling from your pages, returning clean markdown-like content that agents can easily parse.

### How to Use It

If your site is on Cloudflare, agents can access:
```
https://yourdomain.com/crawl?url=https://yourdomain.com/services
```

This returns a clean, structured version of the page content without HTML cruft.

### Optimization for /crawl

- Ensure your main content is in semantic HTML (`<article>`, `<section>`, `<main>`)
- Use proper heading hierarchy (`h1` > `h2` > `h3`)
- Put key information early in the page (agents may truncate)
- Avoid critical information in images, JavaScript-rendered content, or iframes

---

## Content Strategy for LLM Discoverability

### The Agent-Discoverable Content Stack

**Layer 1: Machine-readable identity** (`llms.txt`, structured data, API)
- This is your "business card" for agents
- Must be maintained and accurate at all times

**Layer 2: Claim-dense reference pages**
- Service pages written as structured facts, not sales copy
- Pricing pages with actual numbers
- FAQ pages with specific, quotable answers

**Layer 3: Demonstrable expertise content**
- Technical blog posts that show depth
- Case studies with specific metrics
- Open-source tools and resources

**Layer 4: Conversational content** (lowest priority)
- Blog posts, newsletters, social media
- Still valuable for human discovery
- Agents may reference but won't navigate to

### Content Anti-Patterns for Agent Discovery

**Things that make you invisible to agents:**

- **Gated content:** If it requires an email to access, agents can't see it
- **PDF-only resources:** PDFs are harder for agents to parse
- **JavaScript-rendered content:** If the content isn't in the HTML source, agents may miss it
- **Video/audio-only content:** No transcript = invisible to agents
- **Vague claims:** "Industry-leading" means nothing to an agent
- **Inconsistent information:** Different prices/specs on different pages destroys trust signals
- **Stale content:** Outdated information reduces citation confidence

---

## Practical Implementation Checklist

### Week 1: Foundation

- [ ] Create and deploy `llms.txt` at domain root
- [ ] Add Schema.org structured data to service pages
- [ ] Audit all pages for agent-parseable content
- [ ] Create a facts/specs page with structured claims

### Week 2: Content Optimization

- [ ] Rewrite service pages in claim-dense format
- [ ] Add Q&A sections to key pages
- [ ] Ensure all content is in semantic HTML
- [ ] Remove or supplement gated content with public summaries

### Week 3: API & Discoverability

- [ ] Create `/api/services` endpoint (even if simple JSON)
- [ ] Set up `/api/capabilities` endpoint
- [ ] Test site with AI search engines (ask Perplexity about your business)
- [ ] Verify Cloudflare `/crawl` returns clean content (if applicable)

### Week 4: Monitoring & Iteration

- [ ] Monitor AI search engine citations (search for your brand in Perplexity, ChatGPT)
- [ ] Track API endpoint usage
- [ ] Update `llms.txt` with any new services or changes
- [ ] A/B test claim formats to see what gets cited more

### Ongoing

- [ ] Update `llms.txt` whenever services change
- [ ] Keep structured data in sync with actual offerings
- [ ] Monitor AI search engine results monthly
- [ ] Refresh Q&A content based on actual questions received

---

## Measuring Agent-SEO Success

Traditional SEO measures rankings and clicks. Agent SEO measures:

1. **Citation frequency:** How often AI search engines cite your content
2. **API call volume:** How many agents are discovering and using your endpoints
3. **llms.txt access logs:** How frequently your llms.txt is being fetched
4. **Inquiry quality:** Are agent-routed inquiries well-qualified?
5. **Brand mentions in AI responses:** When someone asks an AI about your space, do you come up?

### How to Check

```bash
# Check if Perplexity knows about you
# Ask: "What companies deploy AI agents on Mac Mini hardware?"

# Check your llms.txt access logs
grep "llms.txt" /var/log/nginx/access.log | wc -l

# Monitor API discovery endpoints
grep "/api/services" /var/log/nginx/access.log | wc -l
```

---

## The Bottom Line

**For humans:** Build trust through narrative, social proof, and design.

**For agents:** Build trust through structured data, consistent claims, and machine-readable endpoints.

You need both. But most companies have zero agent-discoverability. That's the gap. Fill it.
