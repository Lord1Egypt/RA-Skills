## Description:

Transforms product requirements into structured technical specifications when requirements are unclear, multiple implementation approaches exist, or component-level and architecture design is needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wjszxli](https://clawhub.ai/user/wjszxli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn product requirements, brief feature descriptions, or existing specifications into structured technical specification documents with requirements analysis, component design, technology comparisons, risks, and pending questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may auto-activate on broad architecture or implementation-design requests.

Mitigation: Confirm the user is asking for specification or design work before applying the skill, especially for simple bug fixes or direct coding tasks.

Risk: Optional helper scripts can read a PRD path supplied by the user and write a Markdown output file chosen by the user.

Mitigation: Run helper scripts only against intended local files and review the output path before execution.

Risk: The PRD helper script provides a starting point and does not fully generate a finished specification by itself.

Mitigation: Review and complete generated Markdown before using it as implementation guidance.

## Reference(s):

- [Requirements Analysis Trifecta Template](resources/requirements_analysis_template.md)
- [Technical Specification Template](resources/spec_template.md)
- [Component Design Template](resources/component_template.md)
- [Sample PRD Input](examples/sample_input.md)
- [Complete Spec Example](examples/sample_output.md)
- [Claude Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Skills Structure Guide](https://yeasy.gitbook.io/claude_guide/di-san-bu-fen-jin-jie-pian/06_skills/6.2_structure)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown technical specifications with tables, clarification questions, risk analysis, and pseudocode where appropriate.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional helper scripts can read a user-provided PRD path and write a Markdown output file selected by the user.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
