## Description: <br>
Guides AI-assisted development using a five-phase Vibe Coding workflow for requirements, architecture, code generation, debugging, and iteration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shiiyyo](https://clawhub.ai/user/shiiyyo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to guide AI-assisted software projects through a structured workflow: clarify requirements, design architecture, implement modules, debug issues, and plan later iterations. It is especially suited to users who want reusable Markdown development artifacts before and during coding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may create or update project documentation and implementation files during normal use. <br>
Mitigation: Review proposed file paths and diffs before applying changes, and keep edits scoped to the phase and requirements the user confirmed. <br>
Risk: The workflow may guide the agent to run normal project verification steps or suggest committing completed module work. <br>
Mitigation: Inspect commands before execution, run them only in trusted project workspaces, and commit only after reviewing the generated changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shiiyyo/vibe-coding-skill) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown guidance with structured checklists, architecture notes, interface contracts, Mermaid diagrams, code suggestions, and debugging summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow emphasizes user confirmation at phase boundaries and preserves key development artifacts as Markdown.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
