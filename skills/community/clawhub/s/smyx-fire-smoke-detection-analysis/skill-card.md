## Description: <br>
Detects fire and smoke in video streams and images for early warning scenarios such as security surveillance, forest fire prevention, and industrial parks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit surveillance, industrial, forest, or other scene media for fire and smoke detection, then receive structured detection results, report links, and historical report listings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Media inputs, URLs, account identifiers, and workspace identity values may be sent to lifeemergence.com or open.lifeemergence.com services. <br>
Mitigation: Use only media that is approved for external service processing, and review organizational privacy and surveillance handling requirements before installation. <br>
Risk: The skill may create or reuse account identity and store account records or service tokens in a local shared SQLite database. <br>
Mitigation: Protect the local workspace, review generated local data stores, and rotate or remove stored tokens when the skill is no longer needed. <br>
Risk: Fire and smoke detection output is an auxiliary warning signal and may be incomplete or incorrect. <br>
Mitigation: Confirm alarms through operational procedures and do not rely on the skill as the sole emergency response mechanism. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-fire-smoke-detection-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API documentation](references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown reports, Markdown tables, and JSON-formatted structured detection results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include fire and smoke detection status, risk indicators, suggested action text, report links, and historical report listings.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata; artifact frontmatter lists 1.0.7) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
