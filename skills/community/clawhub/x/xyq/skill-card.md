## Description:

xyq helps agents create or edit images and videos through Pippit or Xiaoyunque workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imaoda](https://clawhub.ai/user/imaoda)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit image or video creation requests, continue prior generation threads, and retrieve generated asset links from Pippit or Xiaoyunque.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser session cookies may be exposed through chat logs, workspace files, or the plaintext config file.

Mitigation: Use a scoped authentication flow or secure secret store, avoid pasting browser session cookies into chat, and restrict access to any local config file.

Risk: The skill can act as the user's logged-in Pippit or Xiaoyunque account and consume account resources.

Mitigation: Review requested actions before execution, use accounts with limited privileges where possible, and monitor account activity after installation.

Risk: The bundled helper script is reported as vulnerable to local code execution from crafted input.

Mitigation: Review and fix the helper script before normal use, especially before passing untrusted prompt or thread values to it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/imaoda/skills/xyq)
- [Pippit](https://www.pippit.ai/home)
- [Xiaoyunque](https://xyq.jianying.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with generated JSON request bodies and asset links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update xyq.config.json and may provide generated image or video download links.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
