## Description: <br>
Sovereign persistence for AI agents: encrypted key-value memories and journal entries on Nostr relays. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vveerrgg](https://clawhub.ai/user/vveerrgg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to configure durable encrypted memory and private journaling across conversations. It supports storing, recalling, listing, journaling, and deleting agent memories through a Nostr identity and relay selected by the operator. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally stores durable memory outside the local machine, which can create privacy risk even when content is encrypted. <br>
Mitigation: Use a dedicated Nostr identity, protect the passphrase or nsec, choose a trusted relay, and avoid storing secrets or highly sensitive personal details. <br>
Risk: Relay deletion may not be fully guaranteed for memories the agent is asked to forget. <br>
Mitigation: Treat deletion as best effort and avoid storing information that requires guaranteed erasure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vveerrgg/sense-memory) <br>
- [Project homepage](https://github.com/HumanjavaEnterprises/huje.sensememory.OC-python.src) <br>
- [NostrKey dependency](https://pypi.org/project/nostrkey/) <br>
- [Related NostrKey skill](https://clawhub.ai/vveerrgg/nostrkey) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python snippets and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May cause the agent to persist encrypted memory and journal data to a configured Nostr relay.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata; artifact frontmatter reports 0.1.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
