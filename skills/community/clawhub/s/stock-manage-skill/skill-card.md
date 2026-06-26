## Description: <br>
股票管理技能，支持股票订单管理、交易规则管理和股票信息获取。支持A股、港股、美股等多种股票类型，使用本地文本目录存储数据。Use when user wants to manage stock orders, trading rules or get stock information including adding, deleting, updating, and querying orders and rules, and fetching real-time stock data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a925907195](https://clawhub.ai/user/a925907195) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to manage local stock orders, trading rules, quote snapshots, backups, and logs for A-share, Hong Kong, and U.S. stocks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores stock orders, rules, quantities, platforms, quote snapshots, logs, and backups as local plaintext files. <br>
Mitigation: Use it only in a trusted local workspace and avoid storing sensitive trading data unless local file permissions and retention are acceptable. <br>
Risk: Stock quote retrieval sends stock codes to third-party quote providers. <br>
Mitigation: Confirm that the selected markets and stock codes can be shared with those providers before enabling quote lookups. <br>
Risk: The log delete-by-file command can delete files outside the intended log directory if the filename is not constrained. <br>
Mitigation: Avoid or restrict delete-by-file usage until path validation ensures the target remains inside the configured log directory. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local plaintext JSON data, backups, logs, and stock quote retrieval guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
