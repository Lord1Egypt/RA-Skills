## II. On-Page SEO

### 2.1 TDH Elements (Core Strategy)

- **T = Title**: Page title containing the core keyword
- **D = Description**: Page description that attracts clicks
- **H = Headings** (H1-H6): Page heading hierarchy structure
- Note: Keywords meta tag is obsolete; use Headings instead
  - Source: "From TDK to TDH"

### 2.2 Server-Side Rendering is Essential

- **Client-side rendering = giving up SEO traffic**
- Google crawlers don't execute JavaScript; they only crawl HTML source code
- Verification method: View page source and check if page content appears in HTML tags
  - Source: "If You Don't Want Free Google Traffic, Use Client-Side Rendering"

### 2.3 Keyword Density Tips

- Use CSS Content for button text to avoid interfering with keyword density
```css
.play-button:after {
    content: "Play";
    margin-left: .5rem;
}
```
- Source: "How to Prevent Repeated Button Text from Interfering with Keyword Density"

### 2.4 Canonical Tag

- Every page must have a correct canonical tag
- Multi-language pages: Each language version's canonical should point to itself
- Wrong approach: All pages' canonicals pointing to the homepage
  - Source: "Revisiting the Canonical Tag"

---
