## Description: <br>
Show your verified WayID identity card when a user asks who you are, who owns you, who runs you, or asks to see identity, ownership, provenance, or certificate information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lineagelabs](https://clawhub.ai/user/lineagelabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent operators use this skill to let an agent answer identity and ownership questions by displaying its verified WayID card. The skill reads the agent's local WayID DID file, resolves the public card from the listed issuer, and renders only the returned identity fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Identity or ownership prompts can cause the agent to read its local WayID file and contact the listed WayID issuer. <br>
Mitigation: Use the skill for identity and ownership disclosure workflows, and ensure operators are comfortable with the issuer contact described in the release security guidance. <br>
Risk: The optional @lineagelabs/wayid plugin changes execution from prompt-following to publisher-provided plugin behavior. <br>
Mitigation: Install the optional plugin only when the operator trusts the lineagelabs publisher. <br>
Risk: A stale DID or wrong issuer can produce a failed lookup. <br>
Mitigation: Follow the skill behavior by reporting the queried base URL to the human and stopping instead of reclaiming, retrying broadly, or fabricating card fields. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lineagelabs/whoareyou) <br>
- [Publisher profile](https://clawhub.ai/user/lineagelabs) <br>
- [WayID default issuer](https://way.je) <br>
- [WayID claim skill](https://way.je/claim/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance] <br>
**Output Format:** [Markdown identity card with conditional owner, verification badge, Telegram binding, and certificate link lines.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads one local WayID DID file and makes one HTTPS GET to the DID issuer before rendering the card.] <br>

## Skill Version(s): <br>
3.3.0 (source: frontmatter and server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
