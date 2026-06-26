## Description: <br>
Anonymously fetches the live Weibo hot search list without a Weibo login and saves the results as a Markdown file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kazeMace](https://clawhub.ai/user/kazeMace) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to collect the current Weibo hot search ranking into a Markdown table for reporting, monitoring, or analysis without providing account credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs the agent to terminate Chrome or Edge debugging processes without asking, which can disrupt unrelated browser sessions. <br>
Mitigation: Prompt before terminating browser processes, use an isolated browser profile and random available debug port, and only clean up processes started by the skill. <br>
Risk: The referenced scripts/weibo-hot-search.ts file is not present in the artifact evidence. <br>
Mitigation: Verify that the script is supplied and reviewed before expecting the skill to run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kazeMace/weibo-hot-search) <br>
- [Weibo hot search page](https://weibo.com/newlogin?tabtype=search) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown file containing a timestamped table of Weibo hot search entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports an optional output path and browser profile directory; requires bun or npx and a Chrome, Chromium, or Edge browser.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
