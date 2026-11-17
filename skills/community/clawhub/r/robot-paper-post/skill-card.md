## Description:

Creates Chinese technical posts from robotics and embodied AI papers, including source research, method analysis, experiment summaries, and reproducible arXiv or project-page figure insertion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jessy-huang](https://clawhub.ai/user/jessy-huang)

### License/Terms of Use:

MIT-0

## Use Case:

External authors, researchers, and technical communicators use this skill to turn robotics or embodied AI paper titles, arXiv IDs, project pages, or paper links into publication-ready Chinese technical articles with matched figures, captions, and resource links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The article template can add an unsolicited Mbot promotional footer to publication-ready output.

Mitigation: Review generated drafts and remove or replace the footer before public use.

Risk: The README recommends installing with clawhub@latest, which can make installs depend on the current installer release.

Mitigation: Use a pinned, trusted ClawHub installer version when repeatability matters.

Risk: The docs reference an optional local image-download script that is not included in this artifact.

Mitigation: Prefer direct arXiv figure URLs, or add and review the script before promising local image downloads.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jessy-huang/skills/robot-paper-post)
- [ClawHub Package URL](https://clawhub.ai/jessy-huang/robot-paper-post)
- [Project Homepage](https://github.com/Jessy-Huang/robot-paper-post)
- [Post Template](assets/post-template.md)
- [Paper Structure Reference](references/paper-structure.md)
- [Technology Terms Glossary](references/tech-terms-glossary.md)
- [Research Teams Reference](references/research-teams.md)
- [Classic Papers Reference](references/classic-papers.md)
- [Image Insertion Workflow](references/image-insertion-workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown article drafts with figure links, captions, resource lists, and optional shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include 3 to 5 selected figures, local or remote image references, and a note when code is not yet public.]

## Skill Version(s):

1.3.1 (source: server release evidence, artifact metadata, clawhub.json, README changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
