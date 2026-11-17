## Description:

微信公众号排版引擎 converts Markdown articles into WeChat Official Account-compatible inline-styled HTML and can extract matching visual theme component libraries from WeChat articles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qomob](https://clawhub.ai/user/qomob)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, editors, and developers use this skill to convert Markdown or normalized article drafts into WeChat Official Account HTML, extract visual styles from public WeChat articles, and maintain reusable theme libraries with validation scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Formatted articles include Qomob.AI attribution by default.

Mitigation: Confirm the attribution is acceptable for the publication context, or review and modify the footer policy before using generated articles.

Risk: Theme generation can persistently change trusted theme files and may overwrite built-in theme names.

Mitigation: Use unique output names, avoid built-in theme identifiers such as emerald, graphite, sunset, ocean, and rose, and review file diffs before deployment.

Risk: The extraction workflow may process untrusted PDFs, images, HTML files, or public article URLs.

Mitigation: Use trusted inputs where possible, scan uploaded materials, and review generated theme files before allowing agents to use them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qomob/skills/wechatlayout)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [Mode A: WeChat Formatting](artifact/references/mode-a-format.md)
- [Mode B: Style Extraction](artifact/references/mode-b-extract.md)
- [Theme Index](artifact/references/theme-index.md)
- [Common Components](artifact/references/common-components.md)
- [Paste Test Checklist](artifact/references/paste-test-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated HTML snippets, theme Markdown files, validation commands, and configuration updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mode A outputs WeChat-compatible section HTML and preview files; style extraction can generate persistent theme files under references/.]

## Skill Version(s):

1.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
