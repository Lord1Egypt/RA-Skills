# SEO_RULES — Socialphoto (v0.9)

**Primary Intent:** Navigational / Brand
**Word Count Target:** 100–200 words (caption)
**Schema Required:** `ImageObject`, only if published on the web — confirmed as the correct type
in `SEO_CHECKS/schema-markup.md`'s Master Schema Map and Stacking Order table. **Note:** that
file has no worked `### Full Template` JSON-LD example for this type (unlike Product/Article/
Event/FAQPage/BreadcrumbList) — required fields are listed directly below instead.

---

## Do's

- **Title tag**: short, keyword-rich ("Sustainable Water Bottle | EcoFriendly Gear")
- **Alt text**: present on every image, primary keyword in the main image's alt text
- **Caption**: 100–200 words, describes the visual + product name
- **Hashtags**: platform-specific, 1–2 relevant tags
- **Link integration**: descriptive anchor text linking to the product page
- **Visual SEO**: alt text matches the actual image content

## Don'ts

- Do not ship an image without alt text — critical accessibility violation and missed image traffic
- Do not stuff more than 5 hashtags — reduces engagement, reads as spam
- Do not use generic titles like "Cool Product Photo" — fails search intent
- Do not omit the brand name from the description/tagline
- Do not hide the CTA in non-descriptive anchor text ("click here")

## Required Elements

1. `alt` attribute present on every image
2. Primary keyword in the main image's `alt` text
3. Caption present (100–200w)
4. `ImageObject` schema present if published on the web
5. `ImageObject` schema contains `url`, `name`, `description`, `author`

## Recommended Elements

6. Caption contains 1–2 relevant hashtags
7. Caption contains a CTA or question to drive engagement
8. Image file name is descriptive (not `IMG_4821.jpg`)
9. Image dimensions match the target platform's spec
10. Geographic tag if location-relevant

---

*Migrated from `SEO_CHECKS/do-and-don-lists.md` §5 and `SEO_CHECKS/page-type-specific-checks.md`
§Socialphoto. Audit scoring (HARD FAIL/WARNING) stays in `SEO_CHECKS/page-type-specific-checks.md`.*

*Last updated: 2026-08-24 (v0.9)*
*Maintainer: Chris — Socialphoto writing rules*
