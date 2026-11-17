## Description:

Builds chapter-navigated HTML training courseware with classroom quiz prompt pages for corporate instructors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyuming0823](https://clawhub.ai/user/liuyuming0823)

### License/Terms of Use:

MIT-0

## Use Case:

Corporate instructors use this skill to turn a structured course design table into a local, self-contained HTML training deck with chapter navigation, quiz pages, and review exercises. It is intended for live projection or self-study when the instructor provides the course topic, audience, duration, and knowledge-point list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated output may overwrite an existing courseware.html file in the current directory.

Mitigation: Run the skill in a working directory where courseware.html can be replaced, or rename/back up any existing file before generation.

Risk: Generated training content can become misleading if the source knowledge-point list is incomplete or incorrect.

Mitigation: Have the instructor review the generated HTML against the supplied course design table before live delivery or distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuyuming0823/skills/ym-training-courseware)
- [Server-resolved source repository](https://github.com/liuyuming0823/ym-training-courseware)
- [Adult training attention rhythm reference](artifact/references/teaching-rhythm.md)
- [Courseware planning template](artifact/templates/courseware-plan.md)

## Skill Output:

**Output Type(s):** [Code, Files, Markdown, Guidance]

**Output Format:** [Single self-contained HTML file with Markdown planning-table guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates courseware.html in the current directory and may overwrite an existing file with that name.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
