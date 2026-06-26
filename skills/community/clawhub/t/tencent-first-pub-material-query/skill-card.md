## Description: <br>
首发素材消耗批量查询。根据提供的账户ID列表，查询指定日期内的首发素材（图片+视频）消耗数据。首次使用时自动检查依赖环境（tencentads技能+API Key）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tazdingoooo](https://clawhub.ai/user/tazdingoooo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing operators and agents use this skill to batch query Tencent Ads first-publication image and video material spend for supplied account IDs and date ranges. It returns account-level summaries and detailed JSON that can be converted into readable tables or reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Tencent Ads API credentials and may prompt users to provide an API key. <br>
Mitigation: Use a trusted credential setup path, avoid pasting long-lived keys into chat, and prefer least-privileged Tencent Ads keys. <br>
Risk: The setup flow can install or rely on a global npm package and dependent Tencent Ads skills. <br>
Mitigation: Install only when the publisher, dependency skills, and tencentads-cli package are trusted; review or pin the CLI before allowing global installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tazdingoooo/tencent-first-pub-material-query) <br>
- [Tencent Ads skill install guide](http://skills.ad.qq.com/install/tencentads.md) <br>
- [Tencent Ads skill portal](https://skills.ad.qq.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON report output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries account IDs over a date range, batches up to 20 accounts per request, and returns first-publication material metrics sorted by spend.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
