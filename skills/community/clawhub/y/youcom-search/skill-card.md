## Description: <br>
you.com web search, deep research, and content extraction for OpenClaw, with free basic search and paid research or extraction endpoints that send queries and URLs to you.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crabsticksalad](https://clawhub.ai/user/crabsticksalad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search the web, request you.com deep research with citations, and extract content from specific URLs when built-in browsing or direct HTTP fetches are insufficient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, research prompts, and submitted URLs are sent to you.com or ydc-index.io. <br>
Mitigation: Do not use the skill with secrets, private repositories, internal-only URLs, regulated data, or access-controlled content. <br>
Risk: Research and extraction calls use a sensitive YOUCOM_API_KEY and may incur paid API usage. <br>
Mitigation: Confirm with the user before paid calls and keep the API key in the configured environment rather than in prompts, URLs, or output files. <br>


## Reference(s): <br>
- [you.com API Reference](references/api.md) <br>
- [you.com API keys](https://you.com/platform/api-keys) <br>
- [ClawHub skill page](https://clawhub.ai/crabsticksalad/youcom-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON results from search, research, or extraction scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Basic search can run without an API key; research and extraction require YOUCOM_API_KEY and optional --out writes JSON to a file.] <br>

## Skill Version(s): <br>
0.1.5 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
