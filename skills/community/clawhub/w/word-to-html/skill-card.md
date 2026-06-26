## Description: <br>
Converts Word documents (.docx and .doc) to clean HTML using the MinerU API and mineru-open-api CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[veeicwgy](https://clawhub.ai/user/veeicwgy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content teams, and migration teams use this skill to convert Word documents into structured HTML for web publishing, CMS migration, email templates, and document digitization workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Word documents may contain confidential or regulated content that would be sent to a cloud document service. <br>
Mitigation: Use the skill only with data approved for MinerU processing and avoid submitting confidential documents unless that service is authorized for the data. <br>
Risk: The precision extraction path requires an API token. <br>
Mitigation: Treat MinerU tokens as secrets, configure them through the supported authentication flow, and avoid placing tokens in prompts, logs, or checked-in files. <br>
Risk: The skill relies on the external mineru-open-api package and service. <br>
Mitigation: Verify the package and publisher before installation and review generated HTML before publishing. <br>


## Reference(s): <br>
- [Word to HTML on ClawHub](https://clawhub.ai/veeicwgy/word-to-html) <br>
- [MinerU API token management](https://mineru.net/apiManage/token) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent to run mineru-open-api, choose flash-extract or extract, quote paths, and place generated HTML outputs in an output directory.] <br>

## Skill Version(s): <br>
0.2.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
