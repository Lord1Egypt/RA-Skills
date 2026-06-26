## Description: <br>
Design, review, or implement source-to-source code translation pipelines that convert or port code between programming languages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[syuaibsyuaib](https://clawhub.ai/user/syuaibsyuaib) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design, implement, or review staged code-conversion pipelines with parser probes, semantic IR boundaries, lowering rules, diagnostics, and regression validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Converted or scaffolded code may change behavior when source-language semantics do not map directly to the target language. <br>
Mitigation: Require an explicit feature matrix, semantic-gap diagnostics, and validation through parser probes, IR snapshots, target reparse checks, compile or type checks, and behavior fixtures. <br>
Risk: Unsupported constructs or lossy rewrites could be missed during a broad conversion effort. <br>
Mitigation: Classify features as direct, desugar, runtime-helper, manual-rewrite, or unsupported, and fail loudly or emit warnings for unsupported and lossy cases. <br>
Risk: Implementation or validation tasks may edit local source files or run parser and test tooling. <br>
Mitigation: Run commands only when requested for implementation or validation, review generated edits, and keep tests and parser probes tied to representative fixtures. <br>


## Reference(s): <br>
- [Architecture Blueprint](references/architecture-blueprint.md) <br>
- [Validation Checklist](references/validation-checklist.md) <br>
- [ClawHub Release Page](https://clawhub.ai/syuaibsyuaib/universal-code-converter) <br>
- [Publisher Profile](https://clawhub.ai/user/syuaibsyuaib) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code, shell command, and configuration snippets when implementation or validation is requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include feature matrices, diagnostics, assumptions, warnings, validation plans, and next steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
