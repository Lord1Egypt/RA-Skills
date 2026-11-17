## Description:

Stitch Design Agent guides an agent to request Google Stitch designs with an OAuth token, retrieve generated UI code, and integrate it into an active application codebase.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duvancode](https://clawhub.ai/user/duvancode)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to turn a design prompt into generated UI code and integrate it into an existing React, NestJS, or similar project. It covers token setup, calling the Stitch API, saving generated components, wiring them into the app, and checking the build.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to use broad Google credentials and call a remote design-generation API.

Mitigation: Use a dedicated low-privilege Google credential, keep STITCH_TOKEN out of source code, and review token scope before use.

Risk: Remote-generated code and packages may be added to an active project without enough review controls.

Mitigation: Require the agent to show generated code, dependency changes, and diffs before writing or installing packages, and approve exact package versions manually.

Risk: Automatic component insertion can conflict with project architecture, design tokens, or build requirements.

Mitigation: Run type checks and linting, review the integration path, and adapt generated styling to the app's existing design system before merging.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duvancode/skills/stitch-design-agent)
- [Google OAuth 2.0 authorization endpoint](https://accounts.google.com/o/oauth2/v2/auth)
- [Google OAuth 2.0 token endpoint](https://oauth2.googleapis.com/token)
- [Google Cloud Platform OAuth scope](https://www.googleapis.com/auth/cloud-platform)
- [Google Stitch designs generation endpoint](https://stitch.googleapis.com/v1/designs:generate)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code, JSON, YAML, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses project files, a Google OAuth token from STITCH_TOKEN, and generated Stitch API responses to guide integration.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
