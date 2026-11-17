## Description:

Agent Skill for Swift architecture design and implementation patterns, with architecture-specific playbooks and review checklists for MVVM, MVI, TCA, Clean Architecture, VIPER, and Reactive patterns in SwiftUI/UIKit projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[efremidze](https://clawhub.ai/user/efremidze)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to select and apply Swift architecture patterns when designing features, refactoring modules, reviewing pull requests, or debugging maintainability issues in SwiftUI/UIKit projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can influence how an agent structures Swift code, which may introduce architecture choices that do not fit the project, dependencies, or team conventions.

Mitigation: Review generated architecture changes against the existing codebase, dependency choices, and team conventions before applying them.

Risk: Architecture mismatch handling may still proceed when a user insists on a mismatched pattern, increasing implementation and maintenance risk.

Mitigation: Use the fit check and closest-fit alternative guidance before implementation, and document the mismatch risks when proceeding.

## Reference(s):

- [Architecture Selection Guide](references/selection-guide.md)
- [MVVM Playbook (Swift + SwiftUI/UIKit)](references/mvvm.md)
- [MVI Playbook (Swift + SwiftUI/UIKit)](references/mvi.md)
- [TCA Playbook (Swift + SwiftUI/UIKit)](references/tca.md)
- [Clean Architecture Playbook (Swift + SwiftUI/UIKit)](references/clean-architecture.md)
- [VIPER Playbook (Swift + SwiftUI/UIKit)](references/viper.md)
- [Reactive Architecture Playbook (Swift + Combine/RxSwift)](references/reactive.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown with Swift code examples, architecture checklists, and scoped implementation plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include architecture fit results, mismatch rationale, migration steps, async and error-handling guidance, and PR checklist items tailored to the user's SwiftUI/UIKit context.]

## Skill Version(s):

0.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
