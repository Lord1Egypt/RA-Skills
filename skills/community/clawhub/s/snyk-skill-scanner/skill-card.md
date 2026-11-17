## Description:

Scan installed agent components such as MCP servers, skills, and agent tools for security vulnerabilities using snyk-agent-scan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swiftking100](https://clawhub.ai/user/swiftking100)

### License/Terms of Use:


## Use Case:

Developers and security reviewers use this skill to run snyk-agent-scan against installed or candidate agent components and interpret findings such as prompt injection, malware payloads, credential handling issues, hardcoded secrets, and MCP-specific risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact instructs users to run mutable external code through snyk-agent-scan@latest and a remote shell installer, which the server security summary flagged as relying too heavily on mutable third-party code.

Mitigation: Prefer a pinned, reviewed version of snyk-agent-scan, avoid copy-pasting the curl | sh installer, and run scans only against required paths under a non-administrative account.

## Reference(s):

- [Snyk Agent Scan Issue Codes](https://github.com/snyk/agent-scan/blob/main/docs/issue-codes.md)
- [ClawHub Skill Page](https://clawhub.ai/swiftking100/skills/snyk-skill-scanner)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON scan output when users run snyk-agent-scan with the --json option.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
