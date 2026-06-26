## Description: <br>
Automate X (Twitter) through Chromium CDP to post tweets, reply, quote-retweet, and publish articles using an existing browser login without API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stwith](https://clawhub.ai/user/stwith) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to prepare and publish X posts, replies, quote tweets, and X Premium articles through a logged-in browser session. It is suited to account-level automation workflows where users can review content before live posting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish from a real logged-in X account. <br>
Mitigation: Review the exact text and target URL before every live post and use dry-run mode before sending. <br>
Risk: The skill sets up a persistent browser session controlled through a local CDP port. <br>
Mitigation: Use a dedicated Chromium profile, preferably a dedicated X account, keep the debug port local, and close the CDP-enabled browser when finished. <br>
Risk: The setup flow may install or rely on runtime dependencies for browser automation. <br>
Mitigation: Manually pin or install dependencies when possible and install only if comfortable letting an agent operate the browser session. <br>


## Reference(s): <br>
- [X DOM Selectors Reference](references/selectors.md) <br>
- [X CDP Automation on ClawHub](https://clawhub.ai/stwith/x-cdp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and command results from the automation scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts can run in dry-run mode to compose content and save a screenshot before posting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
