## Description:

SwiftUI oral programming skill that turns Chinese natural-language UI requests into SwiftUI code aligned with physical metaphors and Apple design guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soponcd](https://clawhub.ai/user/soponcd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to convert spoken Chinese UI intent into SwiftUI components, layout patterns, animation parameters, and preview guidance. It is especially suited for SwiftUI design iteration where natural phrasing needs to become implementation-ready code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may persist UI preferences or newly learned phrases across sessions.

Mitigation: Require explicit confirmation before any memory or cheat-sheet update, and review the proposed content before it is written.

Risk: The skill may write Swift files or update skill-related files as part of UI generation workflows.

Mitigation: Run it only in a trusted workspace and require approval before file creation or modification.

Risk: The skill may automate Xcode Canvas preview through local tooling or AppleScript.

Mitigation: Use preview automation only when local Xcode automation is acceptable, and keep the preview step optional.

## Reference(s):

- [Talk2UI ClawHub Skill Page](https://clawhub.ai/soponcd/skills/talk2ui)
- [Talk2UI Declared Homepage](https://github.com/soponcd/timeflow-skills/tree/main/teams/skills/talk2UI)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Swift code blocks, shell command examples, and concise implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local file writes, persistent preference updates, and Xcode preview automation when the user accepts those actions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
