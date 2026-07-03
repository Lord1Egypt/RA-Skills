## Description: <br>
AI运动健康助手 lets an agent record exercise from natural language, estimate calorie burn, generate personalized workout plans, answer exercise questions, and create daily or weekly HTML reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to track exercise, estimate calories, review workout history, and receive general fitness-plan guidance through an agent. It is intended for fitness support and reporting, not as medical advice or a substitute for a clinician or professional coach. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically stores health-adjacent profile and exercise diary data without clear consent, retention, deletion, or export controls. <br>
Mitigation: Use it only when users understand and accept local storage; add explicit consent, storage-path disclosure, and delete/export controls before broader deployment. <br>
Risk: The skill requests web tool permissions that are not necessary for the core local exercise logging, calorie calculation, plan generation, or report generation behavior. <br>
Mitigation: Review and remove unused web permissions unless a specific deployment requires them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/sports-health) <br>
- [Project homepage](https://github.com/bettermen/sports-health) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration, files] <br>
**Output Format:** [Markdown-style agent responses, generated HTML reports, and local JSON profile or diary files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exercise and profile records may be stored locally under the skill's user_data directory; calorie values and plans are estimates.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
