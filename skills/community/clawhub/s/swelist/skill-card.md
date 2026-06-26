## Description: <br>
Helps agents find tech internships and new-grad jobs, track local applications, and prepare interview or career responses without requiring a sign-up. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenyuan99](https://clawhub.ai/user/chenyuan99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, students, and job-search agents use Swelist to browse software engineering internships and new-grad roles, maintain a local application tracker, and generate interview or career-prep writing assistance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local tracking can create or export a SQLite job-application database containing application history and notes. <br>
Mitigation: Confirm the intended database path before tracker commands, protect exported files, and avoid storing unnecessary sensitive notes. <br>
Risk: Tracker behavior may read a local profile file to resolve configuration. <br>
Mitigation: Review the profile configuration before use and pass an explicit database path when predictable local state is required. <br>
Risk: jobgpt can send job-prep prompts or resume text to OpenAI. <br>
Mitigation: Review prompts before submission, omit sensitive personal data where possible, and require an appropriate OpenAI API key configuration. <br>
Risk: The evidence security summary flags conflicting documentation claims around persistent local tracking, profile-file reads, and OpenAI data transmission. <br>
Mitigation: Treat the scanner verdict as a deployment review signal and verify the specific command behavior before enabling automated use. <br>


## Reference(s): <br>
- [Swelist on ClawHub](https://clawhub.ai/chenyuan99/swelist) <br>
- [Swelist on PyPI](https://pypi.org/project/swelist/) <br>
- [Swelist GitHub repository](https://github.com/chenyuan99/swelist) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Configuration] <br>
**Output Format:** [Plain text, Markdown, CLI commands, JSON, and CSV depending on the Swelist command used] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tracker commands can read and write a local SQLite database; jobgpt can send prompts or resume text to OpenAI when used.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release metadata; artifact frontmatter says 0.1.9) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
