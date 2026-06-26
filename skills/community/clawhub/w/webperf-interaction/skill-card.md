## Description: <br>
Intelligent interaction performance analysis with automated workflows for INP debugging, scroll jank investigation, and main thread blocking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nucliweb](https://clawhub.ai/user/nucliweb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and performance engineers use this skill to inspect slow interactions, INP issues, scroll jank, long tasks, long animation frames, and layout shifts in pages opened through Chrome DevTools MCP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs JavaScript in the active browser tab and may capture interaction timing, element targets, script URLs, and layout-shift details. <br>
Mitigation: Run it only on pages intentionally selected for performance testing, and avoid sensitive account or admin pages unless they are the explicit audit target. <br>
Risk: Temporary observers and helper functions can remain active during an audit session. <br>
Mitigation: Reload the page after completing an audit to clear temporary instrumentation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nucliweb/webperf-interaction) <br>
- [Webperf Snippets repository](https://github.com/nucliweb/webperf-snippets) <br>
- [Webperf Snippets site](https://webperf-snippets.nucliweb.net) <br>
- [Snippet descriptions and thresholds](references/snippets.md) <br>
- [Script return value schema](references/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript snippets and structured JSON script results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Chrome DevTools MCP access to the target page; several snippets keep PerformanceObserver tracking active until data is collected.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
