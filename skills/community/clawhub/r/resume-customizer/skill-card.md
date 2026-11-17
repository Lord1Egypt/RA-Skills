## Description:

Tailors resumes to match specific job descriptions with multi-format resume and JD parsing, ATS optimization, keyword analysis, skill matching, and Chinese and English resume support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agjvsxgm](https://clawhub.ai/user/agjvsxgm)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers and career-support agents use this skill to tailor existing resumes or generate new resumes for target job descriptions. It parses resumes and JDs, analyzes skill and keyword gaps, suggests improvements, and exports resume files in formats such as DOCX, PDF, Markdown, HTML, and text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive resume and career data.

Mitigation: Process resumes only in trusted environments and avoid sharing personal data beyond what is needed for the target job application.

Risk: The skill can fetch job descriptions from arbitrary URLs.

Mitigation: Prefer pasted JD text or trusted local files, and review any URL source before allowing the skill to retrieve it.

Risk: HTML export may include resume content without sanitization.

Mitigation: Avoid exporting attacker-supplied or untrusted content to HTML, and review generated HTML before opening or publishing it.

Risk: Resume tailoring can overstate qualifications if generated changes are accepted blindly.

Mitigation: Review all customized resume content before submission and remove any claim not supported by the user's actual experience.

Risk: Dependencies are listed without version pins.

Mitigation: Pin and review dependencies before installing the skill in production or shared environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agjvsxgm/skills/resume-customizer)
- [README.md](README.md)
- [ATS Optimization Guide](references/ats_optimization.md)
- [Resume Best Practices](references/best_practices.md)
- [Resume Structures](references/resume_structures.md)
- [Industry Keywords](references/industry_keywords.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional JSON intermediates and exported resume files in DOCX, PDF, Markdown, HTML, or plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Chinese and English resumes, configurable output format, template, ATS optimization, industry focus, keyword density, and language.]

## Skill Version(s):

1.0.3 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
