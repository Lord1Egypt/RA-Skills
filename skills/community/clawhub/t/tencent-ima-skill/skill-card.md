## Description:

Control the IMA (ima.copilot) desktop application for AI search and private knowledge retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hyddd](https://clawhub.ai/user/hyddd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users on macOS use this skill to let an agent search Tencent IMA and optionally retrieve results from a configured private knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill opens and controls a local IMA debugging session and can rewrite private knowledge-base requests.

Mitigation: Install only from a trusted publisher, use a pinned dependency in a virtual environment, and close IMA after use.

Risk: Private mode sends a configured knowledge ID and returns extracted private knowledge-base text to the agent.

Mitigation: Avoid sensitive private knowledge bases until the CDP exposure and confirmation model are tightened.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hyddd/skills/tencent-ima-skill)
- [Clawdbot project](https://github.com/clawdbot/clawdbot)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Plain text search results with command-line status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the IMA desktop app, Python 3, websocket-client, and a configured knowledge ID for private knowledge-base searches.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
