---
name: safe-share
description: Sanitize logs, configs, prompts, stack traces, and skill content before they are shared publicly. Use when a user wants a local, low-risk pass to remove API keys, tokens, cookies, passwords, emails, IPs, or other sensitive values from text before posting to GitHub issues, chat, READMEs, demos, or ClawHub.
---

# Safe Share

Use this skill to produce a safe-to-share copy of text. Prefer deterministic local sanitization over model-only guessing.

## Workflow

1. Confirm the user wants a shareable copy, not a forensic analysis.
2. Determine the output mode:
   - `placeholder`: best default for docs, issues, READMEs, and tutorials
   - `redact`: best when preserving shape is not important
   - `mask`: best when keeping a hint of the original value is useful
3. Run `scripts/sanitize_text.py` on the exact text the user provided.
4. Return:
   - `sanitized_text`
   - `findings_summary`
   - `review_notes`
5. Never echo the original sensitive value back to the user.

## Operating Rules

- Default to `placeholder` mode unless the user asks for something else.
- Treat secrets and credentials as higher priority than general PII.
- Replace with stable labels such as `<OPENAI_API_KEY>` or `[REDACTED:BEARER_TOKEN]`.
- Keep summaries high level. Report type and count, not the captured value.
- State clearly that sanitization reduces risk but does not guarantee complete detection.
- Do not scan unrelated files or repositories unless the user explicitly asks for that broader scope.
- Do not send text to external services for classification or validation.

## High-Risk Patterns

Prioritize these categories:

- API keys and secret tokens
- Authorization headers and bearer tokens
- Cookies and session identifiers
- `.env`-style credentials and password assignments
- Private key blocks and PEM material
- Sensitive URL query parameters

Then handle lower-risk identifiers:

- Email addresses
- Phone numbers
- IP addresses
- National ID or payment-card-like strings when confidence is high

## Output Contract

Use the JSON contract from `references/output-format.md` when returning structured results from the script. If answering in prose, include the same three sections in human-readable form.

## Resources

- Detection and replacement behavior: `references/patterns.md`
- Output structure and reviewer guidance: `references/output-format.md`
- Smoke-test inputs and expected behavior: `references/test-cases.md`
- Deterministic local sanitizer: `scripts/sanitize_text.py`
