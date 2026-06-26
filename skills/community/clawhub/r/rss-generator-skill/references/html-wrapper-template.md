# HTML Feed Discovery Wrapper Template (v1.0.0)

When the user requests a self-hostable feed page (`/mode both` or `T5`),
generate this HTML file alongside the raw XML. It serves two purposes:

1. Browser-friendly landing page that humans can read
2. Embeds a `<link rel="alternate">` tag so feed readers auto-discover the feed

---

## Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{channel_title}} — Feed</title>

  <!--
    Feed readers and browsers look for this tag to auto-discover the feed.
    Update href to wherever you host the .xml file.
  -->
  <link rel="alternate"
        type="application/rss+xml"
        title="{{channel_title}}"
        href="{{feed_xml_url}}">

  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: system-ui, -apple-system, sans-serif;
      background: #f8f9fa;
      color: #212529;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 2rem;
    }
    .card {
      background: #fff;
      border-radius: 12px;
      box-shadow: 0 4px 24px rgba(0,0,0,.08);
      max-width: 540px;
      width: 100%;
      padding: 2.5rem;
    }
    .feed-icon {
      width: 48px; height: 48px;
      background: #f26522;
      border-radius: 10px;
      display: flex; align-items: center; justify-content: center;
      margin-bottom: 1.25rem;
    }
    .feed-icon svg { fill: #fff; }
    h1 { font-size: 1.4rem; line-height: 1.3; margin-bottom: .5rem; }
    .source-url {
      font-size: .85rem;
      color: #6c757d;
      word-break: break-all;
      margin-bottom: 1.5rem;
    }
    .btn {
      display: inline-block;
      padding: .65rem 1.25rem;
      border-radius: 8px;
      font-size: .9rem;
      font-weight: 600;
      text-decoration: none;
      transition: filter .15s;
      margin-right: .5rem; margin-bottom: .5rem;
    }
    .btn:hover { filter: brightness(.9); }
    .btn-primary  { background: #f26522; color: #fff; }
    .btn-secondary { background: #e9ecef; color: #212529; }
    .meta {
      margin-top: 1.75rem;
      padding-top: 1.25rem;
      border-top: 1px solid #dee2e6;
      font-size: .8rem;
      color: #adb5bd;
    }
    .meta a { color: inherit; }
  </style>
</head>
<body>
  <div class="card">

    <div class="feed-icon">
      <!-- RSS icon -->
      <svg width="28" height="28" viewBox="0 0 24 24">
        <path d="M6.18 15.64a2.18 2.18 0 0 1 2.18 2.18C8.36 19.01 7.38 20 6.18
                 20C4.98 20 4 19.01 4 17.82a2.18 2.18 0 0 1 2.18-2.18M4
                 4.44A15.56 15.56 0 0 1 19.56 20h-2.83A12.73 12.73 0 0 0 4
                 7.27V4.44m0 5.66a9.9 9.9 0 0 1 9.9 9.9h-2.83A7.07 7.07 0 0 0
                 4 12.93V10.1z"/>
      </svg>
    </div>

    <h1>{{channel_title}}</h1>
    <p class="source-url">Source: <a href="{{channel_url}}">{{channel_url}}</a></p>

    <p style="font-size:.95rem; line-height:1.6; margin-bottom:1.5rem;">
      {{channel_description}}
    </p>

    <a class="btn btn-primary" href="{{feed_xml_url}}">Subscribe (RSS)</a>
    <a class="btn btn-secondary" href="{{channel_url}}">Visit site</a>

    <div class="meta">
      Synthetic feed generated {{generated_date}} ·
      {{item_count}} items ·
      <a href="https://validator.w3.org/feed/check.cgi?url={{feed_xml_url_encoded}}">
        Validate feed
      </a>
    </div>

  </div>
</body>
</html>
```

---

## Placeholder Reference

| Placeholder              | Value                                              |
|--------------------------|----------------------------------------------------|
| `channel_title`          | Page `<title>` or user-provided name               |
| `channel_url`            | Source page URL                                    |
| `feed_xml_url`           | Where the `.xml` will be hosted (ask user if unknown; default `./feed.xml`) |
| `channel_description`    | `<meta name="description">` or auto-generated text |
| `generated_date`         | ISO date of generation (e.g. `2024-03-01`)         |
| `item_count`             | Number of `<item>` / `<entry>` elements in feed    |
| `feed_xml_url_encoded`   | URL-encoded version of `feed_xml_url`              |

---

## Output Files

| File                   | Contents                                        |
|------------------------|-------------------------------------------------|
| `<slug>-feed.xml`      | The RSS 2.0 or Atom 1.0 XML feed               |
| `<slug>-feed-page.html`| The HTML discovery wrapper (this template)     |

**Slug** = hostname of the source URL with dots replaced by hyphens.
Example: `vivianvoss-net-feed.xml` and `vivianvoss-net-feed-page.html`
