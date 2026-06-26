---
name: rails-tdd-standards
description: RSpec testing standards and best practices for Rails applications. Use when writing new tests, reviewing test quality, debugging factory errors, setting up FactoryBot, or enforcing single-expectation patterns. Also use when a test fails due to factory misconfiguration, wrong association keys, or missing role traits. Triggers on phrases like "write a test", "add specs", "factory error", "test is failing", "how should I test this", or when reviewing test code in a Rails project.
metadata: {"clawdbot":{"emoji":"🧪","requires":{"bins":["bundle"]},"os":["linux","darwin","win32"]}}
---

# Rails TDD Standards

Best practices for writing clean, reliable RSpec tests in Rails applications.

## Core Principle: Single Expectation

One assertion per test. Tests should read like specifications — each `it` block verifies exactly one thing.

```ruby
# ✅ Correct
it { is_expected.to validate_presence_of(:email) }
it { is_expected.to belong_to(:user) }

# ❌ Wrong — too many expectations in one test
it "validates the user" do
  expect(user).to validate_presence_of(:email)
  expect(user).to validate_presence_of(:name)
  expect(user).to be_valid
end
```

## FactoryBot Patterns

### Always use role traits
```ruby
# ✅ Correct
create(:user, :admin)
create(:user, :member)
create(:user, :guest)

# ❌ Wrong — missing role context
create(:user)
```

### Association keys matter
Check your factory definitions carefully. Wrong keys cause silent failures.

```ruby
# ✅ Example — if your factory uses owner:
create(:profile, owner: user)

# ❌ Wrong key
create(:profile, user: user)  # fails if factory expects owner:
```

### Always set required associations
When a model requires a specific association to be valid, always set it explicitly — don't rely on factory defaults when they might be nil or wrong.

```ruby
# ✅ Explicit — clear intent, no surprises
let(:record) do
  create(:model, required_association: other_record)
end

# ❌ Implicit — may break if factory default changes
let(:record) { create(:model) }
```

### Use `described_class` not hardcoded class names
```ruby
# ✅
subject { described_class.new(params) }

# ❌
subject { MyService.new(params) }
```

## Common FactoryBot Gotchas

### Join tables without primary key
Tables with `id: false` can't use `.last` or `.first`.

```ruby
# ✅ Use a scoped query
record = JoinModel.find_by(field_a: a, field_b: b)

# ❌ Will raise ActiveRecord::MissingRequiredOrderError
record = JoinModel.last
```

### RecordInvalid from missing role/trait
If you see `Validation failed: X must have Y role` — you're missing a trait on the user factory.

```ruby
# ✅
user = create(:user, :editor)

# ❌ causes "must be an editor" validation error
user = create(:user)
```

## Spec Structure

```ruby
RSpec.describe MyClass do
  # Subject
  subject(:instance) { described_class.new(params) }

  # Shared setup
  let(:user) { create(:user, :admin) }

  # Group by behavior
  describe "#method_name" do
    context "when condition is true" do
      it "does the expected thing" do
        expect(instance.method_name).to eq(expected)
      end
    end

    context "when condition is false" do
      it "does something else" do
        expect(instance.method_name).to be_nil
      end
    end
  end
end
```

## Mocking & Stubbing

```ruby
# Stub a method
allow(object).to receive(:method_name).and_return(value)

# Stub and verify it was called
expect(object).to receive(:method_name).once

# Stub HTTP calls (WebMock)
stub_request(:post, "https://api.example.com/endpoint")
  .to_return(status: 200, body: { result: "ok" }.to_json)

# Allow localhost for system tests (if using WebMock)
WebMock.disable_net_connect!(allow_localhost: true)
```

## Service Object Testing

```ruby
RSpec.describe MyService do
  describe "#call" do
    context "with valid params" do
      it "returns the expected result" do
        result = described_class.new(valid_params).call
        expect(result).to be_a(ExpectedClass)
      end

      it "creates the expected record" do
        expect { described_class.new(valid_params).call }
          .to change(Record, :count).by(1)
      end
    end

    context "with invalid params" do
      it "returns false" do
        expect(described_class.new(invalid_params).call).to be(false)
      end
    end
  end
end
```

## Rails 8 Gotchas

### Status codes changed
`:unprocessable_entity` is deprecated in Rails 8.0.2+. Use `:unprocessable_content` in response assertions.

```ruby
# ✅ Rails 8
expect(response).to have_http_status(:unprocessable_content)

# ❌ Deprecated (will warn/fail)
expect(response).to have_http_status(:unprocessable_entity)
```

### params.expect vs require/permit
Rails 8 introduces `params.expect` as the preferred strong params pattern. But watch out: **`params.expect` strips nested hash-keyed arrays** (like `items_attributes: { "0" => { ... } }`).

```ruby
# ✅ params.expect — works for flat + simple nested
params.expect(post: [:title, :body, tag_ids: []])

# ✅ Use require/permit for nested attributes with "0"-keyed hashes
params.require(:post).permit(:title, items_attributes: [:id, :name, :_destroy])

# ❌ params.expect breaks "0"-keyed nested attributes
# params.expect(post: [items_attributes: [...]])  ← strips the hash keys
```

### skip_forgery_protection
```ruby
# ✅ Rails 8
skip_forgery_protection

# ❌ Deprecated
skip_before_action :verify_authenticity_token
```

