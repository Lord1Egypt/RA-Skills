# Psyke Audit — GEO Assessment Framework

GEO (Generative Engine Optimisation) measures how well a site is structured to be discovered and cited by AI systems (ChatGPT, Google AI Overviews, Perplexity, Gemini).

---

## Step 1: AI Citability Audit

Crawl the site and assess each factor:

### Direct Answer Content
- Does the site have pages that directly answer common questions in their space?
- Look for: FAQ sections, how-to guides, buying guides, comparison content, explainers
- Score higher if answers are in clear, parseable paragraphs (not buried in marketing fluff)

### FAQ Implementation
- Are there FAQ sections on key pages?
- Is FAQPage schema markup present?
- Are the questions genuine (what users actually search) vs. marketing FAQs?

### Entity Clarity
- Is the brand clearly defined? (Organization schema, clear about page, consistent NAP)
- Are product/service categories clearly structured?
- Can an AI system easily understand what the company does, who they serve, and where?

### Authoritative Statements
- Does the content contain citable facts, statistics, or definitive claims?
- Is there original research, data, or expert opinions?
- Are claims supported with evidence?

### Content Structure
- Are pages formatted for machine readability? (Clear headings, short paragraphs, bullet lists)
- Is content scannable and well-organised?
- Are there structured data signals that reinforce the content?

---

## Step 2: AI Visibility Testing

### Ahrefs AI Citations (when available)
Pull from Ahrefs Site Explorer:
- Google AI Overview citation count
- ChatGPT citation count
- Compare against 2-3 competitors

### Live AI Query Testing (always do this)
Run 5-8 queries relevant to the client's space through ChatGPT and Perplexity.

**Query selection rules:**
1. Include the client's core service/product category + "Australia" (e.g., "best salary packaging provider Australia")
2. Include a "how to" query related to their space (e.g., "how does novated leasing work")
3. Include a "best [category]" query (e.g., "best camping gear Australia")
4. Include a competitor comparison query (e.g., "[client] vs [competitor]")
5. Include a location-specific query if relevant (e.g., "salary packaging Sydney")

**What to record:**
- Was the client mentioned? (Yes/No)
- Was a competitor mentioned? (Which ones?)
- What sources were cited?
- What type of content was cited? (blog posts, product pages, Wikipedia, review sites?)

**How to test:**
- Use web_fetch or browser to query ChatGPT/Perplexity with the selected queries
- Record the responses, noting citations
- If using Perplexity, note the source URLs it provides

---

## Step 3: Content Architecture Assessment

### Topic Hub Pages
- Does the site have dedicated hub pages for each core topic/service area?
- Are these hubs comprehensive or just thin landing pages?

### Content Clusters
- Are related pages interlinked in a hub-and-spoke pattern?
- Does the site demonstrate depth within verticals?

### Informational Content
- Count of buying guides, how-to articles, explainers, comparison pages
- Is this content genuinely useful or thin marketing filler?

### Long-tail Coverage
- Is there content targeting specific, question-based queries?
- Are there pages that match "what is X", "how to Y", "best Z for [use case]" patterns?

---

## Step 4: Competitive Position (Ahrefs required)

### Data to pull per competitor (2-3 competitors):
- Domain Rating
- Organic keyword count
- Monthly organic traffic
- Referring domains
- Google AI Overview citations
- ChatGPT citations
- Branded vs non-branded traffic split (estimate)

### Analysis:
- Where does the client rank vs competitors on each metric?
- What's the AI citation gap? (express as multipliers: "Competitor has 8.7x more AI citations")
- What content do competitors have that the client lacks?

---

## GEO Opportunity Identification

Based on the assessment, identify:

1. **Quick GEO wins** — existing pages that could be optimised for AI citability (add FAQ schema, restructure content, add structured data)
2. **Content gaps** — specific topics/queries where content should be created
3. **Competitive gaps** — topics where competitors are cited but the client isn't
4. **Keyword opportunities** — specific long-tail queries with volume that the client could target

Present these as specific, actionable recommendations — not generic "create more content" advice.
Each recommendation should include:
- The specific page/topic to create or optimise
- The target query/keyword
- Search volume (if available from Ahrefs)
- Which competitors currently own this space
- What type of content is needed (FAQ, guide, comparison, hub page)
