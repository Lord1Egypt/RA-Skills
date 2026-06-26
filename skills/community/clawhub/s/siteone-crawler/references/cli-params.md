# SiteOne Crawler CLI Parameters Reference

Binary: `/home/lyq/siteone-crawler/siteone-crawler`  
Version: 2.3.0.20260330

## Basic Settings

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--url=<url>` | Target URL or sitemap.xml (required) | - |
| `--single-page` | Crawl only the given page + assets | - |
| `--max-depth=<int>` | Max crawl depth for pages (0=unlimited) | 0 |
| `--device=<val>` | UA device: `desktop`, `tablet`, `mobile` | desktop |
| `--user-agent=<val>` | Custom User-Agent (append `!` to strip signature) | - |
| `--timeout=<int>` | Request timeout (seconds) | 5 |
| `--proxy=<host:port>` | HTTP proxy | - |
| `--http-auth=<user:pass>` | Basic HTTP auth | - |
| `--accept-invalid-certs` | Accept invalid SSL certs | off |

## Output Settings

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--output=<val>` | `text` or `json` | text |
| `--extra-columns=<val>` | Extra columns: `Title`, `Keywords`, `Description`, `DOM`, HTTP headers. Width: `Col(n)` or `Col(n>)` for no-truncate. Custom: `Name=method:pattern#group(length)` | - |
| `--url-column-size=<int>` | URL column width | auto |
| `--timezone=<val>` | Timezone for reports | UTC |
| `--rows-limit=<int>` | Max rows in analysis tables | 200 |
| `--show-inline-criticals` | Show criticals in URL table | - |
| `--show-inline-warnings` | Show warnings in URL table | - |
| `--do-not-truncate-url` | Don't truncate long URLs | - |
| `--show-scheme-and-host` | Show scheme://host for origin domain | - |
| `--hide-progress-bar` | Hide progress bar | - |
| `--hide-columns=<val>` | Hide columns: `type,time,size,cache` | - |
| `--no-color` | Disable colors | - |
| `--force-color` | Force colors | - |

## File Export

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--output-html-report=<file>` | HTML report path | `tmp/report.%domain%.%datetime%.html` |
| `--output-json-file=<file>` | JSON output path | `tmp/output.%domain%.%datetime%.json` |
| `--output-text-file=<file>` | Text output path | `tmp/output.%domain%.%datetime%.txt` |
| `--result-storage=<val>` | Result storage: `memory` or `file` | memory |

## Upload Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--upload` | Enable HTML report upload | - |
| `--upload-to=<url>` | Upload endpoint | `https://crawler.siteone.io/up` |
| `--upload-retention=<val>` | Retention: `1h`, `4h`, `12h`, `24h`, `3d`, `7d`, `30d`, `365d`, `forever` | 30d |
| `--upload-password=<val>` | Access password for online report | - |
| `--upload-timeout=<int>` | Upload timeout (seconds) | 3600 |

## Resource Filtering

| Parameter | Description |
|-----------|-------------|
| `--disable-all-assets` | Disable all asset crawling (shortcut) |
| `--disable-javascript` | Disable JS download, remove JS from HTML |
| `--disable-styles` | Disable CSS |
| `--disable-fonts` | Disable fonts |
| `--disable-images` | Disable images |
| `--disable-files` | Disable downloadable documents |
| `--remove-all-anchor-listeners` | Remove link event listeners (SPA sites) |

## Advanced Crawler Settings

| Parameter | Description | Default |
|-----------|-------------|---------|
| `-w / --workers=<int>` | Max concurrent workers | 3 (1 on Windows) |
| `-rps / --max-reqs-per-sec=<val>` | Max requests/second | 10 |
| `--memory-limit=<size>` | Memory limit (M/G) | 2048M |
| `--resolve=<domain:port:ip>` | Force DNS resolution | - |
| `--allowed-domain-for-external-files=<val>` | External asset domains (repeatable, supports `*`) | - |
| `--allowed-domain-for-crawling=<val>` | Cross-domain crawl targets (repeatable, supports `*`) | - |
| `--single-foreign-page` | Only crawl one page from foreign domains | - |
| `--include-regex=<regex>` | PCRE regex to include URLs (repeatable) | - |
| `--ignore-regex=<regex>` | PCRE regex to ignore URLs (repeatable) | - |
| `--regex-filtering-only-for-pages` | Apply regex only to pages, not assets | - |
| `--analyzer-filter-regex=<regex>` | Filter analyzers by class name regex | - |
| `--accept-encoding=<val>` | Accept-Encoding header | `gzip, deflate, br` |
| `--remove-query-params` | Strip query params from URLs | - |
| `--keep-query-param=<val>` | Keep only specified query params (repeatable) | - |
| `--ignore-robots-txt` | Ignore robots.txt | - |
| `--max-queue-length=<int>` | Max URL queue size | 9000 |
| `--max-visited-urls=<int>` | Max visited URLs | 10000 |
| `--max-skipped-urls=<int>` | Max skipped URLs | 10000 |
| `--max-url-length=<int>` | Max URL length (chars) | 2083 |
| `--add-random-query-params` | Bypass caches with random params | - |
| `--concurrency-mode=<val>` | Concurrency: `multi` or `single` | multi |
| `--basic-auth-per-url=<val>` | Per-URL basic auth `url|user:pass` (repeatable) | - |
| `--header=<val>` | Custom request header `Name: Value` (repeatable) | - |
| `--cookie=<val>` | Cookie header value | - |
| `--follow-redirects=<val>` | Follow redirects: `on`, `off`, `same-host` | on |

