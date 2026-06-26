## Description: <br>
Automates job search and application workflows across LinkedIn, Indeed, Glassdoor, ZipRecruiter, and Wellfound, with SkillBoss API Hub support for compatibility analysis and cover letter generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and job seekers use this skill to search job platforms, compare matches, generate application materials, fill forms, and track application attempts with optional manual confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive applicant data, credentials, resumes, and job profile details. <br>
Mitigation: Provide only the minimum applicant data needed and store profiles, credentials, and generated logs securely. <br>
Risk: Automated submissions can send applications before the user has reviewed job fit or generated materials. <br>
Mitigation: Keep dry-run mode and per-application confirmation enabled until the user has reviewed each application. <br>
Risk: Generated resumes, cover letters, and screening answers may be inaccurate or misleading. <br>
Mitigation: Review every generated resume, cover letter, and screening answer before submission. <br>
Risk: Automation that bypasses CAPTCHA or platform controls can create compliance and account-risk issues. <br>
Mitigation: Do not use CAPTCHA-bypass automation and respect platform terms, rate limits, and manual checkpoints. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/marjoriebroad/qui-job-auto-apply) <br>
- [SkillBoss Job Auto Apply](https://skillboss.co/skills/job-auto-apply) <br>
- [Job Platform Integration Reference](artifact/platform_integration.md) <br>
- [LinkedIn Jobs API Documentation](https://developer.linkedin.com/docs/v2/jobs) <br>
- [Indeed API Documentation](https://opensource.indeedeng.io/api-documentation/) <br>
- [Glassdoor Developer Documentation](https://www.glassdoor.com/developer/index.htm) <br>
- [Wellfound Documentation](https://docs.wellfound.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples, shell commands, JSON configuration, generated application text, and application result JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and may use a local applicant profile containing sensitive personal data.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
