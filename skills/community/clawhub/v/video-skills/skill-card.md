## Description:

Finds a suitable workflow for AI video, image, voice, or music requests and presents options before generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vargai](https://clawhub.ai/user/vargai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to find a suitable workflow for a media request, compare visual options, and get next-step instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The search request sends the user's query to varg.ai.

Mitigation: Check for sensitive details before searching and omit or generalize them.

Risk: Suggested workflow steps may install additional skills from unpinned sources.

Mitigation: Review the selected skill and pin a known revision before installing it in a production environment.

Risk: The full workflow recommends backing up project content to GitHub.

Mitigation: Use a private repository and exclude confidential media and credentials from backups.

## Reference(s):

- [varg how to](https://varg.ai/how-to)
- [ClawHub video-skills release](https://clawhub.ai/vargai/skills/video-skills)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown with links and inline installation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Workflow recommendations and visual options; does not generate media itself.]

## Skill Version(s):

1.0.20 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
