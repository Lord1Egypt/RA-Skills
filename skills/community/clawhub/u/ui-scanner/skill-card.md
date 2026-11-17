## Description:

Crawl and analyze a website's visual design system from a given URL, identifying design style, color system, typography, component styles, and UI patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and product teams use this skill to extract a structured design specification from a public or authorized website for UI generation, restoration, style migration, or competitive design analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent fetches user-provided websites and may access pages that are private, sensitive, or unauthorized.

Mitigation: Use the skill only with public or authorized URLs.

Risk: The skill writes a local {domain}_design.md file, which may overwrite an existing design summary for the same domain.

Mitigation: Check for an existing output file before running the skill when preserving prior scans matters.

Risk: Some visual details, such as hover states or styles hidden behind heavy client-side rendering, may be estimated or incomplete.

Mitigation: Review estimated fields and inference notes before using the output as a design-system source.

## Reference(s):

- [Analysis Dimensions](references/analysis-dimensions.md)
- [Common Anti-Patterns](references/anti-patterns.md)
- [Extraction Methods](references/extraction-methods.md)
- [Output Template](references/output-template.md)
- [Quick Start](references/quick-start.md)
- [ClawHub Skill Page](https://clawhub.ai/openlark/skills/ui-scanner)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files, Configuration]

**Output Format:** [Markdown file with YAML frontmatter and structured design-system sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes results to a domain-specific design summary file named {domain}_design.md.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
