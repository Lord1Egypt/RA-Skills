## Description:

WAF Rule Validator - Tool for testing and validating WAF security rules

This skill is ready for commercial/non-commercial use.

## Publisher:

[realguoxiufeng](https://clawhub.ai/user/realguoxiufeng)

### License/Terms of Use:

MIT-0

## Use Case:

Security engineers and developers use this skill to run authorized WAF, API gateway, and IPS validation with malicious-looking requests across REST, GraphQL, gRPC, SOAP, and XMLRPC targets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides active malicious-request testing that can affect live systems or violate authorization boundaries.

Mitigation: Use it only with written authorization and prefer staging or dedicated test targets.

Risk: The documented Docker example uses host networking and an unpinned image reference.

Mitigation: Pin container digests, restrict Docker networking, and mount only a dedicated empty reports directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/realguoxiufeng/skills/waf-validator-skills)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Code]

**Output Format:** [Markdown with inline shell commands, configuration examples, and YAML snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide generation and review of local JSON, HTML, PDF, or DOCX assessment reports from the underlying WAF validation tool.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
