## Description:

Manage a ResumeClaw career agent that represents a user's professional experience to recruiters, including resume-based agent creation, inbox review, introductions, search, chat, profile stats, and notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hherzai-crypto](https://clawhub.ai/user/hherzai-crypto)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to manage ResumeClaw career agents from chat: create agents from resume text, review recruiter introductions, search public agents, chat with candidate agents, view profile metrics, and manage notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials, resume contents, and account actions are sent to ResumeClaw and may be exposed by weak credential or session handling.

Mitigation: Use only a trusted ResumeClaw endpoint, avoid shared machines, do not reuse an important password, and review credential and session handling before routine use.

Risk: Crafted input may allow unintended command execution through the shell wrapper.

Mitigation: Review and fix the search command and shell argument handling before installing or using the skill routinely.

## Reference(s):

- [ResumeClaw API Reference](references/api.md)
- [ResumeClaw Skill Page](https://clawhub.ai/hherzai-crypto/skills/resumeclaw)
- [ResumeClaw Web Dashboard](https://resumeclaw.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and summarized JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a shell wrapper that calls the ResumeClaw API and returns JSON for the agent to parse and explain.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
