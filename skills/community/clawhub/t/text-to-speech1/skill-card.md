## Description:

Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gf1023456](https://clawhub.ai/user/gf1023456)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to search for installable skills, compare relevant results, and generate installation guidance when a requested capability may already exist in the skills ecosystem.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may suggest unpinned `npx skills` commands that resolve package code at execution time.

Mitigation: Verify the package source and version or commit before running installation commands.

Risk: The skill documents global installation with `-g -y`, which skips confirmation prompts.

Mitigation: Avoid global non-interactive installs by default; prefer reviewed, explicit installs when adding external skills.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gf1023456/skills/text-to-speech1)
- [Skills directory](https://skills.sh/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include skill names, installation commands, and links to skill listings.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
