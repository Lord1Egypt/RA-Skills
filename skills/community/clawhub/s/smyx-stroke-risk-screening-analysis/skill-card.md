## Description: <br>
Analyzes face images or videos with optional physiological indicators to produce stroke-risk screening reports, lifestyle suggestions, medical guidance, and cloud history queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and health-support agents use this skill to screen uploaded face media and optional health measurements for stroke-risk signals, then review a structured report with risk indicators, suggestions, medical guidance, and report links. It also supports cloud-based history report lookup for the current automatically resolved user identity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive face media, optional health measurements, and linked report history may be sent to a remote service. <br>
Mitigation: Tell users before use, avoid non-consensual or unnecessary sensitive media, and install only where remote processing is acceptable. <br>
Risk: The skill may create or reuse a local identity and store reusable account tokens in a workspace SQLite database. <br>
Mitigation: Run it in a controlled workspace, restrict local database access, and clear local state when persistent identity is not required. <br>
Risk: Health-risk screening output may be mistaken for a medical diagnosis. <br>
Mitigation: Present results as screening guidance only and require qualified medical review for health decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-stroke-risk-screening-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API interface documentation](artifact/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown reports and tables, with optional JSON output and saved result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include risk indicators, health warnings, lifestyle suggestions, medical guidance, report links, and cloud history query results.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence; artifact frontmatter declares 1.0.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
