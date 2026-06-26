## Description: <br>
Post tweets, threads, replies, and quote-tweets to X (Twitter) via API v2 with OAuth 1.0a. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[3rdbrain](https://clawhub.ai/user/3rdbrain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to operate a connected X account from a Node.js CLI, including posting tweets and threads, replying, quote-tweeting, liking, deleting tweets, and reading a recent timeline. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify public content on the connected X account, including posting, liking, and deleting tweets. <br>
Mitigation: Use the least-privileged X app or token available and require human approval for posts, likes, and deletions. <br>
Risk: Scheduling instructions may be unreliable without a separately reviewed scheduler. <br>
Mitigation: Treat scheduled-post behavior as unavailable unless the scheduler is reviewed and tested in the deployment environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/3rdbrain/x-leads-api) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown instructions with inline shell commands; executed CLI commands return JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires X OAuth environment variables for the connected account.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
