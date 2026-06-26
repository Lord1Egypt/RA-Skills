## Description: <br>
Research any topic across 26+ sources: Reddit, X, YouTube, GitHub, HN, Bluesky, ArXiv, Dev.to, Polymarket, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vihangd](https://clawhub.ai/user/vihangd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research-focused agent users use Scry to gather, rank, deduplicate, and summarize current public signals about a topic across social, developer, academic, finance, and news sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read local provider tokens and, for X/Twitter, browser session cookies when optional sources are enabled. <br>
Mitigation: Prefer scoped API keys, avoid storing AUTH_TOKEN or CT0 session cookies in environment files, and review configuration before use. <br>
Risk: Research queries and source results may be retained in local caches. <br>
Mitigation: Restrict sources with --sources for sensitive topics and periodically clear ~/.cache/scry and ~/.config/bird when local retention is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vihangd/scry) <br>
- [Homepage](https://github.com/khalidsh/scry-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown research summaries with source statistics, citations, and optional command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May also emit compact or JSON-formatted research reports from the bundled script.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
