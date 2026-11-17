## Description:

Webperf Loading helps agents analyze web page loading performance in Chrome DevTools, including TTFB, FCP, render-blocking resources, script loading, font behavior, resource hints, images, CSS, service workers, and SSR hydration data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nucliweb](https://clawhub.ai/user/nucliweb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and web performance engineers use this skill to audit page loading behavior in Chrome DevTools and identify bottlenecks in server response, initial rendering, scripts, fonts, resource hints, images, CSS, service workers, and SSR hydration. It helps turn browser performance measurements into targeted optimization guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose page structure, resource URLs, service worker/cache metadata, and embedded hydration-size signals to the agent session.

Mitigation: Avoid running it on pages with highly sensitive account data unless that browser telemetry is intended to be shared with the agent session.

Risk: Audit output may lead to incorrect optimization decisions if browser measurements are stale, incomplete, or captured in a non-representative environment.

Mitigation: Review the reported findings against current Chrome DevTools data and validate material changes in the target site's normal testing workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nucliweb/skills/webperf-loading)
- [Source repository](https://github.com/nucliweb/webperf-snippets)
- [Snippet descriptions and thresholds](references/snippets.md)
- [Script return value schema](references/schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown guidance with JavaScript snippets and structured JSON audit results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Chrome DevTools MCP access to the page being audited.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
