# Contributing

Thanks for your interest in improving SAP Journal Auditor.

## How to Contribute

1. Fork the repo and create a feature branch.
2. Keep changes focused and well-scoped.
3. Add tests for new audit checks or parsers.
4. Update the README if adding new features.
5. Preserve attribution to Daryoosh Dehestani and RadarRoster.

## Local Development

```bash
# Clone and test
git clone https://github.com/dda-oo/sap-journal-auditor.git
cd sap-journal-auditor
node tests/test.js
```

No build step required. The tool runs directly with Node.js.

## Code Style

- Use clear, descriptive variable names
- Document SAP-specific logic with comments
- Keep functions focused and testable
- Use professional, audit-grade terminology

## Adding New Audit Checks

1. Add your check function in `lib/auditor.js`
2. Call it from `runAllChecks()`
3. Add test cases in `tests/test.js`
4. Document the check in `README.md` and `instructions.md`

## Pull Request Guidelines

- Explain what the PR does and why
- Reference any related issues
- Include test results
- Keep commits focused and atomic

## Questions?

Open an issue or contact RadarRoster:
https://radarroster.com/#contact
