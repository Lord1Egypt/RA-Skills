## Description: <br>
Provides Chrome DevTools MCP workflows and JavaScript snippets for measuring and debugging LCP, CLS, and INP Core Web Vitals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nucliweb](https://clawhub.ai/user/nucliweb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and web performance engineers use this skill with Chrome DevTools MCP to audit Core Web Vitals, run targeted snippets, and follow decision trees for LCP, CLS, and INP debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Page-context DevTools snippets can inspect the active page and visually highlight DOM elements during analysis. <br>
Mitigation: Run snippets only on pages you trust and intend to analyze; avoid sensitive logged-in, financial, internal, or personal-data pages unless the snippet has been reviewed. <br>
Risk: Core Web Vitals measurements can vary by page state, user interaction, timing, and browser support. <br>
Mitigation: Treat results as diagnostic signals, repeat measurements across representative scenarios, and review error or unsupported statuses before making optimization decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nucliweb/webperf-core-web-vitals) <br>
- [webperf-snippets repository](https://github.com/nucliweb/webperf-snippets) <br>
- [Script return value schema](references/schema.md) <br>
- [Core Web Vitals snippet descriptions and thresholds](references/snippets.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Code, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript snippets and structured JSON script results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs page-context Chrome DevTools snippets that may return ok, tracking, error, or unsupported statuses.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
