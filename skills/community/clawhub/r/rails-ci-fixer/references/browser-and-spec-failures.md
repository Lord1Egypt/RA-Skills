# Browser And Spec Failures

System spec and browser failures that only reproduce in CI.

## System Specs / Browser in CI

### Browser differs between local and CI

The same spec passes locally and fails in CI. The usual causes:

1. **Viewport height.** Headless Chrome's default window is about 683px tall. A
   modal taller than that reports its fields as not visible even though they are
   in the DOM.
   ```ruby
   options.add_argument("--window-size=1400,1400")
   ```
2. **Firefox ignoring `no_proxy`.** Firefox does not honour `NO_PROXY`/`no_proxy`
   for its own traffic. On a proxied runner, WebDriver's localhost connection
   gets intercepted and every system spec fails with a proxy error.
   ```ruby
   options.add_preference("network.proxy.no_proxies_on", "localhost,127.0.0.1")
   ```
3. **Hardcoded browser in the spec.** A spec that forces Firefox while CI runs
   Chrome exercises a different engine than CI will.
4. **Version drift.** Driver and browser versions must match and must be pinned in
   CI.

### A spec overrides the driver

```ruby
# ❌ this spec forces a browser that CI does not have
RSpec.describe "Checkout", type: :system do
  driven_by :selenium, using: :firefox, screen_size: [1400, 1400]
  # ...
end
```

A per-spec `driven_by` overrides the shared driver registration. If the CI
image does not have that browser installed, the spec fails with a driver error
that looks unrelated to the spec.

```ruby
# ✅ use the shared driver, or make the override match CI exactly
RSpec.describe "Checkout", type: :system do
  # no driven_by - inherits the registered headless driver
end
```

Grep for overrides before assuming the shared driver is in effect:

```bash
grep -rn "driven_by" spec/
```

If an override is needed, make it conditional on an env var so CI and local runs
use the same path:

```ruby
driven_by :selenium, using: (ENV["BROWSER"] || :chrome).to_sym
```

### Service worker serves a cached page

A registered service worker can serve stale content, so the spec asserts against
an older page and the failure looks like a rendering bug.

```ruby
# ✅ disable service workers in the test driver
options.add_argument("--disable-features=ServiceWorker")
```

### `deliver_later` never delivers in the test environment

The default `:test` ActiveJob adapter only records the job, so
`ActionMailer::Base.deliveries` does not change.

```ruby
# ✅ assert on the enqueued job
expect { sign_up }.to have_enqueued_job(ActionMailer::MailerJob)

# ✅ or perform it inline
expect { perform_enqueued_jobs { sign_up } }
  .to change { ActionMailer::Base.deliveries.count }.by(1)
```

### `sign_in` undefined in a request spec

```text
NoMethodError: undefined method 'sign_in'
```

```ruby
# spec/rails_helper.rb
config.include Devise::Test::IntegrationHelpers, type: :request
```

And in a Devise app, use Devise's `sign_in`, not Warden's `login_as` - `login_as`
does not create a Devise session, so `current_user` comes back `nil` with no
obvious cause.

---
