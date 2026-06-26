## Description: <br>
主动式 Reddit 科技热点感知，结合当前会话上下文，以毒舌幽默风格生成科技圈热点点评。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QianYushi](https://clawhub.ai/user/QianYushi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch configured Reddit RSS headlines, curate technology-related items, and produce Chinese commentary with source links for agent-mediated news monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Reddit for configured subreddits and stores fetched public headlines in the skill folder. <br>
Mitigation: Review config.json before use and remove topics or subreddits that are not appropriate for the deployment context. <br>
Risk: Reddit headlines and links are untrusted external content that may be inaccurate, misleading, or inappropriate. <br>
Mitigation: Treat fetched headlines and links as untrusted input and review generated commentary before relying on it. <br>
Risk: The artifact includes Python and Bash scripts that execute network and file operations. <br>
Mitigation: Install only after reviewing the included scripts and running them in an environment where Reddit access and local cache writes are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/QianYushi/witpulse-redditnews) <br>
- [Publisher profile](https://clawhub.ai/user/QianYushi) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown links and local text cache] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public Reddit RSS headlines for configured subreddits and stores a small local headline cache.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
