## Description: <br>
Queries real-time queue, store, city, area, and distance-sorted status for Sushiro restaurants in mainland China through a shell-based curl and jq workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gitnapp](https://clawhub.ai/user/gitnapp) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to compare Sushiro China wait queues, find less busy stores by city or area, look up a specific store, or inspect nearby stores from approximate coordinates. It is most useful for low-frequency, decision-support queries before visiting a restaurant. <br>

### Deployment Geography for Use: <br>
Mainland China <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes live requests to Sushiro China's backend with a shared backend token. <br>
Mitigation: Review before installing and prefer a version that removes the shared token or limits access to documented queue endpoints. <br>
Risk: The raw command can pass arbitrary paths to the upstream API. <br>
Mitigation: Avoid raw mode unless you understand the upstream API impact and only use the documented queue, store, and area endpoints. <br>
Risk: Precise coordinates passed with --near may reveal sensitive home or work locations to the upstream service. <br>
Mitigation: Use approximate or public-location coordinates when sorting stores by distance. <br>


## Reference(s): <br>
- [Sushiro China API reference](references/api.md) <br>
- [Sushiro China WeChat backend](https://crm-cn-prd.sushiro.com.cn/wechat/api/2.0) <br>
- [ClawHub release page](https://clawhub.ai/gitnapp/sushiro) <br>
- [Publisher profile](https://clawhub.ai/user/gitnapp) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Plain text tables, one-line summaries, and JSON emitted by shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; live results depend on Sushiro China's upstream service and token availability.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
