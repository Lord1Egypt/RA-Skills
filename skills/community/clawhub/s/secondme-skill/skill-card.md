## Description:

A complete pipeline to build your AI Second Me: distill your identity from personal data, grow a private knowledge base, train a local model, and govern what gets shared.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neiljo-gy](https://clawhub.ai/user/neiljo-gy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users building a personal AI double use this skill to orchestrate identity distillation, private knowledge-base construction, local persona-model training, evaluation gates, and release reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive identity data may be exposed because the skill combines personal-data workflows with broad file, shell, and optional network capabilities.

Mitigation: Review the skill before installation, run it in an isolated workspace, limit filesystem access to the intended persona project data, and require explicit approval before Colab, ACN, A2A, or other network use.

Risk: Regeneration and integration scripts execute local commands and package tooling that can affect generated runtime files.

Mitigation: Pin and verify OpenPersona and related tooling before running regeneration scripts, then run the sync, model-integration, and publish gates before release.

Risk: A persona model could be promoted before it has enough data, acceptable quality, or integrated model artifacts.

Mitigation: Keep the report and deployment recommendation blocked unless data, training, quality, governance, and persona model integration gates pass.

Risk: External publishing or sharing of identity artifacts can exceed the user's consent boundary.

Mitigation: Require explicit human approval for external publishing or sharing of identity artifacts and audit exported outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neiljo-gy/skills/secondme-skill)
- [Product report](references/product-report.md)
- [Report template](references/report-template.md)
- [Submission split guide](references/submission-split.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON state and configuration, shell commands, and generated OpenPersona runtime files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces data, model, and deployment reports only after the configured gates pass.]

## Skill Version(s):

0.1.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