---

## CI Database Setup

**Critical:** Never use `db:prepare` in CI. It runs seeds, which pollutes the test database and causes scoped queries to return unexpected results.

```yaml
# ✅ CI config (GitHub Actions / etc.)
- run: bundle exec rails db:schema:load RAILS_ENV=test

# ❌ Runs seeds → pollutes test DB → scope specs fail
- run: bundle exec rails db:prepare RAILS_ENV=test
```

If you see scope specs randomly returning too many records, check your CI DB setup first. Seeds belong in development, not the test environment.

---

## Callback Testing: before_create vs before_validation

`before_create` callbacks are **skipped by FactoryBot's `build()`**. If your callback needs to fire during `build` (e.g., for token generation, slug assignment), use `before_validation on: :create` instead.

```ruby
# ✅ Works with both build() and create()
before_validation :generate_token, on: :create

# ❌ Skipped by build() — token will be nil in specs using build
before_create :generate_token
```

This is especially important for:
- Token generation (API keys, one-time tokens)
- Slug generation
- Setting default values that specs need to assert on
- Any callback you expect to fire when using `build(:model)`

---

## Token Authentication Testing

Never test for raw token values — tokens should be hashed on save. Test that:
1. A digest was stored (not nil)
2. The `authenticate` / `find_by_token` method works correctly

```ruby
RSpec.describe ApiToken do
  describe "token generation" do
    it "stores a hashed digest, not the raw token" do
      token = build(:api_token)
      token.save!
      expect(token.token_digest).to be_present
    end

    it "authenticates with the raw token" do
      token = ApiToken.new(name: "test")
      token.save!
      raw = token.raw_token  # capture from one-time return before it's gone
      expect(ApiToken.authenticate(raw)).to eq(token)
    end
  end
end
```

For request specs, generate the token in a `let` block and inject it as a header:

```ruby
let(:user) { create(:user) }
let(:raw_token) do
  t = user.api_tokens.build(name: "test")
  t.save!
  t.raw_token
end

before { get "/api/v1/resources", headers: { "Authorization" => "Bearer #{raw_token}" } }
```

> The `raw_token` method name is implementation-specific — adjust to match whatever your model exposes after save.

---

## ActionCable Channel Testing

Use `stub_connection` to inject the authenticated user into the channel connection.

```ruby
RSpec.describe NotificationsChannel, type: :channel do
  let(:user) { create(:user) }

  before { stub_connection current_user: user }

  describe "#subscribed" do
    it "subscribes to the user stream" do
      subscribe
      expect(subscription).to be_confirmed
      expect(streams).to include("notifications:user:#{user.id}")
    end
  end

  describe "#unsubscribed" do
    it "stops all streams" do
      subscribe
      unsubscribe
      expect(streams).to be_empty
    end
  end
end
```

Test broadcast behavior with `have_broadcasted_to`:

```ruby
it "broadcasts a notification to the user stream" do
  subscribe
  expect {
    NotificationsChannel.broadcast_to(user, { type: "alert", message: "You have a new message" })
  }.to have_broadcasted_to(user).with(hash_including(type: "alert"))
end
```

---

## External Service Stubs

Always stub external services in unit and integration specs. Never make real API calls in tests.

### Geocoder
```ruby
# In spec_helper or a shared context
before do
  allow(Geocoder).to receive(:search).and_return(
    [double(coordinates: [40.7128, -74.0060], city: "New York", state: "NY")]
  )
end
```

### Stripe
```ruby
# Stub a PaymentIntent creation
before do
  allow(Stripe::PaymentIntent).to receive(:create).and_return(
    double(id: "pi_test_123", status: "requires_capture", client_secret: "secret_abc")
  )
end

# For HTTP-level stubs (WebMock)
stub_request(:post, "https://api.stripe.com/v1/payment_intents")
  .to_return(status: 200, body: { id: "pi_test_123", status: "requires_capture" }.to_json)
```

### General pattern
Any service that hits the network should be stubbed. If you find yourself relying on VCR cassettes for unit tests, consider switching to explicit doubles — they're faster and don't require recorded responses.

---

## Serializer Testing

Test serializers directly — don't test through controllers. Assert on the JSON output structure.

```ruby
RSpec.describe ArticleSerializer do
  let(:article) { create(:article, :published) }

  subject(:json) { described_class.new(article).as_json }

  it "includes expected public keys" do
    expect(json.keys).to include(:id, :title, :body, :published_at)
  end

  it "excludes sensitive internal fields" do
    expect(json.keys).not_to include(:internal_cost_cents, :vendor_id)
  end

  context "with an admin scope" do
    subject(:json) { described_class.new(article, scope: { role: :admin }).as_json }

    it "includes admin-only fields" do
      expect(json.keys).to include(:cost_breakdown, :vendor_id)
    end
  end
end
```

---

## Running Tests

```bash
# Run full suite
bundle exec rspec

# Run specific file
bundle exec rspec spec/models/user_spec.rb

# Run specific line
bundle exec rspec spec/models/user_spec.rb:42

# Run only failures from last run
bundle exec rspec --only-failures

# Run with documentation format
bundle exec rspec --format documentation
```

## See Also

- `references/factory-patterns.md` — advanced FactoryBot patterns
- `references/system-specs.md` — Capybara / browser testing setup
