## Description: <br>
Daily multi-source intelligence digest that scans X, YouTube, Reddit, GitHub, and web search for high-signal tools, techniques, and updates relevant to active projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pingukim225](https://clawhub.ai/user/pingukim225) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent produce a daily, ranked research digest for fast-moving AI, crypto, content creation, and technical project domains. It helps surface actionable updates before a morning briefing while deduplicating previously seen items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Web searches and source scans can reveal sensitive project interests through digest and history files. <br>
Mitigation: Review or delete local digest and seen-URL files when topics are sensitive, and invoke the skill with explicit target domains. <br>
Risk: The workflow may require OAuth tokens or API keys for services such as X, YouTube, or Reddit. <br>
Mitigation: Use least-privilege credentials, store them outside generated digest files, and rotate them if they may have been exposed. <br>
Risk: External social and repository signals can be noisy, duplicated, stale, or misleading. <br>
Mitigation: Treat surfaced items as leads, verify important claims at the source, and keep the 7/10 relevance filter and deduplication history enabled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pingukim225/tech-scout) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown digest with ranked items, source links, relevance scores, and suggested actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a dated digest file and may maintain a local seen-URL history for deduplication.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
