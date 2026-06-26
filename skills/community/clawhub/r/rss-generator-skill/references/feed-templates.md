# Feed Templates (v1.0.0)

Ready-to-use XML skeletons. Replace `{{placeholders}}` with extracted values.

---

## RSS 2.0 Template

```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
     xmlns:atom="http://www.w3.org/2005/Atom"
     xmlns:content="http://purl.org/rss/1.0/modules/content/"
     xmlns:dc="http://purl.org/dc/elements/1.1/">
  <channel>
    <title>{{channel_title}}</title>
    <link>{{channel_url}}</link>
    <description>{{channel_description}}</description>
    <language>{{language|en}}</language>
    <lastBuildDate>{{last_build_date_rfc822}}</lastBuildDate>
    <generator>RSS Feed Generator Skill v1.0 (synthetic feed)</generator>
    <atom:link href="{{feed_self_url}}" rel="self" type="application/rss+xml"/>

    <!-- REPEAT FOR EACH POST -->
    <item>
      <title><![CDATA[{{item_title}}]]></title>
      <link>{{item_url}}</link>
      <guid isPermaLink="true">{{item_url}}</guid>
      <pubDate>{{item_date_rfc822}}</pubDate><!-- date-estimated if no date found -->
      <description><![CDATA[{{item_summary_html_or_text}}]]></description>
      <!-- Optional fields below — include only when data is available -->
      <dc:creator><![CDATA[{{item_author}}]]></dc:creator>
      <content:encoded><![CDATA[{{item_full_html}}]]></content:encoded>
    </item>
    <!-- END REPEAT -->

  </channel>
</rss>
```

### Placeholder reference (RSS 2.0)

| Placeholder               | Source                                      |
|---------------------------|---------------------------------------------|
| `channel_title`           | `<title>` of the scraped page               |
| `channel_url`             | The scraped page URL                        |
| `channel_description`     | `<meta name="description">` or auto-generated |
| `language`                | `<html lang>` attribute or `en`             |
| `last_build_date_rfc822`  | Scrape timestamp in RFC 822                 |
| `feed_self_url`           | Where user plans to host the feed file      |
| `item_title`              | Extracted per Step 2 of extraction-rules.md |
| `item_url`                | Extracted per Step 3                        |
| `item_date_rfc822`        | Extracted per Step 4, formatted RFC 822     |
| `item_summary_html_or_text` | Extracted per Step 5                      |
| `item_author`             | Extracted per Step 6 (omit tag if missing)  |
| `item_full_html`          | Only in `/fulltext` mode                    |

---

## Atom 1.0 Template

```xml
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>{{channel_title}}</title>
  <id>{{channel_url}}</id>
  <updated>{{last_updated_iso8601}}</updated>
  <link href="{{channel_url}}" rel="alternate"/>
  <link href="{{feed_self_url}}" rel="self" type="application/atom+xml"/>
  <subtitle>{{channel_description}}</subtitle>
  <generator uri="https://openlinksw.com/" version="1.0">
    RSS Feed Generator Skill (synthetic feed)
  </generator>

  <!-- REPEAT FOR EACH POST -->
  <entry>
    <title type="html"><![CDATA[{{item_title}}]]></title>
    <id>{{item_url}}</id>
    <updated>{{item_date_iso8601}}</updated><!-- date-estimated if no date found -->
    <published>{{item_date_iso8601}}</published>
    <link href="{{item_url}}" rel="alternate"/>
    <summary type="html"><![CDATA[{{item_summary_html}}]]></summary>
    <!-- Optional: include only when data available -->
    <author><name>{{item_author}}</name></author>
    <content type="html"><![CDATA[{{item_full_html}}]]></content>
  </entry>
  <!-- END REPEAT -->

</feed>
```

### Placeholder reference (Atom 1.0)

| Placeholder            | Source                                           |
|------------------------|--------------------------------------------------|
| `channel_title`        | `<title>` of the scraped page                    |
| `channel_url`          | The scraped page URL                             |
| `last_updated_iso8601` | Scrape timestamp: `2024-01-15T12:00:00Z`         |
| `feed_self_url`        | Hosting URL of the generated `.xml` file         |
| `channel_description`  | `<meta name="description">` or auto-generated    |
| `item_title`           | Extracted per extraction-rules.md Step 2         |
| `item_url`             | Extracted per Step 3 (absolute URL)              |
| `item_date_iso8601`    | Extracted per Step 4, formatted ISO 8601         |
| `item_summary_html`    | Extracted per Step 5                             |
| `item_author`          | Step 6; omit `<author>` block if not found       |
| `item_full_html`       | `/fulltext` mode only                            |

---

## Minimal "stub" RSS (for pages with no extractable metadata)

Use this skeleton when the page lacks structured post data. Populate manually
with the user's help.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Feed for {{page_url}}</title>
    <link>{{page_url}}</link>
    <description>Synthetic feed generated from {{page_url}}</description>
    <!-- Add <item> blocks here once post data is identified -->
  </channel>
</rss>
```
