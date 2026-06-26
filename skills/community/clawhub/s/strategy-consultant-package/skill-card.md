## Description: <br>
Provides strategy consulting workflows for market research, competitive analysis, business model validation, financial forecasting, interview planning, and expert-informed strategic recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scubiry-glitch](https://clawhub.ai/user/scubiry-glitch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business operators, product teams, founders, and strategy analysts use this skill to prepare external interviews, gather Brave-backed market intelligence, compare competitors, validate business models, forecast financials, and produce strategy documents for planning or workshops. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Brave searches can expose sensitive business, client, or unreleased strategy details through search queries. <br>
Mitigation: Avoid putting secrets, confidential client information, or unreleased strategy into search queries; sanitize prompts before web research. <br>
Risk: API-key setup is privacy-sensitive and can leak credentials if keys are stored directly in shared files. <br>
Mitigation: Use environment variables or the OpenClaw configuration flow for Brave Search credentials when possible. <br>
Risk: Overlapping business or finance skills may produce conflicting recommendations or trigger the wrong workflow. <br>
Mitigation: Invoke this skill explicitly when other business or finance skills are installed. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/scubiry-glitch/strategy-consultant-package) <br>
- [README.md](artifact/README.md) <br>
- [Strategy consultant agent definition](artifact/agents/strategy-consultant.md) <br>
- [Brave search setup guide](artifact/docs/brave-setup.md) <br>
- [Market insight demo](artifact/examples/market-insight-demo.md) <br>
- [Expert library](artifact/expert-library.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with command examples, configuration snippets, generated report outlines, and structured research outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use Brave Search when configured; outputs can include market reports, competitor reports, expert briefs, business model canvases, financial summaries, and strategic recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.json release.version, target metadata, package.json, and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
