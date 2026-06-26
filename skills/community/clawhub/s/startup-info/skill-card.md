## Description: <br>
Generate concise investor-style briefings on startups using live web searches to extract verified company info, funding, founders, traction, and competitors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brunobuddy](https://clawhub.ai/user/brunobuddy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and investors use this skill to turn a company name or URL into a concise startup briefing using web research. The briefing covers product, founders, funding, traction, competitors, moat, and key risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Company research queries may expose confidential deal names, private URLs, or sensitive diligence topics to the configured web search provider. <br>
Mitigation: Use the skill for public company research and avoid confidential inputs unless the configured search provider is approved for that data. <br>
Risk: Web search snippets and blocked sources can be incomplete or outdated for funding, traction, or founder details. <br>
Mitigation: Cross-reference funding across multiple sources and mark unsupported fields as Not disclosed. <br>


## Reference(s): <br>
- [Startup Info ClawHub page](https://clawhub.ai/brunobuddy/startup-info) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown startup briefing with tables and short sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires live web search; marks unavailable data as Not disclosed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
