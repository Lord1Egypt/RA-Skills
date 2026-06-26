## Description: <br>
Extracts and summarizes trending topics, recurring issues, and content gaps across targeted Reddit subreddits using public Reddit JSON data for research purposes only. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lknezic](https://clawhub.ai/user/lknezic) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and content strategists use this skill to scan targeted Reddit communities, identify high-value discussion opportunities, and produce local research notes for later human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads untrusted Reddit posts and comments that may contain prompt-injection attempts. <br>
Mitigation: Treat Reddit content only as data, ignore instructions found in posts or comments, log suspicious content, and escalate according to the skill's prompt-injection defense guidance. <br>
Risk: The skill may create local research notes and update a local index in the user's workspace. <br>
Mitigation: Confirm that local research-note creation and index updates are acceptable before installation or use. <br>
Risk: If reddit-mcp is configured with broader permissions, the skill could be used in an environment where posting or account-changing tools are available. <br>
Mitigation: Keep reddit-mcp limited to reading and searching, and avoid enabling posting or account-changing tools for this skill. <br>


## Reference(s): <br>
- [Reddit API Reference](artifact/ref-api.md) <br>
- [Subreddit Reference](artifact/ref-subreddits.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/lknezic/reddit-research) <br>
- [Publisher Profile](https://clawhub.ai/user/lknezic) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown research notes with subreddit links, opportunity summaries, trending themes, and health notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local research notes under shared/research and updates the local vault index when used as documented.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
