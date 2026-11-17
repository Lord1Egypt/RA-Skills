## Description:

知乎热榜选题 helps content creators fetch Zhihu hot topics and rank question opportunities from public hot-list data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and agent users use this skill to discover current Zhihu hot-list topics, score candidate questions, and choose topics with stronger publishing opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the skill contacts Zhihu over the network and may expose normal request metadata such as IP address and User-Agent to Zhihu.

Mitigation: Run it only when network access to Zhihu is acceptable for the environment, and review the request behavior before deployment.

Risk: The skill depends on Python requests, and the release does not include pinned dependency requirements.

Mitigation: Install dependencies in a virtual environment and prefer pinned requirements if the publisher adds them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/zhihu-topic-finder)
- [Publisher profile](https://clawhub.ai/user/freedompixels)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON-like topic analysis output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches public Zhihu hot-list data and prints ranked topic results locally.]

## Skill Version(s):

1.2.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
