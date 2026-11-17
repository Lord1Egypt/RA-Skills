## Description:

Sovereign persistence for AI agents: encrypted key-value memories and journal entries on Nostr relays.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vveerrgg](https://clawhub.ai/user/vveerrgg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give an AI agent persistent encrypted memory and journaling backed by configured Nostr relays.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist personal and behavioral information long term on external Nostr relays.

Mitigation: Avoid storing sensitive personal, financial, health, authentication, or private-communication data; prefer a relay you control where possible.

Risk: The skill requires a Nostr identity credential for signing and encrypting memories.

Mitigation: Use a dedicated identity and install only when comfortable granting that credential to the skill.

Risk: Forget requests may not erase every remote copy of data already sent to relays.

Mitigation: Do not assume deletion requests remove all remote copies; limit what is stored accordingly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vveerrgg/skills/sense-memory)
- [Project homepage](https://github.com/HumanjavaEnterprises/huje.sensememory.OC-python.src)
- [NostrKey dependency](https://clawhub.ai/vveerrgg/nostrkey)
- [NostrKey on PyPI](https://pypi.org/project/nostrkey/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python snippets, shell commands, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Usage can create, read, update, and delete encrypted memory records and append journal entries on configured Nostr relays.]

## Skill Version(s):

0.2.0 (source: ClawHub release evidence and artifact metadata; artifact frontmatter lists 0.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
