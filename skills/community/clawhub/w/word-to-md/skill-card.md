## Description: <br>
Convert Word documents (.docx and .doc) to clean Markdown using the MinerU API and mineru-open-api CLI, preserving headings, lists, tables, images, and code blocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[veeicwgy](https://clawhub.ai/user/veeicwgy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and documentation teams use this skill to convert Word files into Markdown for Git-based documentation, blog publishing, academic paper conversion, and static site content workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the third-party mineru-open-api npm package and MinerU service. <br>
Mitigation: Verify that the package and service are trusted before installation or use. <br>
Risk: Word documents may be sent to an external conversion service. <br>
Mitigation: Avoid processing confidential documents unless the service is approved for that content. <br>
Risk: Precision conversion can require a MinerU API token. <br>
Mitigation: Keep the token private and avoid exposing it in logs, prompts, or shared files. <br>


## Reference(s): <br>
- [Word to MD on ClawHub](https://clawhub.ai/veeicwgy/word-to-md) <br>
- [MinerU API token management](https://mineru.net/apiManage/token) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files and concise command guidance for mineru-open-api conversions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a local output directory for converted Markdown and extracted document assets.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
