## Description:

Locally and deterministically generates a permanent offline S2-DID and foundational SOUL.md prompt based on an agent name.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to generate a visible SOUL.md identity prompt template and deterministic S2-DID for a local Openclaw agent. The generated template is intended for human review before being saved into a workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated SOUL.md content may become persistent instruction context if a user saves it into an agent workspace.

Mitigation: Review and edit the generated behavior rules before saving the SOUL.md file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spacesq/skills/s2-soul-anchor)
- [Space2.world](https://space2.world)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-oriented text returned to the console, including a SOUL.md template and deterministic identifier]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No automatic file writes, credential access, network calls, or hidden execution were identified in the security evidence.]

## Skill Version(s):

1.0.5 (source: release evidence and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
