# Browser Divergence

Why the same spec passes locally and fails in CI.

## Browser divergence is the #1 source of "passes locally, fails in CI"

The same spec can pass in one browser and fail in another. The failure is often
reported as a *flake* when it is actually a **deterministic** difference.

| Difference | Symptom |
|---|---|
| Firefox vs Chrome | `driver.switch_to.window` unavailable; different focus order; different `document.activeElement` |
| Headless vs headed | window height differs (headless default ~683px) → elements "not visible" |
| Browser version | `:has()` / `:focus-visible` / `dvh` support differs |
| Driver version | WebDriver protocol mismatch → 502, blank page |
| OS | macOS vs Linux font metrics → different layout, different scroll positions |

**Rule: a failure that reproduces on every run is not a flake.** Classify before
assuming randomness - run the exact spec three times before calling it flaky.

### A spec that overrides the driver

```ruby
# BAD - this spec forces a browser that CI does not have
RSpec.describe "Checkout", type: :system do
  driven_by :selenium, using: :firefox, screen_size: [1400, 1400]
end
```

A per-spec `driven_by` overrides the shared driver registration. If the CI
image does not have that browser installed, the spec fails with a driver error
that looks unrelated to the spec.

```ruby
# GOOD - inherit the registered driver
RSpec.describe "Checkout", type: :system do
end
```

Grep for overrides before assuming the shared driver is in effect:

```bash
grep -rn "driven_by" spec/
```

If an override is needed, make it conditional on an env var so CI and local
runs use the same path:

```ruby
driven_by :selenium, using: (ENV["BROWSER"] || :chrome).to_sym
```

### Pin the browser in CI, and mirror it locally

```yaml
# .github/workflows/ci.yml
- uses: browser-actions/setup-chrome@v1
  with:
    chrome-version: stable
- run: bundle exec rspec
```

If CI uses Chrome, run Chrome locally. A Firefox-only local setup against a
Chrome CI job will produce failures you cannot reproduce on demand.

### Viewport height is the silent killer

A full-page modal taller than the headless viewport reports elements as
**not visible** even though they are in the DOM:

```ruby
# ✅ Raise the window, or size the driver explicitly
options.add_argument("--window-size=1400,1400")

# ✅ Or make the spec viewport-independent
expect(page).to have_content("Title")
click_button "Save"
```

### Firefox needs proxy bypass explicitly

Firefox does not honour `NO_PROXY`/`no_proxy` for its own traffic the way Chrome
does. On a proxied machine, WebDriver's localhost connection gets intercepted and
every spec fails with a proxy error:

```ruby
# In the Firefox profile prefs
options.add_preference("network.proxy.no_proxies_on", "localhost,127.0.0.1")
```

---
