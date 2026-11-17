## Description:

Convert a foreign agent-skill directory into an OpenClaw skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silronin](https://clawhub.ai/user/silronin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to vet and convert non-OpenClaw agent skill directories into OpenClaw-compatible skill folders while preserving source capabilities within the approved conversion scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Converted skills may preserve malicious payloads, exfiltration logic, or secrets from source material.

Mitigation: Run conversions in an isolated workspace, review source material carefully, and require sanitization, secret redaction, and quarantine or removal of harmful content before using outputs from untrusted or high-risk sources.

Risk: The conversion workflow may retain sensitive or high-impact capabilities if the user approves a broad conversion scope.

Mitigation: Use the built-in vetting gate before conversion, classify flagged material, and proceed only with an explicit user-approved conversion scope.

## Reference(s):

- [Internal Vetting Rules](references/internal-vetting-rules.md)
- [Mapping Rules](references/mapping-rules.md)
- [ClawHub skill page](https://clawhub.ai/silronin/skills/skill-to-openclaw)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with file edits, code snippets, shell commands, and conversion summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces vetted OpenClaw skill directory content and a human-facing conversion summary when conversion is approved.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
