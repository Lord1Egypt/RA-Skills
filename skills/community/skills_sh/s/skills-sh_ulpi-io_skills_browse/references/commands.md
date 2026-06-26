# browse — Full Command Reference

Read this file when you need command syntax not covered in the SKILL.md Quick Reference, or need exact flags for a specific command category.

## Quick Reference (all examples)

```bash
# Navigate to a page
browse goto https://example.com

# Read cleaned page text
browse text

# Take a screenshot (saved to .browse/sessions/default/screenshot.png)
browse screenshot

# Snapshot: accessibility tree with refs
browse snapshot -i

# Click by ref (after snapshot)
browse click @e3

# Fill by ref
browse fill @e4 "test@test.com"

# Double-click, focus, check/uncheck
browse dblclick @e3
browse focus @e5
browse check @e7
browse uncheck @e7

# Drag and drop
browse drag @e1 @e2

# Run JavaScript
browse js "document.title"

# Get all links
browse links

# Get input value / count elements
browse value "[id=email]"
browse count ".search-result"

# Click by CSS selector
browse click "button.submit"

# Fill a form by CSS selector (use [id=...] instead of # to avoid shell issues)
browse fill "[id=email]" "test@test.com"
browse fill "[id=password]" "abc123"
browse click "button[type=submit]"

# Scroll
browse scroll up
browse scroll down
browse scroll "[id=target]"

# Wait for navigation or network
browse wait ".loaded"
browse wait --url "**/dashboard"
browse wait --network-idle

# iframe targeting
browse frame "[id=my-iframe]"
browse text                    # reads from inside the iframe
browse click @e3               # clicks inside the iframe
browse frame main              # back to main page

# Highlight an element (visual debugging)
browse highlight @e5

# Download a file
browse download @e3 ./file.pdf

# Network mocking
browse route "**/*.png" block
browse route "**/api/data" fulfill 200 '{"mock":true}'
browse route clear

# Offline mode
browse offline on
browse offline off

# JSON output mode
browse --json goto https://example.com

# Security: content boundaries
browse --content-boundaries text

# Security: domain restriction
browse --allowed-domains example.com,*.cdn.example.com goto https://example.com

# State persistence
browse state save mysite
browse state load mysite
browse state clean                    # delete states older than 7 days
browse state clean --older-than 30    # custom threshold

# Cookie management
browse cookie clear                                      # clear all cookies
browse cookie set auth token --domain .example.com       # set with options
browse cookie export ./cookies.json                      # export to file
browse cookie import ./cookies.json                      # import from file

# Cookie import from real browsers (macOS -- Chrome, Arc, Brave, Edge)
browse cookie-import --list                              # show installed browsers
browse cookie-import chrome --domain .example.com        # import cookies for a domain
browse cookie-import arc --domain .github.com            # import from Arc
browse cookie-import chrome --profile "Profile 1" --domain .site.com  # specific Chrome profile

# Session auto-persistence (named sessions survive restarts)
browse --session myapp goto https://app.com/login        # login...
browse session-close myapp                               # state auto-saved (encrypted if BROWSE_ENCRYPTION_KEY set)
browse --session myapp goto https://app.com/dashboard    # cookies auto-restored

# Persistent profiles (full browser state, own Chromium)
browse --profile mysite goto https://app.com       # all state persists automatically
browse --profile mysite snapshot -i                 # still logged in next time
browse profile list                                 # list all profiles with size
browse profile delete old-site                      # remove a profile

# Load state at launch
browse --state auth.json goto https://app.com            # load cookies before first command

# Auth vault (credentials never visible to LLM)
browse auth save github https://github.com/login user pass123
browse auth login github

# HAR recording
browse har start
browse goto https://example.com
browse har stop ./recording.har

# Video recording (watch a .webm of the session)
browse video start ./videos
browse goto https://example.com
browse click @e3
browse video stop

# Command recording (export replayable scripts)
browse record start
browse goto https://example.com
browse click "a"
browse fill "[id=search]" "test query"
browse record stop
browse record export replay ./recording.json    # replay with: npx @puppeteer/replay ./recording.json
browse record export browse ./steps.json        # replay with: cat steps.json | browse chain

# Both together (video + replayable script)
browse video start ./videos
browse record start
browse goto https://example.com
browse snapshot -i
browse click @e3
browse fill "[id=email]" "user@test.com"
browse record stop
browse video stop
browse record export replay ./recording.json

# Device emulation
browse emulate iphone
browse emulate reset

# Parallel sessions
browse --session agent-a goto https://site1.com
browse --session agent-b goto https://site2.com

# Clipboard
browse clipboard
browse clipboard write "copied text"

# Find elements semantically
browse find role button
browse find text "Submit"
browse find testid "login-btn"

# Screenshot diff (visual regression)
browse screenshot-diff baseline.png current.png

# Headed mode (visible browser)
browse --headed goto https://example.com

# Handoff (human takeover for CAPTCHA/MFA -- see guides.md for protocol)
browse handoff "stuck on CAPTCHA"
browse resume

# React debugging
browse react-devtools enable
browse react-devtools tree
browse react-devtools props @e3
browse react-devtools suspense
browse react-devtools disable

# Stealth mode (bypasses bot detection)
browse --runtime rebrowser goto https://example.com

# State list / show
browse state list
browse state show mysite

# Native app automation (Android, iOS, macOS)
browse sim start --platform android --app com.android.settings --visible
browse sim start --platform ios --app com.apple.Preferences --visible
browse --platform android --app com.android.settings snapshot -i
browse --platform ios --app com.apple.Preferences snapshot -i
browse --app "System Settings" snapshot -i              # macOS
browse --platform android --app com.android.settings tap @e3
browse --platform android --app com.android.settings swipe up
browse --platform android --app com.android.settings press back
browse --platform ios --app com.apple.mobilesafari type "example.com"
browse --app TextEdit press "cmd+n"                     # macOS modifier combos
browse sim stop --platform android
browse sim stop --platform ios

# Install and test your own app from a file
browse sim start --platform ios --app ./build/MyApp.app --visible   # .app bundle
browse sim start --platform ios --app ./MyApp.ipa --visible          # .ipa archive
browse sim start --platform android --app ./app-debug.apk --visible  # .apk file

# Cloud providers (encrypted API keys, never visible to agents)
browse provider save browserbase <api-key>
browse --provider browserbase goto https://example.com

# Performance audit
browse perf-audit https://example.com
browse perf-audit save baseline
browse perf-audit compare baseline
```

