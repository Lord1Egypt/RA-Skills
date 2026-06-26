## Description: <br>
查询 Shodan 物联网搜索引擎获取设备信息、安全数据和网络资产；当用户需要进行 IP 地址分析、设备搜索、DNS 查询、网络安全评估或获取物联网设备信息时使用 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Moxin1044](https://clawhub.ai/user/Moxin1044) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security analysts, and asset owners use this skill to query Shodan for host details, device search results, DNS data, port information, and account status. Agents can use the returned data to summarize internet-exposed assets, identify security-relevant signals, and draft structured assessment reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lookup targets are sent to Shodan and may reveal sensitive internal domains, customer names, or investigation targets. <br>
Mitigation: Confirm targets before querying and avoid submitting sensitive or unauthorized targets. <br>
Risk: The Shodan API key may appear in full request URLs, logs, or screenshots. <br>
Mitigation: Use a dedicated Shodan API key and redact full API URLs from logs, screenshots, and shared reports. <br>


## Reference(s): <br>
- [Shodan API reference](references/api-reference.md) <br>
- [Shodan developer API documentation](https://developer.shodan.io/api) <br>
- [ClawHub skill page](https://clawhub.ai/Moxin1044/shodan-skills) <br>
- [Third-party publisher profile](https://clawhub.ai/user/Moxin1044) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SHODAN_API_KEY and sends lookup targets to Shodan.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
