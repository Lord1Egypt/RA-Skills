## Description: <br>
Analyzes family or couple conflict intensity from living-room audio/video and returns acoustic and visual conflict metrics, low/medium/high intensity labels, gentle reminder text, and optional history-report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, family-support product teams, and counseling or mediation workflows can use this skill to analyze uploaded or URL-based home audio/video for conflict intensity signals and generate gentle de-escalation reminders or conflict-frequency report listings. It is not a replacement for legal, emergency, or mental-health judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Domestic audio/video and video URLs may be sent to a remote service for analysis. <br>
Mitigation: Use only with clear prior consent from all affected adults and after the publisher documents remote processing, retention, deletion, and access controls. <br>
Risk: Results may be associated with persistent identifiers and historical report queries. <br>
Mitigation: Confirm the authorization model before enabling history access, and avoid identifiers that expose phone numbers or other unnecessary personal data. <br>
Risk: Local user or token data may be stored by supporting code. <br>
Mitigation: Review credential storage before deployment, keep tokens out of shared workspaces, and rotate credentials after testing. <br>
Risk: Conflict-intensity labels can be wrong or misused in sensitive household situations. <br>
Mitigation: Treat outputs as screening signals only; do not use them for legal conclusions, emergency decisions, or mental-health diagnosis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/smyx-family-conflict-intensity-detect-analysis) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/smyx-sunjinhui) <br>
- [Family conflict intensity API reference](references/api_doc.md) <br>
- [Common analysis API reference](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON-style report text with conflict metrics, reminder text, recommended actions, report links, and command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an open-id and a local audio/video file path or public media URL; history queries return Markdown tables with report links.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
