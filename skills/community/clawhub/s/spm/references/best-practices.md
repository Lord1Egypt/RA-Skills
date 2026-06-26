# Engineering Best Practices

## Code Quality

- Keep functions small (< 50 lines), focused on one thing
- Descriptive names: `calculateTotalPrice()` not `calc()`
- DRY: extract repeated logic into shared functions
- Follow existing codebase patterns

## Testing

- Test Pyramid: 80% unit / 15% integration / 5% e2e
- Test behavior, not implementation
- Tests must be independent and fast

## Architecture

- Layered: Presentation → Application → Domain → Infrastructure
- Clear interfaces between layers
- Dependency injection for loose coupling

## Security

- Validate ALL input
- No hardcoded secrets
- Use parameterized queries (no SQL injection)
- Keep dependencies updated

## Documentation

- Document WHY, not WHAT (code shows what)
- Keep README, API docs, and design docs in sync
- Complex algorithms need comments; obvious code doesn't
