## Description: <br>
Placeholder skill for text-to-image workflows on skills.video. Use when the user is asking about t2i generation and the concrete API contract has not been implemented yet. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[skills-video](https://clawhub.ai/user/skills-video) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this placeholder skill to handle text-to-image requests on skills.video while the concrete API contract is unavailable. It guides the agent to explain the limitation, look for verified provider documentation, and avoid inventing request fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The placeholder has no verified text-to-image API contract, endpoint, payload template, or helper command. <br>
Mitigation: Tell users that t2i is currently a placeholder, check for model-specific OpenAPI or documentation, and avoid inventing unsupported request fields. <br>
Risk: A future implementation may add endpoints, credentials, helper commands, polling, or file and network behavior. <br>
Mitigation: Review and scan any later version before deployment, especially changes that introduce executable behavior or credential handling. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/skills-video/t2i) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown] <br>
**Output Format:** [Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable output; the skill explains placeholder status and requests exact model or endpoint details only when needed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
