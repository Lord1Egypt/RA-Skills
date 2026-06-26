## Description: <br>
Skill Review Pro evaluates AI skills through static review, scoring, adversarial checks, and improvement guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[z-zihan](https://clawhub.ai/user/z-zihan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this agent to review skill quality, score skills against documented criteria, identify robustness issues, and prepare concrete improvement plans. When explicitly requested, it can guide a user-confirmed fix workflow for the selected skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read local skill files and may propose changes that affect another skill's behavior. <br>
Mitigation: Use it on intended target files only and review proposed findings before acting on them. <br>
Risk: The optional fix workflow can edit the selected skill after the user chooses to proceed. <br>
Mitigation: Review proposed diffs before approving fixes, especially for broad improvement requests. <br>


## Reference(s): <br>
- [Skill Review Pro on ClawHub](https://clawhub.ai/z-zihan/skill-review-pro) <br>
- [Publisher Profile](https://clawhub.ai/user/z-zihan) <br>
- [Project Homepage](https://github.com/z-Zihan/awesome-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown review reports with scores, issue summaries, adversarial-check results, improvement priorities, and fix checklists when applicable] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs follow the user's language and may include user-confirmed skill-edit plans during fix workflows.] <br>

## Skill Version(s): <br>
2.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
