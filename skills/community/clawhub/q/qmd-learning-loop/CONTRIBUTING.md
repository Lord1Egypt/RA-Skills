# Contributing

Contributions are welcome.

## Development

1. Keep `SKILL.md` concise and make detailed guidance progressively available
   through focused files in `references/`.
2. Preserve the required workflow and explicit approval boundaries.
3. Add or update evaluation cases for behavior changes.
4. Avoid dependencies, platform-specific paths, private workspace conventions,
   and assumptions that QMD is installed.
5. Run `python3 scripts/validate_skill.py`.

Use focused commits and explain observable behavior changes in pull requests.

## Design principles

- Markdown remains the durable source of truth.
- QMD improves retrieval but is not required.
- No persistent write happens without clear user intent.
- High-authority and sensitive changes require explicit approval.
- Search, evidence, provenance, privacy, and conflict handling precede
  promotion.
- Existing workspace conventions are preferred over new files.
