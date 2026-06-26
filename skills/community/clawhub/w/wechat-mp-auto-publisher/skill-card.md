## Description: <br>
Automates drafting technical articles, generating supporting images, and preparing publication to a WeChat Official Account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lizz0725](https://clawhub.ai/user/lizz0725) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content teams, and operators use this skill to turn a topic into a WeChat-ready technical article workflow, including an outline, background search, Markdown draft, image prompts, and publication steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential-backed external actions can search, generate assets, and publish to WeChat when supporting tools and credentials are configured. <br>
Mitigation: Keep the workflow draft-only until a human reviews and explicitly approves the final WeChat publication step. <br>
Risk: Configured API keys and WeChat credentials may be exposed if environment files are pasted, printed, or included in generated content. <br>
Mitigation: Store credentials outside generated articles, avoid printing .env contents, and review outputs before sharing or publishing. <br>
Risk: Unsafe shell command construction patterns may be risky with untrusted topics, keywords, or filenames. <br>
Mitigation: Review and patch command construction before using untrusted input, and prefer argument arrays or validated inputs in local scripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lizz0725/wechat-mp-auto-publisher) <br>
- [Publisher profile](https://clawhub.ai/user/lizz0725) <br>
- [Alibaba Cloud Bailian API key console](https://bailian.console.aliyun.com/?tab=globalset#/efm/api_key) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown articles and workflow guidance with inline shell commands, frontmatter, and JSON search-result summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create framework and article files, generate image prompts, and call external search, image-generation, and WeChat publishing tools when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
