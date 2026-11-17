## Description:

Generates Chinese-language four-page HTML ToB sales proposals from client, industry, pain point, budget, timeline, and product inputs using bundled case and methodology data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[william202404](https://clawhub.ai/user/william202404)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and presales teams use this skill to turn client discovery inputs into a Chinese-language HTML proposal covering pain-point alignment, solution alignment, implementation path, and ROI with anonymized case examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML proposals may expose confidential client information if users enter sensitive details.

Mitigation: Avoid entering confidential client details unless they are approved for inclusion in the generated proposal file.

Risk: The artifact claims sensitive information is automatically desensitized, but the security evidence says not to rely on that behavior.

Mitigation: Manually review generated proposals for sensitive information before sharing or storing them.

Risk: Proposal case references and ROI claims can be misleading if not verified against the bundled knowledge base and the target client context.

Mitigation: Review case citations, ROI ranges, and assumptions before using the output in a customer-facing proposal.

Risk: The security evidence notes dependency and documentation issues.

Mitigation: Audit or update dependencies before CI use or use on untrusted repositories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/william202404/skills/tob-sales-proposal)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, code, shell commands, guidance, files]

**Output Format:** [HTML file with supporting command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces proposal.html by default; generated proposal content should be reviewed before customer use.]

## Skill Version(s):

1.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
