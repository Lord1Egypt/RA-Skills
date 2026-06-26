## Description: <br>
AI-optimized web search via Tavily API. Returns concise, relevant results for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[litiao1224](https://clawhub.ai/user/litiao1224) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to run web searches, news searches, and URL content extraction through Tavily when they need concise source-backed web results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and supplied URLs are sent through external AISA/Tavily services. <br>
Mitigation: Do not use the skill for secrets, private internal URLs, or proprietary prompts unless that data sharing is approved; review returned content before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/litiao1224/tavily-search-litiao) <br>
- [Tavily homepage](https://tavily.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown] <br>
**Output Format:** [Markdown with an answer section, source links, snippets, or extracted page content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search result count is clamped to 1-20; news searches can be limited by recent days.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
