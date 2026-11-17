## Description:

Use this skill when an agent needs fresh web results with no API key required across web, video, and social search providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lexiforest](https://clawhub.ai/user/lexiforest)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to perform live web, video, and social searches through seekit, choose an appropriate provider, and consume structured search results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The seekit dependency is installed from a package source without a pinned version in the skill instructions.

Mitigation: Install seekit in a virtual environment or sandbox and pin a reviewed version before operational use.

Risk: Search queries are sent to the selected external provider.

Mitigation: Avoid submitting sensitive data in queries and choose providers that match the deployment's privacy and compliance requirements.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python examples, and JSON result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search result quality and availability depend on the selected provider.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
