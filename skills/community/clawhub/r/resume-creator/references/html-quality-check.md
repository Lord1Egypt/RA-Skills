# HTML Resume Quality Check

Use this checklist for the final review of every generated or materially edited
single-file HTML resume. It complements structural validation; do not treat a
passing HTML parse as proof of a usable layout.

## Inspect after rendering

Open the local file in a browser or equivalent renderer and inspect a desktop
view, a narrow view, and the print layout when printing is part of the request.
Check the beginning, a dense middle section, and the final section of every
language version. If a browser check is unavailable, say so rather than
claiming visual validation.

- **Prose:** For a long, full-width summary paragraph, use a deliberate text
  alignment. When the chosen visual style calls for justification, apply it
  only to continuous prose, use `inter-ideograph` for Chinese, and do not
  justify headings, metadata, short labels, bullets, or skill chips.
- **Experience and projects:** Each item header must have exactly two intended
  visual regions: title and optional role on the left, date/status on the
  right. Verify that its list begins below the header, not alongside it.
  Inspect the final item in each repeated section, which is especially prone
  to an unclosed or misplaced wrapper.
- **Alignment:** Confirm dates share a right edge at wide sizes; long titles
  wrap inside their own column without pushing dates into the prose; on narrow
  screens dates intentionally stack below the title and remain left-aligned.
- **Continuity:** Check that repeated cards or timeline items use the same
  indentation, marker position, bullet spacing, and section rhythm. Check
  that no content is clipped, overlaps, overflows horizontally, or becomes
  hidden at the narrow breakpoint.
- **Print:** Confirm A4 or Letter settings requested by the user, legible
  margins, and that an item is not split internally where the browser supports
  `break-inside: avoid`. State the real page count only if a PDF was generated
  and inspected.

## Structural companion checks

Use a parser or focused inspection to confirm every `.item-head` has the
expected closing structure and that no achievement list is nested inside the
header grid. Also check for one inline style block, no unintended scripts or
external stylesheets, sequential headings, and the expected language anchors.

## Deployment companion checks (only when deployment is authorized)

Keep local-file and public-site acceptance separate. A successful upload or
HTTP response does not prove the intended public resume is rendered.

- **Privacy:** Before publishing, confirm which contact details may be public.
  For a public variant, inspect the fetched HTML for omitted phone, email,
  address, or other fields the user chose to withhold; check both language
  versions and `tel:`/`mailto:` links.
- **Source-to-public identity:** Fetch the final public page over HTTPS and
  compare its content hash (or another deterministic content identity) with
  the deployed single-file source. Record a mismatch as a deployment failure,
  cache issue, or transformation to investigate.
- **Domain readiness:** For a custom domain, validate the exact DNS record,
  certificate status, and an HTTPS `200` response. Do not treat a provider
  hostname as proof that the custom domain is ready.
- **Clean visual render:** Inspect the public URL in a clean or extension-free
  browser/profile at desktop and narrow widths. Check element dimensions for
  nonzero readable widths, expected text only once, no unexpected injected
  nodes, no horizontal overflow, and no clipped content. Browser extensions
  can mutate a page after delivery; compare a clean render with the affected
  browser before changing the source.
- **Operational boundary:** Deploy only after explicit authorization. Report
  the public URL, the checks actually run, and any unverified viewer-specific
  behavior; do not claim universal rendering compatibility from a single
  browser profile.
