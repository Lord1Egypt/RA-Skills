## Description: <br>
Monitors a configured Xiaohongshu (RedNote) user's recent post titles for configured keywords and sends WeChat alerts when matches appear. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawntribbiani](https://clawhub.ai/user/shawntribbiani) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to track time-sensitive Xiaohongshu seller or trader updates by configuring target users, keywords, cookies, and WeChat notification settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles live Xiaohongshu account cookies. <br>
Mitigation: Use it only on a trusted private machine, preferably with a dedicated Xiaohongshu account, and protect or remove cookie files after use. <br>
Risk: The bundled helper exposes broader Xiaohongshu account-action tools than read-only monitoring requires. <br>
Mitigation: Remove or restrict generic MCP helper actions when only read-only monitoring is needed. <br>
Risk: The workflow depends on downloaded xiaohongshu-mcp binaries. <br>
Mitigation: Verify downloaded MCP binaries before installing or running them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shawntribbiani/rockingland-trader-monitor) <br>
- [Configuration and troubleshooting guide](artifact/trader_rules.md) <br>
- [xiaohongshu-mcp releases](https://github.com/xpzouying/xiaohongshu-mcp/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python configuration, and JSON cookie/state files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces WeChat alert text at runtime and maintains a local JSON state file to avoid duplicate notifications.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
