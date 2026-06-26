## Description: <br>
Agent skill for Swift architecture design and implementation guidance, with architecture-specific playbooks and review checklists for SwiftUI/UIKit projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[efremidze](https://clawhub.ai/user/efremidze) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to select, adapt, and review Swift architecture patterns for SwiftUI/UIKit features, refactors, debugging, and pull requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may analyze project code or pull request context supplied by the user. <br>
Mitigation: Provide only project code and review context that is appropriate for the agent to inspect. <br>
Risk: Architecture recommendations or Swift snippets may not fully match a codebase's existing conventions. <br>
Mitigation: Review recommendations before applying them, check the stated fit result and assumptions, and adapt the architecture checklist to the local codebase. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/efremidze/swift-architecture-skill) <br>
- [Architecture Selection Guide](references/selection-guide.md) <br>
- [MVVM Playbook](references/mvvm.md) <br>
- [MVI Playbook](references/mvi.md) <br>
- [TCA Playbook](references/tca.md) <br>
- [Clean Architecture Playbook](references/clean-architecture.md) <br>
- [VIPER Playbook](references/viper.md) <br>
- [Reactive Architecture Playbook](references/reactive.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code] <br>
**Output Format:** [Markdown prose with Swift code snippets, architecture fit results, migration guidance, and checklist items.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scoped to the requested feature or review; may include explicit assumptions, mismatch risks, migration steps, and line-level fixes when code context is provided.] <br>

## Skill Version(s): <br>
0.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
