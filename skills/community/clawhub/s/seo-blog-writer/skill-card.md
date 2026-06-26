## Description: <br>
Fully automated SEO article writer that researches a topic and domain, analyzes competitors, drafts an article, verifies links, and produces a publication package. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justinbao19](https://clawhub.ai/user/justinbao19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External site owners, marketers, and content teams use this skill to generate SEO-focused blog articles for a topic and domain, including research, draft content, QA notes, schema markup, and a promotion checklist. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for broad execution authority for local file writes and link verification. <br>
Mitigation: Use it in a dedicated project folder with an explicit output_dir, and grant full subagent execution only when broad command, file, and network authority is acceptable. <br>
Risk: The skill crawls provided domains and competitor pages and may rely on search-result estimates. <br>
Mitigation: Review discovered URLs, claims, citations, generated article text, QA output, and schema markup before publishing or relying on the results. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justinbao19/seo-blog-writer) <br>
- [Schema.org](https://schema.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Files, Guidance] <br>
**Output Format:** [Markdown article, QA report, schema markup, and promotion checklist files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes outputs to a user-configurable directory; express, standard, and expert modes adjust research depth and runtime.] <br>

## Skill Version(s): <br>
3.2.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
