# Accessibility Testing

Setting up automated a11y checks in Rails CI with axe-core, RSpec, and system specs.

## Setup

### Gemfile

```ruby
group :test do
  gem 'axe-core-rspec', '~> 4.10'
  gem 'axe-core-capybara', '~> 4.10'
  gem 'capybara', '~> 3.40'
  gem 'selenium-webdriver', '~> 4.20'
end
```

### RSpec configuration

```ruby
# spec/support/axe.rb
require 'axe-rspec'
require 'axe-capybara'

RSpec.configure do |config|
  config.include AxeHelper, type: :system
end
```

```ruby
# spec/support/axe_helper.rb
module AxeHelper
  # Run axe on the full page
  def expect_accessible(skip: [])
    expect(page).to be_axe_clean
      .according_to(:wcag2a, :wcag2aa, :wcag21a, :wcag21aa)
      .skipping(*skip)
  end

  # Run axe within a specific element
  def expect_element_accessible(selector, skip: [])
    within(selector) do
      expect(page).to be_axe_clean
        .according_to(:wcag2a, :wcag2aa, :wcag21a, :wcag21aa)
        .skipping(*skip)
    end
  end
end
```

### System spec configuration

```ruby
# spec/support/capybara.rb
RSpec.configure do |config|
  config.before(:each, type: :system) do
    driven_by :selenium_headless
  end
end
```

## Smoke Test Pattern

A single spec that visits key pages and runs axe:

```ruby
# spec/system/accessibility_spec.rb
require 'rails_helper'

RSpec.describe 'Accessibility', type: :system do
  # Public pages (no auth required)
  describe 'public pages' do
    %w[/ /about /sign_in /sign_up].each do |path|
      it "#{path} is accessible" do
        visit path
        expect_accessible
      end
    end
  end

  # Authenticated pages
  describe 'authenticated pages' do
    before { sign_in user }

    %w[/dashboard /rides /profile].each do |path|
      it "#{path} is accessible" do
        visit path
        expect_accessible
      end
    end
  end

  # Pages with known issues (skip specific rules)
  describe 'pages with known issues' do
    it 'map page skips color-contrast on third-party map tiles' do
      sign_in user
      visit new_ride_path
      expect_accessible(skip: ['color-contrast'])
    end
  end

  # Form error states
  describe 'form error states' do
    it 'sign up form errors are accessible' do
      visit new_user_registration_path

      # Submit empty form to trigger errors
      click_button 'Sign up'

      # Error summary should be an alert
      expect(page).to have_css('[role="alert"]')

      # Error fields should have aria-invalid
      expect(page).to have_css('input[aria-invalid="true"]')

      # Error messages should be linked to inputs
      expect(page).to have_css('[aria-describedby*="_error"]')

      # Run axe on the error state
      expect_accessible
    end
  end
end
```

**Authenticated smoke tests must use form-based sign-in, not Devise's `sign_in` helper** — see the Devise gotcha at the bottom of this file.

## Per-Feature Testing

Add `expect_accessible` to existing system specs:

```ruby
# spec/system/rides_spec.rb
it 'creates a ride with accessible form' do
  sign_in patron
  visit new_ride_path

  fill_in 'Pickup', with: '123 Main St'
  fill_in 'Dropoff', with: '456 Oak Ave'
  click_button 'Request Ride'

  expect(page).to have_content 'Ride requested'
  expect_accessible
end
```

## CI Integration

### GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4

      - name: Set up Ruby
        uses: ruby/setup-ruby@v1
        with:
          bundler-cache: true

      - name: Set up Node
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'yarn'

      - name: Install dependencies
        run: |
          bundle install
          yarn install

      - name: Prepare database
        env:
          RAILS_ENV: test
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/myapp_test
        run: bin/rails db:create db:schema:load

      - name: Precompile assets
        env:
          RAILS_ENV: test
        run: bin/rails assets:precompile

      - name: Run tests (including a11y)
        env:
          RAILS_ENV: test
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/myapp_test
        run: bin/rspec
