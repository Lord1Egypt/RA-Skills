## Description:

Intelligent Core Web Vitals analysis for measuring and debugging LCP, CLS, and INP with Chrome DevTools workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nucliweb](https://clawhub.ai/user/nucliweb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and performance engineers use this skill to audit Core Web Vitals in Chrome DevTools, diagnose slow LCP, layout instability, and interaction latency, and choose follow-up performance investigations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs page-local JavaScript diagnostics that can inspect page performance data and element metadata on pages being debugged.

Mitigation: Use it only on pages you are authorized to inspect and review the snippets before execution.

Risk: Some diagnostics may temporarily add visual outlines to page elements while highlighting LCP candidates.

Mitigation: Run diagnostics in a debugging session and refresh the page or clear temporary styling after inspection.

## Reference(s):

- [Snippets and thresholds](references/snippets.md)
- [Script return value schema](references/schema.md)
- [Webperf snippets repository](https://github.com/nucliweb/webperf-snippets)
- [ClawHub skill release page](https://clawhub.ai/nucliweb/skills/webperf-core-web-vitals)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with JavaScript snippets and structured JSON return-value expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an active Chrome DevTools MCP page context; tracking snippets may expose follow-up functions for later reads.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact metadata lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
