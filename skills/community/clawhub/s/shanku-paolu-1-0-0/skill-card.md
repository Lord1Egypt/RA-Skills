## Description:

Shanku Paolu is a browser-based file scanning and backup helper that guides users to open a local HTML scanner, select folders, review files, and download selected files as a ZIP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwei03804-a11y](https://clawhub.ai/user/wwei03804-a11y)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals or support agents use this skill to guide Windows or Mac users through scanning a local folder, selecting office documents or other files, and exporting selected files into a ZIP backup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can package selected local files into a ZIP, which may expose confidential, employer-owned, regulated, or otherwise unauthorized files.

Mitigation: Use it only on files the user owns or is explicitly authorized to copy, and review selected files before downloading or sharing the ZIP.

Risk: The HTML scanner loads third-party CDN scripts without integrity pinning.

Mitigation: Avoid use with confidential data unless dependencies are pinned or vendored and reviewed.

Risk: Unsafe filename rendering can make scanning attacker-supplied folders risky.

Mitigation: Avoid untrusted folders and fix filename rendering before use on attacker-controlled content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwei03804-a11y/skills/shanku-paolu-1-0-0)
- [Publisher profile](https://clawhub.ai/user/wwei03804-a11y)
- [Chart.js CDN dependency](https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js)
- [JSZip CDN dependency](https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js)
- [FileSaver.js CDN dependency](https://cdn.jsdelivr.net/npm/file-saver@2.0.5/dist/FileSaver.min.js)
- [Skill definition](artifact/SKILL.md)
- [HTML scanner asset](artifact/assets/scanner.html)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown or plain-text operating guidance for a local HTML scanner]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides users to open a local HTML file, select folders, review scanned files, and create a ZIP download; no shell commands or API calls are required.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
