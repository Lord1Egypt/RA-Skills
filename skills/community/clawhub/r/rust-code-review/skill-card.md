## Description: <br>
Reviews Rust code for ownership, borrowing, lifetime, error handling, trait design, unsafe usage, and common mistakes. Use when reviewing .rs files, checking borrow checker issues, error handling patterns, or trait implementations. Covers Rust 2024 edition patterns and modern idioms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review Rust source, Cargo manifests, unsafe code, concurrency patterns, error handling, trait design, and Rust 2024 idioms before acting on code-review findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may cause an agent to read Rust source files and Cargo manifests during review. <br>
Mitigation: Use it only in repositories where Rust review access is intended, and follow the host environment's handling rules for sensitive code. <br>
Risk: Review output can include incorrect or overstated findings if the agent reports before checking full functions, crate context, and severity calibration. <br>
Mitigation: Apply the artifact's gates before acting on findings: read the relevant Cargo manifest, inspect the full cited code region, and match severity to the documented calibration. <br>
Risk: The skill references related review skills that may add separate guidance if present. <br>
Mitigation: Treat referenced skills as separate inputs and review their guidance before relying on combined review output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anderskev/rust-code-review) <br>
- [Ownership and Borrowing](references/ownership-borrowing.md) <br>
- [Lifetime Variance](references/lifetime-variance.md) <br>
- [Error Handling](references/error-handling.md) <br>
- [Async and Concurrency](references/async-concurrency.md) <br>
- [Concurrency Primitives](references/concurrency-primitives.md) <br>
- [Memory Ordering](references/memory-ordering.md) <br>
- [Lock-Free Patterns](references/lock-free-patterns.md) <br>
- [Concurrency Models](references/concurrency-models.md) <br>
- [Types and Layout](references/types-layout.md) <br>
- [Interface Design](references/interface-design.md) <br>
- [Patterns in the Wild](references/patterns-in-the-wild.md) <br>
- [Unsafe Code, API Design, and Derive Patterns](references/common-mistakes.md) <br>
- [Unsafe Code: Deep Review](references/unsafe-deep.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown code-review findings with file and line references, severity labels, and prose explanations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings follow the artifact's FILE:LINE, severity, and description format.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
