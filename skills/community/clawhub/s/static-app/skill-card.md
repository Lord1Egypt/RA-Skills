## Description:

Deploy static websites to Static.app hosting and manage hosted Static.app sites from an agent workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akellacom](https://clawhub.ai/user/akellacom)

### License/Terms of Use:


## Use Case:

Developers and website maintainers use this skill to deploy static HTML, CSS, JavaScript, and built frontend assets to Static.app. It also supports listing sites, listing site files, downloading site archives for editing, and deleting hosted sites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Static.app API key can authorize listing, updating, downloading, and deleting sites.

Mitigation: Install only for trusted workflows and prefer the STATIC_APP_API_KEY environment variable over command-line API key flags.

Risk: The delete command can remove hosted sites, and forced deletion skips confirmation.

Mitigation: Avoid --force unless the target PID has been independently verified.

Risk: Downloaded archives and output paths may contain sensitive site content.

Mitigation: Treat downloaded files and extraction paths as sensitive until dependency and path-validation issues are fixed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/akellacom/skills/static-app)
- [Static.app](https://static.app)
- [Static.app API key page](https://static.app/account/api)
- [Static.app sites API](https://api.static.app/v1/sites)
- [Static.app zip deploy API](https://api.static.app/v1/sites/zip)
- [Static.app download API](https://api.static.app/v1/sites/download/{pid})

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, files]

**Output Format:** [Markdown guidance, shell commands, plain text command output, optional JSON responses, and downloaded site files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create deployment archives, return Static.app URLs and PIDs, and extract downloaded site archives into workspace paths.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
