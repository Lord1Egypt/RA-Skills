---
name: schema-gen
description: Generate Schema.org JSON-LD structured data markup for Person, Organization, Product, FAQ, HowTo, Article, LocalBusiness, Event, WebSite, BreadcrumbList, VideoObject, and SoftwareApplication.
---

# schema-gen

Generate valid Schema.org JSON-LD structured data markup for any schema type.

## Supported Schema Types

| Type | Key Fields | Google Rich Result |
|------|-----------|-------------------|
| **Person** | name, jobTitle, url, image, sameAs, worksFor | Yes |
| **Organization** | name, url, logo, description, sameAs, foundingDate | Yes |
| **Product** | name, description, image, price, availability, brand | Yes |
| **Article** | headline, author, datePublished, image, publisher | Yes |
| **FAQ** | questions (question + answer pairs) | Yes |
| **HowTo** | name, steps (name + text), totalTime | Yes |
| **LocalBusiness** | name, address, telephone, openingHours, geo | Yes |
| **Event** | name, startDate, location, description, offers | Yes |
| **WebSite** | name, url, potentialAction (SearchAction) | Yes (Sitelinks) |
| **BreadcrumbList** | items (name + url position pairs) | Yes |
| **VideoObject** | name, description, thumbnailUrl, uploadDate, duration | Yes |
| **SoftwareApplication** | name, operatingSystem, applicationCategory, offers | Yes |

## How to Generate

When asked to generate schema markup:

1. Identify which schema type is needed based on the user's request
2. Ask for the required fields (or extract from context)
3. Generate valid JSON-LD with:
   - `@context`: always `https://schema.org`
   - `@type`: the schema type name
   - All provided fields properly formatted
4. Output in a code block with `json` syntax highlighting
5. Wrap in `<script type="application/ld+json">` tags for HTML insertion

## Output Format

Always output like this:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "John Doe",
  "jobTitle": "Software Engineer",
  "url": "https://johndoe.com",
  "sameAs": [
    "https://linkedin.com/in/johndoe",
    "https://twitter.com/johndoe"
  ]
}
</script>
```

## Important Notes

- Always include `@context: "https://schema.org"`
- Remove empty/null fields from output
- For FAQ schema: each question needs both `@type: "Question"` and an `acceptedAnswer` with `@type: "Answer"`
- For HowTo: each step needs `@type: "HowToStep"`
- For BreadcrumbList: each item needs `@type: "ListItem"` with `position` (number)
- Validate at: https://search.google.com/test/rich-results
- For addresses: use `@type: "PostalAddress"` with streetAddress, addressLocality, addressRegion, postalCode, addressCountry
- For geo: use `@type: "GeoCoordinates"` with latitude, longitude
