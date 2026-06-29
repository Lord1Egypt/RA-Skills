## Description: <br>
Analyzes living-room camera images or video to estimate whether an older adult is seated on a sofa and watching TV, then returns behavior statistics, sedentary reminders, and report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External caregivers, elder-care operators, and developers use this skill to analyze sofa-and-TV-area video or image inputs for prolonged seated TV watching and activity reminders. The skill is intended to provide visual behavior statistics and friendly reminders, not medical diagnosis or treatment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private home or elder-care video may be uploaded to cloud services for analysis. <br>
Mitigation: Use only with informed consent from the monitored person or guardian, confirm retention and access policies, and avoid uploading footage that is not needed for the sedentary-watching use case. <br>
Risk: The skill silently creates or reuses local identities and stores tokens for report retrieval. <br>
Mitigation: Review local identity and token storage before installation, restrict filesystem access, and rotate or remove stored tokens when the skill is no longer needed. <br>
Risk: Arbitrary third-party video URLs can expose private media or untrusted remote content to the cloud analysis service. <br>
Mitigation: Accept URLs only from trusted sources and prefer controlled local files or approved storage locations. <br>
Risk: Visual classification can misidentify TV watching when posture, face direction, multiple people, visitors, or camera framing are ambiguous. <br>
Mitigation: Validate camera placement, sofa and TV regions, lighting, and reminder thresholds before relying on alerts in care workflows. <br>
Risk: Sedentary alerts could be mistaken for medical advice. <br>
Mitigation: Present outputs as behavior statistics and friendly reminders only, and direct health concerns to qualified medical professionals. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-elderly-tv-sedentary-reminder-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/smyx-sunjinhui) <br>
- [API documentation](artifact/references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, files, guidance] <br>
**Output Format:** [Plain text, Markdown tables, JSON-like structured reports, report links, and optional saved output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return current analysis results, historical cloud report listings, alert type, alert level, reminder text, recommended action, and report links.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