## Navigation
```
browse goto <url>         Navigate current tab
browse goto <url> --ready Wait for hydration/readiness after navigation
browse goto @google "query"   Search macro — expands to Google search URL
browse goto @youtube "query"  Search macro — YouTube, Amazon, Reddit, Wikipedia, etc.
browse back               Go back
browse forward            Go forward
browse reload             Reload page
browse url                Print current URL
```

## Content extraction
```
browse text               Cleaned page text (no scripts/styles)
browse html [selector]    innerHTML of element, or full page HTML
browse links              All links as "text -> href"
browse forms              All forms + fields as JSON
browse accessibility      Accessibility tree snapshot (ARIA)
browse images             List page images (src, alt, dimensions)
browse images [selector]  Images within a specific element
browse images --limit 20  Limit number of images returned
browse images --inline    Include base64-encoded image data
browse schema             Extract JSON-LD, Microdata, RDFa structured data (parsed JSON)
browse meta               Extract page meta tags (title, description, canonical, OG, Twitter, hreflang, robots, viewport)
browse headings           Extract H1-H6 heading hierarchy with counts and indented tree
```

## Snapshot (ref-based element selection)
```
browse snapshot           Full accessibility tree with @refs
browse snapshot -i        Interactive elements only -- terse flat list (minimal tokens)
browse snapshot -i -f     Interactive elements -- full indented tree with props
browse snapshot -i -V     Interactive elements -- viewport only (skip below-fold)
browse snapshot -c        Compact (no empty structural elements)
browse snapshot -C        Cursor-interactive (detect divs with cursor:pointer/onclick/tabindex)
browse snapshot -d <N>    Limit depth to N levels
browse snapshot -s <sel>  Scope to CSS selector
browse snapshot --offset <N>    Start output from line N (windowing for large snapshots)
browse snapshot --max-chars <N> Limit snapshot output to N characters
browse snapshot --serp    Google SERP fast extraction (structured results, no refs)
browse snapshot-diff      Compare current vs previous snapshot
```

