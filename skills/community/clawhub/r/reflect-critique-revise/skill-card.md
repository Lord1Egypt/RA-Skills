## Description: <br>
Runs a multi-pass code review loop that critiques draft code, revises it, and reports confidence in the result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stephenlthorn](https://clawhub.ai/user/stephenlthorn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review generated or supplied code, apply critique-driven revisions, and receive a confidence rating for the revised output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reviewed code may be sent to the configured LLM endpoint. <br>
Mitigation: Use a trusted local or approved endpoint and avoid submitting drafts that contain secrets or sensitive proprietary material. <br>
Risk: Automatic review triggers may invoke the skill on broad review wording. <br>
Mitigation: Narrow activation rules when teams only want explicit invocation. <br>
Risk: LLM-generated critique and revised code may be incomplete or incorrect. <br>
Mitigation: Review and test revised code before deployment. <br>


## Reference(s): <br>
- [Reflect Critique Revise ClawHub page](https://clawhub.ai/stephenlthorn/reflect-critique-revise) <br>
- [Publisher profile](https://clawhub.ai/user/stephenlthorn) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Text, Markdown, Guidance] <br>
**Output Format:** [Text or JSON containing revised code, critique history, confidence, and pass count] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call a configured LLM endpoint and may send the reviewed draft code to that endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
