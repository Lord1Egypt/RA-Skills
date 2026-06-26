## Description: <br>
Orchestrates CLI and TUI UX improvement across languages, including audits, flow redesign, prompts, progress and result views, implementation stack recommendations, and visible before/after evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[may4748854-rgb](https://clawhub.ai/user/may4748854-rgb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit, redesign, map, and validate terminal interfaces for command-line tools and TUIs. It helps agents choose an appropriate interaction model, plan implementable terminal UX changes, verify framework feasibility when needed, and show the user-visible impact. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional web lookup or visual tools may expose sensitive terminal output when users include secrets, credentials, or private diagnostics. <br>
Mitigation: Review and redact sensitive terminal output before using optional external verification or visualization tools. <br>
Risk: Framework recommendations can become stale when they depend on current terminal library capabilities. <br>
Mitigation: Verify version-sensitive framework behavior with official documentation before implementing a design that depends on specific widgets, lifecycle behavior, async support, mouse support, or resize behavior. <br>


## Reference(s): <br>
- [Audit Checklist](references/audit-checklist.md) <br>
- [Design Principles](references/design-principles.md) <br>
- [Interaction Patterns](references/interaction-patterns.md) <br>
- [Implementation Mapping](references/implementation-mapping.md) <br>
- [Change Visibility](references/change-visibility.md) <br>
- [Tool Coordination](references/tool-coordination.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with optional code, shell command, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include before/after terminal UX comparisons, validation checklists, and implementation mapping.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
