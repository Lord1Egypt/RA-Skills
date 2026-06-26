## Description: <br>
Structured spec-first development workflow with multi-role expert review gates: clarify requirements, author spec documents, generate code from specs, verify with real tests, and iterate while keeping specs and code in sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xhuaustc](https://clawhub.ai/user/xhuaustc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use Spec Coder to plan and implement features through a spec-first workflow: clarify requirements, write specs, produce implementation code and tests, verify behavior, and evolve specs as the project changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated specs, code, tests, or change deltas may be incorrect or misaligned with project requirements. <br>
Mitigation: Review generated specs and code diffs, keep the project under version control, and run the relevant build, lint, type-check, and test commands before accepting changes. <br>
Risk: Spec and status files may capture sensitive project details if users paste secrets or credentials into workflow artifacts. <br>
Mitigation: Avoid putting secrets in spec, task, status, or review files; use environment variables or a secrets manager for sensitive values. <br>
Risk: Broad auto-approval preferences can let review gates progress without explicit confirmation. <br>
Mitigation: Keep explicit confirmation enabled at phase gates when human approval is required, especially before code generation, verification, or trunk spec merges. <br>


## Reference(s): <br>
- [Expert Review Protocol](references/expert-review-protocol.md) <br>
- [Spec Lifecycle Management](references/spec-lifecycle.md) <br>
- [Spec Coding - Core Templates](references/templates.md) <br>
- [Spec Coding - Lifecycle & Review Templates](references/templates-lifecycle.md) <br>
- [UI De-AI Aesthetic Checklist](references/ui-design-guidelines.md) <br>
- [ClawHub release page](https://clawhub.ai/xhuaustc/spec-coder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documents, code or diffs, shell commands, configuration notes, and concise implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update specs, design previews, implementation code, tests, verification reports, status files, and change-management documents in the user's project.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
