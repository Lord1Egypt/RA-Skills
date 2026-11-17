## Description:

Daily hot AI opinion generator that drafts a 150-200 word take on one rotating AI topic in Sol's direct, wry voice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amrree](https://clawhub.ai/user/amrree)

### License/Terms of Use:

MIT-0

## Use Case:

External users and site maintainers use this skill to generate short daily AI opinion posts and publish them to a Jekyll site.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended scheduling and GitHub pushes can publish generated public site content without review.

Mitigation: Make scheduling and automatic push explicitly opt-in, review generated posts before publication, and use a dedicated branch or token with minimal permissions.

Risk: The artifact does not show tight scoping around which files are staged and pushed.

Mitigation: Confirm the workflow stages only the intended Jekyll post path before enabling automatic commits.

Risk: The skill requires a MiniMax API key and a specific local site repository path.

Mitigation: Store the API key in the documented secrets path and verify the target repository path before running the publishing workflow.

## Reference(s):

- [Sol Take on ClawHub](https://clawhub.ai/amrree/skills/sol-take)
- [Publisher profile: amrree](https://clawhub.ai/user/amrree)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [Markdown Jekyll post with generated prose and a Git commit/push workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a 150-200 word opinion post on one rotating AI topic per day.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
