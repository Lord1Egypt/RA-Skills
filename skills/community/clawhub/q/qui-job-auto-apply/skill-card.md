## Description:

Automates job search, job-fit analysis, cover-letter generation, form filling, application submission, and application tracking across major job platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search for matching jobs, generate application materials, prepare profile configuration, and optionally submit applications with dry-run or confirmation safeguards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive applicant profile data, resumes, job details, and generated application materials may be sent to an external AI provider.

Mitigation: Use only with informed consent, restrict access to profile files, avoid unnecessary personal data, and review provider data-handling terms before use.

Risk: Automated submissions can create incorrect, low-quality, or unintended job applications.

Mitigation: Keep dry-run and manual confirmation enabled, set daily limits, use high match thresholds, and review every application before submission.

Risk: Job platform automation may conflict with platform terms or trigger anti-abuse controls.

Mitigation: Prefer official APIs, respect platform rate limits, avoid captcha or proxy bypass guidance, and do not run unattended submission workflows.

Risk: Security evidence flags inconsistent implementation, domains, and safety controls.

Mitigation: Treat the package as a prototype and perform manual code, dependency, and network-review checks before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/marjoriebroad/skills/qui-job-auto-apply)
- [SkillBoss Job Auto Apply Page](https://skillboss.co/skills/job-auto-apply)
- [Job Platform Integration Reference](artifact/platform_integration.md)
- [LinkedIn Jobs API Documentation](https://developer.linkedin.com/docs/v2/jobs)
- [Indeed API Documentation](https://opensource.indeedeng.io/api-documentation/)
- [Glassdoor Developer Documentation](https://www.glassdoor.com/developer/index.htm)
- [Wellfound Documentation](https://docs.wellfound.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python code examples, JSON configuration, and text application materials.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce application logs and application_results.json when the bundled script is run.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
