## Description: <br>
Search X/Twitter profiles, tweets, trends, and OAuth-gated posting through AIsa for research, monitoring, and engagement workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baofeng-tech](https://clawhub.ai/user/baofeng-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to research Twitter/X accounts, posts, trends, lists, communities, and Spaces, then prepare or publish approved posts through OAuth-gated workflows. It is suited for monitoring, engagement, and posting tasks that require an AISA_API_KEY. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports that the AISA API key can appear in normal command output. <br>
Mitigation: Use a dedicated, limited AISA_API_KEY, avoid running status, authorize, or post commands in logged environments until the raw-key output is fixed, and rotate the key if command output has already been captured. <br>
Risk: Tweet text and attached media leave the local machine for AIsa and X/Twitter during search and posting workflows. <br>
Mitigation: Review content and media before sending, avoid sensitive data, and use the skill only when external sharing through those services is acceptable. <br>
Risk: The skill can publish externally through OAuth-gated Twitter/X workflows. <br>
Mitigation: Require explicit user approval before posting and do not claim a post succeeded until the API confirms the publish result. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baofeng-tech/twitter-command-center-search-post) <br>
- [Twitter OAuth reference](references/post_twitter.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-like API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return authorization links, tweet IDs, tweet URLs, search results, and posting status; requires AISA_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
