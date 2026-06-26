## Description: <br>
Generate a categorized and rated Markdown news digest from sre.news for SRE, DevOps, and Solution Architecture professionals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imzye](https://clawhub.ai/user/imzye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
SREs, DevOps engineers, Solution Architects, and developers use this skill to collect recent sre.news links, evaluate their operational relevance, and produce a concise categorized digest. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External news and article pages may contain inaccurate, stale, or irrelevant content. <br>
Mitigation: Review the generated digest before relying on it or sharing it. <br>
Risk: The default output path can overwrite an existing sre_news_digest.md file. <br>
Mitigation: Choose a custom output path when an existing digest file should be preserved. <br>


## Reference(s): <br>
- [sre.news](https://sre.news) <br>
- [SRE/DevOps News Scoring Rubric](references/scoring-rubric.md) <br>
- [Digest Template](templates/digest_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown digest with article links, source names, star ratings, and expert summaries; helper script output is JSON article metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The digest is saved to sre_news_digest.md by default or to a user-specified path.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
