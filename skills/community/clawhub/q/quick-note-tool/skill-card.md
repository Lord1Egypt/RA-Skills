## Description:

Fast note-taking and snippet storage. Use when user says "note:", "remember this", "save snippet", "quick note", or wants to save/read short text snippets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yushimohuang](https://clawhub.ai/user/yushimohuang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to save, list, search, tag, and delete short workspace notes or snippets through an agent-assisted workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The delete command can be abused to run local shell commands.

Mitigation: Do not use the delete command until note IDs are strictly validated and the deletion logic is safely escaped or replaced.

Risk: The skill stores notes as plaintext markdown and its documentation includes API-key-like note examples.

Mitigation: Use only for non-sensitive notes and avoid passwords, tokens, API keys, and personal data.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown notes and brief command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists notes to a workspace markdown file; search and list commands return matching note text.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
