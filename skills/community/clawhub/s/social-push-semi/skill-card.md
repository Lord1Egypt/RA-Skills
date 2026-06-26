## Description: <br>
小红书半自动发布脚手架：自动生成文案、自动抽封面图、产出发布包；最后由人工确认发布。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yugulugulu](https://clawhub.ai/user/yugulugulu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Content creators and operators use this skill to prepare Xiaohongshu posts from videos, themes, or keywords, then review the filled draft before publishing. It supports draft generation, cover extraction, publish-pack creation, and CDP-based preview filling with a manual final publish step. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled scripts include live account actions beyond the documented manual publish flow. <br>
Mitigation: Use only the documented preview wrappers and avoid direct publish, comment, notification, analytics, and account-reset commands unless those live actions are explicitly intended. <br>
Risk: The workflow uses a logged-in browser session through Chrome DevTools Protocol. <br>
Mitigation: Use a dedicated Xiaohongshu account/profile, keep CDP bound to localhost, and inspect the filled post manually before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yugulugulu/social-push-semi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, generated draft files, JSON publish packs, and checklist files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create draft.md, cover.jpg, publish-pack.json, checklist.md, images, and content files under the configured output directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
