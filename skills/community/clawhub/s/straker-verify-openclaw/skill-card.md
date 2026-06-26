## Description: <br>
Professional AI-powered translation with optional human verification. Supports 100+ languages. Quality boost for existing translations. Enterprise-grade security and privacy by straker.ai. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[indynz](https://clawhub.ai/user/indynz) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and localization teams use this skill to translate text or files, improve existing translations, request human verification, and track Straker translation projects from submission through download. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-selected text or files may be sent to Straker for translation, quality boost, or human review. <br>
Mitigation: Use the skill only for content your organization permits to be processed by Straker and any associated human-review workflow. <br>
Risk: The Straker API key could grant access to translation project operations if exposed. <br>
Mitigation: Keep STRAKER_VERIFY_API_KEY private, avoid placing it in prompts or shared files, and rotate it if disclosure is suspected. <br>
Risk: File uploads may accidentally include secrets, regulated data, customer data, or confidential documents. <br>
Mitigation: Review files before submission and remove sensitive content unless approved policy allows sending it to Straker. <br>
Risk: Translation project submissions may create external processing jobs. <br>
Mitigation: Use the confirmation flow for project submissions and confirm project details before sending files. <br>


## Reference(s): <br>
- [Straker Verify ClawHub page](https://clawhub.ai/indynz/straker-verify-openclaw) <br>
- [Straker.ai](https://straker.ai) <br>
- [Straker Verify API documentation](https://api-verify.straker.ai/docs) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with API examples, JSON response examples, and downloaded translation files where requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires STRAKER_VERIFY_API_KEY; may create, confirm, track, and download Straker translation projects.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter and changelog report 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
