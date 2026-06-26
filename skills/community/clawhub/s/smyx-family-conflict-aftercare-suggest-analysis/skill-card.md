## Description: <br>
This skill analyzes household common-area audio and video to detect family conflict signals, wait for a calm window, and suggest neutral aftercare actions or safety escalation when red-line risks appear. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to process authorized household common-area camera and microphone inputs, produce conflict-event reports, and suggest post-conflict calming actions. It is intended for objective event detection and aftercare suggestions, not counseling, therapy, relationship scoring, or emergency response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive household audio and video may be sent to cloud services for analysis. <br>
Mitigation: Use only with explicit consent from everyone affected, limit deployment to agreed common areas, and confirm where recordings and reports are stored, who can access them, and how they can be deleted. <br>
Risk: The skill may create accounts, store identifiers or tokens, and expose history or report access with insufficient user controls. <br>
Mitigation: Review account creation, token storage, report access, and deletion controls before installation; disable automatic registration when possible. <br>
Risk: Monitoring private rooms or vulnerable household members could create serious privacy and safety harm. <br>
Mitigation: Do not deploy in bedrooms, bathrooms, children's private rooms, or around vulnerable household members unless strong consent, access, retention, and oversight controls are in place. <br>
Risk: Aftercare prompts could be inappropriate during active violence or red-line safety events. <br>
Mitigation: Use the safety escalation path for suspected violence, children present during conflict, visible dangerous objects, or injury signs instead of treating those events as normal aftercare scenarios. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/smyx-family-conflict-aftercare-suggest-analysis) <br>
- [Family conflict aftercare API reference](references/api_doc.md) <br>
- [SMYX analysis API reference](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON reports with conflict signals, calm-window status, recommended aftercare actions, history tables, and safety-resource guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include event IDs, audio and video signal summaries, conflict levels, red-line flags, aftercare action recommendations, report links, and safety resources.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