After snapshot, use @refs as selectors in any command:
```
browse click @e3          Click the element assigned ref @e3
browse fill @e4 "value"   Fill the input assigned ref @e4
browse hover @e1          Hover the element assigned ref @e1
browse html @e2           Get innerHTML of ref @e2
browse css @e5 "color"    Get computed CSS of ref @e5
browse attrs @e6          Get attributes of ref @e6
```

Refs are invalidated on navigation -- run `snapshot` again after `goto`.

## Interaction
```
browse click <selector>        Click element (CSS selector or @ref)
browse click <sel> --force     Force-click through overlay interception (bypasses actionability checks)
browse click <sel> --if-exists Click only if element exists (no error if missing)
browse click <sel> --if-visible Click only if element is visible
browse click <x>,<y>           Click at page coordinates (e.g. 590,461)
browse rightclick <selector>   Right-click element (context menu)
browse dblclick <selector>     Double-click element
browse fill <selector> <value> Fill input field
browse fill <sel> <val> --if-empty  Fill only if field is empty
browse select <selector> <val> Select dropdown value
browse hover <selector>        Hover over element
browse hover <sel> --if-exists Hover only if element exists
browse hover <sel> --if-visible Hover only if visible
browse focus <selector>        Focus element
browse focus <sel> --if-exists Focus only if element exists
browse focus <sel> --if-visible Focus only if visible
browse tap <selector>          Tap element (requires touch context via emulate)
browse tap <sel> --if-exists   Tap only if element exists
browse tap <sel> --if-visible  Tap only if visible
browse check <selector>        Check checkbox
browse check <sel> --if-unchecked  Check only if not already checked
browse uncheck <selector>      Uncheck checkbox
browse drag <src> <tgt>        Drag source to target
browse type <text>             Type into focused element
browse press <key>             Press key (Enter, Tab, Escape, etc.)
browse keydown <key>           Hold key down
browse keyup <key>             Release key
browse keyboard inserttext <t> Insert text without key events
browse scroll [sel|up|down]    Scroll element/viewport/bottom
browse scrollinto <sel>        Scroll element into view (explicit)
browse scrollintoview <sel>    Alias for scrollinto
browse swipe <dir> [px]        Swipe up/down/left/right (touch events)
browse mouse move <x> <y>     Move mouse to coordinates
browse mouse down [button]     Press mouse button (left/right/middle)
browse mouse up [button]       Release mouse button
browse mouse wheel <dy> [dx]   Scroll wheel
browse wait <sel>              Wait for element to appear
browse wait <sel> --state hidden  Wait for element to disappear
browse wait <ms>               Wait for milliseconds
browse wait --text "..."       Wait for text to appear in page
browse wait --fn "expr"        Wait for JavaScript condition
browse wait --load <state>     Wait for load state
browse wait --url <pattern>    Wait for URL match
browse wait --network-idle     Wait for network idle
browse wait --request <pattern>  Wait for a matching network request
browse wait --download                    Wait for download, return temp path
browse wait --download ./report.pdf       Wait and save to path
browse wait --download 60000              Custom timeout (ms)
browse wait --download ./file.pdf 60000   Both path and timeout
browse set geo <lat> <lng>     Set geolocation
browse set media <scheme>      Set color scheme (dark/light/no-preference)
browse header <name>:<value>   Set request header
browse useragent <string>      Set user agent string
browse viewport <WxH>          Set viewport size (e.g. 375x812)
browse upload <sel> <files>    Upload file(s) to a file input
browse highlight <selector>    Highlight element (visual debugging)
browse download <sel> [path]   Download file triggered by click
browse download <sel> --inline Return file content as base64 (no disk write)
browse dialog-accept [value]   Set dialogs to auto-accept
browse dialog-dismiss          Set dialogs to auto-dismiss (default)
browse emulate <device>        Emulate device (iphone, pixel, etc.)
browse emulate reset           Reset to desktop (1920x1080)
browse offline [on|off]        Toggle offline mode
```

## Cookies
```
browse cookie <n>=<v>                  Set cookie (shorthand)
browse cookie set <n> <v> [--domain d --secure]  Set cookie with options
browse cookie clear                    Clear all cookies
browse cookie export <file>            Export cookies to JSON file
browse cookie import <file>            Import cookies from JSON file
```

## Network
```
browse route <pattern> block           Block matching requests
browse route <pattern> fulfill <s> [b] Mock with status + body
browse route clear                     Remove all routes
```

