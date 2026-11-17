## Description:

Build custom peer-review skills for specific research areas, problem families, and method combinations using OpenReview evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c-narcissus](https://clawhub.ai/user/c-narcissus)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, reviewers, and developers use this skill to build reusable, research-area-specific reviewer skills grounded in public OpenReview reviewer concerns and accepted-paper response patterns. The generated child skills help review future papers in a selected field, plan rebuttal or revision paths, and check novelty, soundness, baselines, reproducibility, and subtle logic flaws.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can generate future agent skills from unvalidated local text and profile data.

Mitigation: Use trusted profile JSON and reference Markdown files, keep generated outputs in a sandboxed workspace, and inspect generated SKILL.md, agents/openai.yaml, and references before installation.

## Reference(s):

- [Research Area Profile Schema](references/research_area_profile_schema.md)
- [OpenReview Area Evidence Workflow](references/openreview_area_evidence_workflow.md)
- [Generated Area Review Skill Contract](references/generated_area_review_skill_contract.md)
- [Subtle Logic Flaws Checklist](references/subtle_logic_flaws.md)
- [OpenReview API](https://api2.openreview.net)
- [ClawHub Skill Page](https://clawhub.ai/c-narcissus/skills/research-review-skill-factory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, generated skill files, JSON area profiles, Python commands, and YAML configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated child skills should be reviewed and scanned before installation or sharing.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
