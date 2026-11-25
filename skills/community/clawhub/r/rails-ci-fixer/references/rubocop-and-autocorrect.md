# RuboCop And Autocorrect

RuboCop autocorrect that breaks the suite, and whole-tree RuboCop runs.

## RuboCop Autocorrect Breaking RSpec

### `Style/NumericPredicate` turns `be.positive?` into `be_positive`

```text
NoMethodError: undefined method `be_positive'
```

RuboCop's `Style/NumericPredicate` cop rewrites predicate-style matchers to
non-question-mark method calls. It does not know `be.positive?` is an RSpec
matcher, so the autocorrect produces a call to a method that does not exist.

```ruby
# ✅ correct - RSpec matcher form
expect(result).to be.positive

# ❌ produced by RuboCop - raises NoMethodError at runtime
expect(result).to be_positive
```

**Fix:** exclude the RSpec matcher form.

```yaml
# .rubocop.yml
Style/NumericPredicate:
  AllowedMethods:
    - be_positive
    - be_negative
```

**Always read the diff RuboCop produces before committing.** An autocorrect that
changes a matcher form is a runtime bug, not a style fix - the spec suite will
still be green locally if that spec was not run.

### RuboCop with no path walks the whole tree

```bash
# ❌ walks the entire repo including vendored and generated code
bundle exec rubocop -A
```

This can pick up files under `vendor/`, `tmp/`, `node_modules/`, or a gem
checkout, report offenses in code you do not own, and autocorrect them. It is
also slow enough to look like a hang.

```bash
# ✅ scope to the code you actually changed
bundle exec rubocop -A app/ spec/
```

If you must run it repo-wide, exclude the paths you do not own:

```yaml
# .rubocop.yml
AllCops:
  Exclude:
    - "vendor/**/*"
    - "node_modules/**/*"
    - "tmp/**/*"
    - "db/schema.rb"
```

### `rubocop -A` changed a test's structure

`-A` (unsafe autocorrect) can rewrite test code beyond formatting - collapsing
a `describe` block, changing `should` syntax, or merging assertions. That breaks
the single-expectation convention this repo follows.

```bash
# ✅ check what changed before committing
bundle exec rubocop -A app/ spec/
git diff --stat spec/
git diff spec/   # read it
```

**Never accept an autocorrect that changed the number of expectations in a
spec.** Revert it and fix the offense by hand.

---
