# Schema Markup Examples

Complete JSON-LD templates for the most common schema.org types. Copy, customize the placeholder values, and paste into your page's `<head>` or before `</body>`.

---

## 1. Organization

Use on company homepages and about pages. Enables Knowledge Panel in search results.

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Acme Corporation",
  "url": "https://www.example.com",
  "logo": "https://www.example.com/images/logo.png",
  "description": "Brief description of what the company does.",
  "foundingDate": "2020-01-15",
  "sameAs": [
    "https://twitter.com/acmecorp",
    "https://www.linkedin.com/company/acmecorp",
    "https://github.com/acmecorp"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+1-555-123-4567",
    "contactType": "customer service",
    "availableLanguage": ["English"],
    "areaServed": "US"
  },
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main Street",
    "addressLocality": "San Francisco",
    "addressRegion": "CA",
    "postalCode": "94105",
    "addressCountry": "US"
  }
}
```

**Required:** `name`, `url`
**Recommended:** `logo`, `sameAs`, `contactPoint`, `description`

---

## 2. WebSite + SearchAction

Use on the homepage to enable sitelinks search box in search results.

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Acme Corporation",
  "url": "https://www.example.com",
  "potentialAction": {
    "@type": "SearchAction",
    "target": {
      "@type": "EntryPoint",
      "urlTemplate": "https://www.example.com/search?q={search_term_string}"
    },
    "query-input": "required name=search_term_string"
  }
}
```

**Required:** `name`, `url`
**For search box:** `potentialAction` with `SearchAction`

---

## 3. Article / BlogPosting

Use on blog posts and news articles. Enables article rich results with headline, image, and date.

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "How to Implement Schema Markup for Better SEO",
  "description": "A complete guide to adding structured data to your website.",
  "image": [
    "https://www.example.com/images/article-hero-16x9.jpg",
    "https://www.example.com/images/article-hero-4x3.jpg",
    "https://www.example.com/images/article-hero-1x1.jpg"
  ],
  "datePublished": "2025-01-15T08:00:00+00:00",
  "dateModified": "2025-02-01T10:30:00+00:00",
  "author": {
    "@type": "Person",
    "name": "Jane Smith",
    "url": "https://www.example.com/authors/jane-smith"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Acme Corporation",
    "logo": {
      "@type": "ImageObject",
      "url": "https://www.example.com/images/logo.png"
    }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://www.example.com/blog/schema-markup-guide"
  },
  "wordCount": 2500,
  "keywords": ["schema markup", "SEO", "structured data", "JSON-LD"]
}
```

**Required:** `headline`, `image`, `datePublished`, `author`
**Recommended:** `dateModified`, `publisher`, `description`
**Note:** Use `BlogPosting` instead of `Article` for blog posts. Use `NewsArticle` for news.

---

## 4. Product

Use on individual product pages. Enables product rich results with price, availability, and ratings.

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Wireless Bluetooth Headphones",
  "description": "Premium noise-cancelling wireless headphones with 30-hour battery life.",
  "image": [
    "https://www.example.com/images/headphones-front.jpg",
    "https://www.example.com/images/headphones-side.jpg"
  ],
  "sku": "WBH-PRO-2025",
  "mpn": "925872",
  "brand": {
    "@type": "Brand",
    "name": "AudioPro"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://www.example.com/products/wireless-headphones",
    "price": "149.99",
    "priceCurrency": "USD",
    "priceValidUntil": "2025-12-31",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition",
    "seller": {
      "@type": "Organization",
      "name": "Acme Electronics"
    },
    "shippingDetails": {
      "@type": "OfferShippingDetails",
      "shippingRate": {
        "@type": "MonetaryAmount",
        "value": "0",
        "currency": "USD"
      },
      "deliveryTime": {
        "@type": "ShippingDeliveryTime",
        "handlingTime": {
          "@type": "QuantitativeValue",
          "minValue": 0,
          "maxValue": 1,
          "unitCode": "DAY"
        },
        "transitTime": {
          "@type": "QuantitativeValue",
          "minValue": 2,
          "maxValue": 5,
          "unitCode": "DAY"
        }
      },
      "shippingDestination": {
        "@type": "DefinedRegion",
        "addressCountry": "US"
      }
    }
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.7",
    "reviewCount": "342",
    "bestRating": "5",
    "worstRating": "1"
  },
  "review": [
    {
      "@type": "Review",
      "reviewRating": {
        "@type": "Rating",
        "ratingValue": "5",
        "bestRating": "5"
      },
      "author": {
        "@type": "Person",
        "name": "Alex Johnson"
      },
      "datePublished": "2025-01-10",
      "reviewBody": "Best headphones I've ever owned. The noise cancellation is incredible."
    }
  ]
}
```

