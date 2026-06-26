## Description: <br>
A WeChat public-account writing assistant that helps agents manage account profiles, search for topic ideas, draft articles in the selected account style, optionally archive finished articles to WeCom Docs, and learn from user-marked high-quality articles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sophiayuan1984-jpg](https://clawhub.ai/user/sophiayuan1984-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, operators, and writing agents use this skill to run a WeChat public-account writing workflow: initialize or switch account profiles, generate timely topic options, draft long-form posts, archive accepted articles, and refine future style guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved account profiles and article indexes may contain business strategy, audience information, brand voice, or unpublished content. <br>
Mitigation: Review workspace profile and article-index files before sharing or publishing them, and treat them as local user data. <br>
Risk: Optional WeCom document archiving can move draft content into a separate integration and storage surface. <br>
Mitigation: Use the WeCom archive option only after reviewing the article and confirming the separate wecom-doc integration is trusted for the organization. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sophiayuan1984-jpg/wechat-writer-kit) <br>
- [README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Writing Rules](artifact/references/writing-rules.md) <br>
- [Profile Template](artifact/references/profile-template.md) <br>
- [Article Index](artifact/references/article-index.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown guidance and article drafts, with local profile and article-index file updates when the agent applies the workflow.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include topic lists, article title options, completed WeChat article drafts, profile updates, and optional WeCom archive references.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
