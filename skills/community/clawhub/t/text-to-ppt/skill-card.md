## Description:

Convert any text input (research reports, summaries, proposals, plans, etc.) into a beautiful HTML-based presentation with Chart.js data visualization, Font Awesome icons, keyboard and touch navigation, and modern design themes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rendylong](https://clawhub.ai/user/rendylong)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers use this skill to turn pasted text, files, URLs, or Obsidian notes into polished single-file HTML slide decks. It is suited for reports, summaries, proposals, plans, and other content that benefits from structured slides and optional data visualization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes generated presentations to a fixed Obsidian vault path unless the destination is overridden.

Mitigation: Confirm or override the output path before use, especially on shared systems or when working with sensitive notes.

Risk: Generated presentations load third-party CDN resources for styling, charts, icons, and fonts.

Mitigation: Open decks only in environments where remote asset loading is acceptable, or vendor and pin dependencies before broader distribution.

Risk: Converting attacker-controlled web pages or sensitive notes into active HTML can expose users to unsafe or unintended content.

Mitigation: Use trusted inputs, review generated HTML before sharing, and avoid sensitive source material until destination confirmation, dependency pinning, and HTML sanitization are added.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rendylong/skills/text-to-ppt)
- [Design System](references/design-system.md)
- [Shell Template](references/shell-template.html)
- [Tailwind CSS CDN](https://cdn.tailwindcss.com)
- [Chart.js CDN](https://cdn.jsdelivr.net/npm/chart.js@4)
- [Chart.js DataLabels CDN](https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2)
- [Font Awesome CDN](https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css)
- [Google Fonts Inter](https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON planning output, HTML slide blocks, and a self-contained HTML presentation file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets 8-15 slides, caps generated decks at 20 slides, and saves the assembled presentation as a topic-slugged HTML file.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
