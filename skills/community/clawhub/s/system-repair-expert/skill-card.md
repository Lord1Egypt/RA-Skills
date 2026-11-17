## Description:

System Repair Expert guides agents through a strict, prioritized troubleshooting workflow for system, software, configuration, and error-repair tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xqicxx](https://clawhub.ai/user/xqicxx)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and support engineers use this skill to diagnose system and software failures, gather missing context, prioritize official fixes, and evaluate lower-priority community or scripted repair options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostic details may be sent to search tools or stored in memory without enough scoping, consent, or redaction.

Mitigation: Review and redact secrets, full logs, configuration files, hostnames, tokens, and private paths before using web search or memory features.

Risk: Recommended third-party skills, GitHub results, or repair commands may be unverified.

Mitigation: Check source trust, permissions, and command impact before installation or execution, and prefer official vendor guidance when available.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xqicxx/skills/system-repair-expert)
- [README](artifact/README.md)
- [Usage Guide](artifact/USAGE_GUIDE.md)
- [Usage Examples](artifact/examples/usage_examples.md)
- [Release Notes](artifact/RELEASE_NOTES.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions, Code]

**Output Format:** [Markdown with structured troubleshooting steps and inline command or code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include confidence ratings, source-priority notes, and requests for missing diagnostic information.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
