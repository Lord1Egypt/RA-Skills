## Description: <br>
Assists job seekers with polishing, tailoring, scoring, and exporting resumes and CVs, including checklist-based reviews and multi-format output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Wscats](https://clawhub.ai/user/Wscats) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and job seekers use this skill to improve existing resumes, tailor them to job descriptions, evaluate quality and ATS readiness, and generate resume content in formats suitable for editing, submission, or conversion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Resume and job-description text may contain sensitive personal or employer information. <br>
Mitigation: Redact unnecessary personal details and confidential third-party information before sharing content with the agent or API provider running the skill. <br>
Risk: Generated achievements, scores, or role-fit claims may be inaccurate or overstate the user's experience. <br>
Mitigation: Review all generated resume content for factual accuracy and keep only claims the user can substantiate. <br>
Risk: Export workflows may include conversion commands for local resume files. <br>
Mitigation: Run export and conversion commands only on files the user trusts. <br>


## Reference(s): <br>
- [ClawHub Resume Assistant release page](https://clawhub.ai/Wscats/resume-assistant) <br>
- [Skill manifest](artifact/skill.json) <br>
- [Usage examples](artifact/examples/usage.md) <br>
- [Export prompt](artifact/prompts/export.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, structured prose, HTML, LaTeX, Pandoc-oriented Markdown, and conversion commands depending on the requested workflow] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports English and Chinese resume workflows, four resume templates, and export guidance for Markdown, HTML, Word, LaTeX, and PDF.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
