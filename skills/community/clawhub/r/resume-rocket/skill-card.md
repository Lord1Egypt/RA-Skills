## Description:

Resume Rocket rewrites a user's resume against a target job description, scores the match, and can generate interview preparation cards or optional Boss Zhipin auto-apply outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenmoon-genshin-impact](https://clawhub.ai/user/chenmoon-genshin-impact)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers and career-support agents use this skill to parse resumes and job descriptions, produce a match report, rewrite resume content around grounded candidate experience, and prepare interview talking points. Pro usage can also prepare tailored resumes for reviewed batch application workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles resumes, job descriptions, and LLM prompts that may contain personal or career-sensitive information.

Mitigation: Configure LLM secrets locally, use sanitized samples where possible, and avoid sending API keys, payment screenshots, identity details, or real resumes to the publisher over chat or private messages.

Risk: JD URL fetching can retrieve content from user-provided URLs.

Mitigation: Use trusted job-posting URLs, avoid internal or private links, and review fetched job descriptions before using them in resume rewriting.

Risk: Auto-apply mode can affect job-board accounts and submit applications at scale.

Mitigation: Use auto-apply only after explicit review of each target, keep daily limits low, and monitor account and platform-policy impacts.

## Reference(s):

- [Resume Rocket project homepage](https://github.com/openclaw-community/resume-rocket)
- [Resume Rocket ClawHub listing](https://clawhub.ai/chenmoon-genshin-impact/skills/resume-rocket)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Console text plus Markdown and DOCX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces resume-optimized.docx, match-report.md, and paid-tier interview-cards.md; auto-apply mode can create per-job batch output directories.]

## Skill Version(s):

0.1.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
