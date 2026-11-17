## Description:

TRIZ innovation solution analysis assistant that supports system component analysis, contact relationship analysis, functional modeling, causal chain analysis, and innovation solution generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn a product problem into a structured TRIZ workflow: component analysis, contact mapping, functional modeling, causal chain analysis, concept solution generation, and solution detail generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user technical problem descriptions and generated intermediate analysis into TRIZ-related tools.

Mitigation: Avoid using confidential engineering details unless the connected TRIZ tools are approved for that data.

Risk: Generated TRIZ solutions and patent-inspired implementation details may be incomplete, impractical, or unsuitable for a specific product context.

Mitigation: Have qualified engineering and IP reviewers evaluate recommendations before implementation or external use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/triz-innovation-pro)
- [System Component Analysis](artifact/references/01_system_component_analysis.md)
- [Contact Relationship Analysis](artifact/references/02_component_touch_analysis.md)
- [Functional Modeling](artifact/references/03_functional_modeling.md)
- [Problem Description and Core Problem Selection](artifact/references/04_functional_modeling_problem_summary.md)
- [Causal Chain Analysis](artifact/references/05_causal_chain_analysis.md)
- [Causal Chain Problem Filtering](artifact/references/06_causal_chain_problem_summary.md)
- [Solution Generation](artifact/references/07_solution.md)
- [Solution Detail Generation](artifact/references/08_solution_detail.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with tables, plain-text summaries, JSON-derived fields, and Mermaid code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports summary and detail display modes; downstream tool results are passed between workflow steps as complete JSON rather than truncated display text.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter and manifest show 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
