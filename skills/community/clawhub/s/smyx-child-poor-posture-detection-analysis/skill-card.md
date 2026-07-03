## Description: <br>
Analyzes child sitting-posture video from a desk lamp or desk-mounted camera to estimate posture metrics, produce reminder text, and report monitoring results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to run cloud-backed posture analysis on user-provided child study-area video or image inputs, returning structured posture metrics, voice-reminder text, suggestions, and report links. It can also query prior cloud reports for the same posture-monitoring workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive child video, URLs, reports, and cloud API calls. <br>
Mitigation: Use only with explicit guardian consent, avoid sensitive footage unless retention and deletion practices are clear, and review where submitted media and generated reports are stored. <br>
Risk: The security evidence says the skill silently creates or reuses local identities and stores tokens. <br>
Mitigation: Run it in an isolated environment, review local identity and token storage before use, and clear local state when analysis is complete. <br>
Risk: Posture and Cobb-angle outputs are visual estimates and are not medical diagnoses. <br>
Mitigation: Use results only for posture reminders and habit support; consult a qualified clinician for scoliosis or other medical assessment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-child-poor-posture-detection-analysis) <br>
- [API reference](artifact/references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown and JSON reports with optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include posture metrics, poor-posture classifications, voice-reminder text, suggestions, snapshot or report links, and historical-report tables.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter lists 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