## Inspection
```
browse js <expression>         Run JS, print result
browse eval <js-file>          Run JS file against page
browse css <selector> <prop>   Get computed CSS property
browse attrs <selector>        Get element attributes as JSON
browse element-state <selector> Element state (visible/enabled/checked/focused)
browse value <selector>        Get input field value
browse count <selector>        Count matching elements
browse box <selector>          Get bounding box as JSON {x, y, width, height}
browse layout <selector>       Get element layout details
browse request <index|url>     Inspect a captured network request by index or URL pattern
browse dialog                  Last dialog info or "(no dialog detected)"
browse console [--clear]       View/clear console messages
browse errors [--clear]        View/clear page errors (filtered from console)
browse network [--clear]       View/clear network requests
browse cookies                 Dump all cookies as JSON
browse storage [set <k> <v>]   View/set localStorage
browse perf                    Page load performance timings
browse devices [filter]        List available device names
browse clipboard               Read system clipboard text
browse clipboard write <text>  Write text to system clipboard
```

## Visual
```
browse screenshot [path]              Viewport screenshot (default: .browse/sessions/{id}/screenshot.png)
browse screenshot --full [path]       Full-page screenshot (entire scrollable page)
browse screenshot <sel|@ref> [path]   Screenshot specific element
browse screenshot --clip x,y,w,h [path]  Screenshot clipped region
browse screenshot --annotate [path]   Screenshot with numbered badges + legend
browse pdf [path]                     Save as PDF
browse responsive [prefix]            Screenshots at mobile/tablet/desktop
```

## Frames (iframe targeting)
```
browse frame <selector>        Target an iframe (subsequent commands run inside it)
browse frame main              Return to main page
```

## Find (semantic element locators)
```
browse find role <query>              Find elements by ARIA role
browse find text <query>              Find elements by text content
browse find label <query>             Find elements by label
browse find placeholder <query>       Find elements by placeholder
browse find testid <query>            Find elements by test ID
browse find alt <query>               Find elements by alt text
browse find title <query>             Find elements by title attribute
browse find first <sel>               First matching element
browse find last <sel>                Last matching element
browse find nth <n> <sel>             Nth matching element (0-indexed)
```

## Compare
```
browse diff <url1> <url2>             Text diff between two pages
browse screenshot-diff <base> [curr]  Pixel-diff two PNG screenshots
```

## Multi-step (chain)
```
echo '[["goto","https://example.com"],["snapshot","-i"],["click","@e1"]]' | browse chain
```

## Tabs
```
browse tabs                    List tabs (id, url, title)
browse tab <id>                Switch to tab
browse newtab [url]            Open new tab
browse closetab [id]           Close tab
```

## Sessions (parallel agents)
```
browse --session <id> <cmd>    Run command in named session
browse sessions                List active sessions
browse session-close <id>      Close a session
```

## Profiles
```
browse --profile <name> <cmd>             Use persistent browser profile
browse profile list                       List profiles with disk size
browse profile delete <name>              Delete a profile
browse profile clean [--older-than <d>]   Remove old profiles (default: 7 days)
browse profiles                           List available camoufox profiles from .browse/camoufox-profiles/
```

## State persistence
```
browse state save [name]       Save cookies + localStorage (all origins)
browse state load [name]       Restore saved state
browse state list              List saved states
browse state show [name]       Show contents of saved state
browse state clean             Delete states older than 7 days
browse state clean --older-than N   Custom age threshold (days)
```

## Cookie import (macOS -- borrow auth from real browsers)
```
browse cookie-import --list                         List installed browsers
browse cookie-import <browser> --domain <d>         Import cookies for a domain
browse cookie-import <browser> --profile <p> --domain <d>   Specific Chrome profile
```

## Auth vault
```
browse auth save <name> <url> <user> <pass|--password-stdin>   Save credentials (encrypted)
browse auth login <name>                       Auto-login using saved credentials
browse auth list                               List saved credentials
browse auth delete <name>                      Delete credentials
```

## HAR recording
```
browse har start               Start recording network traffic
browse har stop [path]         Stop and save HAR file
```

## Video recording
```
browse video start [dir]       Start recording video (WebM, compositor-level)
browse video stop              Stop recording and save video files
browse video status            Check if recording is active
```

