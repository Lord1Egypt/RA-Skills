## Description:

Super Agent Browser guides agents in using the agent-browser CLI for headless browser automation with accessibility snapshots, ref-based interactions, session isolation, state persistence, and network controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subaru0573](https://clawhub.ai/user/subaru0573)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to operate the agent-browser CLI for deterministic browser navigation, form interaction, data extraction, testing workflows, and reusable browser sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends saving and loading authenticated browser state, which can expose cookies, local storage, credentials, or authenticated page content if mishandled.

Mitigation: Treat saved state files as secrets, keep them out of source control, isolate them by account or task, avoid loading state from untrusted sources, and redact sensitive browser data from logs and shared outputs.

Risk: The install guidance uses a global package install without a pinned package version.

Mitigation: Pin and verify the agent-browser package where possible and avoid elevated privileges unless the installation environment explicitly requires them.

## Reference(s):

- [agent-browser homepage](https://github.com/vercel-labs/agent-browser)
- [ClawHub skill page](https://clawhub.ai/subaru0573/skills/super-agent-browser)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON output conventions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include browser automation commands, session names, state file paths, selectors, refs, and JSON parsing recommendations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
