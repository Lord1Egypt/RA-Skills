## Description: <br>
Fetches current GitHub Trending repositories by daily, weekly, or monthly star gains, with optional language filtering and text or JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[callmegod66](https://clawhub.ai/user/callmegod66) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to see currently popular GitHub repositories, compare daily, weekly, or monthly trends, and filter results by programming language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public GitHub pages over the network. <br>
Mitigation: Run it only in environments where outbound access to GitHub is allowed. <br>
Risk: Repository names and descriptions are external web content. <br>
Mitigation: Treat returned repository text as informational data, not instructions for the agent to follow. <br>
Risk: Results depend on GitHub Trending HTML and may be empty or stale if the page structure changes or the request times out. <br>
Mitigation: Retry, use JSON output for downstream handling, and verify important results against GitHub before relying on them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/callmegod66/skill-github-trending) <br>
- [GitHub Trending](https://github.com/trending) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands] <br>
**Output Format:** [Plain text summary or JSON object emitted by a Python command.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports period, limit, language filter, and JSON flag; uses public GitHub Trending pages without credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
