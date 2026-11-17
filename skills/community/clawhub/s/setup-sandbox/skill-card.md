## Description:

Sets up the initial file system for a new Recoup sandbox by fetching organizations and artists via the Recoup CLI and scaffolding an opinionated org and artist folder structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sweetmantech](https://clawhub.ai/user/sweetmantech)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill after creating a Recoup sandbox to initialize organization and artist workspace folders and create persistent RECOUP.md identity files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad git staging and push commands can publish unintended repository changes.

Mitigation: Run only in the intended repository, inspect generated files and git status before committing, stage only intended orgs/.../RECOUP.md paths, and explicitly approve the remote and branch before pushing.

Risk: The follow-on setup-artist install command references an unpinned remote skill.

Mitigation: Install any follow-on skill only from a pinned or reviewed source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sweetmantech/skills/setup-sandbox)
- [Publisher profile](https://clawhub.ai/user/sweetmantech)

## Skill Output:

**Output Type(s):** [shell commands, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated RECOUP.md files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates orgs/{org}/artists/{artist-slug}/RECOUP.md marker files from Recoup CLI responses.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
