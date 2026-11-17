## Description:

TaoHtml helps agents turn Word, PDF, PPT, HTML, or idea-only inputs into polished offline 16:9 HTML reports and presentations with visual-system selection, runtime controls, QA, and delivery checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taogeo](https://clawhub.ai/user/taogeo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content teams, and report authors use TaoHtml to create or revise browser-deliverable reports and presentation decks from source files or incomplete ideas. It supports guided intake, visual-system selection, static-reference or corporate-template handling, runtime presentation controls, local QA, and packaged offline delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses browser automation and local file handling to build and test HTML report outputs.

Mitigation: Install and run it in an isolated virtual environment or container and review generated workspace files before reuse or distribution.

Risk: Python and browser dependencies create supply-chain and reproducibility considerations.

Mitigation: Use reviewed pinned dependencies where reproducibility requirements are stronger, and run the bundled preflight checks before gated work.

Risk: Optional corporate-template profiles can persist brand materials outside the project workspace under TAOHTML_HOME or ~/.taohtml.

Mitigation: Review, archive, export, or delete persisted profiles when they contain brand materials that should no longer be reused.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/taogeo/skills/taohtml)
- [Publisher profile](https://clawhub.ai/user/taogeo)
- [Project homepage](https://github.com/TaoGEO/TaoHtml)
- [Agent workflow](artifact/references/agent-workflow.md)
- [Runtime contract](artifact/references/runtime-contract.md)
- [Environment preflight](artifact/references/environment-preflight.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated HTML, JSON, CSS, Python, and shell-command artifacts when the workflow calls for them]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local offline report assets and QA evidence; may write workspace files and optional corporate-template profiles under TAOHTML_HOME or ~/.taohtml.]

## Skill Version(s):

0.6.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
