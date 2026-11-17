## Description:

Analyze Terraform plans for risk before apply, classify changes as safe, moderate, dangerous, or critical, and detect destroys, IAM changes, data-loss risks, and blast radius without running apply.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tkuehnl](https://clawhub.ai/user/tkuehnl)

### License/Terms of Use:

MIT

## Use Case:

Developers and infrastructure engineers use this skill to review Terraform or OpenTofu plans, validation results, and state summaries before making manual apply decisions. It helps identify destructive, security-sensitive, and high-blast-radius infrastructure changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger Terraform initialization, which may write local dependency files and contact registries, provider APIs, or remote state backends.

Mitigation: Use trusted provider and module sources, scoped credentials, and a trusted or disposable workspace before allowing the agent to run Terraform commands.

Risk: Terraform plan and state review can expose infrastructure metadata and relies on configured cloud credentials.

Mitigation: Run with least-privilege credentials and limit sharing of reports when resource names or topology reveal sensitive architecture.

Risk: Risk classification is heuristic and may not capture every provider-specific production impact.

Mitigation: Treat the report as a review aid and require human review for destroys, replacements, IAM or security changes, databases, and production plans.

## Reference(s):

- [Terraform installation documentation](https://developer.hashicorp.com/terraform/install)
- [OpenTofu installation documentation](https://opentofu.org/docs/intro/install/)
- [jq download documentation](https://jqlang.github.io/jq/download/)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Guidance]

**Output Format:** [Structured JSON plus Markdown risk reports and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports summarize resource changes, risk levels, destructive actions, drift, and pre-apply review items; the skill does not run apply.]

## Skill Version(s):

0.2.1 (source: server release metadata; artifact frontmatter and changelog list 0.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
