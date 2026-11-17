## Description:

Bind and verify a public custom domain for an existing Volcengine TOS bucket.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tenshowinnovation](https://clawhub.ai/user/tenshowinnovation)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to inspect, bind, and validate a direct Volcengine TOS custom storage domain with DNS, certificate, and object URL checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud credentials, private keys, or one-off DNS validation secrets may be exposed during troubleshooting.

Mitigation: Use least-privilege credentials and avoid sharing AK/SK, private keys, certificate private keys, or live validation secrets in chat or documentation.

Risk: Unreviewed changes can alter DNS records, TOS custom-domain rules, or certificate bindings.

Mitigation: Start with read-only inspection, then review proposed write operations before execution.

## Reference(s):

- [TOS Custom Storage Domain Runbook](references/tos-custom-domain-runbook.md)
- [ClawHub skill page](https://clawhub.ai/tenshowinnovation/skills/volc-tos-storage-domain)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline bash, JavaScript, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes read-first checks, proposed cloud write sequence, and validation commands.]

## Skill Version(s):

0.1.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
