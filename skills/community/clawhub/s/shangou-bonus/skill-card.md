## Description: <br>
查询淘宝闪购每日隐藏的大额福利优惠券和红包。包含通用红包、超市红包、夜宵红包、买药红包、零食红包、学生专享等。无需扫码，无需复制口令，搜索专用口令词即可获得隐藏各类福利活动，安全便捷，通过API获取当日最新活动。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[z65919](https://clawhub.ai/user/z65919) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to fetch current Taobao Shāngòu promotion keywords, coupons, and red packet instructions from the disclosed third-party API, then search those keywords in the Taobao app. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Coupon results come from a third-party API and may be inaccurate, unavailable, or promotional in nature. <br>
Mitigation: Review returned offers in the Taobao app before acting on them. <br>
Risk: The skill depends on network access to one disclosed external API, so fresh results may fail if that API is unavailable. <br>
Mitigation: Use the locally cached latest response when available, and treat cached offers as potentially stale. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/z65919/shangou-bonus) <br>
- [Jumanjian promotion API](https://v.jumanjian.com/api/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [Plain text with dated promotion entries and usage instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May cache the latest API response locally when data is fetched successfully.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
