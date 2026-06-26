## Description: <br>
Identifies babies kicking off blankets or exposing their bodies during sleep and alerts parents to cover them up to prevent catching a cold. | 婴儿蹬被监测技能，识别婴儿夜间睡觉踢开被子、身体裸露，及时提醒家长给宝宝盖被保暖，预防着凉感冒 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and caregivers use this skill to analyze infant sleep images or videos for blanket-kicking, body exposure, and related reminders. It can also query cloud-hosted historical monitoring reports for the current internally associated user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may upload sensitive infant sleep videos, local files, or media URLs to an external cloud API for analysis. <br>
Mitigation: Install and run it only when users accept cloud processing for nursery footage; review the configured service endpoints and avoid sending media that should remain local. <br>
Risk: The skill can query cloud report history and may create, reuse, and persist an internal user identity or service tokens. <br>
Mitigation: Review account-persistence behavior before deployment, restrict access to the runtime workspace, and remove stored credentials or identities when the skill is no longer needed. <br>
Risk: Analysis results are auxiliary reminders and may be incomplete or incorrect for infant safety decisions. <br>
Mitigation: Use results only as supplemental alerts and maintain direct caregiver oversight and safe sleep practices. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-infant-blanket-kick-monitoring-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API documentation](references/api_doc.md) <br>
- [SMYX analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-like structured analysis text with report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write the returned report text to a requested output file.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
