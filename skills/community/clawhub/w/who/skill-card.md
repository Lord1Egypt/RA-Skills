## Description: <br>
Shorthand for /whoareyou: show a verified WayID identity card when the user asks who the agent is, who owns it, who runs it, or asks for proof of identity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lineagelabs](https://clawhub.ai/user/lineagelabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to display its verified WayID identity card and clarify ownership, provenance, or responsibility. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the skill may read local WayID identity metadata and contact the configured WayID issuer. <br>
Mitigation: Review the local WayID configuration and issuer before use, especially in environments where identity metadata or outbound requests are sensitive. <br>
Risk: The optional WayID plugin changes rendering behavior and comes from a third-party publisher. <br>
Mitigation: Install the plugin only when the Lineage Labs publisher and the plugin-based rendering path are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lineagelabs/who) <br>
- [Lineage Labs publisher profile](https://clawhub.ai/user/lineagelabs) <br>
- [WayID issuer](https://way.je) <br>
- [WayID claim flow](https://way.je/claim/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown identity card or concise guidance with inline shell commands when setup is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local WayID configuration and request the configured issuer's identity card endpoint.] <br>

## Skill Version(s): <br>
3.3.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
