---
name: seo-content-pipeline
description: SEO automated content pipeline skill. Automates the entire workflow from competitor research and keyword mining to article generation and publishing.
---

# SEO Automated Content Pipeline

Automates the entire workflow from competitor research and keyword mining to article generation and publishing.

## Use Cases

Executes competitor analysis, keyword research, article topic selection, content generation (titles/images/table of contents/internal links/external links), and automated publishing to CMS when acting as an SEO Content Strategist.

## Quick Start

```
Competitor Analysis → Keyword Mining → Generate Topic List → Content Creation → Auto-Publish
```

When the user provides a product name and target customer, execute the full pipeline.

## Workflow

### Step 1: Competitor Research and Keyword Mining

**Role**: SEO Content Strategist

**Input Information**:
- Product (provided by user)
- Target Customer (provided by user)

**Execution Content**:
1. Search for potential competitor websites
2. Analyze competitor content layout and keyword coverage
3. Identify content gaps
4. Output a list of article topics in JSON format

**Output Format**:
```json
{
  "topics": [
    {
      "keyword": "core keyword",
      "title": "article title",
      "angle": "content angle",
      "search_intent": "informational|commercial|transactional",
      "target_url": "target URL"
    }
  ]
}
```

### Step 2: Content Generation

Based on the topic list, generate for each article:
- Title (includes core keywords, SEO compliant)
- Introduction (summarizes content value)
- Table of Contents (based on article structure)
- Body (step-by-step / modular)
- FAQ (frequently asked questions)
- Conclusion and Further Reading

**Publishing Action**:
- Auto-publish to website CMS
- Supports mainstream website builders (WordPress, custom CMS)

### Step 3: Content Template Selection

Select the corresponding template based on **search intent**:

| Search Intent | Template Type | Structure |
|---------------|---------------|-----------|
| Transactional | Product Page | Features + Specs + Pricing + Buy Button |
| Commercial | Comparison Page | Feature Comparison Table + Pros/Cons Analysis + Recommendation |
| Informational | Tutorial Page | Step-by-Step Guide + Images + FAQ + Summary |
| Informational | List Page | Resource Roundup + Recommendation Reasons + Use Cases |
| Commercial | Case Study Page | Background + Problem + Solution + Results + Data |

See [references/templates.md](references/templates.md) for details.

## Usage Example

**User Input**:
```
Product: AI Writing Tool
Target Customers: Content Creators, SEO Practitioners
```

**Automated Execution Flow**:
1. Search competitors: Jasper, Copy.ai, Writesonic
2. Identify content gaps: Tool comparisons, usage tutorials, case studies
3. Generate topic list (JSON format)
4. Generate and publish articles based on templates

## Notes

| Item | Description |
|------|-------------|
| Content Quality | Auto-generated content requires manual review to avoid factual errors. |
| SEO Compliance | Avoid keyword stuffing; maintain a natural reading experience. |
| Publishing Frequency | Control daily publishing volume to avoid being flagged as spam. |
| Internal Linking Strategy | Newly published articles should reasonably link to existing content. |