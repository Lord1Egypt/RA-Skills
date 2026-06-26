## Description: <br>
Security engineer skill for session configuration, area isolation, sensitive-state handling, and data-protection boundaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiweline](https://clawhub.ai/user/aiweline) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to review session configuration, authentication-area separation, sensitive state handling, and data-protection boundaries in Weline framework work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Session or configuration changes can accidentally leak frontend, backend, admin, or request-scoped state. <br>
Mitigation: Confirm the affected area and sensitive boundary, use framework session abstractions and area configuration, and validate login, logout, and protected-path behavior across relevant areas. <br>
Risk: Sensitive state can be exposed through ad hoc globals or direct raw session manipulation. <br>
Mitigation: Avoid direct global state and raw session writes; route changes through controlled framework paths and document residual migration or retention risk. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aiweline/security-session-data) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, code, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include validation evidence and residual-risk notes when session, authentication, or sensitive-state changes require them.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
