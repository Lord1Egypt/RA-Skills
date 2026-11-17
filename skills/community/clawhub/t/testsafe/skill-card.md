## Description:

A constrained browser automation skill for web navigation, screenshots, public data extraction, and testing when safety boundaries are enabled.

This skill is ready for commercial/non-commercial use.

## Publisher:

[janewert](https://clawhub.ai/user/janewert)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to drive browser sessions for navigation, screenshots, structured page inspection, form workflows, public data extraction, debugging, profiling, and test capture tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted page content can influence the agent through browser snapshots or extracted text.

Mitigation: Enable content boundaries for every run and treat page-sourced output as untrusted input.

Risk: Broad browser automation can navigate or act outside the intended site scope.

Mitigation: Use strict domain allowlists and an action policy that denies sensitive actions unless explicitly approved.

Risk: Authenticated sessions and saved state can expose cookies, tokens, or account access.

Mitigation: Encrypt saved state, avoid reusing authentication state unless required, and clear session files after use.

Risk: Unpinned browser tooling can change behavior between installs.

Mitigation: Pin the agent-browser package version and review updates before using the skill in trusted workflows.

Risk: Screenshots, PDFs, downloads, traces, and snapshots can contain sensitive page data.

Mitigation: Set output limits, store generated files in controlled locations, and scrub or delete captured artifacts when they are no longer needed.

## Reference(s):

- [Authentication](references/authentication.md)
- [Commands](references/commands.md)
- [Profiling](references/profiling.md)
- [Proxy Support](references/proxy-support.md)
- [Session Management](references/session-management.md)
- [Snapshot and Refs](references/snapshot-refs.md)
- [Video Recording](references/video-recording.md)
- [ClawHub Skill Page](https://clawhub.ai/janewert/skills/testsafe)
- [Publisher Profile](https://clawhub.ai/user/janewert)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and file-producing browser automation commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce screenshots, PDFs, downloads, session state, trace files, and browser snapshots depending on the command sequence.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
