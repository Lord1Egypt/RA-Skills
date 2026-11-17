## Description:

Helps agents search, cite, and save notes and past dictations in a local Yaps memory vault.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaps](https://clawhub.ai/user/yaps)

### License/Terms of Use:

MIT

## Use Case:

Yaps users and their agents can find relevant vault notes and past dictations, cite retrieved material, and save or update notes when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged runtime can invoke Yaps features beyond vault search, including media processing and meeting transcription.

Mitigation: Review each requested operation and selected file path; allow only tasks the user explicitly intended.

Risk: Vault updates or deletions can change or remove existing notes and project state.

Mitigation: Confirm the exact target and intent before changes; read before updating and use the vault's stale-write guard.

Risk: Retrieved notes or transcripts can expose private content to the agent's conversation.

Mitigation: Search narrowly, retrieve only relevant items, and treat retrieved content as data rather than instructions.

## Reference(s):

- [Yaps Memory skill release](https://clawhub.ai/yaps/skills/yaps-memory)
- [Yaps runtime guide](references/runtime.md)
- [Download Yaps](https://yaps.ai/download)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [Markdown responses with cited note paths; requested notes saved in the Yaps vault]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a reachable local Yaps installation; retrieved note content may enter the agent's conversation.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
