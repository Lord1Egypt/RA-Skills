## Description: <br>
Provides a business strategy analysis workflow for market sizing, competitor matrices, SWOT+, Porter's Five Forces, and business model canvas reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentlau2046-sudo](https://clawhub.ai/user/vincentlau2046-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Strategy, product, and business development teams use this skill to structure market research, competitive analysis, strategic positioning, and business model evaluation into reusable reports and presentation-ready outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tavily-backed web research may expose sensitive strategy prompts or rely on unverified web data. <br>
Mitigation: Use non-confidential inputs when possible, restrict the Tavily key, and review sources and generated claims before business use. <br>
Risk: The skill uses local API-key configuration files. <br>
Mitigation: Prefer managed secrets or protected environment files, avoid sharing plaintext key files, and rotate or scope the Tavily key. <br>
Risk: The skill writes reports and raw analysis data to persistent local paths. <br>
Mitigation: Change the output path for the deployment environment and avoid storing confidential analyses in shared locations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/vincentlau2046-sudo/technical-business-strategy-analysis) <br>
- [TAM/SAM/SOM Framework](references/frameworks/tam-sam-som.md) <br>
- [Competitor Matrix Framework](references/frameworks/competitor-matrix.md) <br>
- [SWOT+ Framework](references/frameworks/swot-plus.md) <br>
- [Porter Five Forces Framework](references/frameworks/porter-five-forces.md) <br>
- [Business Model Canvas Framework](references/frameworks/business-model-canvas.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with cited data, tables, CSV/JSON data files, and HTML presentation artifacts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Tavily-backed web research and writes persistent analysis outputs to local paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
