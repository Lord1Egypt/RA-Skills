## Description: <br>
Fetch a public WeChat article URL, archive the raw HTML, and convert the article into a stage-1 compatible brief in content-production/inbox/. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abigale-cyber](https://clawhub.ai/user/abigale-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content-production agents use this skill to turn a public mp.weixin.qq.com article URL into a reusable writing brief and raw HTML archive for downstream collect-to-create workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Briefs and raw HTML archives may retain source content in the workspace. <br>
Mitigation: Use only public article URLs, avoid private or sensitive pages, review retained files, and clean up content-production/inbox/raw/wechat/ when archives are no longer needed. <br>
Risk: Deleted, blocked, or anti-crawl WeChat pages may fail or produce reduced-quality extraction. <br>
Mitigation: Review the generated brief before downstream reuse and retry only after resolving any public-page access challenge. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/abigale-cyber/wechat-collect) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, files] <br>
**Output Format:** [Markdown brief plus archived HTML file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a brief under content-production/inbox/ and archives raw HTML under content-production/inbox/raw/wechat/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
