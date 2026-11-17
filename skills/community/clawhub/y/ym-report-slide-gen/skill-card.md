## Description:

Lays weekly or monthly report data into presentation-ready HTML slides with a conclusion page and data tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyuming0823](https://clawhub.ai/user/liuyuming0823)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and team leads use this skill to turn structured weekly or monthly report Markdown into conclusion-first HTML slide decks for leader or all-hands updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the renderer can create or overwrite a local HTML output file.

Mitigation: Run it in the intended working directory and choose any --out path deliberately before execution.

Risk: The generated deck uses the user's source Markdown as the factual basis for report content.

Mitigation: Review the source Markdown and generated HTML before presenting, especially figures, metric definitions, and support requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuyuming0823/skills/ym-report-slide-gen)
- [Server-resolved source repository](https://github.com/liuyuming0823/ym-report-slide-gen)
- [Server-resolved source commit](https://github.com/liuyuming0823/ym-report-slide-gen/tree/9261087681d463048786bc2d0d82c14195021fec)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with Python commands and a generated standalone HTML slide deck]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates report-deck.html by default and may overwrite an existing file with the same output path.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