**Required:** `name`, `image`, `offers` (with `price` + `availability`)
**Recommended:** `sku`, `brand`, `aggregateRating`, `review`
**Availability values:** `InStock`, `OutOfStock`, `PreOrder`, `BackOrder`, `Discontinued`

---

## 5. SoftwareApplication

Use on SaaS product pages, app landing pages, or download pages.

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "ProjectFlow",
  "description": "Project management software for agile teams.",
  "url": "https://www.example.com",
  "applicationCategory": "BusinessApplication",
  "operatingSystem": "Web, iOS, Android",
  "offers": {
    "@type": "AggregateOffer",
    "lowPrice": "0",
    "highPrice": "49",
    "priceCurrency": "USD",
    "offerCount": "3"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "ratingCount": "1250"
  },
  "screenshot": "https://www.example.com/images/app-screenshot.png",
  "featureList": "Task management, Kanban boards, Time tracking, Reporting"
}
```

**Required:** `name`, `offers`
**Recommended:** `aggregateRating`, `applicationCategory`, `operatingSystem`
**Application categories:** `BusinessApplication`, `DeveloperApplication`, `EducationalApplication`, `GameApplication`

---

## 6. FAQPage

Use on FAQ pages or any page with question-and-answer content. Enables FAQ rich results with expandable questions in search.

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is schema markup?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Schema markup is structured data vocabulary that helps search engines understand the content on your web pages. It uses schema.org types implemented in JSON-LD format to describe entities like products, articles, organizations, and FAQs."
      }
    },
    {
      "@type": "Question",
      "name": "How do I add schema markup to my website?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Add a <code>&lt;script type=\"application/ld+json\"&gt;</code> tag to your page's HTML containing the JSON-LD structured data. Place it in the <code>&lt;head&gt;</code> section or before the closing <code>&lt;/body&gt;</code> tag."
      }
    },
    {
      "@type": "Question",
      "name": "Does schema markup improve SEO rankings?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Schema markup doesn't directly boost rankings, but it can improve click-through rates by enabling rich results (stars, prices, FAQs) in search listings. Rich results make your listing more visually prominent, which can lead to more clicks."
      }
    }
  ]
}
```

**Required:** `mainEntity` (array of `Question` objects with `acceptedAnswer`)
**Note:** FAQPage content must be visible on the page. Don't mark up content that doesn't appear to users.
**HTML in answers:** You can include basic HTML (`<a>`, `<br>`, `<p>`, `<code>`, lists) in answer text.

---

## 7. HowTo

Use on tutorial and instructional pages. Enables how-to rich results with step-by-step instructions.

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to Add Schema Markup to a Next.js Application",
  "description": "Step-by-step guide to implementing JSON-LD structured data in a Next.js app.",
  "totalTime": "PT15M",
  "estimatedCost": {
    "@type": "MonetaryAmount",
    "currency": "USD",
    "value": "0"
  },
  "tool": [
    { "@type": "HowToTool", "name": "Code editor (VS Code)" },
    { "@type": "HowToTool", "name": "Next.js project" }
  ],
  "step": [
    {
      "@type": "HowToStep",
      "position": 1,
      "name": "Create a schema component",
      "text": "Create a new file called JsonLd.tsx in your components directory.",
      "url": "https://www.example.com/guides/nextjs-schema#step-1",
      "image": "https://www.example.com/images/step1.png"
    },
    {
      "@type": "HowToStep",
      "position": 2,
      "name": "Define the schema data",
      "text": "Create a TypeScript interface for your schema type and populate it.",
      "url": "https://www.example.com/guides/nextjs-schema#step-2"
    },
    {
      "@type": "HowToStep",
      "position": 3,
      "name": "Add to your page layout",
      "text": "Import the JsonLd component and pass the schema data as a prop.",
      "url": "https://www.example.com/guides/nextjs-schema#step-3"
    },
    {
      "@type": "HowToStep",
      "position": 4,
      "name": "Validate with Rich Results Test",
      "text": "Open Google's Rich Results Test, enter your URL, and verify.",
      "url": "https://www.example.com/guides/nextjs-schema#step-4"
    }
  ]
}
```

**Required:** `name`, `step` (array of `HowToStep` with `text`)
**Recommended:** `totalTime` (ISO 8601 duration), `image`, `estimatedCost`
**Duration format:** `PT15M` = 15 minutes, `PT1H30M` = 1 hour 30 minutes

---

## 8. BreadcrumbList

Use on any page with breadcrumb navigation. Enables breadcrumb trails in search results.

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://www.example.com"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Products",
      "item": "https://www.example.com/products"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "Headphones",
      "item": "https://www.example.com/products/headphones"
    },
    {
      "@type": "ListItem",
      "position": 4,
      "name": "Wireless Bluetooth Headphones"
    }
  ]
}
```

