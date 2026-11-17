# SEO_RULES — Socialvideo (v0.9)

**Primary Intent:** Navigational / Commercial
**Word Count Target:** 150–300 words (description)
**Schema Required:** `VideoObject`, if embedded on a webpage — confirmed as the correct type in
`SEO_CHECKS/schema-markup.md`'s Master Schema Map and Stacking Order table. **Note:** that file
has no worked `### Full Template` JSON-LD example for this type — required fields are listed
directly below instead.

---

## Do's

- **Title tag**: optimized for search + platform algorithm ("Best Hiking Water Bottles 2026 | Review")
- **Description**: primary keyword + a hook within the first 200 characters
- **VideoObject schema**: `thumbnailUrl` + `contentUrl` + `uploadDate` present if embedded on a webpage
- **Transcript timestamps**: for accessibility and search indexing
- **Alt text/description**: voiceover alt text under 100 chars describing key scenes
- **Internal linking**: link to the product page with descriptive anchor text

## Don'ts

- Do not use generic titles like "Video Review" — fails search intent
- Do not omit the thumbnail from schema — critical for platform optimization
- Do not exceed 2% keyword density in the description (spam signal)
- Do not bury the CTA link deep in the description, requiring extra clicks
- Do not skip transcript alt text — accessibility violation and missed search indexing

## Required Elements

1. Video title contains primary keyword
2. Video title is 60–70 characters
3. Description present, minimum 150w
4. Primary keyword in the first 2 sentences of the description
5. `VideoObject` schema present if embedded on a webpage
6. `VideoObject` contains `name`, `description`, `thumbnailUrl`, `uploadDate`, `duration`

## Recommended Elements

7. 5–10 relevant tags/hashtags included
8. Call to action in the description (subscribe, visit site, etc.)
9. Transcript or auto-caption enabled
10. Custom thumbnail contains a text overlay with the keyword
11. Video chapters/timestamps in the description if over 3 minutes
12. End-screen CTA and cards configured (platform-specific)

---

*Migrated from `SEO_CHECKS/do-and-don-lists.md` §6 and `SEO_CHECKS/page-type-specific-checks.md`
§Socialvideo. Audit scoring (HARD FAIL/WARNING) stays in `SEO_CHECKS/page-type-specific-checks.md`.*

*Last updated: 2026-08-24 (v0.9)*
*Maintainer: Chris — Socialvideo writing rules*
