## Description: <br>
Structured continuity and follow-up skill for OpenClaw agents that routes dialogue into casual chat, staged memory, or tracked follow-up with state-backed carryover, closure, quiet-hours behavior, traceability, and setup guards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kylnwu](https://clawhub.ai/user/kylnwu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and OpenClaw host operators use this skill to add structured continuity, staged memory, tracked follow-up, routine-aware wording, and natural-language settings updates to an existing OpenClaw agent without replacing the agent persona or chat-platform adapter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent conversation-derived memory and audit files may retain sensitive user content in OpenClaw state. <br>
Mitigation: Use a dedicated state directory, document the state locations, and provide an operator process for inspecting, exporting, and deleting stored memory and audit files. <br>
Risk: Proactive follow-up can surprise users if enabled without clear consent or quiet-hours controls. <br>
Mitigation: Keep proactive behavior opt-in, honor quiet hours and sleep/rest suppression, and expose settings for cadence, cooldown, dispatch caps, and disablement. <br>
Risk: Credential-backed embedding fallback may use sensitive credentials in a path that is not obvious to operators. <br>
Mitigation: Disable embedding fallback unless needed, or provide dedicated low-scope credentials and document when that path is active. <br>
Risk: File move-to-trash capability can affect local files if exposed too broadly. <br>
Mitigation: Remove or gate file_output_sop.py behind explicit operator confirmation and scope checks before real-user deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kylnwu/test-continuity) <br>
- [README](README.md) <br>
- [Harness](docs/harness.md) <br>
- [Release Acceptance](docs/release-acceptance.md) <br>
- [V2 Known Limits](docs/v2-known-limits.md) <br>
- [Security](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands plus JSON configuration and state artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces user-facing continuity guidance and may write persistent conversation-derived state, audit traces, settings, profile, jobs, and harness reports in configured OpenClaw state locations.] <br>

## Skill Version(s): <br>
2.0.22 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
