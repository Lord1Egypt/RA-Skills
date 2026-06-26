# Webflow Optimization

## SEO Checklist

### Per-Page
- [ ] Unique title tag (50-60 chars)
- [ ] Meta description (150-160 chars)
- [ ] H1 present and descriptive
- [ ] Images have alt text
- [ ] Open Graph image set (1200x630px)
- [ ] Canonical URL (if duplicate content exists)

### Site-Wide
- [ ] sitemap.xml auto-generated (Site Settings → SEO)
- [ ] robots.txt configured
- [ ] 301 redirects for old URLs
- [ ] SSL enabled (automatic on Webflow hosting)
- [ ] Custom 404 page designed

### CMS SEO
- [ ] Dynamic title: `{Post Name} | {Site Name}`
- [ ] Dynamic meta from post excerpt/summary field
- [ ] Structured data for articles/products

## Performance

**Image optimization:**
- Webflow auto-compresses but not aggressively
- Use WebP format when possible
- Set explicit width/height to prevent layout shift

**Lazy loading:**
```html
<!-- Add to image embed or via attributes -->
loading="lazy"
```

**Above-the-fold:**
- First meaningful paint under 2.5s
- Don't lazy-load hero images
- Minimize custom fonts (2 weights max)

**Page weight targets:**
- Total: under 2MB
- Images: under 500KB each
- Custom code: under 100KB

## Accessibility

**Minimum requirements:**
- [ ] Sufficient color contrast (4.5:1 for text)
- [ ] Keyboard navigation works
- [ ] Focus states visible
- [ ] Form labels connected to inputs
- [ ] Skip navigation link present
- [ ] Alt text on all images

**Webflow-specific:**
- Set `aria-label` on icon-only buttons
- Use semantic HTML (section, nav, article)
- Don't disable focus outlines without replacement

## Pre-Launch Checklist

**Technical:**
- [ ] Forms tested with real submissions
- [ ] 404 page set
- [ ] Favicon uploaded (32x32, 16x16)
- [ ] Touch icon for mobile (180x180)
- [ ] SSL certificate active
- [ ] www/non-www redirect configured
- [ ] Analytics verified in real-time
- [ ] Sitemap submitted to Search Console

**Content:**
- [ ] No Lorem Ipsum remaining
- [ ] Phone numbers clickable (tel: links)
- [ ] Email addresses clickable (mailto: links)
- [ ] External links open in new tab
- [ ] Footer year is current

**Legal:**
- [ ] Privacy policy page
- [ ] Cookie consent (if required by region)
- [ ] Terms of service (if applicable)
