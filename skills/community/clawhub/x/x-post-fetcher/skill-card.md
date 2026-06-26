## Description: <br>
Automates an isolated browser session to fetch and summarize publicly visible X posts from a specified user into a local Markdown report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hitjcl](https://clawhub.ai/user/hitjcl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to collect publicly visible posts from a specified X account and produce a local Markdown summary report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent-controlled browser access to X.com. <br>
Mitigation: Use the isolated browser session, log in manually in the browser window, and avoid sending X credentials through chat. <br>
Risk: Generated reports may include content that should not be shared broadly. <br>
Mitigation: Review the local Markdown report before sharing it and avoid using the skill for private or protected content. <br>
Risk: High-volume collection can create platform or account risk. <br>
Mitigation: Use the skill for limited collection tasks and avoid high-volume scraping. <br>


## Reference(s): <br>
- [X](https://x.com) <br>
- [ClawHub skill page](https://clawhub.ai/hitjcl/x-post-fetcher) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Tool commands, Guidance] <br>
**Output Format:** [Markdown report with browser automation tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes reports to the local workspace; relies on an isolated browser session and manual X login when needed.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
