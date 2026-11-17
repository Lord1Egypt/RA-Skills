## Description:

Searches for community Mini Program AI Skills, helps users review matching options, and installs selected skills into existing Mini Program projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binggg](https://clawhub.ai/user/binggg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill when adding AI capabilities to an existing Mini Program project and need help finding, comparing, and installing community skills instead of building one from scratch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned remote npm commands can install community code.

Mitigation: Use a pinned, trusted mp-skills version and inspect selected remote skill content before installation.

Risk: Setup can change project files, cloud functions, databases, and environment configuration.

Mitigation: Run setup only in a version-controlled project with minimal cloud permissions.

Risk: Installing all available skills can add more code than intended.

Mitigation: Avoid add --all unless the user intentionally wants every available skill installed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/binggg/skills/wxa-find-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in installed skill directories and app.json registration entries when the recommended commands are executed.]

## Skill Version(s):

0.2.0 (source: server release evidence; artifact metadata reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
