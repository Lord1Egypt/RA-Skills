# Package Provenance

- Slug: `wellknown-audit-corpus-skill`
- Name: `Agent Well-Known Readiness Audit`
- Version: `1.0.0`
- Generated: `2026-05-14T18:23:45Z`
- Type: `skill`
- Price: `$9`
- Backend: `https://wellknown-audit-corpus.mtree.workers.dev`
- Secrets included: `none` (use buyer/provider env vars for runtime credentials)
- Build policy: excludes `__pycache__`, compiled Python bytecode, and local-only artifacts
- Verification: run `python3 scripts/verify_backend.py` before install/support; it performs unpaid backend and x402-envelope checks only.

## File checksums

| Path | Bytes | SHA-256 |
|---|---:|---|
| `CAPABILITIES.json` | 1905 | `470e846c22b0a2d534d21caebd507f41b3530a13011a72c981823a05b8e24611` |
| `PACKAGE_SECURITY.md` | 2862 | `f72e76f5d3f8f723aa7de0aa50efa9933692fc1c5f70b4feecca78675e94a353` |
| `README.md` | 3376 | `f2cdbe9804284dca60d389567c933847c7df54f1279ce4a679ddaa83c1f7dada` |
| `SKILL.md` | 2702 | `987ff1957e4705ed77f2dc9c9ba84d3968262d5cba0d30329a8d1837d8c395a2` |
| `examples/requests.json` | 695 | `dc5de5508238cab8eb072a606b69a1e8f294ef397d67d68d6d185774ce6e6469` |
| `listing.json` | 1064 | `2050c460f0e178ac5efc00d87173bde84849c3a4b4c8bc32934509f7edfd4ea7` |
| `scripts/install_skill.py` | 3319 | `697138eff9881abbd3f8dab23e5dc772544ed747dbf615e8af593c2a44f4a82f` |
| `scripts/show_examples.py` | 1978 | `0af6adc0fd23606b7e269fc3178524a2c10383546c8a27977ce36d832aaeaf19` |
| `scripts/verify_backend.py` | 1972 | `f23c314b90f728946cf48874c17869364e38c9a0930279f0b8ba941ac52c8508` |
| `scripts/verify_package.py` | 2048 | `2482fc49cb09d4e4e7bf2c3883b403b21da7bbac6116244f761c6086733dead8` |
