## Description:

Webperf helps agents audit and debug web performance in Chrome DevTools, including Core Web Vitals, loading, interaction, media, and network quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nucliweb](https://clawhub.ai/user/nucliweb)

### License/Terms of Use:

MIT

## Use Case:

Developers and performance engineers use Webperf to run Chrome DevTools based page audits, interpret metrics such as LCP, CLS, INP, and TTFB, and identify concrete performance fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running page-context performance snippets on sensitive logged-in pages may expose or inspect private page data during an audit.

Mitigation: Confirm the target URL before use and avoid banking, admin, private, or other sensitive logged-in pages unless that audit is intentional.

## Reference(s):

- [Webperf Snippets repository](https://github.com/nucliweb/webperf-snippets)
- [Webperf ClawHub skill page](https://clawhub.ai/nucliweb/skills/webperf)

## Skill Output:

**Output Type(s):** [Analysis, Code, Guidance]

**Output Format:** [Markdown with JavaScript snippets, Chrome DevTools tool guidance, and performance recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Chrome DevTools MCP interactions to inspect the target page when available.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
