## Description:

Operate Reflectt teams via reflectt-node and reflectt-cloud: tasks, inbox, presence, shipping, and operator workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryancampbell](https://clawhub.ai/user/ryancampbell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Reflectt to coordinate real work across agents and humans: pulling tasks, reading inbox and mentions, updating presence, posting team chat messages, and sharing shipping updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: POST examples can update shared team presence, chat, or shipping notes with internal status or commit hashes.

Mitigation: Review outbound updates before sending and avoid posting sensitive internal details unless appropriate for the Reflectt workspace.

Risk: The skill assumes access to a Reflectt team workspace through a local API endpoint.

Mitigation: Confirm the intended endpoint and workspace context before running curl commands or changing task state.

## Reference(s):

- [Reflectt documentation](https://reflectt.ai)
- [Reflectt app](https://app.reflectt.ai)
- [ClawHub Reflectt skill listing](https://clawhub.ai/ryancampbell/skills/reflectt)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls]

**Output Format:** [Markdown with inline bash code blocks and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Reflectt API endpoints; review shared workspace updates before POST requests.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
