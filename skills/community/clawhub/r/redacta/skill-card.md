## Description:

Redacta pseudonymises medical and clinical text by replacing patient identifiers with stable labelled tokens, returning redacted text, a redaction report, and optional re-identification support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickjlamb](https://clawhub.ai/user/nickjlamb)

### License/Terms of Use:

MIT-0

## Use Case:

Healthcare users, developers, and agents use Redacta to pseudonymise clinical letters, notes, referrals, discharge summaries, and patient records before sharing them or processing them with other tools. It can also restore original values from a protected token map when reversible redaction is required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive medical text may be written to a predictable temporary file path during the skill workflow.

Mitigation: Use stdin or a secure per-run temporary file, delete it immediately after processing, and avoid shared temporary paths for clinical or regulated data.

Risk: The MCP setup example can install the latest package version without pinning.

Mitigation: Pin MCP npm invocations to an exact reviewed version before deployment, especially in clinical or regulated environments.

Risk: The skill produces token maps that can reverse pseudonymisation.

Mitigation: Store token maps separately from redacted text, restrict access, and handle them with the same care as the source clinical data.

Risk: Residual identifiers may remain because deterministic and reasoning-based redaction is not a guarantee.

Mitigation: Review the redaction report and self-check output before sharing, and use formal data-protection review where required.

## Reference(s):

- [Redacta Skill Page](https://clawhub.ai/nickjlamb/skills/redacta)
- [Redacta Reference](reference.md)
- [Redacta README](README.md)
- [Redacta MCP Server README](mcp-server/README.md)
- [Redacta npm Package](https://www.npmjs.com/package/redacta-mcp)
- [PharmaTools Redacta](https://www.pharmatools.ai/redacta)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown response with redacted clinical text, a redaction report, optional token map table or JSON, and shell command snippets when needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include reversible token maps; token maps should be kept separate and protected when the user wants identifiers isolated.]

## Skill Version(s):

1.2.0 (source: SKILL.md frontmatter, release evidence, npm package metadata, MCP package metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
