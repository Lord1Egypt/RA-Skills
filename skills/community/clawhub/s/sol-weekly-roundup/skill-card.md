## Description:

Weekly AI roundup that curates the 5 most significant AI stories from the week, written in Sol's voice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amrree](https://clawhub.ai/user/amrree)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content publishers use this skill to generate a weekly AI news roundup from recent Hacker News AI/ML stories, write contextual commentary with MiniMax, and create a Jekyll post for a configured site repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads a local MiniMax API key.

Mitigation: Run it only in an environment where that key is intended for this workflow, and use a scoped or replaceable credential.

Risk: The skill modifies a named Jekyll repository and may commit and push generated content without a separate review step.

Mitigation: Run against a controlled branch or staging repository, and require review or CI checks before publication.

Risk: The server security summary flags under-scoped permissions and limited user control for the scheduled publishing workflow.

Mitigation: Review the requested permissions and configured repository path before installation, and disable unattended scheduling unless it matches the intended release process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/amrree/skills/sol-weekly-roundup)
- [ClawHub publisher profile](https://clawhub.ai/user/amrree)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands]

**Output Format:** [Jekyll Markdown post and repository update actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates _posts/YYYY-MM-DD-ai-weekly-roundup.md and may commit and push generated content to GitHub.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
