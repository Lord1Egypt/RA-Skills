## Description:

X Design routes visual design requests into workflows for slide decks, interactive UI prototypes, animation, design systems, and review passes, producing polished HTML-based visual deliverables and export guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qomob](https://clawhub.ai/user/qomob)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and content teams use this skill to turn vague visual requests into decks, landing pages, dashboards, animations, brand systems, review passes, and exportable HTML-based artifacts. It is most useful when an agent needs structured routing, design references, and quality checks for polished visual work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable install or remote-code guidance can resolve different code over time.

Mitigation: Install only from a reviewed immutable package or commit, and avoid following unpinned npx commands as written.

Risk: Generated HTML may include CDN scripts or browser integrations.

Mitigation: Review generated HTML and external script references before opening, publishing, or sharing artifacts.

Risk: The package documentation may overstate bundled resources or capabilities.

Mitigation: Confirm required templates, themes, layouts, and exporters are present in the reviewed package before relying on them.

Risk: The skill may create or edit local visual artifacts and use network access for brand assets.

Mitigation: Run it in a controlled workspace and verify that brand assets come from official or approved sources.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qomob/skills/xdesign)
- [Server-Resolved Source Repository](https://github.com/qomob/xdesign)
- [X Design Skill Definition](artifact/SKILL.md)
- [Agent Playbook](artifact/references/agent-playbook.md)
- [Workflow Guide](artifact/references/workflow-guide.md)
- [Mode 2 and Mode 3 Prototype Guide](artifact/references/mode-2-prototype.md)
- [Deck Studio Catalog](artifact/references/deck-studio-catalog.md)
- [Brand Asset Protocol](artifact/references/brand-asset-protocol.md)
- [Review Passes](artifact/references/review-passes.md)
- [Evaluation Scenarios](artifact/evals/evals.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with code blocks and generated HTML/CSS/JavaScript files; may include PPTX, PDF, PNG, or self-contained HTML export instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or edits local visual artifacts and may use network access for current product facts or official brand assets when requested.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
