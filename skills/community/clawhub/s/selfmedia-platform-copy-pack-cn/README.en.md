# Cross-Platform Copy Pack (Chinese)

Turn approved Chinese content into copy-ready, platform-specific title options, descriptions, and relevant tag drafts. Provide the finalized text, a real source, and target platforms; missing required material is returned as a clear checklist rather than invented copy.

## Install

```bash
npx skills add xxjrq/selfmedia-platform-copy-pack-cn
```

## Input and output

Required input: finalized content, a verifiable source, and a platform list. Optional input includes audience, tone, banned words, and length limits. The result is a card for each platform with title options, description, tag drafts, and an adaptation note. See the [successful example](fixtures/success.md) and [missing-material example](fixtures/failure.md).

This Skill adapts wording only: it does not upload or publish content, and does not promise tag popularity or reach. Run `node scripts/self-test.mjs` from the repository root to validate the package.
