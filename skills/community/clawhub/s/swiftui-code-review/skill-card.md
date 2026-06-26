## Description: <br>
Reviews SwiftUI code for view composition, state management, performance, and accessibility. Use when reviewing .swift files containing SwiftUI views, property wrappers (@State, @Binding, @Observable), or UI code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to review SwiftUI .swift files for view composition, state management, performance, and accessibility issues. It guides reviews toward evidence-bound findings with file and line references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may read Swift source files supplied for review. <br>
Mitigation: Use this skill only with code you are comfortable processing with your agent. <br>
Risk: Review findings may be incomplete or incorrect if they are not anchored to the reviewed code. <br>
Mitigation: Require file and line references for substantive findings and review recommendations before applying changes. <br>


## Reference(s): <br>
- [View Composition](references/view-composition.md) <br>
- [State Management](references/state-management.md) <br>
- [Performance](references/performance.md) <br>
- [Accessibility](references/accessibility.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown code review findings with file and line references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only guidance; no shell commands or code execution indicated.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
