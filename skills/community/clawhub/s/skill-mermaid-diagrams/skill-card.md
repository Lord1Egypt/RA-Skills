## Description:

Generates consistent, template-based Mermaid diagrams for technical content across 12 diagram types, with template selection, content generation, syntax validation, and error handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chunhualiao](https://clawhub.ai/user/chunhualiao)

### License/Terms of Use:

MIT

## Use Case:

Developers and technical writers use this skill to create Mermaid-based architecture diagrams, flowcharts, sequences, timelines, comparisons, UML class diagrams, state machines, and related documentation visuals. It supports both subagent and manual workflows that generate diagram content, render files, and validate outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted file paths may cause local scripts to run unintended commands.

Mitigation: Install only after command-injection issues are fixed with non-shell process calls and argument arrays; do not run generator or validator on paths, directories, or filenames influenced by someone else.

Risk: Global Mermaid CLI installation and sudo-based npm guidance can increase installation risk.

Mitigation: Prefer a pinned local Mermaid CLI dependency and avoid sudo-based npm installation.

## Reference(s):

- [Mermaid Syntax Guide](references/mermaid-syntax.md)
- [Example Content](assets/example-content.json)
- [Mermaid Docs](https://mermaid.js.org/)
- [Mermaid Syntax Reference](https://mermaid.js.org/intro/syntax-reference.html)
- [Mermaid Theming Guide](https://mermaid.js.org/config/theming.html)
- [Mermaid CLI Documentation](https://github.com/mermaid-js/mermaid-cli)
- [Mermaid Live Editor](https://mermaid.live/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON content examples, Mermaid source, and generated SVG/PNG diagram files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated diagram directories may include .mmd source, .svg vector output, .png raster output, and summary.json metadata.]

## Skill Version(s):

1.0.0 (source: package.json and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
