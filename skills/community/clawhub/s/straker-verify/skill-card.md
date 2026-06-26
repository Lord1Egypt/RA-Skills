## Description: <br>
Professional AI-powered translation with optional human verification, support for 100+ languages, and quality boost for existing translations through Straker Verify. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[indy-at-straker](https://clawhub.ai/user/indy-at-straker) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to request AI translation, improve existing translations, create translation projects, and add optional human review through Straker Verify. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected text, files, and related project metadata are sent to Straker Verify for processing. <br>
Mitigation: Use the skill only for content your organization has approved for Straker Verify, and avoid submitting secrets, regulated data, or confidential customer documents without approval. <br>
Risk: The skill depends on the STRAKER_VERIFY_API_KEY environment variable for authenticated API calls. <br>
Mitigation: Keep the API key scoped, protected, and out of prompts, source files, logs, and shared documents. <br>


## Reference(s): <br>
- [Straker Verify API Documentation](https://api-verify.straker.ai/docs) <br>
- [Straker.ai](https://straker.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/indy-at-straker/straker-verify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API request details, project status guidance, and references to translated file downloads when the Straker Verify API is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
