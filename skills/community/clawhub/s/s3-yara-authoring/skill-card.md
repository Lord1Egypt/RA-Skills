## Description:

Write high-quality YARA-X detection rules for malware identification and threat hunting, covering naming conventions, string selection, performance optimization, and false positive reduction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solomonneas](https://clawhub.ai/user/solomonneas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to write, review, optimize, and troubleshoot YARA-X malware detection rules, including turning indicators into signatures and reducing false positives before deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may suggest package-manager install commands or file scans for YARA-X workflows.

Mitigation: Confirm that installation commands, sample files, and target directories are intentional before running scans or commands.

Risk: Detection guidance can produce overly broad or misleading rules if not validated.

Mitigation: Review generated rules and test them against representative clean file sets before operational use.

## Reference(s):

- [Trail of Bits YARA Authoring Methodology](https://github.com/trailofbits/skills/tree/main/plugins/yara-authoring)
- [ClawHub skill page](https://clawhub.ai/solomonneas/skills/s3-yara-authoring)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with YARA rule examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include YARA-X rule templates, review guidance, testing commands, and false-positive reduction recommendations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
