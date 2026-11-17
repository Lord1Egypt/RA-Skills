## Description:

Removes and identifies AI watermarks and provenance marks in images, video, and text the user generated or edited.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wiltodelta](https://clawhub.ai/user/wiltodelta)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to inspect user-owned images, video, and text for AI watermarks or provenance signals, then choose documented identification or removal commands. It is intended for content the user created, edited, or is authorized to change.

### Deployment Geography for Use:

Global, subject to local restrictions; the skill states that label removal and removal tools are prohibited in mainland China.

## Known Risks and Mitigations:

Risk: Removing local watermarks or provenance signals can alter files and may be mistaken for proof that content is human-made.

Mitigation: Work only on content the user is authorized to change, preserve the original by writing to an explicit output path, and report that removal does not establish authorship or erase server-side history.

Risk: A missing detection may be misread as proof that a file is clean or has a known origin.

Mitigation: Report only the command result and its caveats; describe an absent local signal as unknown rather than as proof of origin.

## Reference(s):

- [Commands reference](references/commands.md)
- [Installation guide](references/install.md)
- [Project homepage](https://raiw.cc)
- [Python API guide](https://github.com/wiltodelta/remove-ai-watermarks/blob/main/docs/python-api.md)
- [ClawHub skill page](https://clawhub.ai/wiltodelta/skills/remove-ai-watermarks)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance, shell commands, and processed image, video, or text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output depends on the selected command and input; commands use an explicit output path by default and preserve the source file.]

## Skill Version(s):

1.0.20 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
