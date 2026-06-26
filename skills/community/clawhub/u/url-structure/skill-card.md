## Description: <br>
Guides agents in planning and auditing SEO-friendly URL structures, including hierarchy, static paths, parameters, slugs, multilingual paths, and redirects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kostja94](https://clawhub.ai/user/kostja94) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
SEO practitioners, content teams, and developers use this skill to plan or audit clean URL hierarchies, handle parameters and multilingual paths, and prepare redirects when URL patterns change. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read local project context files if present, which could include sensitive site or business details. <br>
Mitigation: Review .claude/project-context.md and .cursor/project-context.md before use and keep secrets out of project context files. <br>
Risk: URL restructuring recommendations can cause redirect, canonicalization, or indexing issues if applied without validation. <br>
Mitigation: Review recommendations before implementation and test redirect and canonical behavior in staging. <br>


## Reference(s): <br>
- [Alignify URL optimization](https://alignify.co/zh/seo/url-optimization) <br>
- [Google URL guidelines](https://developers.google.com/search/docs/crawling-indexing/url-structure) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown] <br>
**Output Format:** [Markdown guidance with recommendation lists and tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read .claude/project-context.md or .cursor/project-context.md if present; the reviewed artifact does not run commands, modify files, use credentials, or persist data.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
