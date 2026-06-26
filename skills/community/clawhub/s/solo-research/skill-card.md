## Description: <br>
Performs deep market research for product ideas, including competitor analysis, user pain points, SEO/ASO keywords, naming and domain checks, and TAM/SAM/SOM sizing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fortunto2](https://clawhub.ai/user/fortunto2) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, product builders, and founders use this skill to investigate market opportunities before planning or building a product. It guides competitive research, demand analysis, naming checks, market sizing, and a GO/NO-GO/PIVOT recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may direct the agent to bypass Reddit CAPTCHA checks while collecting user research. <br>
Mitigation: Remove or ignore CAPTCHA-bypass instructions and use approved, compliant access methods. <br>
Risk: The skill can search private knowledge bases, prior sessions, and source code without a narrow scope. <br>
Mitigation: Require explicit user approval and project boundaries before private-context searches. <br>
Risk: The generated research file may include incorrect market claims, source interpretation, or sizing assumptions. <br>
Mitigation: Review sources, calculations, and file diffs before using or publishing the research. <br>


## Reference(s): <br>
- [Domain Check Reference](references/domain-check.md) <br>
- [Research Output Template](references/research-template.md) <br>
- [PRAW Python Reddit API Wrapper](https://github.com/praw-dev/praw) <br>
- [SearXNG Docker Tavily Adapter](https://github.com/fortunto2/searxng-docker-tavily-adapter) <br>
- [PullPush Reddit Submission Search](https://api.pullpush.io/reddit/submission/search) <br>
- [TrustMRR Scraper](https://apify.com/actor_builder/trustmrr-scraper/api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown research document plus concise text summary and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes docs/research.md when run; asks before overwriting an existing research file.] <br>

## Skill Version(s): <br>
1.7.1 (source: release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
