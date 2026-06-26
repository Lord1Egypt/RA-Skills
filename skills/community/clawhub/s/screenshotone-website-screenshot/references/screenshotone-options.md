# ScreenshotOne Options Reference

Source: [Screenshot Options](https://screenshotone.com/docs/options/)

This file is a compact working reference for direct ScreenshotOne `curl` requests. It does not replace the official docs. Use it to choose request parameters quickly, then pass them through repeated `--data-urlencode "key=value"` flags.

## Required and Core

- `access_key`: required API credential
- `url`: website to capture
- `format`: output format such as `png`, `jpg`, `webp`, `pdf`, `html`, or `markdown`
- `response_type`: defaults to binary output; use `json` when you need metadata in the response body or a temporary screenshot URL;

This skill intentionally uses only `access_key` authentication and does not include signed-request or secret-key handling.

To get an API key, go to [https://screenshotone.com/](https://screenshotone.com/), sign up, and then open [https://dash.screenshotone.com/access](https://dash.screenshotone.com/access).

## Full Page and Targeting

- `full_page=true`: capture the full page instead of only the visible viewport
- `full_page_scroll=true`: scroll through the page before stitching
- `full_page_scroll_delay`: pause between scroll steps
- `full_page_max_height`: cap the resulting height
- `selector`: capture a specific element
- `selector_algorithm`: control how selectors are matched
- `selector_scroll_into_view=true`: scroll the selected element into view
- `scroll_into_view=<selector>`: scroll a target element into view before capture
- `capture_beyond_viewport=true`: allow capturing outside the visible viewport where supported

## Viewport and Device Emulation

- `viewport_width`, `viewport_height`: explicit viewport size
- `viewport_device`: device preset from ScreenshotOne's device list
- `viewport_mobile=true`: emulate a mobile viewport
- `viewport_has_touch=true`: emulate touch support
- `viewport_landscape=true`: landscape orientation
- `device_scale_factor`: retina or other DPR scaling

## Waiting and Reliability

- `wait_until`: page readiness condition
- `delay`: fixed delay in seconds after load
- `timeout`: overall timeout
- `navigation_timeout`: navigation-specific timeout
- `wait_for_selector=<selector>`: wait for an element to appear
- `wait_for_selector_algorithm`: selector matching behavior
- `error_on_selector_not_found=true`: fail instead of returning a screenshot when the element never appears
- `fail_if_request_failed=true`: fail when page resources fail to load

## Image and PDF Output

- `image_quality`: quality for lossy or configurable formats
- `image_width`, `image_height`: resize the final image while preserving aspect ratio
- `omit_background=true`: transparent background for supported formats
- For PDF output close to a full-page screenshot, the docs recommend combining:
  `format=pdf`, `media_type=screen`, `pdf_print_background=true`, `pdf_fit_one_page=true`
- PDF-specific options include `pdf_landscape`, `pdf_paper_format`, `pdf_margin`, and side-specific margin overrides

## Cleanup and Customization

- `block_cookie_banners=true`: hide common consent banners
- `block_banners_by_heuristics=true`: heuristic banner blocking
- `block_chats=true`, `block_ads=true`, `block_trackers=true`
- `block_requests=<patterns>` or `block_resources=<types>`: stricter request/resource blocking
- `hide_selectors=<selector list>`: hide specific elements before capture
- `styles=<css>`: inject custom CSS
- `scripts=<js>`: inject JavaScript
- `scripts_wait_until`: when injected scripts should run
- `click=<selector>` or `hover=<selector>`: interact before capture

## Request Context

- `authorization`: auth header helper
- `cookies`: cookies to preload
- `headers`: custom request headers
- `user_agent`: custom user agent
- `proxy` or `ip_country_code`: route traffic through ScreenshotOne-supported proxy locations
- `time_zone`: emulate a time zone
- `dark_mode=true` or `false`
- `reduced_motion=true`
- `media_type=screen` or print-oriented alternatives
- `geolocation_latitude`, `geolocation_longitude`, `geolocation_accuracy`

## Metadata and Storage

- `metadata_image_size=true`: receive actual image dimensions
- `metadata_page_title=true`: receive the page title
- `metadata_content=true`: receive extracted page content
- `metadata_fonts=true`, `metadata_icon=true`, `metadata_open_graph=true`
- `store=true`: upload the result to configured S3-compatible storage
- `storage_path`, `storage_bucket`, `storage_endpoint`, `storage_class`, `storage_acl`
- `storage_return_location=true`: receive the uploaded object location

## Practical Patterns

- Basic PNG screenshot:
  `--data-urlencode "format=png"`
- Stable full-page capture:
  `--data-urlencode "full_page=true" --data-urlencode "wait_until=networkidle" --data-urlencode "delay=2"`
- Element screenshot:
  `--data-urlencode "selector=.hero" --data-urlencode "selector_scroll_into_view=true"`
- Cleaner marketing page screenshot:
  `--data-urlencode "block_cookie_banners=true" --data-urlencode "block_ads=true" --data-urlencode "hide_selectors=.chat,.modal"`
