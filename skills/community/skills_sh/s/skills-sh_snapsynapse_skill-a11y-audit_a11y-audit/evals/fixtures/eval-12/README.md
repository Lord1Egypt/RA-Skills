# eval-12: Cross-Origin Sitemap Blocking

Validates that discovery no longer follows a robots.txt sitemap on a
different origin unless cross-origin sitemap use is explicitly enabled.

Fixture shape:

- `robots.txt` on `http://base.test` points at `http://cdn.test/sitemap.xml`.
- The default same-origin sitemap on `http://base.test/sitemap.xml`
  contains one page.
- Discovery should block the CDN sitemap, disclose the blocked fetch, and
  continue with the same-origin sitemap.
