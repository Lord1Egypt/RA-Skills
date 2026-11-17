## Description:

Structured continuity and follow-up skill for OpenClaw agents that routes dialogue as casual chat, staged memory, or tracked follow-up with carryover, lifecycle controls, routine-aware wording, and frontstage safety guards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kylnwu](https://clawhub.ai/user/kylnwu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to add state-backed continuity, `/new` topic reattachment, follow-up tracking, guided setup, and natural-language settings changes to an existing OpenClaw agent without bundling a channel adapter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill records selected conversation context, writes daily memory traces, and may create follow-up hooks.

Mitigation: Treat continuity state as sensitive, keep live state outside the public package, and ensure users can inspect, edit, and delete stored continuity data.

Risk: Server security evidence flags under-disclosed external embedding behavior.

Mitigation: Disable or tightly restrict remote embedding fallback unless the operator has reviewed provider configuration, data handling, and credential exposure.

Risk: Server security evidence flags broad file-moving or trashing utilities.

Mitigation: Remove, sandbox, or review the file output helper before installation in environments where unintended file movement would be harmful.

Risk: Dependencies and runtime state paths can affect installation risk.

Mitigation: Pin dependencies, use sandbox harness runs before live deployment, and verify writable state paths point to the intended OpenClaw workspace.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kylnwu/skills/test-continuity)
- [Publisher Profile](https://clawhub.ai/user/kylnwu)
- [README](README.md)
- [Install guide](docs/install.md)
- [Call Flow](docs/call-flow.md)
- [Harness](docs/harness.md)
- [Host Operator Settings](docs/host-operator-settings.md)
- [V2 Known Limits](docs/v2-known-limits.md)
- [Modules Reference](references/modules.md)
- [Templates Reference](references/templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON state/configuration, shell commands, and text for agent continuity context]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 plus configured OpenClaw state and config paths; produces stateful continuity artifacts outside the package during use.]

## Skill Version(s):

2.0.22 (source: ClawHub server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
