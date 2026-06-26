## Description: <br>
Auto-documentation generator that analyzes code and generates README, API docs, architecture docs, and inline comments when documentation is missing or outdated. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NakedoShadow](https://clawhub.ai/user/NakedoShadow) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to inspect project files and generate accurate Markdown documentation such as README files, API references, architecture notes, and useful inline comments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated documentation can be inaccurate if the agent has not read the relevant source files or if examples are not checked against current code. <br>
Mitigation: Review generated Markdown before committing or publishing, and require examples, endpoints, and signatures to match the current source. <br>
Risk: Inline comments or new documentation files may modify a repository in ways the user did not intend. <br>
Mitigation: Explicitly tell the agent whether it may create new files or modify existing source files for inline comments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NakedoShadow/shadows-doc-forge) <br>
- [Publisher profile](https://clawhub.ai/user/NakedoShadow) <br>
- [OpenClaw homepage metadata](https://clawhub.ai/NakedoShadow) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown documents with code examples and optional inline source comments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces standalone documentation files alongside source files or at the project root.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata and artifact SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
