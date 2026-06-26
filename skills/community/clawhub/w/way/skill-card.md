## Description: <br>
Shorthand for /whoareyou - show your verified WayID identity card when users ask who the agent is, who owns it, who is responsible for it, or ask to see identity or provenance proof. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lineagelabs](https://clawhub.ai/user/lineagelabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent render its WayID identity card in response to identity, ownership, responsibility, or provenance questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read local WayID metadata and contact the configured WayID issuer with the agent identifier needed to fetch the identity card. <br>
Mitigation: Review the configured WayID issuer and local WayID metadata before use in environments where agent identity details are sensitive. <br>
Risk: The skill recommends installing a separate WayID plugin but does not include that plugin's code. <br>
Mitigation: Review and scan the WayID plugin separately before installing it. <br>


## Reference(s): <br>
- [WayID issuer](https://way.je) <br>
- [WayID claim flow](https://way.je/claim/SKILL.md) <br>
- [ClawHub skill page](https://clawhub.ai/lineagelabs/way) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown identity-card response with inline installation guidance when relevant] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local WayID metadata and contact the configured WayID issuer to fetch the agent card.] <br>

## Skill Version(s): <br>
3.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
