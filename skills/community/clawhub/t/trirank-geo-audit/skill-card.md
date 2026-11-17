## Description:

Audits a public website for AI search readiness by fetching key crawl surfaces, checking indexability, metadata, structured data, and AI-crawler access, then producing a scored gap report with concrete fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[supersky0820](https://clawhub.ai/user/supersky0820)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and SEO teams use this skill to audit public websites for AI search readiness. It helps identify crawlability, metadata, structured data, and AI-crawler access gaps before deeper live citation testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL fetching may access internal, private-network, loopback, link-local, or cloud metadata targets if run in a permissive environment.

Mitigation: Use it only for public websites intended for audit and enforce a fetch or runtime policy that blocks private, loopback, link-local, metadata, and unsafe redirect targets.

Risk: A static readiness score can be mistaken for actual AI citation status.

Mitigation: State that the score measures AI readiness only and exclude live citation status unless validated with live engine testing.

## Reference(s):

- [Server-resolved source import](https://github.com/supersky0820/trirank-skills/tree/main/skills/trirank-geo-audit)
- [ClawHub skill page](https://clawhub.ai/supersky0820/skills/trirank-geo-audit)
- [AI Visibility Benchmark](https://trirankai.com/data/ai-visibility-benchmark)
- [TriRank Free Audit](https://trirankai.com/free-audit)
- [TriRank](https://trirankai.com)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown report with a score, gap list, warnings, passing checks, and not-measurable disclosures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses only measured website fetch results for scoring and excludes static-unmeasurable signals from the score.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
