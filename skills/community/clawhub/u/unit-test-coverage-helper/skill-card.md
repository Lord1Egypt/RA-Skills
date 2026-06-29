## Description: <br>
Helps software teams add useful unit tests and improve coverage in existing codebases through a repeatable workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyro-ma](https://clawhub.ai/user/kyro-ma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, maintainers, and product teams use this skill to plan, write, and validate unit tests that improve confidence in existing codebases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad testing or quality prompts may activate the skill when the user did not intend to use it. <br>
Mitigation: Prefer explicit invocation for this skill and confirm that its proposed workflow matches the user's current testing goal. <br>
Risk: Generated test plans or code changes may encode incorrect assumptions about the target codebase. <br>
Mitigation: Review proposed tests and run the suggested verification commands before applying or merging changes. <br>


## Reference(s): <br>
- [Requirement Plan](references/requirement-plan.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with optional code blocks and verification commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tailored to the user's codebase, constraints, and requested testing goal.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
