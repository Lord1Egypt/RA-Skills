## Description:

Webperf Resources helps agents assess browser network quality with Chrome DevTools and recommend adaptive loading strategies for slow connections, high latency, and save-data mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nucliweb](https://clawhub.ai/user/nucliweb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and performance engineers use this skill to inspect network connection quality in Chrome DevTools and turn connection data into adaptive loading, media, and resource-budget recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included browser snippet may not return the claimed connection metrics when the Network Information API is available.

Mitigation: Review and fix the snippet before relying on its network metrics, and verify returned data against DevTools throttling or another trusted measurement source.

Risk: The workflow encourages follow-up script execution based on earlier results, which could inspect more page state than the user expects.

Mitigation: Require explicit user confirmation before each follow-up script and run only on pages the user is comfortable inspecting through DevTools.

Risk: Network Information API support and precision vary by browser, so connection classification can be unavailable or approximate.

Mitigation: Treat unsupported or approximate results as advisory and use fallbacks such as TTFB, throttled testing, and user preference controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nucliweb/skills/webperf-resources)
- [WebPerf Snippets repository](https://github.com/nucliweb/webperf-snippets)
- [Network snippets reference](references/snippets.md)
- [Script return value schema](references/schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with JavaScript snippets and Chrome DevTools MCP command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an inspected browser page and Chrome DevTools MCP; script output can be unsupported when the Network Information API is unavailable.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
