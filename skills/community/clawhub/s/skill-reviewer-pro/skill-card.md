## Description: <br>
Performs thorough format validation, content quality assessment, and functional verification of OpenClaw skills for compliance and completeness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YKaiXu](https://clawhub.ai/user/YKaiXu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and skill publishers use this skill to audit OpenClaw skills before publishing, evaluate downloaded skills, and improve existing skills with structured checks and recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Validation commands may be run against an unintended local path. <br>
Mitigation: Verify the target path is the local skill directory intended for review before running validation commands. <br>
Risk: Review recommendations could be incorrect or misleading if accepted without inspection. <br>
Mitigation: Review recommendations and scan the skill before deployment. <br>
Risk: Automatic language adaptation may choose a less clear language when the user's preference is ambiguous. <br>
Mitigation: Use an explicit language preference when clarity matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/YKaiXu/skill-reviewer-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown review reports with scorecards, checklists, findings, recommendations, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Adapts response language to the user's request when possible.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
