## Description: <br>
Reviews serde serialization code for derive patterns, enum representations, custom implementations, and common serialization bugs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review Rust code that uses serde, serde_json, toml, bincode, or related serialization formats. It helps check derive usage, enum representations, field attributes, custom serialization, edition 2024 compatibility, and round-trip correctness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may produce incorrect or unsupported review findings if the agent has not inspected the current Cargo.toml and relevant source lines. <br>
Mitigation: Follow the documented gates: confirm serde context from disk and cite current-tree FILE:LINE evidence before reporting each finding. <br>
Risk: Some checks refer to a companion review-verification-protocol skill that may not be available in every agent environment. <br>
Mitigation: Confirm that companion protocol is available before relying on it, or perform equivalent verification against the referenced source code before adding findings. <br>


## Reference(s): <br>
- [Derive Patterns](references/derive-patterns.md) <br>
- [Custom Serialization](references/custom-serialization.md) <br>
- [Serde Code Review on ClawHub](https://clawhub.ai/anderskev/serde-code-review) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown review findings with file and line citations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are expected to include severity, description, and current-tree file references.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
