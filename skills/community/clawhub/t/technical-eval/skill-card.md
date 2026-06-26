## Description: <br>
Compares candidate technologies after market research and produces structured comparison data, recommendations, reports, and presentation materials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentlau2046-sudo](https://clawhub.ai/user/vincentlau2046-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineering leads, and technical decision makers use this skill to evaluate competing technologies through an eight-step workflow covering requirements, market scanning, maturity assessment, deep evaluation, PoC planning, risk control, selection, and reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may save evaluation artifacts to the local workspace. <br>
Mitigation: Review generated reports, data files, and presentations before sharing or committing them. <br>
Risk: Research queries may be sent to external services through Tavily-backed collection. <br>
Mitigation: Avoid confidential project names, internal strategy details, and sensitive requirements unless that disclosure is acceptable. <br>
Risk: The helper reads a Tavily API key from ~/.openclaw/.env. <br>
Mitigation: Use a dedicated Tavily API key and keep unrelated secrets out of ~/.openclaw/.env. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vincentlau2046-sudo/technical-eval) <br>
- [Technical Evaluation Design Specifications](references/design-spec.md) <br>
- [Technical Evaluation Slide Types](references/slide-types.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, HTML presentations, CSV and JSON data files, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves evaluation artifacts locally and may use Tavily-backed web research when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
