## Description: <br>
Standardized WeChat official account writing workflow that integrates WeChat publishing, toolkit, writing, search, and analysis skills across material research, drafting, formatting, publishing, and post-publication optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[earthwalking](https://clawhub.ai/user/earthwalking) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content operators and developers use this skill to plan and execute WeChat official account articles, including material research, drafting, Markdown formatting, publishing checks, and performance analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can expose WeChat credentials such as WECHAT_APP_SECRET through prompts, logs, or shell history. <br>
Mitigation: Treat WeChat secrets as sensitive, avoid echoing them into prompts or logs, and rotate any secret that may have been exposed. <br>
Risk: Publishing, scheduling, or group-send actions can affect live public WeChat posts. <br>
Mitigation: Use draft and preview-only defaults, and require explicit manual approval before scheduling, publishing, or group-sending content. <br>
Risk: Rewrite guidance could be misused to disguise copied work or insufficiently attributed sources. <br>
Mitigation: Use original writing, limited quotation, attribution, and licensed sources instead of using rewrite steps to hide copied content. <br>
Risk: The workflow depends on referenced publisher and toolkit skills whose behavior is not assessed by this card. <br>
Mitigation: Review and scan each referenced publisher, toolkit, search, writing, and analysis skill separately before installation or deployment. <br>


## Reference(s): <br>
- [WeChat Official Account Developer Documentation](https://developers.weixin.qq.com/) <br>
- [wenyan-cli](https://github.com/wenyan-md/cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and generated article-planning artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May coordinate other WeChat publishing, search, writing, and analysis skills; live publishing requires explicit manual approval.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
