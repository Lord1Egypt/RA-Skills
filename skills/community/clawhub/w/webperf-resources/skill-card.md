## Description: <br>
Intelligent network quality analysis with adaptive loading strategies for slow connections, mobile optimization, save-data support, and Chrome DevTools MCP workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nucliweb](https://clawhub.ai/user/nucliweb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and performance engineers use this skill to inspect a page's network conditions in Chrome DevTools, interpret connection quality and save-data signals, and choose adaptive loading follow-ups for images, CSS, prefetching, and Core Web Vitals work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running DevTools JavaScript on sensitive logged-in pages can expose page context to the agent. <br>
Mitigation: Use the skill only on pages you intend to inspect, avoid sensitive sessions, and review suggested cross-skill follow-ups before executing them. <br>
Risk: The included network-quality script appears incomplete and browser Network Information API support may be unavailable. <br>
Mitigation: Verify results against browser support, DevTools throttling, and additional performance measurements before making optimization decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nucliweb/webperf-resources) <br>
- [WebPerf Snippets Repository](https://github.com/nucliweb/webperf-snippets) <br>
- [Network Bandwidth & Connection Quality Script](https://github.com/nucliweb/webperf-snippets/blob/main/snippets/Resources/Network-Bandwidth-Connection-Quality.js) <br>
- [Snippet Descriptions and Thresholds](references/snippets.md) <br>
- [Script Return Value Schema](references/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript snippets and structured JSON script results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Chrome DevTools MCP and a page selected for inspection; results may be limited when the browser does not expose the Network Information API.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
