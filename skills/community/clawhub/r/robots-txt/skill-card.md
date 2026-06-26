## Description: <br>
Guides configuration and auditing of robots.txt for search engine and AI crawler control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kostja94](https://clawhub.ai/user/kostja94) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site owners, and SEO practitioners use this skill to audit crawler access and prepare robots.txt recommendations for search engines and AI crawlers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project context files may contain private business details when the skill asks the agent to read .claude/project-context.md or .cursor/project-context.md. <br>
Mitigation: Review those files before use and remove confidential details that are not needed for robots.txt guidance. <br>
Risk: robots.txt is public, advisory, and does not reliably prevent indexing or protect sensitive content. <br>
Mitigation: Use authentication, noindex directives, or X-Robots-Tag where appropriate, and verify crawler and indexing behavior after changes. <br>


## Reference(s): <br>
- [Google robots.txt documentation](https://developers.google.com/search/docs/crawling-indexing/robots/create-robots-txt) <br>
- [Vercel AI crawler study](https://vercel.com/blog/the-rise-of-the-ai-crawler) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown with robots.txt examples, audit findings, checklists, and references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a full recommended robots.txt file, current-state audit, compliance checklist, and crawler-specific notes.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
