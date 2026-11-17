## Description:

Search Google for LinkedIn in Chrome and identify the official LinkedIn log in or sign up result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luckill](https://clawhub.ai/user/luckill)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to perform a Chrome-based Google search for LinkedIn and locate the official linkedin.com log in or sign up result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on Chrome, Google search availability, and current search-result presentation.

Mitigation: Confirm the query is loaded on Google results and verify that the located result is on linkedin.com before treating it as official.

Risk: The evidence notes minor source-metadata and documentation cleanup concerns.

Mitigation: Review the skill metadata before deployment and remove embedded local source paths from published artifacts when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luckill/skills/search-google-for-linkedin-and-locate-the-offici-61f2c70c)
- [Workflow documentation](WORKFLOW.md)
- [Executable workflow graph](workflow.json)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Markdown guidance for browser actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces a located official LinkedIn result on a Google results page; it does not require sign-in.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
