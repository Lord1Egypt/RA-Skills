## Description:

Apply WCAG 2 Level AA accessibility standards to design systems, UI components, and web pages, including contrast validation, design-token patterns, typography and focus-state rules, and a semantics checklist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raunakkathuria](https://clawhub.ai/user/raunakkathuria)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and agents use this skill to build or review UI against WCAG 2 AA expectations, especially color contrast, design tokens, typography, focus states, semantics, keyboard behavior, and screen-reader readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to run a local Node contrast checker or suggest adding it to build or CI workflows.

Mitigation: Review proposed commands and run the bundled checker only against intended contrast-pair configuration files; the reviewed artifact does not request sensitive access or network behavior.

Risk: Automated contrast and accessibility checks can be mistaken for complete WCAG conformance.

Mitigation: Treat automated results as partial evidence and require keyboard walk-throughs, screen-reader checks, zoom and reflow testing, and content semantics review before claiming full accessibility.

## Reference(s):

- [WCAG 2 Level AA Conformance](https://www.w3.org/WAI/WCAG2AA-Conformance)
- [WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/?currentsidebar=%23col_customize&levels=aaa)
- [WCAG 2.2 AA checklist with fix patterns](references/wcag-checklist.md)
- [ARIA Authoring Practices Patterns](https://www.w3.org/WAI/ARIA/apg/patterns/)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline code, shell commands, and checklist references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local Node contrast-checker commands and CI integration guidance]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
