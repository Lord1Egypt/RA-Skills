## Description:

UI Craft Pro helps agents design, refine, and implement UI for websites, dashboards, apps, landing pages, and components using a local design knowledge base and code-first workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[airaeliteagent](https://clawhub.ai/user/airaeliteagent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and UI-building agents use this skill to choose an appropriate visual direction, generate or infer a design system, translate that system into interface code, and review whether the result remains coherent and non-generic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional save workflow can overwrite Markdown files outside its intended design-system folder when crafted names or paths are supplied.

Mitigation: Use trusted project and page names, choose trusted output directories, and review containment and overwrite behavior before using persistence.

Risk: Generated UI guidance can still produce mismatched, generic, inaccessible, or low-contrast interfaces if applied without review.

Mitigation: Apply the included implementation patterns and review checklist, then manually verify hierarchy, component consistency, readability, focus states, mobile behavior, and reduced-motion handling.

## Reference(s):

- [Implementation Patterns](references/implementation-patterns.md)
- [Review Checklist](references/review-checklist.md)
- [Product Archetypes](references/product-archetypes.md)
- [Anti-Generic UI Review](references/anti-generic-review.md)
- [Design System Teardown Checklist](references/design-system-teardown-checklist.md)
- [Style Cloning Playbook](references/style-cloning-playbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional JSON output and generated design-system Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May optionally persist design-system Markdown files when the save workflow is used.]

## Skill Version(s):

0.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