**Required:** `itemListElement` (array of `ListItem` with `position` and `name`)
**Note:** The last item (current page) should omit the `item` URL. All other items must include `item`.

---

## 9. LocalBusiness

Use on local business pages (restaurants, stores, offices). Enables local business Knowledge Panel and Maps integration.

```json
{
  "@context": "https://schema.org",
  "@type": "Restaurant",
  "name": "The Golden Fork",
  "description": "Farm-to-table Italian restaurant in downtown San Francisco.",
  "url": "https://www.goldenfork.com",
  "telephone": "+1-555-987-6543",
  "image": "https://www.goldenfork.com/images/restaurant.jpg",
  "priceRange": "$$",
  "servesCuisine": ["Italian", "Mediterranean"],
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "456 Market Street",
    "addressLocality": "San Francisco",
    "addressRegion": "CA",
    "postalCode": "94105",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 37.7749,
    "longitude": -122.4194
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "11:00",
      "closes": "22:00"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Saturday", "Sunday"],
      "opens": "10:00",
      "closes": "23:00"
    }
  ],
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.5",
    "reviewCount": "287"
  },
  "hasMenu": "https://www.goldenfork.com/menu"
}
```

**Required:** `name`, `address`
**Recommended:** `geo`, `openingHoursSpecification`, `telephone`, `image`
**Subtypes:** Use specific types like `Restaurant`, `Dentist`, `AutoRepair`, `LegalService` instead of generic `LocalBusiness`.

---

## 10. Event

Use for events, webinars, conferences, and meetups. Enables event rich results with date, location, and ticket info.

```json
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "Web Performance Summit 2025",
  "description": "Annual conference on web performance optimization and Core Web Vitals.",
  "url": "https://www.example.com/events/web-perf-summit-2025",
  "image": "https://www.example.com/images/event-banner.jpg",
  "startDate": "2025-09-15T09:00:00-07:00",
  "endDate": "2025-09-17T17:00:00-07:00",
  "eventStatus": "https://schema.org/EventScheduled",
  "eventAttendanceMode": "https://schema.org/MixedEventAttendanceMode",
  "location": [
    {
      "@type": "Place",
      "name": "Moscone Center",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "747 Howard Street",
        "addressLocality": "San Francisco",
        "addressRegion": "CA",
        "postalCode": "94103",
        "addressCountry": "US"
      }
    },
    {
      "@type": "VirtualLocation",
      "url": "https://www.example.com/events/web-perf-summit-2025/livestream"
    }
  ],
  "organizer": {
    "@type": "Organization",
    "name": "Web Performance Community",
    "url": "https://www.example.com"
  },
  "performer": [
    {
      "@type": "Person",
      "name": "Sarah Chen",
      "url": "https://www.example.com/speakers/sarah-chen"
    }
  ],
  "offers": {
    "@type": "Offer",
    "url": "https://www.example.com/events/tickets",
    "price": "299",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "validFrom": "2025-05-01T00:00:00-07:00"
  }
}
```

**Required:** `name`, `startDate`, `location`
**Recommended:** `endDate`, `offers`, `image`, `organizer`, `eventStatus`
**Event status values:** `EventScheduled`, `EventCancelled`, `EventPostponed`, `EventRescheduled`
**Attendance modes:** `OfflineEventAttendanceMode`, `OnlineEventAttendanceMode`, `MixedEventAttendanceMode`

---

## 11. VideoObject

