## Description:

资深培训项目设计专家，专注企业内训、职业技能、人才发展类课程全流程设计，具备深度需求调研、行业前沿趋势搜索、课程体系架构、创新设计方案落地输出完整能力

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Training, HR, talent development, and vocational education teams use this skill to collect course requirements, review reference materials, research industry trends, and produce original course design proposals for internal training, vocational skills, or talent development programs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Word export script can write to arbitrary local paths when an output path is supplied.

Mitigation: Constrain exports to a dedicated workspace directory and require confirmation before creating or overwriting files.

Risk: The skill asks agents to read uploaded documents and visit reference URLs, while web and URL access behavior is under-disclosed.

Mitigation: Require confirmation before visiting external links and treat uploaded files and web pages as untrusted source material.

## Reference(s):

- [Course Structure Template](artifact/references/course-structure-template.md)
- [Reference Materials Guide](artifact/references/reference-materials-guide.md)
- [Server-Resolved GitHub Provenance](https://github.com/duding-engicool/skill-course-design-innovator)
- [ClawHub Skill Page](https://clawhub.ai/duding-engicool/skills/skill-course-design-innovator)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown course proposal and optional Word document generated from structured course data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include needs diagnosis, trend analysis, course architecture, assessment guidance, templates, and a .docx export.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
