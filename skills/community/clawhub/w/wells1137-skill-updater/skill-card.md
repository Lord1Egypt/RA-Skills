## Description:

Updates a specific skill within a repository and triggers the automated publishing pipeline for a single-skill release.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wells1137](https://clawhub.ai/user/wells1137)

### License/Terms of Use:


## Use Case:

Developers and skill maintainers use Skill Updater to collect release details for one modified skill and run the repository's release script to publish the update through an existing ClaWHub pipeline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger an external ClaWHub publish workflow by running a repository release script.

Mitigation: Before use, confirm the target repository, skill name, version, changelog, publishing destination, and behavior of the repository's scripts/release.sh.

## Reference(s):

- [Skill Updater on ClaWHub](https://clawhub.ai/wells1137/skills/wells1137-skill-updater)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Interactive prompts and shell command execution status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts for repository path, skill name, new version, and changelog before invoking the repository release script.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
