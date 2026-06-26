## Description: <br>
Unified web search skill. Fallback order: web_search with Brave, then DuckDuckGo, then claude.ai; search results are automatically cached under memory/research/. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mupengi-bot](https://clawhub.ai/user/mupengi-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to perform web research through Brave search, DuckDuckGo, or a Claude.ai browser fallback and preserve results for later reference. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Searches may be sent to Brave, DuckDuckGo, or a logged-in Claude.ai browser session. <br>
Mitigation: Avoid sensitive queries unless the destination service is acceptable, and force a specific search method when needed. <br>
Risk: Search results are automatically persisted under memory/research/. <br>
Mitigation: Review or delete cached research files periodically, and avoid caching confidential search content. <br>
Risk: The Claude.ai fallback can consume account message limits and may be affected by browser automation detection. <br>
Mitigation: Use Brave or DuckDuckGo for routine searches, and make the Claude.ai fallback opt-in or throttle its use in shared environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mupengi-bot/web-claude) <br>
- [Claude.ai new chat](https://claude.ai/new) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline tool calls and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save search queries, links, summaries, and extracted insights to memory/research/.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
