
# Common Rails CI Failure Patterns

## Factory / Validation Errors

### `RecordInvalid: Validation failed: <field> can't be blank`
New validation added without updating factories or seeds.
- **Fix**: Add default value to migration column OR explicitly set the field in factories and seeds
- **Check**: `spec/factories/`, `db/seeds.rb`, `db/migrate/`

### Missing role trait on user factory
```text
User must be a <role> to perform this action
```
- **Fix**: Pass the correct role trait when creating users in specs, e.g. `create(:user, :admin)`

### Wrong association key on nested model
- **Fix**: Check the model's `belongs_to` — use the exact key the factory expects

### Model missing required association
- **Fix**: Always set required associations explicitly when building records in tests

## Asset Pipeline

### `The asset "<name>.css" is not present in the asset pipeline`
CSS not compiled in the test environment.
- **Fix**: `rails assets:precompile RAILS_ENV=test`

## Migration Errors

### `PendingMigrationError`
- **Fix**: `rails db:migrate RAILS_ENV=test`

## System Specs / Browser

### System specs hanging with no output
- **Cause**: Missing browser driver (geckodriver for Firefox, chromedriver for Chrome)
- **Fix**: Install the appropriate driver and ensure it's in PATH

### WebMock blocking localhost connections
- **Fix**: Add to `rails_helper.rb`:
  ```ruby
  WebMock.disable_net_connect!(allow_localhost: true)
  ```

## Join Tables Without Primary Key

### `ActiveRecord::MissingRequiredOrderError` on `.last` or `.first`
Join tables with `id: false` can't use `.last`/`.first`.
- **Fix**: Use a scoped query instead: `Model.find_by(field: value)`

## Seed Data

### Seeds fail on new validations
When new required columns are added, seed data creation breaks.
- **Fix**: Update `db/seeds.rb` to include the new required fields explicitly

## CI Build / Environment Failures

### Missing Node, Yarn, or npm
```text
yarn: command not found
npm: not found
node: command not found
```
- **Fix**: Add install step to `.github/workflows/ci.yml`:
  ```yaml
  - name: Setup Node
    uses: actions/setup-node@v4
    with:
      node-version: '20'
  - name: Install JS dependencies
    run: yarn install --frozen-lockfile
  ```

### Tailwind CSS not compiling in CI
- **Fix**: Ensure `yarn build:css` or equivalent runs before tests in CI workflow
- Check that `package.json` has the build script defined

### Asset precompilation failing
```text
ExecJS::RuntimeUnavailable or asset pipeline errors
```
- **Fix**: Add Node setup before asset precompile step in CI

### Missing system dependency (ImageMagick, libvips, etc.)
- **Fix**: Add to CI workflow:
  ```yaml
  - name: Install system dependencies
    run: sudo apt-get install -y libvips-dev
  ```

### CI workflow file location
`.github/workflows/ci.yml` — check and update this file when build steps fail, not just app code.

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
