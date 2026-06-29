## Description: <br>
Crawl and analyze a website's visual design system from a given URL, identifying design style, color system, typography, component styles, and UI patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and designers use this skill to analyze a website URL and produce a design-system specification for UI generation, restoration, style migration, competitive design review, or reverse engineering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scanning websites where design analysis is not appropriate could create policy, permission, or compliance issues. <br>
Mitigation: Only scan websites where this kind of design analysis is appropriate and permitted. <br>
Risk: The generated local report filename may conflict with an existing similarly named file. <br>
Mitigation: Check the `{domain}_design.md` filename before running the skill and review the generated report before relying on it. <br>
Risk: Fetched HTML or CSS may be incomplete, especially for heavily client-rendered pages, causing estimated or partial design values. <br>
Mitigation: Treat inferred values as estimates, mark uncertain values, and review the design specification before using it for UI generation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openlark/skills/ui-scanner) <br>
- [Quick Start](references/quick-start.md) <br>
- [Output Template](references/output-template.md) <br>
- [Analysis Dimensions](references/analysis-dimensions.md) <br>
- [Extraction Methods](references/extraction-methods.md) <br>
- [Common Anti-Patterns](references/anti-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, guidance] <br>
**Output Format:** [Markdown file with YAML frontmatter and structured design analysis sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a local `{domain}_design.md` report for the scanned domain.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
