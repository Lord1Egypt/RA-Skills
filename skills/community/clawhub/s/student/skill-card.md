## Description:

Help with coursework. Use when taking notes, summarizing readings, formatting citations, outlining essays, or calculating GPA.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Students and learning-support agents use this skill to manage coursework notes, summarize readings, format citations, outline essays, run study timers, and calculate GPA.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The note command may write outside the intended notes directory when given a crafted subject name.

Mitigation: Use only non-sensitive coursework files and avoid subjects with slashes, dot-dot path components, or symlinked folders until note path handling is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/student)
- [Publisher profile](https://clawhub.ai/user/ckchzh)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Plain text to stdout and Markdown note files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Notes are stored under ~/.student/notes/<subject>/.]

## Skill Version(s):

3.4.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
