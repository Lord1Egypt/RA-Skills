# Running the collectors

Use Python 3.10+ on macOS/Linux. Work inside the installed skill directory. Node is optional for the bridge. Install dependencies only in a fresh isolated environment; these commands are setup instructions, not a claim that a clean install was exercised in this release:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m playwright install chromium
```

YouTube comments require `yt-dlp` and its current supported YouTube JS runtime where applicable. To use the release's optional pin, install `.venv/bin/python -m pip install --index-url https://pypi.org/simple -r requirements-comments.txt`. It pins yt-dlp 2026.8.19 with default extras (including yt-dlp-ejs 0.8.0); JS runtime installation and authentication remain separate operator choices. The collector prefers `yt-dlp` next to its Python interpreter, then PATH; `--ytdlp /absolute/path/to/yt-dlp` selects an approved executable. Record its version and confirm current official YouTube requirements. The pinned Python caption library is independent of yt-dlp. A new upstream release may be needed when site protocols change; recheck the adapter before changing pins.

The approved vault/service operator supplies `PROXYLANE_PROXY_URL` through the process environment, or creates a private one-line connection file for `--proxy-file /private/path/connection.private`. The URL is an HTTP/HTTPS connection with an explicit port, optional percent-encoded username/password, no path/query. Do not paste actual credentials into shell history, command arguments, articles or the release folder. SOCKS requires different dependency/browser support and is excluded from this release contract. Ambient HTTP_PROXY/HTTPS_PROXY variables are ignored by Requests.

Fixture commands need no network, proxy, account, API key or browser:

```sh
python3 scripts/collect.py --mode demo --fixture --out output/fixture-demo
python3 scripts/collect.py --mode youtube-transcript --fixture --out output/transcript-fixture
python3 scripts/collect.py --mode youtube-comments --fixture --out output/comments-fixture
python3 scripts/collect.py --mode google-citations --fixture --out output/google-fixture
python3 scripts/collect.py --mode xiaohongshu --fixture --out output/xhs-fixture
python3 scripts/collect.py --mode price --fixture --out output/price-fixture
```

The synthetic transcript/comment ids, note ids, URLs and prices are parser inputs, not live records. Never fetch those fixture targets live.

Live commands, after the approved connection is supplied:

```sh
python3 scripts/collect.py --mode youtube-transcript --target VIDEO_ID --languages ru,en --limit 500 --attempts 1 --timeout 120 --out output/transcript-live
python3 scripts/collect.py --mode youtube-comments --target VIDEO_ID --comment-sort top --limit 20 --attempts 1 --timeout 120 --out output/comments-live
python3 scripts/collect.py --mode google-citations --query "how to choose a running shoe" --surface ai-mode --country us --language en --locale en-US --dom-contract /private/path/reviewed-google-dom.json --limit 20 --timeout 120 --out output/google-live
python3 scripts/collect.py --mode xiaohongshu --mcp-url http://localhost:18060/mcp --query "跑鞋" --limit 20 --timeout 180 --out output/xhs-live
python3 scripts/collect.py --mode price --target https://www.amazon.com/dp/ASIN --expected-id ASIN --platform amazon --variant "EXPECTED SELECTED VARIANT" --timeout 120 --out output/amazon-live
python3 scripts/collect.py --mode price --target https://SHOP/product/PRODUCT --expected-id EXACT_SKU --platform jsonld --timeout 120 --out output/store-live
```

`VIDEO_ID`, `ASIN`, product URLs, `EXACT_SKU`, the variant and contract path are explicit input placeholders, not working live outputs. Use a product whose visible ASIN/SKU and selected variant are already known. A price run observes one page; schedule repetition in the calling agent, keeping prior outcomes rather than overwriting them.

Google's illustrative [DOM schema](../examples/google-dom-contract.json) contains synthetic selectors. Do not pass it as a supported live default. A reviewed contract must identify exactly one visible AI root and answer, a visible marker, and citation anchors inside that answer. `citation_selector` is scoped to the answer node. Only visible anchors and external nongoogle URLs are retained, but those filters alone do not establish source semantics. Set `reviewed=true`, a matching `surface`, and an `observed_on` date only after checking that the selected anchors are actually citations in a current rendered page. Optional `surface_marker_selector` finds a visible UI label outside the root; optional `location_selector` records a location footer. A changed UI returns `unsupported_surface`. AI Overview and AI Mode require separate contracts.

XHS uses an already running, logged-in `xpzouying/xiaohongshu-mcp` server. Supply `XHS_PROXY` as a declaration matching that server's existing startup configuration; the client does not launch/restart/configure it. If server access auth is enabled, supply `XHS_MCP_AUTH_TOKEN` privately. For a known note use `--target NOTE_ID` and private `XHS_XSEC_TOKEN`; both originate from the same current Feed/search result. Without a target, `--query` chooses the first returned `modelType=note` result. No other notes, replies, writes or OCR are fetched. Expired tokens and absent login require an operator remedy; the collector never requests QR codes or reads cookie files.

Limits: one source target per invocation, 1..500 records, at most 2 explicit attempts, 10..300 seconds total deadline. XHS top-level comments clamp to 100 and tool discovery to three pages; it never replays a long MCP detail call. Google has no source-panel expansion; price has no pagination. Default retry count is one attempt. `--verify-egress` adds a public IP probe before a non-XHS live collection; no country or target-IP claims follow from it.

When Playwright's bundled Chromium is unavailable, `--browser-executable /absolute/path/to/approved/Chrome` may use an already installed Chromium-family browser with a new temporary context. It never opens the user's existing profile or imports its cookies. This is a browser-specific compatibility choice, and must be recorded with live receipts.
