## Description:

Webperf Interaction helps agents analyze web interaction performance in Chrome DevTools by running JavaScript snippets for INP debugging, scroll jank investigation, main-thread blocking analysis, layout-shift correlation, and long-animation-frame attribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nucliweb](https://clawhub.ai/user/nucliweb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and performance engineers use this skill to investigate slow interactions, janky scrolling, unresponsive pages, INP regressions, layout shifts during interaction, and script work that blocks the browser main thread.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DevTools page scripts may inspect sensitive information on the current page.

Mitigation: Use the skill mainly on pages you own or are comfortable inspecting, and avoid sensitive logged-in pages unless necessary.

Risk: Automated decision trees can chain multiple follow-up snippets in the page context.

Mitigation: Confirm before allowing chained snippet execution, especially on production or sensitive pages.

Risk: The scroll performance audit changes page-level event listener instrumentation until the page is reloaded.

Mitigation: Reload the page after running Scroll-Performance.js to remove the instrumentation.

Risk: Long Animation Frame helper exports can include script URLs and function names.

Mitigation: Treat helper exports as local performance diagnostics and review them before sharing outside the debugging context.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nucliweb/skills/webperf-interaction)
- [Webperf Snippets Repository](https://github.com/nucliweb/webperf-snippets)
- [Webperf Snippets Site](https://webperf-snippets.nucliweb.net)
- [Script Return Value Schema](artifact/references/schema.md)
- [Interaction Snippet Descriptions](artifact/references/snippets.md)

## Skill Output:

**Output Type(s):** [Analysis, Code, Guidance]

**Output Format:** [Markdown guidance with JavaScript snippets and structured JSON results from Chrome DevTools MCP]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some workflows chain follow-up snippets based on performance thresholds and browser API support.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
