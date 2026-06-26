## Description: <br>
Orchestrate the official WeChat draft publishing path for already-prepared article HTML or Markdown using md2wechat, with mandatory draft/get verification before reporting success. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerryxn](https://clawhub.ai/user/jerryxn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to push prepared WeChat Official Account HTML or Markdown into the draft box, upload the cover image, and verify the created draft before reporting success. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads selected article content and a cover image to the configured WeChat Official Account. <br>
Mitigation: Review the article, cover image, title, author, and digest before running publish.sh, and use it only when draft creation is intended. <br>
Risk: The workflow depends on md2wechat credentials and WeChat API access. <br>
Mitigation: Protect WECHAT_APPID, WECHAT_SECRET, and the md2wechat config file; confirm the current public IP is authorized before publishing. <br>
Risk: Generated verification JSON files can contain draft metadata or article content. <br>
Mitigation: Delete generated verification files when they contain sensitive draft content or are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jerryxn/wechat-publisher-md2wechat-draftget) <br>
- [md2wechat skill repository](https://github.com/geekjourneyx/md2wechat-skill) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Themes and layout notes](references/themes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated JSON verification files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces draft request, upload result, create-draft result, and draft/get verification artifacts next to the article.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
