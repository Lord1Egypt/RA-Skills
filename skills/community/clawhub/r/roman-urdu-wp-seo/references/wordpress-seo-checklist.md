# WordPress SEO Checklist

Use this checklist for a WordPress post or page before publication. Verify the active theme, SEO plugin, hosting setup, and site policy instead of assuming a default configuration.

## Metadata and indexing

| Check | What to verify | Expected action |
| --- | --- | --- |
| SEO title | The English keyword core is present, the promise is accurate, and the wording is readable. | Set one title in the active SEO plugin; remove duplicate title templates if the theme adds another one. |
| Meta description | One useful benefit, one natural mixed-language phrase where relevant, and no unsupported claims. | Save in Yoast or Rank Math and preview the snippet. |
| Focus keyphrase | One primary English keyword is selected; Roman Urdu variants are treated as supporting language rather than a keyword dump. | Add the primary keyphrase in the plugin and use variants naturally in headings or copy. |
| Canonical | The page points to its preferred URL and does not self-conflict with archives or parameters. | Inspect the canonical field and any site-wide canonical rules. |
| Indexability | No accidental `noindex`, blocked resource, password protection, or draft-only setting remains. | Check WordPress visibility, SEO plugin robots settings, and HTTP headers. |
| Search appearance | The title, description, URL, and social sharing fields match the page's actual content. | Preview on desktop and mobile; edit for clarity, not only pixel count. |

## URL and structure

- Use a short, lowercase, hyphenated permalink that is stable after publication.
- Keep the English keyword core in the slug when it improves clarity. Do not place a long Roman Urdu sentence in the URL.
- Use one clear H1 supplied by the post title. Keep H2 and H3 headings hierarchical and descriptive.
- Link to relevant cornerstone pages and related posts using descriptive anchor text. Do not repeat the exact anchor unnaturally.
- Check that category, tag, author, date, and search-result archives do not create avoidable duplicate or thin pages.

## Yoast SEO and Rank Math compatibility

Do not assume both plugins are installed. First identify the active plugin and theme.

| Scenario | Yoast SEO | Rank Math |
| --- | --- | --- |
| Focus keyword | Use the focus keyphrase field as a primary editorial aid, not a score target. | Use the focus keyword field as an editorial aid and review the generated suggestions. |
| Meta title/description | Edit the SEO title and meta description fields in the snippet editor. | Edit the SEO title and description fields in the snippet preview. |
| Schema | Confirm the post type and author/date fields are correct. | Confirm the selected Schema Generator type and required fields. |
| XML sitemap | Inspect the sitemap index and excluded content types. | Inspect sitemap settings and excluded post types. |
| Social cards | Verify Open Graph and X/Twitter fields if custom values are needed. | Verify social metadata fields and fallback images. |
| Redirections | Use an existing redirect manager or site policy; avoid creating duplicate redirect rules. | Review redirection modules only if enabled and governed by the site's policy. |

Never install, disable, or reconfigure a plugin as part of an audit unless the site owner explicitly authorizes it.

## Images and media

- Give each meaningful image concise, accurate alt-text that describes its function or content.
- Suggest Roman Urdu alt-text only when it describes the image naturally for the intended audience. For example, `30 hazar ke andar smartphone ka comparison chart` is useful for a chart if the chart actually contains that comparison.
- Use empty alt-text for decorative images when appropriate; do not force keywords into decorative-image attributes.
- Compress images, choose a suitable format, define dimensions, and check lazy-loading behavior without harming above-the-fold content.
- Ensure captions, visible labels, and image text are accessible as HTML where the information matters.

## Schema and sitemap

- Select schema that matches the content: Article, BlogPosting, Recipe, Product, FAQPage, HowTo, or another legitimate type.
- Populate schema from visible, accurate page content. Do not add reviews, prices, dates, or FAQs that are not actually present.
- For recipes, keep ingredients, instructions, times, yield, and images consistent between the page and structured data.
- For products, verify price, availability, currency, and brand/model details.
- Confirm the XML sitemap contains the canonical, indexable URL and excludes drafts, private pages, and intentional noindex content.
- Check that the sitemap is reachable and submitted through the site's configured webmaster tools when authorized.

## Performance, accessibility, and localization

- Test mobile layout, tap targets, font rendering, contrast, and language readability.
- Check Core Web Vitals or the site's performance monitoring workflow after image and plugin changes.
- Use `lang` attributes and visible language choices consistently with the site's editorial policy.
- Keep Roman Urdu phrases understandable to readers who know Urdu but read Latin script; preserve English terms where they are standard.
- Confirm date, currency, units, timezone, and Pakistan-specific claims where the post uses local context.

## Pre-publish sign-off

Record the reviewer, date, target audience, primary keyword, approved variants, active SEO plugin, canonical URL, schema type, sitemap result, image review, and any remaining assumption. Re-check time-sensitive pricing, schedules, rankings, health guidance, legal requirements, and product availability immediately before publication.
