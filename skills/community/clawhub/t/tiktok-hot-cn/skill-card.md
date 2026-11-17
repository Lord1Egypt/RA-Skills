## Description:

Automatically fetches the Douyin hot-search Top 50 list with heat values.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangjinghua0127](https://clawhub.ai/user/yangjinghua0127)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to retrieve the latest Douyin hot-search topics, formatted with rankings and heat values, and save a local JSON copy for later use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the skill makes a network request to Douyin using browser-like headers.

Mitigation: Review network access expectations before installation and run only in environments where outbound requests to Douyin are acceptable.

Risk: The skill writes the latest results to workspace/scripts/douyin-hot-clean.json and replaces any prior file at that path.

Mitigation: Back up or redirect the output file when prior saved results must be retained.

## Reference(s):

- [Douyin Hot](https://www.douyin.com/hot/)
- [ClawHub skill page](https://clawhub.ai/yangjinghua0127/skills/tiktok-hot-cn)

## Skill Output:

**Output Type(s):** [text, json, files]

**Output Format:** [Console text and structured JSON file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and network access; writes results to workspace/scripts/douyin-hot-clean.json.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
