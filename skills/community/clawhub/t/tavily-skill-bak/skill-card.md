## Description: <br>
Uses the Tavily API for real-time web search and content extraction when an agent needs current information from the web. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aysun168](https://clawhub.ai/user/aysun168) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Tavily-backed searches for current news, research, and web content extraction. It is intended for cases where up-to-date information is needed and a Tavily API key is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a Tavily API key and includes guidance that could expose the key. <br>
Mitigation: Use masked or presence-only checks, keep configuration files containing the key private, and avoid sending secrets, personal data, or confidential business topics as search queries. <br>


## Reference(s): <br>
- [Tavily](https://tavily.com) <br>
- [ClawHub skill page](https://clawhub.ai/aysun168/tavily-skill-bak) <br>
- [Publisher profile](https://clawhub.ai/user/aysun168) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and a Tavily API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
