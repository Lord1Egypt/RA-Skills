## Description: <br>
Reddit CLI using cookies for authentication. Read posts, search, and get subreddit info. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kelsia14](https://clawhub.ai/user/kelsia14) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to retrieve Reddit posts, search Reddit, inspect subreddit information, and check Reddit cookie authentication from a command-line workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to handle REDDIT_SESSION and TOKEN_V2 values that grant access to a Reddit browser session. <br>
Mitigation: Treat these values like passwords, avoid committing or sharing shell profiles that contain them, prefer temporary environment variables or a secret store, and rotate or log out of Reddit sessions if values may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kelsia14/reddit-cli) <br>
- [Reddit](https://reddit.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces read-only Reddit post, search, subreddit, and connection-check results using Reddit session cookie environment variables.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