## Command recording & export
```
browse record start                    Start recording commands
browse record stop                     Stop recording, keep steps for export
browse record status                   Recording state and step count
browse record export browse [path]     Export as chain-compatible JSON (replay with browse chain)
browse record export replay [path]    Export as Chrome DevTools Recorder (Playwright/Puppeteer)
browse record export replay --selectors css,aria [path]  Filter selector types in export
```

## Native App Automation
```
browse sim start --platform ios|android --app <id-or-path> [--visible] [--device <name>]  Start + install/launch app
browse sim stop --platform ios|android                          Stop simulator/emulator
browse sim status --platform ios|android                        Check runner status
browse --platform ios --app <bundleId> <command>                Target iOS app
browse --platform android --app <package> <command>             Target Android app
browse --app <name> <command>                                   Target macOS app
```

The `--app` flag accepts a bundle ID, package name, **or file path** (.app/.ipa/.apk). File paths auto-install the app into the simulator/emulator.

Supported commands on all app platforms: `snapshot`, `text`, `tap`, `fill`, `type`, `press`, `swipe`, `screenshot`.
macOS also supports modifier combos: `browse --app TextEdit press "cmd+n"`.
Android auto-installs adb, Java, SDK, and emulator on first use (macOS via Homebrew).

### Common iOS Bundle IDs
| App | Bundle ID |
|-----|-----------|
| Settings | `com.apple.Preferences` |
| Safari | `com.apple.mobilesafari` |
| Maps | `com.apple.Maps` |
| Photos | `com.apple.mobileslideshow` |
| Calendar | `com.apple.mobilecal` |

### Common Android Package Names
| App | Package Name |
|-----|-------------|
| Settings | `com.android.settings` |
| Chrome | `com.android.chrome` |
| Dialer | `com.google.android.dialer` |
| Messages | `com.google.android.apps.messaging` |
| Calculator | `com.google.android.calculator` |

### Platform enablement (run once)
```
browse enable android    # Auto-installs adb, JDK, SDK, emulator, driver
browse enable ios        # Builds iOS runner (needs Xcode)
browse enable macos      # Builds browse-ax bridge
browse enable all        # All platforms
```

## Performance audit
```
browse perf-audit [url]                  Full performance audit (Web Vitals, resources, images, fonts, DOM, render-blocking, third-party, stack detection, correlations, recommendations)
browse perf-audit [url] --no-coverage    Skip JS/CSS coverage collection (faster)
browse perf-audit [url] --no-detect      Skip framework/SaaS/infrastructure detection
browse perf-audit [url] --json           Output as structured JSON (for programmatic use)
browse perf-audit [url] --budget lcp:2500,cls:0.1,tbt:300  Set performance budgets (fail if exceeded)
browse perf-audit save [name]            Save audit report to .browse/audits/ (auto-names from URL + date if omitted)
browse perf-audit compare <base> [curr]  Compare saved baseline vs current page or another saved audit (regression detection)
browse perf-audit list                   List saved audit reports (name, size, date)
browse perf-audit delete <name>          Delete a saved audit report
browse detect                            Detect tech stack: frameworks, SaaS platforms, CDN, protocol, compression, caching, DOM complexity, third-party inventory
browse coverage start                    Start JS/CSS code coverage collection
browse coverage stop                     Stop collection and report per-file used/unused bytes
browse initscript set <code>             Inject JS that runs before every page load (pre-navigation observers, mocks, polyfills)
browse initscript show                   Show current init script
browse initscript clear                  Remove init script
```

## YouTube transcript
```
browse youtube-transcript <url>            Extract captions from YouTube video
browse youtube-transcript <url> --lang en  Specify caption language
```

## API requests
```
browse api <method> <url>                          Make HTTP request (GET, POST, PUT, DELETE, etc.)
browse api <method> <url> --body '{"key":"val"}'   With JSON body
browse api <method> <url> --header "Auth:Bearer x"  With custom header
```

## Assertions (expect)
```
browse expect --url <pattern>                      Assert current URL matches
browse expect --text <text>                        Assert text exists on page
browse expect --visible <selector>                 Assert element is visible
browse expect --hidden <selector>                  Assert element is hidden
browse expect --count <selector> <n>               Assert element count
browse expect --request <pattern>                  Assert a network request was made
browse expect --timeout 5000                       Custom timeout for assertions (ms)
```

