## Description: <br>
Guides an agent through WeChat Official Account publishing from an existing Markdown draft, including visual formatting, editorial review, API-assisted publishing after explicit confirmation, and post-publication data review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[little-ke](https://clawhub.ai/user/little-ke) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators, editors, and publishing agents use this skill to convert an approved Markdown article into WeChat-ready assets, create a draft, publish only after explicit user approval, and review 24-hour and 48-hour performance data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing to the wrong WeChat account, draft, media item, or time could release unintended content. <br>
Mitigation: Review the generated draft, target account, media_id, timing, and preview before approving any publish action. <br>
Risk: The workflow relies on a separate wechat_publish.cjs helper and configured WeChat API credentials that were not included as executable code in the reviewed package. <br>
Mitigation: Confirm the helper source and credential configuration are trusted before installation or use. <br>
Risk: Formatted article assets or factual corrections may need editorial review before release. <br>
Mitigation: Use the stated editorial review gate and return to content creation if factual errors are found. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/little-ke/wechat-publish-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, API Calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON draft instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before executing any publish action.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
