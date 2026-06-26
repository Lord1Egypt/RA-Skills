## Description: <br>
Helps users configure their own Xianyu and Sam's Club account details and follow a self-service ordering workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SxLiuYu](https://clawhub.ai/user/SxLiuYu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to check account configuration and receive guidance for Sam's Club purchases coordinated through Xianyu. The recommended flow keeps ordering and payment in the user's own Sam's Club app or mini program. <br>

### Deployment Geography for Use: <br>
Global, subject to local availability of Xianyu and Sam's Club services. <br>

## Known Risks and Mitigations: <br>
Risk: Session cookies or account details stored in the workspace can grant access to a user's Xianyu or Sam's Club account if exposed. <br>
Mitigation: Keep the .env file private, avoid sharing the workspace with untrusted skills, and remove or rotate cookies when they are no longer needed. <br>
Risk: Automated ordering with account credentials can create unwanted account or purchase activity. <br>
Mitigation: Prefer the manual ordering flow and confirm purchases directly in the user's own Sam's Club app or mini program. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SxLiuYu/xianyu-sam-order) <br>
- [Publisher profile](https://clawhub.ai/user/SxLiuYu) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance and terminal text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference XIANYU_COOKIE and SAM_PHONE environment variables; manual ordering is recommended.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
