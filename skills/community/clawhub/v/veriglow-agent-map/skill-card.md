## Description: <br>
Look up VeriGlow Agent Map for any website URL to discover its data functions, internal APIs, browser automation recipes, and agent reliability reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChizhongWang](https://clawhub.ai/user/ChizhongWang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to find Agent-readable maps for website data extraction, hidden API calls, and browser automation fallback recipes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to query external websites and use returned curl commands, hidden API calls, browser automation steps, or proxy suggestions. <br>
Mitigation: Review returned recipes before use, confirm authorization to access the target site, and comply with site terms, rate limits, and data-use restrictions. <br>
Risk: Submitting sensitive internal URLs, secret query strings, or customer-specific pages to VeriGlow may disclose information outside the user's environment. <br>
Mitigation: Avoid sending sensitive URLs or parameters unless sharing them with VeriGlow is acceptable. <br>


## Reference(s): <br>
- [VeriGlow homepage](https://veri-glow.com) <br>
- [ClawHub skill page](https://clawhub.ai/ChizhongWang/veriglow-agent-map) <br>
- [VeriGlow Agent Map lookup pattern](https://veri-glow.com/{target-url-without-protocol}) <br>
- [SSE bond daily overview Agent Map](https://veri-glow.com/www.sse.com.cn/market/bonddata/overview/day/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline bash and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for programmatic map fetching; returned website recipes may include external API calls, browser automation steps, rate-limit notes, freshness caveats, and proxy guidance.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
