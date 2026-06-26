## Description: <br>
Reviews Python code for type safety, async patterns, error handling, and common mistakes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review Python files for style, typing, async behavior, exception handling, and common implementation mistakes before reporting findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a referenced review-verification-protocol skill for final reporting guidance, and that dependency may be absent or untrusted in a user's environment. <br>
Mitigation: Before relying on final review output, confirm that the referenced verification protocol skill exists locally and comes from a trusted source. <br>


## Reference(s): <br>
- [Async Patterns](references/async-patterns.md) <br>
- [Common Mistakes](references/common-mistakes.md) <br>
- [Error Handling](references/error-handling.md) <br>
- [PEP8 Style Guide](references/pep8-style.md) <br>
- [Type Safety](references/type-safety.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Markdown] <br>
**Output Format:** [Markdown review notes with scoped Python file and line references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings should follow the skill's gates for scope, false-positive screening, evidence, verification, and final reporting.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
