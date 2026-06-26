## Description: <br>
Automates WeChat Official Account article drafting and publishing, including Markdown rendering with WeMD themes, image and cover upload, draft creation or update, manual-confirmation publishing, status checks, asset lookup, and theme management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[traceless929](https://clawhub.ai/user/traceless929) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to prepare WeChat Official Account articles from Markdown or text, render them with WeMD themes, upload referenced media, create or update drafts, and publish only after explicit human confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses WeChat publisher credentials and can upload local files referenced by article inputs. <br>
Mitigation: Keep article inputs and assets in a dedicated directory, review resolved file paths before execution, and require explicit confirmation before uploading unexpected local files. <br>
Risk: First use can run a Node/GitHub build process for WeMD dependencies. <br>
Mitigation: Review or pin the WeMD setup path and dependency installation before first use. <br>
Risk: The artifact includes client wrappers for deleting materials, drafts, and published articles. <br>
Mitigation: Do not trigger delete operations by default; require an explicit user request and confirmation before deletion. <br>


## Reference(s): <br>
- [WeChat Publisher API Mapping](artifact/references/api-mapping.md) <br>
- [WeChat Publisher Safety Rules](artifact/references/safety-rules.md) <br>
- [WeMD Renderer](https://github.com/tenngoxars/WeMD) <br>
- [ClawHub Skill Page](https://clawhub.ai/traceless929/wechat-publisher-wemd) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON status/result objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit human confirmation before publishing; script outputs include draft and publish identifiers, preview links, status data, and theme lists.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
