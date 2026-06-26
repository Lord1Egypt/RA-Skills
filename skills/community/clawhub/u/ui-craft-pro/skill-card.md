## Description: <br>
Design, refine, and implement better UI for websites, dashboards, apps, landing pages, and components using a local design knowledge base and a code-first implementation workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AiraEliteAgent](https://clawhub.ai/user/AiraEliteAgent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and designers use this skill to choose a UI direction, generate project-specific design systems, translate those decisions into interface code, and review the result for coherence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated UI recommendations may be visually plausible but mismatched to brand, audience, accessibility, or inclusivity needs. <br>
Mitigation: Review generated visual direction, contrast, copy, and component behavior before using the output in production. <br>
Risk: When persistence is explicitly requested, the skill can write design-system Markdown files into the working project. <br>
Mitigation: Run persistence only in the intended project directory and review file diffs before adopting the generated design-system files. <br>


## Reference(s): <br>
- [Anti-Generic UI Review](references/anti-generic-review.md) <br>
- [Design System Teardown Checklist](references/design-system-teardown-checklist.md) <br>
- [Implementation Patterns](references/implementation-patterns.md) <br>
- [Product Archetypes](references/product-archetypes.md) <br>
- [Review Checklist](references/review-checklist.md) <br>
- [Style Cloning Playbook](references/style-cloning-playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, and plain text CLI output; optional persisted Markdown design-system files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local CSV-backed recommendations and can create design-system/MASTER.md plus page override files when persistence is requested.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
