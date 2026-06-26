# Inertia Prop Options in Alba

Full syntax for all `inertia:` option variants on attributes and associations.

## All Options

```ruby
class DashboardIndexResource < ApplicationResource
  # Regular prop
  attributes :title

  # Optional — only evaluated on partial reload requesting it
  has_many :users, resource: UserResource, inertia: :optional

  # Deferred — loaded after initial page render
  attribute :stats, inertia: :defer

  # Deferred with group — multiple deferred props fetched in one request
  attribute :chart, inertia: { defer: { group: 'analytics' } }

  # Deferred with group and merge — appended to existing data
  attribute :chart, inertia: { defer: { group: 'analytics', merge: true } }

  # Once — resolved once, cached across navigations
  has_many :countries, inertia: :once

  # Once with expiry — re-evaluated after time limit
  has_many :live_now, inertia: { once: { expires_in: 5.minutes } }

  # Merge — for infinite scroll (appends to existing array)
  has_many :items, inertia: { merge: true }

  # Merge with match_on — deduplicates by field
  has_many :items, inertia: { merge: { match_on: :id } }

  # Scroll — scroll-aware prop for infinite scroll
  has_many :feed, inertia: :scroll

  # Always — included even in partial reloads
  attribute :csrf, inertia: { always: true }
end
```

## Combining Options

Options can be combined in the hash form:

```ruby
# Deferred + grouped + merged
attribute :feed, inertia: { defer: { group: 'feed', merge: { match_on: :id } } }

# Once with expiry
has_many :categories, inertia: { once: { expires_in: 10.minutes } }
```