## Mailer Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--mail-to=<emails>` | Recipients (comma-separated) | - |
| `--mail-from=<email>` | Sender email | - |
| `--mail-subject=<val>` | Subject template | `SiteOne Crawler Report: %domain%` |
| `--mail-smtp-host=<host>` | SMTP host | localhost |
| `--mail-smtp-port=<int>` | SMTP port | 25 |
| `--mail-smtp-user=<val>` | SMTP username | - |
| `--mail-smtp-pass=<val>` | SMTP password | - |
| `--mail-smtp-encryption=<val>` | Encryption: `tls`, `ssl`, `none` | none |

## Offline Export

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--offline-export-dir=<dir>` | Offline save directory (activates export) | - |
| `--offline-export-remove-unwanted-code` | Remove analytics/cookie/JS cruft | 1 |
| `--offline-export-no-auto-redirect-html` | Skip auto-redirect HTML files | - |
| `--offline-export-preserve-url-structure` | Use `path/index.html` structure | - |
| `--offline-export-preserve-urls` | Keep production URLs in exports | - |
| `--replace-content=<val>` | Replace content `foo -> bar` or PREG regex | - |
| `--replace-query-string=<val>` | Replace query string chars | - |
| `--offline-export-lowercase` | Lowercase filenames | - |
| `--ignore-store-file-error` | Ignore file store errors | - |
| `--disable-astro-inline-modules` | Don't inline Astro module scripts | - |

## Markdown Export

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--markdown-export-dir=<dir>` | Markdown save directory (activates export) | - |
| `--markdown-export-single-file=<file>` | Combine into single file | - |
| `--markdown-move-content-before-h1-to-end` | Move header/nav to end | - |
| `--markdown-disable-images` | No images in markdown | - |
| `--markdown-disable-files` | No non-HTML files (PDF etc) | - |
| `--markdown-remove-links-and-images-from-single-file` | Strip links/images in single-file mode | - |
| `--markdown-exclude-selector=<val>` | CSS selectors to exclude (repeatable) | - |
| `--markdown-replace-content=<val>` | Replace content (foo->bar or regex) | - |
| `--markdown-replace-query-string=<val>` | Replace query string chars | - |
| `--markdown-ignore-store-file-error` | Ignore store errors | - |

## Sitemap Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--sitemap-xml-file=<file>` | XML sitemap output path | - |
| `--sitemap-txt-file=<file>` | TXT sitemap output path | - |
| `--sitemap-base-priority=<val>` | Base priority | 0.5 |
| `--sitemap-priority-increase=<val>` | Priority increase per slash depth | 0.1 |

## Server Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--serve-markdown=<dir>` | Serve markdown export as styled HTML | - |
| `--serve-offline=<dir>` | Serve offline export | - |
| `--serve-port=<int>` | Server port | 8321 |
| `--serve-bind-address=<val>` | Bind address | 127.0.0.1 |
| `--html-to-markdown=<val>` | Convert local HTML file to markdown (stdout) | - |
| `--html-to-markdown-output=<val>` | Output file for --html-to-markdown | - |

## Analyzer Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--fastest-urls-top-limit=<int>` | Top N fastest URLs | 20 |
| `--fastest-urls-max-time=<val>` | Max time to qualify as fast (sec) | 1 |
| `--slowest-urls-top-limit=<int>` | Top N slowest URLs | 20 |
| `--slowest-urls-min-time=<val>` | Min time to qualify as slow (sec) | 0.01 |
| `--slowest-urls-max-time=<val>` | Max time to qualify as very slow (sec) | 3 |
| `--max-heading-level=<int>` | Max heading level for SEO analysis (1-6) | 3 |

## CI/CD Quality Gate

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--ci` | Enable CI/CD mode | - |
| `--ci-min-score=<val>` | Min overall score (0.0-10.0) | 5.0 |
| `--ci-min-performance=<val>` | Min Performance score | 5 |
| `--ci-min-seo=<val>` | Min SEO score | 5 |
| `--ci-min-security=<val>` | Min Security score | 5 |
| `--ci-min-accessibility=<val>` | Min Accessibility score | 3 |
| `--ci-min-best-practices=<val>` | Min Best Practices score | 5 |
| `--ci-max-404=<int>` | Max allowed 404s | 0 |
| `--ci-max-5xx=<int>` | Max allowed 5xx errors | 0 |
| `--ci-max-criticals=<int>` | Max critical findings | 0 |
| `--ci-max-warnings=<int>` | Max warning findings | - |
| `--ci-max-avg-response=<val>` | Max avg response time (sec) | - |
| `--ci-min-pages=<int>` | Min HTML pages required | 10 |
| `--ci-min-assets=<int>` | Min assets required | 10 |
| `--ci-min-documents=<int>` | Min documents required | 0 |
