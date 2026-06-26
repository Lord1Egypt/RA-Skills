# Contributing to Shadow Binance Bot

Thank you for your interest in contributing!

## How to Contribute

### Reporting Issues

Found a bug or have a feature request? Open an issue on GitHub with a clear description and any relevant logs or screenshots.

### Pull Requests

1. **Fork the repository** and create a new branch for your feature or fix.
2. Keep changes **focused and small** — one feature or fix per PR.
3. Write a clear PR description explaining **what** changed and **why**.
4. Test your changes locally before submitting.
5. Ensure `npm test` passes.

### Code Style

- Use **2-space indentation** for consistency.
- Add JSDoc comments for all public functions.
- Keep lines under **120 characters**.
- No trailing whitespace.
- This project uses **EditorConfig**. Please install the plugin for your editor.

### Security

- **Never commit API keys, secrets, or credentials.**
- Use environment variables or a local `config.env` (already in `.gitignore`).
- If you discover a security vulnerability, please report it privately rather than as a public issue.

### Scope

This tool is a **read-only analysis and coaching** skill. It does not:
- Execute trades automatically
- Access withdrawal or deposit functions
- Store user trading data externally

Large changes should be discussed via a GitHub issue before submitting a PR.

---

_By contributing, you agree that your contributions will be licensed under the MIT License._
