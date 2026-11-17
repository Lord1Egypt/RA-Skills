## Description:

Write high-quality YARA-X detection rules for malware hunting, including atom selection, string optimization, false positive reduction, module usage, rule templates, and testing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solomonneas](https://clawhub.ai/user/solomonneas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to draft, review, test, and optimize YARA-X malware detection rules with attention to performance and false positive reduction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated YARA-X rules may produce false positives, miss target samples, or perform poorly on large file sets.

Mitigation: Review generated rules, validate syntax with yr check, test against representative malware and goodware corpora, and place inexpensive file checks before expensive string or module conditions.

## Reference(s):

- [YARA-X rule authoring methodology and module guidance](https://github.com/trailofbits/skills/tree/main/plugins/yara-authoring)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with YARA rule examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include illustrative malware-family names and detection strings; generated rules should be reviewed before operational use.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
