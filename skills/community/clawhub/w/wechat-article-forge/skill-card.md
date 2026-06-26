## Description: <br>
End-to-end WeChat Official Account article writing and publishing pipeline with topic research, Chinese-first drafting, blind review, fact-checking, formatting, human preview, illustrations, and draft-box publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chunhualiao](https://clawhub.ai/user/chunhualiao) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External WeChat Official Account authors and teams use this skill to research topics, draft Chinese articles, review quality, fact-check claims, format WeChat HTML, preview locally, generate illustrations, and save finished content to the WeChat draft box. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use WeChat app credentials and image-generation API keys. <br>
Mitigation: Review setup and configuration before use, keep credentials outside shared draft files, avoid plaintext secrets where possible, and grant only credentials needed for the chosen workflow. <br>
Risk: The workflow can upload images and create WeChat draft-box content. <br>
Mitigation: Require explicit human confirmation before any WeChat upload, browser automation step, or draft creation. <br>
Risk: The skill keeps persistent local workflow state, drafts, images, and configuration. <br>
Mitigation: Review permissions on ~/.wechat-article-writer and remove drafts or generated files that should not persist. <br>
Risk: The preview server may expose draft article content if bound beyond localhost. <br>
Mitigation: Bind preview to localhost unless remote access is intentional and protected. <br>
Risk: Setup can modify workspace agent rules and install a persistent preview service. <br>
Mitigation: Inspect setup.sh before running it and apply it only in the intended workspace and user environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chunhualiao/wechat-article-forge) <br>
- [README](README.md) <br>
- [Writer Prompt](references/writer-prompt.md) <br>
- [Reviewer Rubric](references/reviewer-rubric.md) <br>
- [Fact Checker Prompt](references/fact-checker-prompt.md) <br>
- [Browser Automation Publishing](references/browser-automation.md) <br>
- [Pipeline State](references/pipeline-state.md) <br>
- [WeChat HTML Rules](references/wechat-html-rules.md) <br>
- [Data Layout and Schemas](references/data-layout.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown drafts, JSON workflow state, WeChat-compatible HTML, shell commands, configuration files, and publishing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create persistent draft state, local preview files, generated images, and WeChat draft-box content after user-provided credentials and approvals.] <br>

## Skill Version(s): <br>
2.4.1 (source: skill.yml, CHANGELOG, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
