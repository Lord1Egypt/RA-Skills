## Description: <br>
X Interact helps agents search X.com (Twitter) content, inspect linked URLs, and monitor accounts or topics through Tavily web search and extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0x-wzw](https://clawhub.ai/user/0x-wzw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to research X.com (Twitter) posts, accounts, topics, and linked articles through Tavily and mcporter when direct X.com extraction is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tavily API keys can be exposed if real keys are pasted into shared terminals, chats, screenshots, or logs. <br>
Mitigation: Use a dedicated Tavily API key, avoid sharing command lines that contain real keys, and rotate the key if it is exposed. <br>
Risk: Search queries and extracted URLs may contain sensitive information that is sent to Tavily. <br>
Mitigation: Avoid submitting sensitive private queries or URLs unless that disclosure is acceptable for the use case. <br>
Risk: X.com direct extraction is blocked, so search-index results may be incomplete, stale, or missing context. <br>
Mitigation: Verify important findings against accessible source material and use linked-article extraction for supporting context. <br>


## Reference(s): <br>
- [X Interact ClawHub Page](https://clawhub.ai/0x-wzw/x-interact) <br>
- [Tavily](https://tavily.io) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Tavily API key and mcporter; Tavily service limits may apply.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
