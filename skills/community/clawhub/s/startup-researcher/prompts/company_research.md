# Individual Company Research

Your goal is to perform a deep-dive research sprint on a single tech startup. You must use web search exclusively to find credible, recent data (last 6-12 months).

## Research Strategy (CRITICAL)
1. **Find Primary Sources First:** Always explicitly search for and identify the company's official website URL. Verify it matches the company context (not a similarly named company).
2. **Direct Extraction:** Once the official website is found, prioritize reading its "About Us", "Product", or "Documentation" pages directly (e.g., using `read_url_content` or `browser_subagent`) to extract accurate, first-hand information about products and mission.
3. **Trusted Databases:** Supplement direct extraction by searching for the company's Crunchbase or Pitchbook pages to reliably verify funding and valuation. Avoid guessing from unrelated news.

## Rules & Anti-Hallucination
- **DO NOT GUESS FUNDING:** If a funding round or valuation cannot be verified via web search, state "Undisclosed".
- **DO NOT HALLUCINATE PRODUCTS:** Only list products explicitly mentioned in recent search results.
- **EXPLICIT CITATIONS:** ALL statements and claims must precisely originate from an explicit search result. Every individual company profile **MUST** include a dedicated 'References' section at the bottom, listing the source URLs used.

## Profile Format
Produce a Markdown document for the company with the following structure:

### 1. Fundamental Facts (Markdown Table)
The fundamental facts must be presented in a **Markdown Table**:
| | |
|---|---|
| **Company Name** | [Name] |
| **Company Website URL** | [URL] |
| **Public or Private** | [Status] |
| **Founding Year & HQ** | [Year, Location] |
| **Founders and Key Leadership** | [Names/Roles] |
| **Key Investors** | [Investors] |
| **Total Raised, Latest Round & Current Valuation, or Stock Price if Public** | [Details] |
| **Main Products / Technology** | [Summary] |
| **Market Focus / Target Audience** | [Focus] |

### 2. Narrative Overview
Below the table, include prose for:
- Recent developments (last 6–12 months)
- Competitive positioning

### 3. Product Details (Markdown Table)
Deep dive into the company's main products or technologies. You must explicitly format the product list as a table:

| Product Name | Product Website URL | Description & Value Proposition | Target Users / Customers | Pricing Model | Key Features & Underlying Technology |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... |

### 4. Hiring
List key open roles at the company and their requirements, linking to their careers page.

### 5. Highlights
Automatically flag the following:
- Funding events >= $100M (e.g., `🚩 Funding >$100M`)
- Major product launches or announcements
- Leadership changes
- Valuation milestones (>$1B, >$10B, etc.)

### 6. References
List all URLs explicitly used to generate this profile.
