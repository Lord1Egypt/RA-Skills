## Description: <br>
Generate professional PDF resumes and cover letters via the useresume.ai API. Supports creating, tailoring (AI-optimized for a job), and parsing documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[accelerated-ideas](https://clawhub.ai/user/accelerated-ideas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to create, tailor, parse, and check the status of resumes and cover letters through the UseResume CLI and API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Resume, cover-letter, job-description, and uploaded document contents may be sent to useresume.ai. <br>
Mitigation: Share only necessary personal information and review the provider's privacy and retention practices before using the service. <br>
Risk: USERESUME_API_KEY is required to call the service. <br>
Mitigation: Treat the API key as a secret, avoid committing it to files, and verify credentials with the zero-credit credentials:test command before paid operations. <br>
Risk: The skill relies on a globally installed npm CLI package. <br>
Mitigation: Verify the @useresume/cli package provenance before global installation. <br>


## Reference(s): <br>
- [UseResume skill page](https://clawhub.ai/accelerated-ideas/useresume) <br>
- [UseResume API platform](https://useresume.ai/account/api-platform) <br>
- [UseResume website](https://useresume.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI commands described by the skill return JSON and may produce PDF file URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
