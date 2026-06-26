# Common Errors Quick Reference

## Password failures
- Re-check the password
- Quote passwords with special characters
- Avoid exposing passwords unnecessarily in logs

## PATH failures
- Check `where rar`, `where winrar`, or `which rar`
- Search common install paths
- Use absolute path if PATH updates do not apply immediately

## Multipart failures
- Start from the first volume only

## Prompt blocking
- Add `-o+ -y` for unattended runs when safe

## Encoding problems on Windows
- Run `chcp 65001` before extraction when non-ASCII paths display incorrectly
