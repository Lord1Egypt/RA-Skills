## Description: <br>
Query Weibo public data, including hot searches, search results, user profiles, feeds, followers, post details, and comments through the Weibo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Marvae](https://clawhub.ai/user/Marvae) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill when they need an agent to propose Weibo CLI commands for public Weibo trend, search, user, feed, follower, post, and comment lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An optional WEIBO_COOKIE can represent a logged-in Weibo session and is sensitive. <br>
Mitigation: Use the skill without WEIBO_COOKIE when possible, and provide a cookie only when the user understands the session exposure. <br>
Risk: The skill depends on a third-party npm package to run Weibo lookups. <br>
Mitigation: Prefer the local npm install path over global installation and review the referenced package before trusting it. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON parsing examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated CLI guidance should prefer --json for structured output and avoid WEIBO_COOKIE unless the user explicitly needs authenticated rate limits.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
