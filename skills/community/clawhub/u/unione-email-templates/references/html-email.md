# HTML that works in mail clients

Mail clients (Outlook for Windows renders with Word, Gmail strips `<style>` in some cases) support a small, old
subset of HTML and CSS. Build for it:

- **Layout:** tables (`<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">`), a centred
  content table 600 px wide; no flexbox, grid, `position` or floats for layout.
- **CSS:** inline styles on the elements (`style="..."`); a `<style>` block only for media queries and dark mode, as an
  enhancement. Use longhand properties, `px` units, web-safe font stacks (`Arial, Helvetica, sans-serif`).
- **Document:** `<!DOCTYPE html>`, `<html lang="…">`, `<meta charset="utf-8">`,
  `<meta name="viewport" content="width=device-width, initial-scale=1">`, a `<title>`.
- **Preheader:** the first text in `<body>`, hidden: `<div style="display:none;max-height:0;overflow:hidden">…</div>`.
- **Images:** absolute `https://` URLs (or `inline_attachments` with `cid:`), `width`/`height` attributes, `alt` text,
  `style="display:block;border:0"`; never put essential text only in an image; no SVG, no background images that
  carry meaning.
- **Buttons:** a link styled as a button inside a table cell (`<a href="…" style="display:inline-block;padding:12px 24px;…">`);
  the whole button must be the link.
- **Links:** absolute URLs; the visible text says where it goes. UniOne rewrites links for click tracking.
- **Size:** keep the HTML under ~100 KB (Gmail clips longer messages and hides the rest, including the unsubscribe link).
- **Plaintext:** always send `body.plaintext` with the same content.
- **Dark mode:** do not rely on white backgrounds; give text and backgrounds explicit colours with enough contrast.
- **Accessibility:** `lang`, real headings (`<h1>`, `<h2>`), `role="presentation"` on layout tables, a contrast ratio
  of at least 4.5:1, font size ≥ 14 px, meaningful link text.
- **No:** JavaScript, forms, iframes, embedded video, web fonts as the only font, external CSS files.

## Skeleton

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Your order has shipped</title>
</head>
<body style="margin:0;padding:0;background-color:#f4f4f5;">
  <div style="display:none;max-height:0;overflow:hidden;">Your order is on its way</div>
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f4f4f5;">
    <tr>
      <td align="center" style="padding:24px 12px;">
        <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0"
               style="width:100%;max-width:600px;background-color:#ffffff;">
          <tr>
            <td style="padding:32px;font-family:Arial,Helvetica,sans-serif;font-size:16px;line-height:24px;color:#111827;">
              <h1 style="margin:0 0 16px;font-size:24px;line-height:32px;">Hello, {{ name }}!</h1>
              <p style="margin:0 0 24px;">Order {{ order.number }} has shipped.</p>
              <table role="presentation" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td style="background-color:#2563eb;border-radius:6px;">
                    <a href="{{ order.url }}" style="display:inline-block;padding:12px 24px;color:#ffffff;
                       font-family:Arial,Helvetica,sans-serif;font-size:16px;text-decoration:none;">Track the order</a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
```

The skeleton uses Liquid (`template_engine: "liquid"`).
