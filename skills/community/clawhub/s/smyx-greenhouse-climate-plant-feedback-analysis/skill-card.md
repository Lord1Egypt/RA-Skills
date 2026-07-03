## Description: <br>
Analyzes greenhouse plant images or videos with environmental context to produce structured plant-state reports and climate-control action recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Greenhouse operators, agronomy teams, and automation developers use this skill to inspect plant morphology from media, query prior analysis reports, and receive prioritized irrigation, shading, ventilation, wet-curtain, or heating recommendations for local review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ClawScan reports a suspicious verdict because the skill may send uploaded videos, images, remote URLs, account identifiers, and history requests to a cloud API. <br>
Mitigation: Install only after confirming trust in the publisher and backend service, and avoid submitting sensitive greenhouse media, account data, or URLs unless that transfer is acceptable. <br>
Risk: The skill can persist local attachments and token or profile state while accessing cloud report history. <br>
Mitigation: Review local storage and identity handling before deployment, prefer versions with documented retention behavior, and clear stored state when the skill is no longer needed. <br>
Risk: Climate-control recommendations are generated from media analysis and may be incomplete or incorrect for the physical greenhouse. <br>
Mitigation: Treat outputs as decision support and require local controller safeguards or human review before applying irrigation, shading, fan, wet-curtain, or heater actions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/smyx-sunjinhui/skills/smyx-greenhouse-climate-plant-feedback-analysis) <br>
- [Greenhouse API documentation](references/api_doc.md) <br>
- [Analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown/text report with optional saved output file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include structured analysis results, prioritized climate-control commands, report links, and history tables.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