Use on pages with video content. Enables video rich results with thumbnail and duration.

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "Getting Started with Schema Markup",
  "description": "Learn how to add structured data to your website in 10 minutes.",
  "thumbnailUrl": "https://www.example.com/images/video-thumbnail.jpg",
  "uploadDate": "2025-01-20T08:00:00+00:00",
  "duration": "PT10M30S",
  "contentUrl": "https://www.example.com/videos/schema-markup-intro.mp4",
  "embedUrl": "https://www.youtube.com/embed/abc123",
  "interactionStatistic": {
    "@type": "InteractionCounter",
    "interactionType": { "@type": "WatchAction" },
    "userInteractionCount": 15000
  },
  "publisher": {
    "@type": "Organization",
    "name": "Acme Corporation",
    "logo": {
      "@type": "ImageObject",
      "url": "https://www.example.com/images/logo.png"
    }
  }
}
```

**Required:** `name`, `thumbnailUrl`, `uploadDate`
**Recommended:** `description`, `duration`, `contentUrl` or `embedUrl`
**Duration format:** `PT10M30S` = 10 minutes 30 seconds

---

## 12. Multi-Schema with @graph

Combine multiple schema types on a single page using `@graph`. Common for pages that represent multiple entities.

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://www.example.com/#organization",
      "name": "Acme Corporation",
      "url": "https://www.example.com",
      "logo": "https://www.example.com/images/logo.png"
    },
    {
      "@type": "WebSite",
      "@id": "https://www.example.com/#website",
      "name": "Acme Corporation",
      "url": "https://www.example.com",
      "publisher": { "@id": "https://www.example.com/#organization" }
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.example.com" },
        { "@type": "ListItem", "position": 2, "name": "Blog", "item": "https://www.example.com/blog" },
        { "@type": "ListItem", "position": 3, "name": "Schema Markup Guide" }
      ]
    },
    {
      "@type": "Article",
      "headline": "Complete Guide to Schema Markup",
      "image": "https://www.example.com/images/article-hero.jpg",
      "datePublished": "2025-01-15T08:00:00+00:00",
      "dateModified": "2025-02-01T10:00:00+00:00",
      "author": {
        "@type": "Person",
        "name": "Jane Smith"
      },
      "publisher": { "@id": "https://www.example.com/#organization" },
      "isPartOf": { "@id": "https://www.example.com/#website" }
    }
  ]
}
```

**Key concepts:**
- Use `@id` to create referenceable entities (organization defined once, referenced by article and website)
- Use `@graph` to combine multiple schema types in a single `<script>` tag
- Link entities with `{ "@id": "..." }` references instead of duplicating data

---

## Common Validation Errors

| Error | Cause | Fix |
|-------|-------|-----|
| Missing required field | Required property not included | Add the missing property (check type docs) |
| Invalid URL | Relative URL or malformed URL | Use fully qualified URLs (`https://...`) |
| Invalid date format | Date not in ISO 8601 | Use `YYYY-MM-DDTHH:MM:SS+00:00` format |
| Invalid enum value | Wrong value for enumerated types | Use exact schema.org URLs (e.g., `https://schema.org/InStock`) |
| Content mismatch | Schema doesn't match visible page content | Ensure schema data reflects actual page content |
| Invalid price | Price with currency symbol or commas | Use numeric value only (`"149.99"`, not `"$149.99"`) |
| Missing image | No image property on types that require it | Add at least one image URL |
| Self-referencing errors | Circular `@id` references | Ensure `@id` chains don't form loops |

---

## Implementation Patterns

### Next.js / React Server Component

```tsx
// components/JsonLd.tsx
export function JsonLd({ data }: { data: Record<string, unknown> }) {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
    />
  );
}

// app/page.tsx
import { JsonLd } from '@/components/JsonLd';

export default function HomePage() {
  const schema = {
    "@context": "https://schema.org",
    "@type": "Organization",
    name: "Acme Corporation",
    url: "https://www.example.com",
  };

  return (
    <>
      <JsonLd data={schema} />
      <main>{/* page content */}</main>
    </>
  );
}
```

### Dynamic Product Schema (Server Component)

```tsx
// app/products/[slug]/page.tsx
import { JsonLd } from '@/components/JsonLd';
import { getProduct } from '@/lib/products';

export default async function ProductPage({ params }: { params: { slug: string } }) {
  const product = await getProduct(params.slug);

  const schema = {
    "@context": "https://schema.org",
    "@type": "Product",
    name: product.name,
    description: product.description,
    image: product.images,
    sku: product.sku,
    brand: { "@type": "Brand", name: product.brand },
    offers: {
      "@type": "Offer",
      price: product.price.toString(),
      priceCurrency: "USD",
      availability: product.inStock
        ? "https://schema.org/InStock"
        : "https://schema.org/OutOfStock",
    },
  };

  return (
    <>
      <JsonLd data={schema} />
      <main>{/* product content */}</main>
    </>
  );
}
```

---

## Quick Reference

| Schema Type | Primary Use | Rich Result |
|-------------|------------|-------------|
| Organization | Company homepage/about | Knowledge Panel |
| WebSite | Homepage with search | Sitelinks Search Box |
| Article | Blog posts, news | Article carousel, headline + date |
| Product | Product pages | Price, availability, ratings |
| SoftwareApplication | SaaS / app pages | App info, ratings |
| FAQPage | FAQ content | Expandable Q&A in search |
| HowTo | Tutorials, guides | Step-by-step instructions |
| BreadcrumbList | Any page with breadcrumbs | Breadcrumb trail in search |
| LocalBusiness | Local stores, restaurants | Maps, hours, contact info |
| Event | Events, webinars | Date, location, ticket info |
| VideoObject | Video content pages | Video thumbnail, duration |
