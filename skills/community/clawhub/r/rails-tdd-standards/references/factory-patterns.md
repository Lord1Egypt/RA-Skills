# Advanced FactoryBot Patterns

Reference for `references/factory-patterns.md` in the `rails-tdd-standards` skill.

Patterns that go beyond "use role traits" — the ones where a factory is
misconfigured in a way that produces a *silently wrong* test rather than a loud
error.

---

## Transient attributes

Use `transient` for values that shape the factory but are **not** columns.
Never write them to the record — `ActiveRecord::UnknownAttributeError` is the
loud version, and a persisted column with a test-only value is the quiet version.

```ruby
# ✅
factory :user do
  transient do
    upcased { false }
  end

  name { upcased ? "JANE DOE" : "Jane Doe" }
end

# ❌ upcased leaks into attributes → tries to write a `upcased` column
factory :user do
  upcased { false }
end
```

## Interdependent attributes

A `name` that depends on an `email` needs the email resolved first. Use a block
that reads the attribute, not a captured local.

```ruby
factory :user do
  email { "jane.doe@example.com" }
  name { "User from #{email.split('@').first}" }
end
```

Reading the attribute inside the block (not via a local variable) is what makes
the dependency order correct.

---

## Traits as behavior, not just as role labels

A trait that sets a boolean is usually better expressed as a named trait, because
the spec reads as behavior:

```ruby
# ✅
factory :user do
  trait :admin do
    role { :admin }
  end

  trait :suspended do
    suspended_at { Time.current }
  end

  trait :with_email do
    email { "user@example.com" }
  end
end

create(:user, :admin, :with_email)
```

```ruby
# ❌ magic booleans in specs
create(:user, role: :admin, email: "user@example.com")
```

Magic booleans are the main reason people duplicate factories. A trait named
`:with_email` documents intent; `email: "user@example.com"` does not.

---

## `build` vs `create` vs `build_stubbed`

| Method | DB | Callbacks | `id` | Speed |
|---|---|---|---|---|
| `build` | no | validation only, **no `before_create`** | nil | fast |
| `create` | yes | all | yes | slow |
| `build_stubbed` | no | `after_initialize` + `after_find` only | yes | fastest |

```ruby
# ✅ Use build_stubbed for anything that only needs an identity
user = build_stubbed(:user)
expect(user.persisted?).to be(false)
expect(user.id).to be_present
```

**`build` skips `before_create`.** If a model generates a token in
`before_create`, `build(:user).token` is `nil`. Use
`before_validation on: :create` instead — see the Callback Testing section in
the main SKILL.md.

---

## Sequences vs. explicit values

```ruby
factory :user do
  sequence(:email) { |n| "user#{n}@example.com" }
end
```

`sequence` guarantees uniqueness. An explicit `email: "user@example.com"` in two
specs creates a unique-index violation depending on spec order — which is the
worst kind of flake, because it passes in isolation and fails in CI.

Use explicit values only when the value itself is the thing under test.

---

## Shared traits across models

Put shared traits in a shared trait file and include them:

```ruby
# spec/factories/traits/addressable.rb
FactoryBot.define do
  trait :with_address do
    address { build(:address) }
  end
end
```

```ruby
# spec/factories.rb
Dir[Rails.root.join("spec/factories/**/*.rb")].each { |f| load f }
```

The `Dir[...].each { load }` glob matters: a single `require` of
`spec/factories.rb` will not pick up nested files on all setups.

---

## Callback-heavy factories

When a factory triggers callbacks that a spec does not care about, the factory
gets slow and brittle. Two mitigations:

```ruby
# ✅ Skip callbacks you don't need, via a transient
factory :user do
  transient do
    skip_welcome_email { false }
  end

  after_create :send_welcome_email, unless: :skip_welcome_email
end
```

```ruby
# ✅ Or use a dedicated minimal factory for the unit under test
factory :user_without_callbacks do
  initialize_with { User.new(attributes) }
end
```

The second is a smell — a factory named `without_callbacks` usually means the
specs are asserting against a model that cannot occur in production. Prefer
fixing the callback.

---

## Association strategies

```ruby
factory :post do
  # ✅ create the parent
  association :user, factory: :user

  # ✅ build the parent (no extra INSERT)
  association :user, factory: :user, strategy: :build

  # ✅ use an existing record without creating one
  association :user, factory: :user, strategy: :nullify  # or use an existing let
end
```

**`strategy: :build`** matters for `belongs_to` associations when the parent
only needs to exist in memory. The default `:create` inserts a row you never
assert on, which inflates record counts and slows the suite.

---

## `FactoryBot.lint` — turn it on

```ruby
# spec/rails_helper.rb
FactoryBot.lint traits: true
```

`lint` runs every factory through the full lifecycle and checks that
associations are valid. It catches the majority of factory bugs at load time
instead of in a random spec three hours into a CI run.

Run `lint` locally in CI, and expect it to surface a batch of failures the
first time you enable it. That batch is the value.

---

## Common failure → cause → fix

| Failure | Cause | Fix |
|---|---|---|
| `ActiveRecord::RecordInvalid` | required association missing | set it explicitly, don't rely on defaults |
| `Validation failed: ... must have X role` | missing role trait | add the trait: `create(:user, :admin)` |
| `ActiveRecord::RecordNotUnique` | non-unique explicit value | use `sequence(:email)` |
| `NoMethodError: undefined method 'token'` | `before_create` skipped by `build` | `before_validation on: :create` |
| `ActiveRecord::MissingRequiredOrderError` | `.last`/`.first` on `id: false` table | scoped `find_by` |
| `AssociationNotFoundError` | wrong association key | check the factory's association name |
| Spec passes alone, fails in suite | factory creates a record the spec counts | `strategy: :build`, or scope the query |

---

## Related

- `rails-tdd-standards` — main skill
- `references/system-specs.md` — Capybara / browser testing setup
- `rails-ci-fixer` — CI failure triage
