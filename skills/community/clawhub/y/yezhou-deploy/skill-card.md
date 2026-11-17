## Description:

Publish an HTML file, project directory, or ZIP package to 页舟 and update an existing project while preserving its share URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gebangfeng](https://clawhub.ai/user/gebangfeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to publish or update web projects on 页舟 while keeping an existing public share URL when a project is already bound.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An environment-controlled endpoint override could direct a saved Yezhou credential and uploaded project contents to an unintended server.

Mitigation: Install only in trusted agent environments and confirm YEZHOU_BASE_URL is unset or points to the intended Yezhou service before publishing.

Risk: The local .yezhou.json manifest can expose internal project identifiers if committed or shared.

Mitigation: Review the manifest before sharing a project repository and decide explicitly whether it should be tracked or ignored.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gebangfeng/skills/yezhou-deploy)
- [Publisher profile](https://clawhub.ai/user/gebangfeng)
- [Artifact-declared official source](https://cnb.cool/gebangfeng/yezhou-deploy)
- [Yezhou service](https://yz.gbfeng.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise deployment guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the published or updated public URL when the deploy command succeeds.]

## Skill Version(s):

0.1.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
