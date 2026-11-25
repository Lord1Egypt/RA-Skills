# Stale Content And Waiting

Stale page content, frame timing conflicts, and correct waiting.

## Service workers break headless loads

A registered service worker can serve a **cached** copy of the page, so a spec
asserts against stale content and the failure looks like a rendering bug.

```ruby
# ✅ disable service workers in the test driver
Capybara.register_driver :headless_chrome do |app|
  options = Selenium::WebDriver::Chrome::Options.new
  # ...
  options.add_argument("--disable-features=ServiceWorker")
end
```

This is the reliable fix, because it does not depend on the application code
taking a different path in the test environment.

**Assert on the effect, not the registration.** When a spec fails and you are
not sure whether the browser is showing a stale page, check the content that
the spec is actually asserting on rather than looking for registration calls:

```ruby
# ✅ ask the browser what it has cached
page.execute_script("caches.keys().then(ks => ks.join(','))")
```

If the application does register a worker outside the test environment, the
two things worth asserting in a system spec are that the page still renders
current content:

```ruby
it "does not serve a cached page" do
  expect(page).to have_content(current_expected_copy)
end
```

**Symptom:** a spec asserts on content that was edited minutes ago, and the
assertion fails against what looks like a correct page.

---

## `data-turbo-frame` + `data-turbo="false"` conflict

If a form has both attributes, Turbo's behavior is undefined and the submit
silently does nothing. Pick one:

```erb
<%# ❌ both attributes — undefined behavior %>
<%= form_with model: @record, data: { turbo_frame: "modal", turbo: false } %>
```

```erb
<%# ✅ Turbo-managed, targeted at the frame %>
<%= form_with model: @record, data: { turbo_frame: "modal" } %>
```

---

## Waiting correctly

```ruby
# ✅ wait for the outcome, not for a sleep
expect(page).to have_content("Saved")
click_button "Save"

# ❌
sleep 2
expect(page).to have_content("Saved")
```

For elements that appear asynchronously, `have_content` and `have_css` wait up
to `Capybara.default_max_wait_time` (default 2s — raise it to 5 for Turbo apps).

For an element that should *disappear*:

```ruby
expect(page).to have_no_content("Loading")
```

For a Turbo Drive navigation, `have_current_path` waits for the URL:

```ruby
expect(page).to have_current_path(root_path)
```

---
