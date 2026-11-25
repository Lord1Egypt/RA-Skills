# Local audit checklist

## Crawlability and indexability

- HTTP outcome and redirect destination
- robots.txt access and relevant allow/disallow rules
- sitemap presence, status, and canonical URL consistency
- robots meta and X-Robots-Tag directives
- canonical declaration and conflicting signals
- internal discovery depth and orphan candidates when sitemap evidence exists

## On-page structure

- unique, descriptive title aligned with page purpose
- useful meta description without applying rigid character limits as pass/fail rules
- one clear main topic and logical heading hierarchy
- meaningful visible content and page-type-appropriate depth
- descriptive internal anchors and navigational paths
- meaningful image alternative text; empty alt for decorative images
- Open Graph and social preview metadata when sharing matters

## Structured data

- valid JSON-LD syntax
- schema types appropriate to visible content
- required and recommended properties supported by the page
- organization, person, product, article, breadcrumb, local business, event, or other relevant entity clarity
- no markup for content that is absent or misleading

## GEO readiness

- clear entity identity and relationships
- named authors or accountable organization where appropriate
- firsthand experience, credentials, methods, dates, and source citations
- specific facts that can be quoted with context
- consistent claims across key pages
- accessible About, contact, editorial, and policy information

## AEO readiness

- direct answers near relevant questions
- headings that reflect real user tasks without forcing question wording
- concise definitions, steps, comparisons, and tables where useful
- FAQ or HowTo markup only when eligible visible content exists
- unambiguous terminology and page purpose

## Performance and experience

Assess only from measurements or direct observation:

- Core Web Vitals from Lighthouse, CrUX, or another named source
- server response timing as a separate metric
- viewport and mobile rendering
- intrusive overlays or blocked primary content
- broken resources and client-side rendering failures

## Interpretation rules

- Prefer patterns across templates over isolated trivia.
- Separate critical access/indexation blockers from optimizations.
- Explain intentional noindex, redirect, canonical, and short utility pages as context, not automatic defects.
- Report sampling and inaccessible pages.
