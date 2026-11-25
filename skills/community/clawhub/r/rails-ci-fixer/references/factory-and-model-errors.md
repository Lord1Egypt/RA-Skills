# Factory And Model Errors

Factory, validation, and association errors in Rails CI.

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

## Join Tables Without Primary Key

### `ActiveRecord::MissingRequiredOrderError` on `.last` or `.first`
Join tables with `id: false` can't use `.last`/`.first`.
- **Fix**: Use a scoped query instead: `Model.find_by(field: value)`
