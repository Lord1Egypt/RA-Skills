## Description:

Detects malicious behavior and security threats in target skills using analysis of obfuscation, encoding, encryption, and dynamic code techniques.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ninjagpt](https://clawhub.ai/user/ninjagpt)

### License/Terms of Use:


## Use Case:

Developers and security reviewers use this skill to inspect local skill files for malicious behavior, obfuscation, encoding, encryption, dynamic code, and other suspicious patterns, then produce a security audit report with usage guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may include sensitive content from inspected skills, including decoded payloads, credential-looking strings, or malicious examples.

Mitigation: Treat reports as sensitive review artifacts and limit their storage, sharing, and retention to the security review workflow.

Risk: Decoded or reconstructed snippets in a report may contain executable malicious examples from the target skill.

Mitigation: Inspect decoded content as evidence only and do not execute commands, scripts, or reconstructed payloads from the target skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ninjagpt/skills/skill-security-reviewer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown security audit report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are written under a target-specific review-report directory and may include decoded evidence and usage recommendations.]

## Skill Version(s):

3.0.0 (source: server release metadata and SKILL.md header)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
