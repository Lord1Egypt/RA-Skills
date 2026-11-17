## Description:

Generate and serve live HTML/CSS/JS UI designs from natural language prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wing8169](https://clawhub.ai/user/wing8169)

### License/Terms of Use:


## Use Case:

Developers and designers use this skill to prototype, build, review, iterate, and package live frontend pages from natural language requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privileged setup can make persistent Nginx changes and expose generated files over the network.

Mitigation: Review before installing; prefer an unprivileged local dev server or isolated environment. If setup.sh is used, bind to localhost, validate the port and serve directory, and remove the Nginx site when finished.

Risk: Generated frontend code and design guidance may be incorrect, inaccessible, or unsuitable for deployment without review.

Mitigation: Review generated pages before deployment, run desktop and mobile visual checks, and verify accessibility, security, and content requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wing8169/skills/ui-ux-dev)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline HTML, CSS, JavaScript, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create static page files, WebP assets, screenshots, and zipped project exports during the guided workflow.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
