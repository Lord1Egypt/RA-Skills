## Description: <br>
Meta-skill that orchestrates comprehensive testing across a project by coordinating testing-patterns, e2e-testing, and testing agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to plan, implement, validate, and maintain project test coverage across unit, integration, and end-to-end workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent to edit tests, documentation, or CI quality gates. <br>
Mitigation: Review diffs before allowing commits or CI changes, and verify that proposed changes match the project's testing policy. <br>
Risk: The workflow routes to related testing skills that may affect the final testing strategy. <br>
Mitigation: Inspect the routed skills before relying on the full workflow. <br>
Risk: Installing from an unreviewed or moving source can change the skill behavior over time. <br>
Mitigation: Install only from a trusted source, preferably from a reviewed or pinned version. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wpank/testing-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, test strategy templates, and file-change guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or edit tests, documentation, and CI quality-gate configuration when applied by an agent.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter says 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
