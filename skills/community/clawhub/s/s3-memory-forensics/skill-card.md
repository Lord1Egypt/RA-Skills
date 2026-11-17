## Description:

Master memory forensics techniques including memory acquisition, process analysis, and artifact extraction using Volatility and related tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solomonneas](https://clawhub.ai/user/solomonneas)

### License/Terms of Use:

MIT-0

## Use Case:

Security analysts, incident responders, and forensic engineers use this skill to plan authorized RAM acquisition, analyze memory dumps, and extract forensic artifacts during malware analysis or incident response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full-system memory acquisition and credential extraction guidance can expose secrets or exceed authorization if used outside an approved investigation.

Mitigation: Use the skill only for authorized memory-forensics work, and define the target system, written authorization, evidence location, retention period, and secret-handling rules before following acquisition or credential commands.

Risk: Memory captures and extracted artifacts can contain raw hashes, tokens, passwords, or environment values.

Mitigation: Avoid returning raw secrets in chat or logs; summarize sensitive findings and handle captured evidence according to the investigation's retention and access rules.

Risk: Memory acquisition can affect forensic quality if evidence handling is not documented.

Mitigation: Document the acquisition time, tool, and capture hash, then maintain chain-of-custody records for generated memory images and analysis artifacts.

## Reference(s):

- [Volatility 3 Symbol Tables](https://downloads.volatilityfoundation.org/volatility3/symbols/)
- [S³ Memory Forensics on ClawHub](https://clawhub.ai/solomonneas/skills/s3-memory-forensics)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes forensic workflow checklists and tool-specific commands; does not generate memory dumps directly.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
