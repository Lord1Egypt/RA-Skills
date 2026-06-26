## Description: <br>
Transforms product requirements into structured technical specifications when requirements are unclear, multiple implementation approaches exist, or component-level and architecture design is needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjszxli](https://clawhub.ai/user/wjszxli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn product requirements, PRDs, and existing technical specifications into structured implementation plans with requirements analysis, component design, technology comparisons, risk analysis, and pending questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Manual GitHub installation can bypass the reviewed ClawdHub package. <br>
Mitigation: Prefer the reviewed ClawdHub package; if cloning manually, verify the repository before use. <br>
Risk: Optional helper scripts can read PRD inputs and write generated Markdown to user-selected paths. <br>
Mitigation: Run helper scripts only when file generation is intended, choose input and output paths carefully, and review generated files before relying on them. <br>
Risk: Generated specifications may be incomplete or misleading if the source requirements are ambiguous. <br>
Mitigation: Review generated Markdown and resolve clarification questions before using the specification as an implementation plan. <br>


## Reference(s): <br>
- [Requirements Analysis Trifecta Template](resources/requirements_analysis_template.md) <br>
- [Technical Specification Template](resources/spec_template.md) <br>
- [Component Design Template](resources/component_template.md) <br>
- [Sample Technical Specification Output](examples/sample_output.md) <br>
- [Claude Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) <br>
- [Skills Structure Guide](https://yeasy.gitbook.io/claude_guide/di-san-bu-fen-jin-jie-pian/06_skills/6.2_structure) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Markdown technical specifications with optional shell commands for local helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May output clarification questions instead of a full specification when the requirements are incomplete.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
