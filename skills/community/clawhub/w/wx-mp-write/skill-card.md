## Description: <br>
wx-mp-write helps agents plan, draft, polish, illustrate, and optionally publish WeChat public-account articles as Markdown drafts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onceyoungs](https://clawhub.ai/user/onceyoungs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, technical bloggers, and public-account operators use this skill to choose article topics, gather supporting material, draft and polish WeChat posts, suggest images, and prepare draft publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated article content, title, summary, image choices, or target account may be inaccurate or unsuitable for publication. <br>
Mitigation: Review the complete article, title, author, summary, image sources, and destination account before creating or publishing any draft. <br>
Risk: The Tavily API key could be exposed if placed in prompts, shared files, or screenshots. <br>
Mitigation: Keep TAVILY_API_KEY in a secure environment variable or local environment file and avoid including it in prompts or shared artifacts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/onceyoungs/wx-mp-write) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, API calls] <br>
**Output Format:** [Markdown article content with supporting prose, image suggestions, and optional publishing instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May rely on TAVILY_API_KEY for search and a WeChat publishing helper for draft creation.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