## Visual & Accessibility audit
```
browse visual                  Visual snapshot of the page
browse a11y-audit              Accessibility audit (WCAG violations, warnings, passes)
```

## Flows (reusable test sequences)
```
browse flow <file.yaml>        Run a flow from a YAML file
browse flow save <name>        Save recorded commands as a named flow
browse flow run <name>         Run a saved flow by name
browse flow list               List saved flows
```

## Retry & Watch
```
browse retry "<cmd>" --until <condition>            Retry a command until condition is met
browse retry "<cmd>" --until <cond> --max 5         Max retry attempts (default: 10)
browse retry "<cmd>" --until <cond> --backoff       Exponential backoff between retries
browse watch "<selector>"                           Watch an element for changes
browse watch "<sel>" --on-change "<cmd>"            Run command when element changes
browse watch "<sel>" --timeout 30000                Custom watch timeout (ms)
```

## Cloud Providers
```
browse provider save <name> <key>  Save provider API key (encrypted)
browse provider list               List saved providers
browse provider delete <name>      Delete provider key
```

## React DevTools
```
browse react-devtools enable           Enable React DevTools (downloads hook, injects, reloads)
browse react-devtools disable          Disable React DevTools
browse react-devtools tree             Component tree with indentation
browse react-devtools props <sel>      Props/state/hooks of component at element
browse react-devtools suspense         Suspense boundaries + status
browse react-devtools errors           Error boundaries + caught errors
browse react-devtools profiler         Render timing per component
browse react-devtools hydration        Hydration timing (Next.js)
browse react-devtools renders          What re-rendered since last commit
browse react-devtools owners <sel>     Parent component chain
browse react-devtools context <sel>    Context values consumed by component
```

## Server management
```
browse status                  Server health, uptime, session count
browse instances               List all running browse servers (instance, PID, port, status)
browse version                 Print CLI version
browse doctor                  System check (Node, Playwright, Chromium)
browse upgrade                 Self-update via npm
browse stop                    Shutdown server
browse restart                 Kill + restart server
browse inspect                 Open DevTools (requires BROWSE_DEBUG_PORT)
```

## CLI Flags

| Flag | Description |
|------|-------------|
| `--session <id>` | Named session (isolates tabs, refs, cookies — auto-persists on close) |
| `--profile <name>` | Persistent browser profile (own Chromium, full state) |
| `--state <path>` | Load state file (cookies/storage) before first command |
| `--json` | Wrap output as `{success, data, command}` |
| `--content-boundaries` | Wrap page content in nonce-delimited markers (prompt injection defense) |
| `--allowed-domains <d,d>` | Block navigation/resources outside allowlist |
| `--max-output <n>` | Truncate output to N characters |
| `--headed` | Run browser in headed (visible) mode |
| `--chrome` | Shortcut for `--runtime chrome --headed` (uses real Chrome, bypasses bot detection) |
| `--cdp <port>` | Connect to Chrome on a specific debugging port |
| `--connect` | Auto-discover and connect to a running Chrome instance |
| `--provider <name>` | Cloud browser provider (browserless, browserbase) |
| `--runtime <name>` | Browser engine: playwright (default), camoufox (anti-detection Firefox), rebrowser (stealth), lightpanda, chrome |
| `--ready` | Wait for hydration/readiness after goto |
| `--force` | Force-click through overlay interception |
| `--serp` | Google SERP fast extraction mode |
| `--mcp` | Run as MCP server (for Cursor, Windsurf, Cline) |
| `--context` | Show state changes after commands |
| `--context delta` | ARIA diff with refs |
| `--context full` | Complete snapshot with refs after write commands |
| `--camoufox-profile <name>` | Use a named camoufox profile for browser launch (JSON in `.browse/camoufox-profiles/<name>.json`). Only applies when starting a new server. |
| `--platform <ios\|android>` | Target native app platform |
| `--app <id-or-path>` | Target app by bundle ID, package name, or file path (.app/.ipa/.apk) |
| `--device <name>` | Simulator/emulator device name (e.g. "iPhone 15", "Pixel 7") |

## Handoff (human takeover)
```
browse handoff [reason]        Swap to visible browser for user to solve CAPTCHA/MFA
browse resume                  Swap back to headless, returns fresh snapshot
```

See [guides.md](guides.md) for the mandatory handoff protocol.
