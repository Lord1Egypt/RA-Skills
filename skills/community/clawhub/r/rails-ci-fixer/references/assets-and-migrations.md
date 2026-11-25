# Assets And Migrations

Asset pipeline and migration failures.

## Asset Pipeline

### `The asset "<name>.css" is not present in the asset pipeline`
CSS not compiled in the test environment.
- **Fix**: `rails assets:precompile RAILS_ENV=test`

## Migration Errors

### `PendingMigrationError`
- **Fix**: `rails db:migrate RAILS_ENV=test`
