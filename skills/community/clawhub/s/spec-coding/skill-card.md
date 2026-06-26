## Description: <br>
A specification-driven coding workflow that helps agents draft feature, API, and component specifications from user requirements or existing code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pupuking723](https://clawhub.ai/user/pupuking723) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to create structured software specification drafts before implementation, during requirements review, or when reverse-engineering specs for legacy code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated specifications may omit relevant code paths or requirements when reverse-engineering an existing project. <br>
Mitigation: Point the skill only at the files or modules that should be analyzed and review the resulting draft before using it for implementation. <br>
Risk: The skill describes collaboration with sub-agents, which could broaden the work beyond drafting if delegated without review. <br>
Mitigation: Confirm before allowing any sub-agent handoff or implementation work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pupuking723/spec-coding) <br>
- [Template guide](artifact/assets/templates/README.md) <br>
- [Feature specification template](artifact/assets/templates/feature-spec.md) <br>
- [API specification template](artifact/assets/templates/api-spec.md) <br>
- [Component specification template](artifact/assets/templates/component-spec.md) <br>
- [Feature specification example](artifact/assets/examples/feature-example.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown specification documents with tables, checklists, and code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Draft, review, approved, in-progress, and done status labels are used to track specification state.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
