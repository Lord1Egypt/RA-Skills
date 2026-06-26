# Changelog

## v1.0.0 (2026-05-26)

Initial release. You can now run `/thumbnail-qa` to automatically detect and fix poorly cropped images across your Next.js site.

- **Image registry** -- scans your codebase for `<Image fill>` components, resolves dynamic sources and conditional classNames, and builds a complete inventory of every thumbnail candidate
- **Focal point analysis** -- classifies each image by type (portrait, group, architecture, event, landscape) and computes optimal `object-position` values based on where the subject actually is
- **Before/after verification** -- every fix is screenshot-verified; if the computed position makes things worse, it's reverted and flagged for manual review
- **Atomic commits** -- each image fix gets its own commit with a descriptive message, so you can cherry-pick or revert individual changes
- **Structured reports** -- generates a full QA report with results for every image, saved to `.gstack/thumbnail-qa/`

### Supported patterns

- Static className strings (`className="object-center"`)
- Conditional ternaries keyed on data fields (`category.id === 'worship' ? 'object-top' : 'object-center'`)
- Arbitrary Tailwind values (`object-[50%_25%]`)
- Position maps for multi-image components

### Requirements

- [gstack](https://github.com/garrytan/gstack) (provides the `browse` headless browser)
- Next.js project with `<Image fill>` components
