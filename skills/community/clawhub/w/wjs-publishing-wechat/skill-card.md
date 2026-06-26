## Description: <br>
Helps prepare WeChat Official Account articles by lightly polishing drafts, creating title and summary options, generating cover and explanation images, and packaging files for upload. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jianshuo](https://clawhub.ai/user/jianshuo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, and WeChat account operators use this skill to turn rough Chinese article drafts or notes into a publishable article package with supporting images and upload guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The upload helper can use configured WeChat account credentials to create drafts. <br>
Mitigation: Confirm the intended WeChat account configuration before running upload-draft.sh, and run it only when a draft should be created. <br>
Risk: Article content may be sent to external AI or image-generation services when generating images. <br>
Mitigation: Avoid confidential drafts unless the user accepts sending the article text to the configured image provider. <br>
Risk: The image-generation dependency is external and unpinned in the artifact instructions. <br>
Mitigation: Install the dependency only from a trusted source and review it before using this skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jianshuo/wjs-publishing-wechat) <br>
- [Publisher profile](https://clawhub.ai/user/jianshuo) <br>
- [gpt-image-2-skill dependency](https://github.com/Wangnov/gpt-image-2-skill) <br>
- [WeChat Official Account backend](https://mp.weixin.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown article drafts, HTML content, JSON metadata, PNG image assets, and shell command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces an article folder containing original and polished drafts, metadata, cover image, illustration, and upload artifacts when the helper scripts are run.] <br>

## Skill Version(s): <br>
0.1.0 (source: evidence.json release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
