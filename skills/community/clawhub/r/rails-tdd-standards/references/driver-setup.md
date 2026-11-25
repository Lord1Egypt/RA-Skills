# Driver Setup

Capybara + Selenium driver configuration for system specs.

## Setup

```ruby
# spec/rails_helper.rb
require "capybara/rails"
require "selenium-webdriver"

Capybara.register_driver :headless_chrome do |app|
  options = Selenium::WebDriver::Chrome::Options.new
  options.add_argument("--headless=new")
  options.add_argument("--disable-gpu")
  options.add_argument("--window-size=1400,1400")
  options.add_argument("--disable-dev-shm-usage")
  options.add_argument("--disable-search-engine-choice-screen")
  # Required when the app is behind a proxy. Scope the bypass to loopback so
  # the browser still routes external traffic through the proxy. A wildcard
  # bypass list would let the browser reach every destination directly.
  options.add_argument("--proxy-bypass-list=localhost;127.0.0.1;[::1]")
  options.binary = "/path/to/chrome" # optional, if not on PATH
  Capybara::Selenium::Driver.new(app, browser: :chrome, options: options)
end

Capybara.default_driver = :headless_chrome
Capybara.server = :puma, { Silent: true }
Capybara.default_max_wait_time = 5
```

**About the proxy bypass:** the bypass list above is scoped to loopback
addresses, because that is the only traffic a system spec needs to reach
directly. Do not widen it to `*`. A wildcard bypass means the browser ignores
the machine's proxy configuration for every destination, which silently routes
external traffic around any network controls the environment relies on. If a
spec needs to reach a non-loopback host, add that specific host instead.

**About `--no-sandbox`:** Chrome's sandbox is what isolates the browser process
from the rest of the machine. Disabling it removes that containment, so anything
the browser renders runs with the full privileges of the test user. Do not add
it by default.

It is occasionally needed inside a container that lacks the user namespaces the
sandbox requires, and it is occasionally needed on CI images that run as root.
If you do need it, scope it to that environment rather than putting it in the
shared driver:

```ruby
# ✅ only when the environment requires it
if ENV["CHROME_NO_SANDBOX"] == "1"
  options.add_argument("--no-sandbox")
end
```

On a normal developer machine and on a CI image with a non-root user, the
sandbox works fine and should stay on.

---
