## Description: <br>
Reviews Swift code for concurrency safety, error handling, memory management, and common mistakes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review Swift changes for async/await, actor isolation, Sendable conformance, error handling, memory management, Swift Observation, and common Swift correctness issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reviews Swift source files and build settings, which may expose proprietary code or project configuration to the agent. <br>
Mitigation: Use it only in repositories where the agent is permitted to inspect the relevant Swift files, package manifests, and Xcode build settings. <br>
Risk: The workflow references a separate review-verification-protocol skill that is not included in this artifact. <br>
Mitigation: Inspect and approve that referenced skill separately before relying on its verification gates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anderskev/swift-code-review) <br>
- [Swift Concurrency](references/concurrency.md) <br>
- [Swift Observation Framework](references/observable.md) <br>
- [Swift Error Handling](references/error-handling.md) <br>
- [Swift Common Mistakes](references/common-mistakes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown review findings with file and line references, severity, and explanation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are gated by a Swift version baseline, full-symbol reading, scoped checklist selection, and pre-report verification.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
