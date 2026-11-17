## Description:

Publishes a WeChat Official Account draft to followers by submitting its media_id.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaoyang78](https://clawhub.ai/user/chaoyang78)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill when they need an agent to submit a WeChat Official Account draft for final publication after confirming the correct media_id and access token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A successful run submits a final WeChat public-account publication to followers.

Mitigation: Run the skill only after the user explicitly confirms that final publication is intended and verifies the target media_id.

Risk: The WeChat access token is required to publish and could authorize unintended posting if mishandled.

Mitigation: Keep WECHAT_ACCESS_TOKEN scoped, protected, and available only in the execution environment where publication is intended.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a media_id argument and the WECHAT_ACCESS_TOKEN environment variable; successful execution submits the publication request to WeChat.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
