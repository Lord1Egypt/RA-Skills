## Description: <br>
Create, edit, and publish WordPress posts via REST API with full Gutenberg block support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chirukinbb](https://clawhub.ai/user/chirukinbb) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content automation teams use this skill to generate Gutenberg-compatible WordPress content, upload media, manage taxonomy metadata, and create or publish posts through the WordPress REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use WordPress site credentials to create, publish, delete, or upload content. <br>
Mitigation: Use least-privilege application passwords, prefer staging and draft-by-default workflows, and require explicit approval before publishing, deleting, or uploading media. <br>
Risk: Credentials or authenticated responses could be exposed through inline secrets or verbose logging. <br>
Mitigation: Use environment variables or reviewed configuration, avoid admin credentials, and avoid verbose authenticated logging with real credentials. <br>
Risk: Media upload workflows can send unintended local files to a WordPress site. <br>
Mitigation: Restrict uploads to reviewed files or a small reviewed directory before running upload commands. <br>


## Reference(s): <br>
- [WordPress REST API Reference](artifact/references/api_reference.md) <br>
- [Gutenberg Block Examples](artifact/references/common_blocks.md) <br>
- [Troubleshooting WordPress API Issues](artifact/references/troubleshooting.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/chirukinbb/wordpress-api-gutenberg) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown guidance with Python, JSON, HTML, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce WordPress REST API payloads, Gutenberg block HTML, publishing scripts, and configuration steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
