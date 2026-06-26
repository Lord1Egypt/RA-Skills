## Description: <br>
闲鱼自动化发布工具，帮助用户在闲鱼平台自动发布商品，支持商品信息填写、图片上传、价格设置和批量发布。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
External users and developers use this skill to automate Xianyu listing workflows, including login, product listing creation, image upload, price entry, batch publishing, listing refresh, and unpublishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automate a live Xianyu marketplace account with browser-level access to a Taobao/Xianyu session and saved login state. <br>
Mitigation: Use a dedicated account where possible, run it only in an environment you control, and confirm how to inspect and delete saved cookies before use. <br>
Risk: Publish, batch publish, refresh, and unpublish actions can modify live marketplace listings. <br>
Mitigation: Review product JSON or CSV inputs and command targets before execution, then test with a single non-critical listing before batch operations. <br>
Risk: Automation frequency or anti-detection behavior may conflict with platform rules or trigger account restrictions. <br>
Mitigation: Follow Xianyu/Taobao rules, avoid platform-rule evasion, and use conservative intervals for listing operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/onlyloveher/xianyu-publisher) <br>
- [Xianyu publish page](https://2.taobao.com/publish/xianyu) <br>
- [Xianyu listing management page](https://2.taobao.com/commodity/manage/listing) <br>
- [Taobao login page](https://login.taobao.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with shell, Python, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May refer to local product JSON or CSV inputs and browser automation steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
