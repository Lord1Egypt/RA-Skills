# Debugging A Failing Spec

Techniques for getting a useful failure message out of a spec that fails for an unclear reason.

## Debug Approach

For sub-agent / non-interactive debugging:
```ruby
pp object                                    # inspect any object
raise object.inspect                         # force output and halt
puts object.errors.full_messages.inspect     # ActiveRecord errors
puts object.class                            # check type
```

For local interactive debugging (if pry is available):
```ruby
binding.pry
```
**Never commit debug statements** — remove before pushing.
