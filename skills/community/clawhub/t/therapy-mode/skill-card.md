## Description:

Comprehensive AI-assisted therapeutic support framework with CBT, ACT, DBT, MI, session notes CLI, and crisis protocols.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesethrose](https://clawhub.ai/user/thesethrose)

### License/Terms of Use:


## Use Case:

Agents use this skill to provide structured mental-health support using established therapy-informed approaches and to maintain therapy session notes. It is intended for supportive conversations and continuity, not as a substitute for professional or emergency mental-health care.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist sensitive therapy notes as durable local plaintext records.

Mitigation: Use it only with explicit consent, verify where notes are stored, and keep records out of shared or synced folders.

Risk: The included CLI uses a hardcoded personal storage path that differs from the documented workspace notes path.

Mitigation: Review or change the notes directory before use so records are written only to the intended local location.

Risk: Users may rely on AI-assisted support for professional or emergency mental-health needs.

Mitigation: Keep the skill framed as supportive guidance and route crisis or clinical needs to qualified human or emergency resources.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with optional shell commands for session note management]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, update, view, archive, restore, or delete local therapy note files.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
