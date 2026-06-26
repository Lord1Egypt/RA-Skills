# Package Extraction Template

For extracting packages as standalone libraries.

## Pre-Extraction Checklist

- [ ] Package has minimal internal dependencies
- [ ] Test coverage > 50%
- [ ] Public API is clean and documented
- [ ] No hardcoded paths or configs
- [ ] External dependencies are minimal and stable

## Extraction Steps

1. **Copy Source**
   ```bash
   cp -r internal/package/ /new/repo/
   ```

2. **Remove Internal Imports**
   ```bash
   grep -r "github.com/original/repo/internal" /new/repo/
   # Remove or replace each import
   ```

3. **Update Module**
   ```bash
   go mod init github.com/you/package
   go mod tidy
   ```

4. **Verify Independence**
   ```bash
   go build ./...
   go test ./...
   ```

5. **Add Standalone Tests**
   - Integration tests that don't require original repo
