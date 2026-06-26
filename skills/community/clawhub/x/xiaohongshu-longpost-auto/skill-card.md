## Description: <br>
When users have long-form content ready to publish on Xiaohongshu, automatically completes the entire process: login detection, long content segmentation optimization, AI-generated images, content filling, AI-generated tags, tag activation, original content declaration, and publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and operators use this skill to prepare and publish existing long-form note content to Xiaohongshu, including formatting, descriptions, tags, originality declaration, and final posting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish public Xiaohongshu posts and make originality declarations without a required final approval step. <br>
Mitigation: Require a draft or preview and explicit user approval of the title, body, images, tags, originality declaration, destination account, and live publish action before posting. <br>
Risk: The skill operates a logged-in Xiaohongshu creator account. <br>
Mitigation: Use it only with an account the user is authorized to control, and require manual QR-code login rather than storing credentials in the skill. <br>


## Reference(s): <br>
- [Xiaohongshu Creator Platform](https://creator.xiaohongshu.com/) <br>
- [Xiaohongshu Community Guidelines](https://www.xiaohongshu.com/community_guidelines) <br>
- [Xiaohongshu Creator Help](https://creator.xiaohongshu.com/help) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code] <br>
**Output Format:** [Markdown guidance with JavaScript browser automation snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided long-form content and a logged-in Xiaohongshu creator session; QR code login remains manual.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
