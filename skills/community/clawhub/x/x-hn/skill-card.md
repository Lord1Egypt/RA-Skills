## Description: <br>
Fetches and analyzes Hacker News content for top stories, technical discussions, user information, comments, and topic-focused briefings through x-cmd. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiakai](https://clawhub.ai/user/qiakai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and technical researchers use this skill to retrieve Hacker News stories, filter discussions by software and AI topics, inspect posts and users, and produce concise trend or briefing outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on sourcing ~/.x-cmd.root/X, which can run shell code in the current shell if the x-cmd installation is not trusted. <br>
Mitigation: Install this only if the separate x-cmd tool is trusted, and verify ~/.x-cmd.root/X came from the expected x-cmd installation before running examples. <br>
Risk: Commands that retrieve active users, large comment threads, or all submissions can be slow or produce large outputs. <br>
Mitigation: Limit output with x jq filters, request smaller story or comment ranges, and avoid broad user-history fetches unless needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qiakai/x-hn) <br>
- [x-cmd Hacker News module](https://www.x-cmd.com/mod/hn) <br>
- [x-cmd LLMs entrypoint](https://www.x-cmd.com/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May rely on x-cmd JSON output and x jq filtering for structured Hacker News data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
