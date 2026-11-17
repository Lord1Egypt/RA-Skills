## Description:

Prove Before Act accountability integration for AI agents. REST API, MCP, and x402. The @jasonxkensei/xproof ClawHub slug is a legacy compatibility identifier.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonxkensei](https://clawhub.ai/user/jasonxkensei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add accountability records to agent workflows by hashing decisions or outputs locally, anchoring proofs through REST, MCP, or payment-enabled calls, and later verifying the resulting proof records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proof records and payment transactions can be public and irreversible.

Mitigation: Hash content locally, avoid sensitive filenames or metadata, and require explicit approval plus spending limits before x402, batch, or certification actions.

Risk: API keys or payment credentials could be exposed through logs, repositories, or agent transcripts.

Mitigation: Keep API keys out of logs and repositories, treat pm_ keys as secrets, and prefer ClawHub installation or pinned SDK and source versions.

Risk: Unpinned install examples or SDK versions can drift from the reviewed release.

Mitigation: Install through ClawHub where possible, or pin any GitHub and SDK versions before use.

## Reference(s):

- [Prove Before Act homepage](https://provebeforeact.com)
- [ClawHub skill page](https://clawhub.ai/jasonxkensei/skills/xproof)
- [API Reference](references/api-reference.md)
- [Certification API](references/certification.md)
- [MCP Server](references/mcp.md)
- [x402 Payments](references/x402.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code examples, shell commands, API payloads, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides agents to hash content locally, submit proof metadata, handle optional payment flows, and verify proof status before relying on records.]

## Skill Version(s):

4.0.18 (source: server release metadata; artifact frontmatter reports 3.3.14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
