# Accessibility checks (WCAG 2.2)

**Scripts:** `check_html.py` covers the static-HTML list below. `check_rendered.py` (Tier C) covers the rendered list via Lighthouse's accessibility audits. Anything neither script ran stays under Not checked.

Automated and static checks catch only part of real accessibility problems. Say so in the report.

## Checkable from static HTML (A)
- `<html lang>` present and valid (WCAG 3.1.1).
- Page has a meaningful `<title>` (2.4.2).
- Images: informative images have alt text; decorative ones use `alt=""` (1.1.1).
- Form controls have programmatic labels (`<label for>`, `aria-label`), not placeholder-only (1.3.1, 3.3.2, 4.1.2).
- Links and buttons have accessible names; flag empty links and icon-only buttons without a label (2.4.4, 4.1.2).
- Heading structure is logical; landmarks (`main`, `nav`, `header`, `footer`) present (1.3.1, 2.4.1); skip link on content-heavy pages.
- Viewport meta does not disable zoom (`user-scalable=no`, tiny `maximum-scale`) (1.4.4).
- `tabindex` greater than 0; `aria-hidden="true"` on focusable elements; ARIA roles that contradict the element.
- Data tables have header cells (`th`, `scope`); video has captions or a transcript link.

## Needs a rendered browser or axe-core (C)
- Color contrast (1.4.3, 1.4.11), visible focus (2.4.7, 2.4.11), keyboard traps and tab order (2.1.1, 2.1.2), reflow at 320px width (1.4.10), text spacing (1.4.12), motion and autoplay.
- `check_rendered.py` runs Lighthouse's automated accessibility audits (axe-based): every failing binary audit becomes an `a11y.<audit-id>` issue with the failing elements as evidence — this includes color contrast. Audits Lighthouse marks *manual* cannot be automated; the script lists them under `accessibility_manual_checks_not_done`, and they belong in **Not checked** (keyboard traps and focus order are among them — a passing Lighthouse run does not prove keyboard access).
- If Tier C is unavailable, list all of these under **Not checked**.

## Reporting
Cite the WCAG criterion with each finding. Group repeated issues (for example, "23 images missing alt, all in the gallery template") instead of listing every instance.
