## Description: <br>
Tvs Deep Interview guides an agent through structured one-question-at-a-time requirements interviews, topology confirmation, ambiguity scoring, and explicit approval gates before implementation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[inksnowhailong](https://clawhub.ai/user/inksnowhailong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to turn ambiguous product or code-change ideas into clear, verifiable specifications before execution. It is suited to complex greenfield or brownfield requests where direct implementation could cause avoidable rework. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may slow down ambiguous requests by requiring clarification before implementation. <br>
Mitigation: Use it for requirements-heavy work and narrow its trigger wording if direct execution is preferred. <br>
Risk: Interview outputs can still encode incorrect assumptions if the user approves an incomplete specification. <br>
Mitigation: Review the ambiguity score, open questions, acceptance criteria, and approval status before using the specification to implement changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/inksnowhailong/tvs-deep-interview) <br>
- [Publisher profile](https://clawhub.ai/user/inksnowhailong) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown interview prompts, ambiguity scoring reports, and specification drafts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces clarification questions and approval-ready specifications; it instructs the agent not to modify code until explicit approval is given.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
