## Description:

Multi-agent dispatcher skill. Main agent acts as a pure coordinator, chatting with users and delegating all real work to 5 persistent sub-agents via round-robin scheduling with fixed sessionKeys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[be1human](https://clawhub.ai/user/be1human)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to route task work from the main agent to a fixed pool of persistent sub-agents while keeping the main agent focused on user-facing coordination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill broadly redirects real work into persistent sub-agent sessions, which can reduce main-agent inspection and validation of delegated work.

Mitigation: Install it only when dispatcher behavior is desired, and review sub-agent outputs before using them for decisions, code changes, or external actions.

Risk: Persistent sub-agent sessions may retain conversation context without documented isolation or reset controls.

Mitigation: Avoid sharing sensitive data unless session persistence is acceptable, and reset or rotate sessions through platform controls when available.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Markdown or plain text coordination messages with delegated sub-agent tasks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Delegation uses fixed session keys and 300-second sub-agent run timeouts when available.]

## Skill Version(s):

11.0.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
