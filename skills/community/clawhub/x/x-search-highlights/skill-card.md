## Description: <br>
Search and extract high-value posts from X (Twitter) with engagement-based ranking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ghostwritten](https://clawhub.ai/user/ghostwritten) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search X/Twitter for a topic, collect visible posts from a logged-in browser session, and rank them by engagement for research or content curation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses the user's logged-in X.com browser profile to read visible search-result pages. <br>
Mitigation: Use a dedicated low-privilege browser profile and review searches before execution. <br>
Risk: Large or repeated searches may encounter X rate limits or terms-of-service concerns. <br>
Mitigation: Keep search volume modest and reduce scroll iterations when rate-limit behavior appears. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ghostwritten/x-search-highlights) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON search highlights with engagement metrics and source links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output is ranked by likes, retweets, and views from visible X search-result posts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
