## Description:

Converts film or video scripts into structured storyboard tables with shot numbers, shot type and camera angle, visual content, characters, scene, and sound.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eita19](https://clawhub.ai/user/eita19)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, video teams, and developers use this skill to convert screenplay text into storyboard planning artifacts and CSV-ready shot lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated CSV cells may contain formula-like text that spreadsheet tools interpret when opened.

Mitigation: Treat screenplay input as untrusted and review or sanitize CSV contents before opening them in spreadsheet applications.

Risk: The bundled examples may need review for respectful cultural representation in some workflows.

Mitigation: Review and revise example content before using it as a creative or production reference.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eita19/skills/script-to-storyboard)
- [Example screenplay](references/示例剧本.md)
- [Example storyboard](references/示例分镜.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown storyboard table, console text, and CSV file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The converter writes UTF-8 CSV with a byte order mark for spreadsheet compatibility.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
