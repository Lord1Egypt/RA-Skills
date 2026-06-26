# Soul Memory v3.6.0

## Fixes

1. **CLI pure JSON contract restored**
   - search output no longer leaks internal debug lines into stdout
   - plugin can parse search results reliably again

2. **Query source fixed**
   - plugin now prefers the actual last user message
   - prompt-last-line only used as fallback

3. **Parser hardening**
   - plugin recovers JSON payload even if unexpected wrapper text appears
   - cli formatter now supports both dict-style and object-style results

## Expected flow

user message -> extract last real user query -> soul-memory search -> build distilled context -> prependContext injection -> model response

## Version

- Core: v3.6.0
- Plugin manifest: v0.3.6
