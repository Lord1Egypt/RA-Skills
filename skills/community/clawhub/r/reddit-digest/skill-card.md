## Description: <br>
Fetches popular posts from a specified subreddit from the last 24 hours, retrieves post details and comments, and generates a concise Chinese Markdown digest with summaries, key points, practical suggestions, inspirations, and social media copy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redisread](https://clawhub.ai/user/redisread) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content analysts use this skill to turn a target subreddit's recent popular discussion into a daily Markdown brief for review, ideation, and social media drafting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public Reddit content through autocli and writes digest artifacts locally. <br>
Mitigation: Set REDDIT_DIGEST_BASE_DIR to a workspace-owned folder, review the target subreddit before running, and inspect retained temporary JSON plus Markdown outputs. <br>
Risk: Collected post details or comments may be incomplete when fetching fails. <br>
Mitigation: Review per-post error fields in the temporary JSON files and treat summaries based only on metadata as lower confidence. <br>


## Reference(s): <br>
- [Reddit Digest Skill Page](https://clawhub.ai/redisread/reddit-digest) <br>
- [Output Template](references/output-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown document with front matter, per-post summaries, key points, practical suggestions, inspirations, and social media copy] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes temporary JSON files and a final daily Markdown digest under the configured base directory.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
