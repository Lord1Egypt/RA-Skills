## Description: <br>
Analyzes child study-area videos to estimate posture metrics and produce real-time voice reminder guidance plus session reports for hunching, head tilt, forward head, shoulder asymmetry, and sitting too close. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and product teams use this skill to connect a smart desk lamp, desk-mounted camera, or uploaded study-area video to posture analysis that returns reminder text and report summaries. It is intended for habit-correction reminders, not medical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive child videos, URLs, and derived posture reports may be sent to remote services. <br>
Mitigation: Use only with guardian consent, avoid phone numbers as identifiers where possible, and confirm retention, deletion, report-link access, and local token storage before deployment. <br>
Risk: The skill silently manages account tokens and history records. <br>
Mitigation: Review token storage and history-record behavior before installation, and restrict access to report links and stored identifiers. <br>
Risk: Visual posture estimates can be mistaken for medical findings. <br>
Mitigation: Use outputs only for habit reminders and posture reports; do not treat them as diagnosis or a substitute for medical evaluation. <br>


## Reference(s): <br>
- [Child posture API documentation](references/api_doc.md) <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/smyx-child-poor-posture-detection-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, API Calls, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown tables and JSON-like posture analysis results with optional shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include posture metrics, poor-posture type, hold duration, voice prompt text, event time, snapshot/report links, and session summaries.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
