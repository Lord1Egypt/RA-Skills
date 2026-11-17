## Description:

Reviews Remix v2 code for caching header misuse, missing server/client split, hydration mismatches (Date, Math.random, locale), prefetch hygiene, and asset bottlenecks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Remix v2 TypeScript route modules for SSR safety, cache correctness, server/client boundary hygiene, prefetch and streaming behavior, and asset performance issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Two referenced review documents are outside the packaged artifact, so review results may vary if those files are unavailable.

Mitigation: Use the packaged reference files as the primary basis for review and confirm any external review protocol or canonical pattern document is available before relying on it.

Risk: Code-review findings can be misleading when they are not tied to concrete source evidence.

Mitigation: Require each reported issue to include a file path, source quote or line location, and the applicable exemption check before drafting user-facing findings.

## Reference(s):

- [Caching Headers Review](artifact/references/caching-headers.md)
- [Server/Client Split Review](artifact/references/server-client-split.md)
- [Hydration Safety Review](artifact/references/hydration.md)
- [Prefetch & Streaming Review](artifact/references/prefetch-streaming.md)
- [Assets, Images, Fonts & CSS Review](artifact/references/assets.md)
- [ClawHub skill page](https://clawhub.ai/anderskev/skills/remix-v2-perf-ssr-review)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Code, Guidance]

**Output Format:** [Markdown review findings with file locations, code quotes, rationale, and remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for static Remix code review and should be grounded in concrete file paths and source quotes.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
