## Description:

Evaluates Clawdbot skills for quality, reliability, and publish-readiness using automated structural checks plus a 25-criterion rubric based on ISO 25010, OpenSSF, Shneiderman, and agent-specific heuristics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terwox](https://clawhub.ai/user/terwox)

### License/Terms of Use:


## Use Case:

Developers and skill maintainers use this skill to evaluate Clawdbot skills before publishing. It combines automated structural checks, a manual 25-criterion rubric, and an evaluation template for publish-readiness reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The evaluator reads local skill directories, so overly broad scan targets can expose unrelated local files to the review process.

Mitigation: Run it only against the intended skill directory and avoid providing credentials or unrelated workspace paths during audits.

Risk: Required or optional third-party tooling can change behavior when dependency versions are not pinned.

Mitigation: Pin PyYAML and any optional SkillLens version in the audit environment before repeatable or commercial release checks.

## Reference(s):

- [Skill Evaluation Rubric](references/rubric.md)
- [Evaluation Template](assets/EVAL-TEMPLATE.md)
- [SkillLens](https://www.npmjs.com/package/skilllens)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with command examples, an evaluation template, and optional JSON from eval-skill.py]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces automated pass/warn/fail checks and supports manual scoring across 25 rubric criteria.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
