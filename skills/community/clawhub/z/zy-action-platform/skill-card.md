## Description:

Connect and operate ZY Action Platform by guiding verified installation and API key setup, then using the platform client for health checks, login, natural-language data queries, workflow automation, datasets, ontology, intelligence search, and deployment inspection across AIP, Foundry, Gotham, Apollo, and Swift.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youkpan](https://clawhub.ai/user/youkpan)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, operators, analysts, and developers use this skill to connect an agent to a local or approved remote ZY Action Platform deployment, run data and automation tasks, and summarize platform JSON responses for the user. It is intended for operational data queries, workflow runs, ontology and search workflows, deployment inspection, and installation guidance with explicit consent for sensitive steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generic API pass-through may expose sensitive or administrative routes if path handling or URL redaction controls are insufficient.

Mitigation: Prefer built-in commands and bundled platform documentation; avoid generic pass-through for sensitive or administrative routes, and require dry-run review plus explicit user consent before any write.

Risk: Credentials or bearer tokens can be exposed through command-line arguments, terminal history, process listings, or copied transcripts.

Mitigation: Use a dedicated low-privilege or read-only platform account, avoid passing passwords or tokens on the command line when possible, and run logout to clear cached tokens when finished.

Risk: Remote platform access can send credentials or tokens to the wrong endpoint if the destination is not verified.

Mitigation: Require HTTPS for non-loopback hosts, preview login destinations with dry-run, confirm new remote origins before trusting them, and keep tokens bound to the approved origin.

Risk: Downloaded platform installers can introduce supply-chain risk if executed without verification.

Mitigation: Use versioned artifacts only, verify SHA-256 and digital signature before extraction or execution, and proceed only after the user confirms the artifact and verification results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/youkpan/skills/zy-action-platform)
- [Publisher profile](https://clawhub.ai/user/youkpan)
- [ZY Action Platform download page](https://zyinfo.pro/action/)
- [API Quick Reference](references/api-spec.md)
- [Session Transcripts](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and concise text summaries with inline shell commands and JSON-derived results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill instructs the agent to run the platform client, read JSON output before summarizing, and request explicit confirmation for credentials, remote hosts, writes, and installer execution.]

## Skill Version(s):

1.1.1 (source: ClawHub release metadata; artifact frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
