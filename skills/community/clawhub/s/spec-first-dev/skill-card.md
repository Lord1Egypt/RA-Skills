## Description: <br>
Spec-driven development workflow. Before writing any code, generates a comprehensive SPEC.md covering data models, user flows, API contracts, file structure, and edge cases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevdogg102396-afk](https://clawhub.ai/user/kevdogg102396-afk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill at the start of non-trivial build tasks to clarify intent, inspect the existing codebase, and create a SPEC.md before implementation begins. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect files in the current project while preparing a specification. <br>
Mitigation: Run it only in workspaces where project files may be read for planning, and review the generated SPEC.md before approving implementation. <br>
Risk: The skill can create or modify SPEC.md and may trigger from broad build requests. <br>
Mitigation: Confirm the generated specification and requested scope before allowing any coding to proceed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kevdogg102396-afk/spec-first-dev) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown document with concise status text and optional shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces SPEC.md in the project root and may optionally produce SPEC_APPROVED.md after approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
