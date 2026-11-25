# Rails 8 Spec Compatibility

Rails 8 changed two controller-side APIs. Specs that exercise those endpoints
need to match the new behaviour. This reference covers what changed and how to
spec it.

## Strong parameters

Rails 8 introduces a stricter parameter helper as the preferred pattern. It
works for flat parameters and simple nested lists.

```ruby
# works for flat + simple nested
params.expect(post: [:title, :body, tag_ids: []])
```

**It does not work for nested attributes keyed by index.** A form that posts
nested attributes as a hash keyed by `"0"`, `"1"`, and so on will have those
keys stripped, and the spec fails on missing nested attributes rather than on
anything that looks like a parameter problem.

```ruby
# use the classic helper for index-keyed nested attributes
params.require(:post).permit(:title, items_attributes: [:id, :name, :_destroy])
```

**How to spot it in a failing spec:** the controller received the top-level
attributes correctly but the nested collection came back empty. If the spec
posts nested attributes and they are missing, this is the cause.

## CSRF behavior

Rails 8 replaced the `skip_before_action` callback form with a class macro.
The new macro is the one to use, but its scope matters.

**The macro belongs on an API-only controller** - one that renders no forms and
authenticates machine clients that carry their own token. It is not something
to add to a controller that serves an HTML form.

**For the specs:** a request spec that fails on an invalid-authenticity-token
error is usually missing the token that the real form includes. That is a spec
problem, not a controller problem. Fix the spec so it posts the way the browser
posts.

```ruby
# the spec should exercise the same path the browser takes
post user_path, params: { user: { name: "Ada" } }
```

Do not weaken the controller to satisfy a test. If the endpoint is genuinely an
API endpoint with no browser form, then the token check is not what that spec
was testing, and the failure points at a different assertion.

## Rails 8 response status codes

`:unprocessable_entity` is deprecated in favour of `:unprocessable_content`.

```ruby
expect(response).to have_http_status(:unprocessable_content)
```

## Forgery protection in tests

```ruby
# the Rails 8 form of the callback
skip_forgery_protection
```

Only appropriate on an API-only controller. See the CSRF behavior section above
for the scoping rule and for how to fix a spec that trips the token check.

## Related

- `references/devise-and-mailers.md` - signing in and background delivery in specs
