## Description: <br>
AI-powered JD-matched resume generator with Chinese and English support that collects a reusable profile, analyzes target job descriptions, and produces print-optimized resume output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[26048608982lp-ai](https://clawhub.ai/user/26048608982lp-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and job seekers use this skill to tailor resumes to specific job descriptions, including ATS-oriented optimization and Chinese or English resume generation. The workflow supports profile collection, JD parsing, match analysis, self-contained HTML resume generation, and optional PDF export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow stores personal resume information in a local resume-profile.md file in the workspace. <br>
Mitigation: Install only where local workspace storage of resume data is acceptable, and review or remove the profile file when it is no longer needed. <br>
Risk: PDF export references a local headless-browser script, while the release evidence advises treating PDF export as unavailable unless the script is reviewed separately. <br>
Mitigation: Prefer the generated HTML output or review the PDF export script before relying on automated PDF generation. <br>
Risk: Job description URL handling is not clarified by the security evidence. <br>
Mitigation: Prefer pasted job description text or local files unless URL handling has been reviewed. <br>


## Reference(s): <br>
- [HTML Resume Template Guide](references/html-template-guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/26048608982lp-ai/resume-jd-match) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with match analysis, self-contained HTML resume code, and optional PDF export command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May store a local resume-profile.md and write generated resume files under resumes/.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
