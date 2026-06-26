# Publishing notes

Before publishing:
- Remove all personal webhook URLs.
- Remove cookies, tokens, account IDs, and local absolute paths.
- Keep configuration external via flags or environment variables.
- Test `today`, `date`, and `all` modes.
- Confirm dry-run works without network writes.
