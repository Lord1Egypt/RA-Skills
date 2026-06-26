## Description: <br>
Connects Playwright to a user's logged-in Chrome browser session over CDP to compose and publish posts on X. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1067873313](https://clawhub.ai/user/1067873313) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to post user-provided content to X from a Chrome profile that the user has already authenticated. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires broad control of a logged-in Chrome session through a local CDP endpoint. <br>
Mitigation: Use a dedicated Chrome profile or disposable X account, review post_tweet.js before installation, and close the remote-debugging port when finished. <br>
Risk: The skill can publish to X without a final in-browser confirmation. <br>
Mitigation: Require explicit user confirmation of the exact post content before running the skill, and avoid running it without an explicit tweet argument. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1067873313/x-twitter-poster) <br>
- [Publisher profile](https://clawhub.ai/user/1067873313) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, browser actions] <br>
**Output Format:** [JavaScript function result object with console logs and setup instructions in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an already logged-in Chrome session with a local CDP endpoint.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata; artifact/package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
