# Schema Markup Templates

Copy and customize these JSON-LD templates for each article.

## Article Schema

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "ARTICLE_TITLE",
  "description": "META_DESCRIPTION",
  "author": {
    "@type": "Person",
    "name": "AUTHOR_NAME",
    "url": "AUTHOR_URL"
  },
  "publisher": {
    "@type": "Organization",
    "name": "SITE_NAME",
    "url": "SITE_URL"
  },
  "datePublished": "YYYY-MM-DD",
  "dateModified": "YYYY-MM-DD",
  "mainEntityOfPage": "PAGE_URL"
}
```

## FAQ Schema

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "QUESTION_1",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "ANSWER_1"
      }
    },
    {
      "@type": "Question",
      "name": "QUESTION_2",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "ANSWER_2"
      }
    }
  ]
}
```

## HowTo Schema

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "HOW_TO_TITLE",
  "description": "DESCRIPTION",
  "step": [
    {
      "@type": "HowToStep",
      "name": "STEP_NAME",
      "text": "STEP_DESCRIPTION"
    }
  ]
}
```

## BreadcrumbList Schema

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "SITE_URL"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Blog",
      "item": "SITE_URL/blog"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "ARTICLE_TITLE",
      "item": "PAGE_URL"
    }
  ]
}
```

## Usage Notes

- Place all schema in a single `<script type="application/ld+json">` tag in the page head
- Multiple schemas can be combined in a JSON array: `[{...}, {...}]`
- Test with Google Rich Results Test: https://search.google.com/test/rich-results
- Article + FAQ + Breadcrumb is the standard combo for blog posts
- Add HowTo only for genuine step-by-step tutorials
