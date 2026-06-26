# CSS Selector Reference for Web Scraping

## Basic Selectors

| Selector | Example | Description |
|----------|---------|-------------|
| `*` | `*` | Any element |
| `element` | `div`, `p`, `a` | Element by tag name |
| `.class` | `.product-title` | Element by class |
| `#id` | `#main-content` | Element by ID |
| `[attr]` | `[href]` | Element with attribute |
| `[attr=value]` | `[data-type="product"]` | Element with specific attribute value |

## Combinators

| Selector | Example | Description |
|----------|---------|-------------|
| ` ` (space) | `div p` | Descendant (any level) |
| `>` | `div > p` | Direct child |
| `+` | `h1 + p` | Adjacent sibling |
| `~` | `h1 ~ p` | General sibling |

## Attribute Selectors

```css
[href]                    /* Has href attribute */
[href="https://example.com"]  /* Exact match */
[href^="https"]           /* Starts with */
[href$=".pdf"]            /* Ends with */
[href*="example"]         /* Contains */
[class~="active"]         /* Word match in class list */
[lang|="en"]              /* Prefix match with hyphen */
```

## Pseudo-classes

```css
:first-child              /* First child element */
:last-child               /* Last child element */
:nth-child(n)             /* Nth child */
:nth-child(odd)           /* Odd children */
:nth-child(even)          /* Even children */
:first-of-type            /* First of tag type */
:last-of-type             /* Last of tag type */
:not(.hidden)             /* Not matching selector */
:contains("text")         /* Contains text (jQuery) */
```

## Common Scraping Patterns

### Product Cards
```css
.product-card             /* Container */
.product-card h2          /* Title */
.product-card .price      /* Price */
.product-card img         /* Image */
.product-card a[href]     /* Link */
```

### Article Lists
```css
article                   /* Article container */
article h1                /* Headline */
article .author           /* Author name */
article time              /* Publish date */
article .summary          /* Excerpt */
```

### Tables
```css
table tr                  /* Table row */
table tr td:first-child   /* First column */
table tr td:nth-child(2)  /* Second column */
thead th                  /* Header cells */
tbody tr                  /* Body rows */
```

### Navigation/Pagination
```css
nav a                     /* Nav links */
.pagination a             /* Pagination links */
.pagination .next         /* Next page button */
.pagination .active       /* Current page */
```

### Forms
```css
form input                /* Input fields */
form button               /* Submit button */
input[name="email"]       /* Specific input */
select option             /* Dropdown options */
```

## Extracting Attributes

```css
/* Get href from links */
a.product-link[href]

/* Get src from images */
img.product-image[src]

/* Get data attributes */
[data-product-id]
[data-price]

/* Get content from meta tags */
meta[property="og:title"][content]
```

## Tips

1. **Use browser DevTools** to test selectors before scraping
2. **Prefer specific selectors** over generic ones
3. **Avoid dynamic classes** (often contain random strings)
4. **Use attribute selectors** for more stability
5. **Test with `querySelectorAll`** in console:
   ```javascript
   $$('your-selector').length  // Count matches
   $$('your-selector')[0].innerText  // Test extraction
   ```
