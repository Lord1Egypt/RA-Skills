# Devise And Mailers

Devise vs Warden sign-in, and background mail delivery in specs.

## Devise vs Warden — `sign_in` is not `login_as`

These are different mechanisms and they are not interchangeable.

```ruby
# ✅ Devise — full authentication, sets the session cookie
sign_in user
sign_out

# ✅ Devise with specific scope
sign_in user, scope: :admin

# ✅ Warden — the underlying mechanism, for non-Devise setups
login_as user
```

**Failure mode:** a spec uses `login_as` in a Devise app. The user has no
`remember_me` cookie, no Devise session entry, and every Devise
`current_user` check returns `nil`. The spec then fails at an authorization
redirect with no obvious cause.

**The reverse failure:** a spec uses `sign_in` where it needed only a stubbed
identity — this triggers real Devise callbacks and can create audit records.

Use `sign_in` for Devise apps. Use `login_as` only when the app has no Devise.

### Devise `sign_in` in a controller/request spec

`sign_in` is a Devise test helper for system specs. In request specs, use the
Devise integration helpers:

```ruby
RSpec.configure do |config|
  config.include Devise::Test::IntegrationHelpers, type: :request
end

# ✅
sign_in user
get dashboard_path
```

Forgetting this include means `sign_in` is undefined — the classic
`NoMethodError: undefined method 'sign_in'` in a request spec.

---

## `deliver_later` races in system specs

`deliver_later` enqueues to ActiveJob. In the test environment the default
adapter is `:test`, which **does not perform the job** — it only records it. So:

```ruby
# ❌ The email is never sent in the test env
expect { sign_up }.to change { ActionMailer::Base.deliveries.count }.by(1)
```

The count does not change, because `deliver_later` enqueues rather than sends.

```ruby
# ✅ Use deliver_now in the environment under test
# OR perform the job inline
ActiveJob::Base.queue_adapter = :inline

# OR assert on the enqueued job instead of the delivery
expect { sign_up }
  .to have_enqueued_job(ActionMailer::MailerJob)
  .with("Welcome", "user@example.com")
```

Choose deliberately:

| Approach | Use when |
|---|---|
| `deliver_now` in code | the app should send synchronously; fine for low volume |
| `queue_adapter = :inline` | testing the full mail path including delivery |
| `have_enqueued_job` | asserting on scheduling, not delivery |
| `perform_enqueued_jobs` | inside a block, to also assert the result |

```ruby
# ✅ perform_enqueued_jobs inside the block
expect {
  perform_enqueued_jobs { sign_up }
}.to change { ActionMailer::Base.deliveries.count }.by(1)
```

---
