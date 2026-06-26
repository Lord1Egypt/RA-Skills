## Description: <br>
Webperf Media guides agents through Chrome DevTools audits for image, video, and SVG performance, including LCP, CLS, loading strategy, format, sizing, and priority recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nucliweb](https://clawhub.ai/user/nucliweb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and performance engineers use this skill to audit page media in Chrome DevTools and produce practical recommendations for reducing LCP, CLS, bandwidth, and media loading issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Media audits may expose DOM details and media URLs from logged-in or internal pages to the agent. <br>
Mitigation: Run the skill only on pages acceptable for DevTools inspection and confirm before follow-up audits when tighter control is needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nucliweb/webperf-media) <br>
- [Publisher profile](https://clawhub.ai/user/nucliweb) <br>
- [Repository](https://github.com/nucliweb/webperf-snippets) <br>
- [Script return value schema](references/schema.md) <br>
- [Snippet descriptions](references/snippets.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Code] <br>
**Output Format:** [Markdown guidance with structured JSON audit results from Chrome DevTools scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Chrome DevTools MCP evaluation and structured script return values for image, video, and SVG audit findings.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
