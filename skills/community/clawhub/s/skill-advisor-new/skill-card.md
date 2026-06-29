## Description: <br>
Smart Skill Advisor matches a user's natural-language task request against local, built-in, SkillHub, and ClawHub skills, then returns the top three recommendations with comparison notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiuwu2495](https://clawhub.ai/user/jiuwu2495) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent users and developers use this skill to identify suitable skills for a task, compare the strongest candidates, and decide which skill to install or use next. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may proceed from recommending skills to installing third-party skills, despite claims of read-only and no-shell behavior. <br>
Mitigation: Require explicit user confirmation before any installation and separately verify the selected skill's source, permissions, and trustworthiness. <br>
Risk: Recommendations can include third-party marketplace skills whose safety and maintenance status vary. <br>
Mitigation: Review the recommendation details, source links, and security status before using or installing a recommended skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiuwu2495/skills/skill-advisor-new) <br>
- [Publisher profile](https://clawhub.ai/user/jiuwu2495) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown recommendation report with ranked skill comparisons and optional installation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Ranks up to three skills and includes fit scores, pros, cons, source links, and recommendation rationale.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
