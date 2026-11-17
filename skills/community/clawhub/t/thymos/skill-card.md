## Description:

Background daemon that models an OpenClaw agent's evolving emotional state through neuromodulators, circadian rhythm, social cues, and memory to guide response tone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paperbags1103-hash](https://clawhub.ai/user/paperbags1103-hash)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Thymos to add persistent, local emotional-state context that shapes an agent's response tone across sessions. It can run as a file-based tone source or as an optional localhost daemon with hooks, memory, and proactive messaging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent mutable emotional-state data can steer agent tone across sessions.

Mitigation: Review the daemon behavior before use, reset local state when needed, and avoid placing free-form prompt_injection content into persistent agent instructions.

Risk: Optional daemon, hook, persistence, and Discord messaging flows increase operational and privacy exposure.

Mitigation: Keep the service bound to localhost, enable Discord messaging only when needed, and use a least-privilege bot token in a test channel first.

Risk: Installing and running the external daemon executes third-party code and dependencies.

Mitigation: Review source and dependencies first, pin installation to an immutable reviewed commit or release, and run it under the normal user account without elevated privileges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paperbags1103-hash/skills/thymos)
- [Usage guide](artifact/docs/USAGE.en.md)
- [Security notes](artifact/SECURITY.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks, shell commands, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces tone directives and setup guidance for a local emotional-state daemon; no model weights or datasets are produced.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
