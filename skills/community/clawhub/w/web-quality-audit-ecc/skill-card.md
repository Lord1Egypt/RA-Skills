## Description:

Comprehensive web quality audit covering performance, accessibility, SEO, best practices, and browser automation testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huamu668](https://clawhub.ai/user/huamu668)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to audit websites and web projects for performance, accessibility, SEO, best practices, and real-browser behavior. It returns prioritized findings with concrete recommendations and examples for remediation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PinchTab installation guidance may introduce supply-chain risk if run from an unreviewed or unpinned source.

Mitigation: Review the PinchTab source and use pinned, verified releases; avoid curl-to-bash installation.

Risk: Browser-control services can expose local browsing actions or page content if reachable beyond the local machine.

Mitigation: Bind browser-control services to 127.0.0.1 and use an isolated browser profile with no saved credentials.

Risk: Automated screenshots, text extraction, clicks, form fills, or JavaScript evaluation may affect authenticated or production sites.

Mitigation: Require explicit approval before those actions on authenticated or production sites.

## Reference(s):

- [Web Quality Audit Skill Page](https://clawhub.ai/huamu668/skills/web-quality-audit-ecc)
- [PinchTab Documentation](https://pinchtab.com/docs)
- [PinchTab GitHub](https://github.com/pinchtab/pinchtab)
- [Lighthouse](https://developers.google.com/web/tools/lighthouse)
- [Web Vitals](https://web.dev/vitals/)
- [axe DevTools](https://www.deque.com/axe/)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with structured findings, code examples, shell commands, and optional JSON from the analyzer script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are categorized by severity and web quality area.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
