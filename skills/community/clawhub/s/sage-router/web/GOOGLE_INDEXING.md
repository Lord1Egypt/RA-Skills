# Google indexing

The landing site publishes passive discovery files for Google and other crawlers:

- `public/sitemap.xml`
- `public/robots.txt`
- `public/llms.txt`
- `public/llms-full.txt`

The previous active submission helper used `google-indexing-script@0.4.0`.
That package currently has unpatched transitive audit findings, so it is no
longer installed by `npm install` or exposed through `npm run` scripts.

## Manual Search Console setup

1. Verify `https://sagerouter.dev/` in Google Search Console.
2. Submit `https://sagerouter.dev/sitemap.xml` in Search Console.
3. Use URL inspection manually for priority pages after deployment.

## Notes

- Google's Indexing API is officially intended for pages with `JobPosting` or
  `BroadcastEvent` structured data. Sage Router pages should rely on sitemap
  discovery unless a maintained, audited submission client is added later.
- Do not commit Google service account JSON files or Search Console credentials.
