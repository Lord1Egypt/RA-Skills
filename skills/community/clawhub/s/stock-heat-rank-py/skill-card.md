## Description: <br>
Gets real-time A-share stock heat rankings by aggregating popularity lists from Wencai, Xueqiu, and Eastmoney and producing a composite TOP50 ranking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[n1e](https://clawhub.ai/user/n1e) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and market-analysis agents use this skill to retrieve and summarize currently popular A-share stocks across Wencai, Xueqiu, and Eastmoney. It is suited for questions about hot stocks, stock heat rankings, popularity rankings, and market attention lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a large opaque JavaScript browser-emulation helper for Wencai signature generation. <br>
Mitigation: Review the helper before installation and run the skill in a restricted environment with no credentials or sensitive browser sessions. <br>
Risk: The skill fetches live ranking data from external financial-data websites and may fail or return incomplete results if those services change behavior. <br>
Mitigation: Treat outputs as informational ranking data, check source availability, and verify important market decisions against authoritative financial sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/n1e/stock-heat-rank-py) <br>
- [Publisher profile](https://clawhub.ai/user/n1e) <br>
- [Wencai](https://www.iwencai.com/) <br>
- [Xueqiu hot stocks](https://xueqiu.com/hot/stock) <br>
- [Eastmoney stock rank API](https://emappdata.eastmoney.com/stockrank/getAllCurrentList) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Console table or JSON ranking data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces ranked A-share stock records with code, name, per-source ranks, composite score, and source appearance count.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
