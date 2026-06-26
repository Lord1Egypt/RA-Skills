---
name: schemaorg-site-enhancer
description: Helps agents integrate Schema.org structured data into websites for rich search results, better SEO, and improved communication with search engines. Provides ready-to-use JSON-LD templates, generation scripts, and implementation patterns for common schema types.
author: Chaika
package: schemaorg-site-enhancer
runtime: node
version: 0.1.0
---

# Schema.org Site Enhancer

This skill enables OpenClaw agents to embed Schema.org structured data (JSON-LD) into web pages, boosting SEO, enabling rich snippets, and improving how search engines understand content.

## Features

- Ready‑to‑use JSON‑LD templates for FAQPage, HowTo, Article, Product, LocalBusiness, Event, Organization, and more.
- Helper functions to generate structured data from simple inputs.
- Guidance on where to inject the `<script type="application/ld+json">` tag in HTML.
- Validation helpers to ensure generated JSON‑LD conforms to schema.org specifications.
- Example usage patterns for static sites, React/Vue apps, and SSR frameworks.

## How to Use

### 1. Install the skill

```bash
clawhub install schemaorg-site-enhancer
```

### 2. Import in your agent code or scripts

```javascript
const { generateFAQPage, injectJSONLD } = require('schemaorg-site-enhancer');
```

### 3. Example: Create an FAQPage

```javascript
const faqData = {
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is Schema.org?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Schema.org is a collaborative, community activity with a mission to create, maintain, and promote schemas for structured data on the Internet."
      }
    },
    {
      "@type": "Question",
      "name": "Why use JSON-LD?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "JSON-LD is the recommended format for Schema.org because it’s easy to read, doesn’t interfere with HTML, and is supported by all major search engines."
      }
    }
  ]
};

const jsonLD = generateFAQPage(faqData);
// jsonLD is now a ready‑to‑insert <script type="application/ld+json"> block
```

## Provided Utilities

- `generateFAQPage(data)` – returns a JSON‑LD string for an FAQPage.
- `generateHowTo(data)` – creates a HowTo schema.
- `generateArticle(data)` – for news articles or blog posts.
- `generateProduct(data)` – for e‑commerce product pages.
- `injectJSONLD(html, jsonLD)` – inserts the script tag into the `<head>` of an HTML string.
- `validateJSONLD(jsonLD)` – basic syntax and @type validation.

## Installation Requirements

- Node.js ≥ 14
- No external dependencies (uses only built‑in Node modules)

## License

MIT

## Contributing

Feel free to open issues or submit pull requests to add more schema types or improve the templates.