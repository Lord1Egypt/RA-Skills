## Description:

Generate AI music with Udio via API wrappers or browser automation, with prompt engineering and song extensions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers, creators, and agents use this skill to create Udio music workflows: craft prompts and lyrics, use community API wrappers when authorized, automate the Udio browser UI, extend tracks, and track local project history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to extract a live Udio browser session token for unofficial community wrappers.

Mitigation: Prefer prompt-only or browser-only use when automation is not required; if wrappers are used, store the token only in a credential manager or environment variable and never in plain text project files.

Risk: Unofficial wrapper packages may change behavior or handle account tokens unexpectedly.

Mitigation: Review and pin wrapper versions before installation, and run wrapper-based workflows in an isolated environment.

Risk: Prompts, lyrics, and creative project details are sent to Udio when generation workflows are used.

Mitigation: Use Udio only for creative content the user is comfortable sending to that service, and avoid retaining sensitive project details unless local history is desired.

## Reference(s):

- [ClawHub Udio skill page](https://clawhub.ai/ivangdavila/skills/udio)
- [Udio website](https://www.udio.com)
- [Udio create page](https://www.udio.com/create)
- [Python UdioWrapper repository](https://github.com/flowese/UdioWrapper.git)
- [TypeScript udio-wrapper repository](https://github.com/josephgodwinkimani/udio-wrapper)
- [Clawic Udio homepage](https://clawic.com/skills/udio)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline code, shell commands, browser actions, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local notes under ~/udio/ and save downloaded audio files when the user chooses generation workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
