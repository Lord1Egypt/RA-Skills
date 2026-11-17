---
id: browser-ext
kind: asset
unlocks: [chrome-web-store, edge-addons, firefox-addons]
source: https://extensionworkshop.com/documentation/develop/firefox-builtin-data-consent/, https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/manifest.json/browser_specific_settings, https://extensionworkshop.com/documentation/publish/source-code-submission/, https://developer.chrome.com/docs/webstore/cws-dashboard-privacy, https://learn.microsoft.com/en-us/microsoft-edge/extensions/publish/publish-extension, https://extensionworkshop.com/documentation/develop/getting-started-with-web-ext/ (loaded 2026-11-08)
---
## Smallest version
One MV3 extension that does one job with the product's existing API: e.g. a popup or context-menu action that sends the current page URL/selection to one endpoint and shows the result, with the user's API key saved in extension storage on an options page. One `manifest.json` for all three stores; no content scripts or host permissions unless the one job needs them.

## Scaffold
No official cross-browser scaffold. Hand-write `manifest.json` + `popup.html`/`popup.js` + `options.html` + icons; plain JS (no bundler) avoids AMO source upload.

## Fields the listings check
- `manifest_version: 3`, `name`, `version`, `description`, `icons`, `action`, `permissions` (minimal, e.g. `storage`), `host_permissions` only for the API origin.
- Firefox: `browser_specific_settings.gecko.id` is required for signing MV3 (AMO does not assign one): email-like `name@example.org` (<=80 chars, `^[a-zA-Z0-9-._]*@[a-zA-Z0-9-._]+$`) or a GUID; must be unique on AMO.
- Firefox: `browser_specific_settings.gecko.data_collection_permissions` required for new AMO submissions since 2025-11-03. Sub-keys `required` / `optional`; nothing collected -> `"required": ["none"]`. Types: `personallyIdentifyingInfo`, `healthInfo`, `financialAndPaymentInfo`, `authenticationInfo`, `personalCommunications`, `locationInfo`, `browsingActivity`, `websiteContent`, `websiteActivity`, `searchTerms`, `bookmarksInfo`, `technicalAndInteraction` (must be optional). Sending page content to your API means declaring `websiteContent` (and likely `authenticationInfo` for the key): decide honestly.
- Firefox Android: `"gecko_android": {}` to ship there too.
- AMO source upload: required with every version if code came from minifiers, bundlers, template engines or other pre-processing (webpack, browserify...). Source zip <=200MB with a README giving OS/env, tool versions, exact build commands, the lockfile; open-source local build tools only; no obfuscation. Default review env: Ubuntu 24.04.4, Node 24.14.0, npm 11.9.0.
- Chrome Privacy practices tab: "Single purpose description", "Permissions justification" (one per permission), "Remote Code" declaration, "Data usage" (collected categories + certification checkboxes), privacy policy URL.
- Edge Partner Center: zip with the manifest; privacy step mirrors Chrome (purpose, permission justifications, remote code, data usage certification, privacy policy); listing pulls `name`/`description` from the manifest; up to 7 search terms (30 chars each, 21 words total); "Notes for certification" for test accounts; certification up to 7 business days.

## Steps
claude: pick the one job and the single endpoint from the API docs; write manifest, popup, options page (key in `chrome.storage`/`browser.storage`)
claude: add the `browser_specific_settings.gecko` block (`id`, `data_collection_permissions`)
claude: if a bundler is used, write the source zip README with build commands and lockfile
claude: draft single-purpose text, per-permission justifications, data-usage answers and a privacy policy page
claude: zip with manifest.json at the zip root (`web-ext build` packages a .zip)
human: Chrome developer registration (fee) and Edge Partner Center account and AMO account
human: upload the zip to each store, fill listing (screenshots, icon) and privacy forms, add a test API key in reviewer notes
approve: submit each store listing for review

## Verify locally
`npm install --global web-ext@10.8.0`, then `web-ext lint` (manifest errors) and `web-ext run` (Firefox) / `web-ext run --target chromium`; load unpacked in chrome://extensions and run the one job with a test key.
