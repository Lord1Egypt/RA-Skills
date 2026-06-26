## Description: <br>
Tailor resumes for specific job applications using the Tamar AI API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evgenyshneyderman](https://clawhub.ai/user/evgenyshneyderman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to tailor a resume for a specific job description or job URL, review match analysis and gaps, apply feedback, and download the result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Resume files, job descriptions, profile information, and feedback are sent to Tamar through its CLI/API. <br>
Mitigation: Use the skill only when that data sharing is acceptable, confirm files and text before upload, and redact unrelated sensitive information where possible. <br>
Risk: The Tamar API key is sensitive and enables access to the user's Tamar account. <br>
Mitigation: Use a revocable API key, avoid pasting secrets into chat or screenshots, and check authentication with Tamar CLI commands instead of reading local config files directly. <br>
Risk: Job descriptions, URLs, resume paths, and feedback are user-provided inputs that may be unsafe if interpolated directly into shell commands. <br>
Mitigation: Write multi-line text to temporary files or quote arguments safely before invoking the Tamar CLI. <br>


## Reference(s): <br>
- [Tamar API Documentation](https://ask-tamar.com/developers) <br>
- [Tamar Account and Pricing](https://ask-tamar.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/evgenyshneyderman/tamar-resume-tailor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and summaries of Tamar CLI JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to upload resume files, pass job descriptions to the Tamar CLI, summarize generated analysis, and download PDF or JSON resume output.] <br>

## Skill Version(s): <br>
1.4.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
