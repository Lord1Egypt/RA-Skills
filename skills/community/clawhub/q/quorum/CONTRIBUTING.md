# Contributing to Quorum

Thank you for your interest in contributing to Quorum. This document covers how to get involved.

## Ways to Contribute

### 🔍 Submit Custom Rubrics

The rubric system is Quorum's most extensible surface. If you've built a rubric for a domain we don't cover yet, we'd love to include it.

**How:**
1. Create a JSON rubric following the format in `examples/rubrics/`
2. Test it against at least one real artifact
3. Open a PR adding it to `examples/rubrics/` with a brief description

**Good rubric contributions:**
- New domains (code review, documentation, API design, data pipelines)
- Specialized variants (security-focused, performance-focused)
- Industry-specific criteria (healthcare, finance, government)

### 🔗 Submit Cross-Artifact Relationship Manifests

Cross-artifact manifests are a new and growing contribution surface. If you have a project structure where multiple files have declared relationships (spec/implementation, schema/consumer, config/profile), contributing a well-structured manifest example helps the community understand how to use `--relationships` effectively.

**How:**
1. Create a `quorum-relationships.yaml` for a real or representative project
2. Test it with `quorum run --relationships` against the described files
3. Open a PR adding it to `examples/relationships/` with a description of the project structure and what consistency checks it enables

**Good manifest contributions:**
- Real-world project patterns (API spec ↔ handler, OpenAPI schema ↔ consumer)
- Framework-specific patterns (FastAPI, Django, OpenClaw swarms)
- Documentation consistency patterns (README ↔ code, SPEC ↔ implementation)

### 🐛 Bug Reports

Found an issue? Open a GitHub Issue with:
- What you were validating (artifact type, depth profile)
- What you expected vs. what happened
- Model and tier configuration
- Any relevant log output

### 💡 Feature Proposals

Have an idea for a new critic, aggregation strategy, or rubric feature? Open a Discussion thread. We're particularly interested in:
- New critic specializations
- Alternative aggregation strategies
- Integration patterns with specific agent frameworks
- Cost optimization techniques

### 📝 Documentation

Improvements to docs, tutorials, and examples are always welcome. If something was confusing when you first used Quorum, it's probably confusing for others too.

### 🔬 External Reviews

Run Quorum against your own system and share the results. See `docs/reviews/EXTERNAL_REVIEWS.md` for how to submit.

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Ensure any new rubrics include at least one example validation
5. Open a PR with a clear description of what changed and why

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By participating, you agree to uphold this standard.

## Questions?

Open a Discussion thread or reach out on X: [@Cervera](https://twitter.com/Cervera) or [@AkkariNova](https://twitter.com/AkkariNova).

---

*Quorum is maintained by Daniel Cervera and Akkari at SharedIntellect.*
