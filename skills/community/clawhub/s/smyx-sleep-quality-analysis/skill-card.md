## Description: <br>
Identifies sleep stages including falling asleep, light sleep, deep sleep, and REM; monitors body movement, nighttime awakenings, and sleep apnea for sleep monitoring scenarios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze sleep-monitoring videos or video URLs, obtain structured sleep-stage and respiratory observations, and query prior cloud-generated sleep analysis reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sleep-monitoring videos, video URLs, and report history may be sent to Lifeemergence cloud services. <br>
Mitigation: Use the skill only when the user accepts the publisher's privacy, retention, and deletion terms for sensitive sleep or medical-adjacent media. <br>
Risk: The skill may create or reuse a local identity database that stores tokens and profile data with limited user control. <br>
Mitigation: Review local storage behavior before deployment and avoid use in environments where automatic identity persistence is not acceptable. <br>
Risk: The analysis is sleep-quality guidance and may be mistaken for clinical diagnosis. <br>
Mitigation: Present results as informational only and direct users to professional sleep-monitoring equipment or a clinician for diagnosis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-sleep-quality-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API interface documentation](references/api_doc.md) <br>
- [Shared analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, files, guidance] <br>
**Output Format:** [Markdown or JSON sleep analysis report, with optional saved output file and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include sleep-stage observations, movement and apnea indicators, historical report listings, and cloud report export links.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata; artifact SKILL.md frontmatter says 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
