---
name: commit-ai
description: Use when user wants to generate a good git commit message from their changes.
triggers: ["commit", "提交", "git commit", "写提交信息"]
version: 1.0.0
author: VBot
---

# Git Commit AI

> Generate meaningful commit messages from git diff

## Usage

```bash
git diff --staged
```

Analyze the diff and generate a commit message following conventional commits:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation
- `refactor:` for code refactoring
- `test:` for tests
- `chore:` for maintenance

## Example Output

```
feat(auth): add OAuth2 login support

- Implement Google OAuth2 flow
- Add user session management
- Store refresh tokens securely
```

## Rules

1. First line: type(scope): short description (max 72 chars)
2. Body: bullet points explaining *why*, not *what*
3. Be specific, not generic
4. No "Update file" or "Fix bug" messages
