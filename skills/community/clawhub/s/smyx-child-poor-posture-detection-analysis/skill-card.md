## Description: <br>
This skill analyzes child study-area posture videos or image inputs through a cloud service to estimate posture metrics, detect poor posture such as hunchback or head tilt, produce reminder text, and return structured posture reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and product teams can use this skill to analyze child study-area posture media, generate visual posture metrics and reminder text, and retrieve historical posture analysis reports from the provider's cloud service. The output is intended for habit-support and monitoring workflows, not medical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Child posture videos or URLs are processed by the provider's cloud service. <br>
Mitigation: Use only with appropriate guardian consent and confirm retention, access, and handling expectations before deployment. <br>
Risk: The skill can create or reuse a local account identity and tokens automatically. <br>
Mitigation: Review local token storage and cleanup procedures, and restrict access to systems where the skill runs. <br>
Risk: Historical child-related posture reports are fetched from the provider's cloud service. <br>
Mitigation: Confirm report access controls and authorization expectations before enabling historical report queries. <br>
Risk: Estimated posture metrics may be mistaken for clinical findings. <br>
Mitigation: Present results as visual posture reminders and habit-support guidance, not as medical diagnosis or treatment advice. <br>


## Reference(s): <br>
- [Child posture API documentation](references/api_doc.md) <br>
- [Shared analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-oriented structured analysis reports with command examples and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include posture metrics, reminder text, cloud report links, and historical report tables.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