```

## Common axe-core Rules to Skip

Some rules produce false positives or are out of scope:

| Rule | Why Skip |
|---|---|
| `color-contrast` | Third-party content (maps, embeds) you don't control |
| `landmark-one-main` | Pages with multiple `<main>` elements (rare, usually a real bug) |
| `region` | Pages where sections don't need labels (use sparingly) |
| `duplicate-id` | Third-party scripts injecting elements (fix if it's your code) |

**Don't skip rules globally.** Skip per-test with a comment explaining why:

```ruby
# Map tiles are third-party — we can't control their contrast
expect_accessible(skip: ['color-contrast'])
```

## Devise `sign_in` Gotcha

Devise's `sign_in` test helper can silently fail in `driven_by(:selenium_headless)` — the session cookie doesn't transfer to the browser process. Symptoms:

- `current_url` returns `data:,` after `sign_in user`
- Authenticated elements not found
- Tests pass in isolation but fail in larger suites

**Fix:** Sign in through the actual form:

```ruby
def sign_in_via_form(user)
  visit new_user_session_path
  fill_in 'Email', with: user.email
  fill_in 'Password', with: user.password
  click_button 'Sign in'
  expect(page).to have_content 'Signed in successfully'
end
```

## Turbo Frame `click_link` race condition

Clicking a `data: { turbo_frame: "modal" }` link fires an async fetch and returns immediately. Capybara's default 2s wait is often shorter than the round-trip, so the next assertion runs against a frame that still has `aria-busy="true"` and no body. The failure looks like "form field not found" but the controller is fine.

**Symptoms:**

- `click_link "X"` followed by `expect(page).to have_selector("turbo-frame#modal", visible: :all)` passes (matches the empty frame)
- `within(:css, "main") { fill_in "Field", with: "..." }` fails with `Capybara::ElementNotFound` for fields the form definitely contains
- A direct `get "/x/new", headers: { "Turbo-Frame" => "modal" }` request spec returns the full form
- The captured page HTML shows `<turbo-frame id="modal" src="..." busy="" aria-busy="true"></turbo-frame>` — frame issued, response not landed

**Diagnostic — confirm it's the race, not a real bug:**

```ruby
# In a throwaway spec, swap to rack_test and request the modal endpoint directly.
# If the body contains the form, the controller is correct and the Selenium
# test is racing the frame-swap.
it "dumps the modal response" do
  sign_in user
  get "/rides/new", headers: { "Turbo-Frame" => "modal" }
  puts response.body[0, 3000]  # look for the form
  expect(true).to eq(true)
end
```

**Fixes (pick one):**

1. **Wait for the frame content, not the frame element** — `have_selector` matches empty frames, so wait for something only the populated frame contains:
   ```ruby
   click_link "Schedule A Ride"
   expect(page).to have_selector("turbo-frame#modal form", wait: 10)
   within(:css, "main") { fill_in "Pickup address", with: "..." }
   ```
2. **Bump Capybara's default wait** in `spec/rails_helper.rb`:
   ```ruby
   Capybara.default_max_wait_time = 10
   ```
   Broader change; affects every system spec.
3. **Use `:rack_test` for modal-flow tests** when you only need to assert the form is rendered, not the JS swap. A rack-test request to the same endpoint returns the full form without the browser round trip, which makes it a fast way to separate "the controller renders the wrong thing" from "the browser never got there".

**When to skip this rule:** if a `data-turbo-frame` link is meant to do a synchronous full-page render (it isn't — that's what `data-turbo="false"` is for), or if your test doesn't read the frame body.

## Performance

Axe-core adds ~200-500ms per `expect_accessible` call. For large test suites:

- Run a11y checks on key pages only (smoke test pattern)
- Don't add `expect_accessible` to every single system spec
- Consider a separate CI job for the full a11y suite

## Related

This file is the home for the `expect_accessible` matcher referenced by every other reference (`forms.md`, `modals.md`, `navigation.md`, `dynamic-content.md`, `color-contrast.md`). When you add a new system spec anywhere, the axe-core call goes through the helpers defined here.
