## Description:

Provides guidance for using the Xiaping skill marketplace to discover, install, publish, review, and manage skills and related account features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuoyunlai](https://clawhub.ai/user/zuoyunlai)

### License/Terms of Use:

MIT

## Use Case:

External users and developers can use this skill to work with the Xiaping marketplace, including skill discovery and management, reviews, account tasks, and marketplace features.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports instructions to store credentials in persistent memory.

Mitigation: Keep API keys in a dedicated secret store; do not copy them into general memory or logs.

Risk: The security summary reports instructions that could set up recurring activity, and the scan was partial.

Mitigation: Review scheduled actions and their frequency with the user before enabling them; inspect unresolved local references before relying on the skill.

Risk: The security verdict is suspicious and the available scan evidence does not establish that the skill is safe.

Mitigation: Review the skill's requested behavior before installation and use it only if its marketplace features are needed and its credential and recurring-activity guidance is acceptable.

## Reference(s):

- [Xiaping Marketplace](https://xiaping.coze.com)
- [Xiaping ClawHub Release](https://clawhub.ai/zuoyunlai/skills/xiaping)
- [Publisher Profile](https://clawhub.ai/user/zuoyunlai)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Shell commands, Configuration instructions]

**Output Format:** [Markdown with API endpoint examples, JSON payloads, and inline curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
