## Description: <br>
Helps agents translate Chinese stock and market-data questions into authenticated yyqdata OpenAPI REST calls for A-share, Hong Kong, U.S. equity, fund, macro, derivative, research, forex, and related datasets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kouyusanpi](https://clawhub.ai/user/kouyusanpi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and market-data users use this skill to let an agent resolve Chinese stock questions, authenticate with a yyqdata token, call documented REST endpoints, and return market, financial, macro, and screening results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A bearer token may be exposed or used with broader privileges than needed. <br>
Mitigation: Use a platform secret or 0600 config file, avoid query-string authentication when headers are available, and provide only a narrowly scoped data token. <br>
Risk: The bundled updater can download and replace the installed skill from the publisher's server. <br>
Mitigation: Run update.sh only after trusting the publisher and accepting the replacement behavior; do not execute it automatically during ordinary data lookups. <br>
Risk: Agent-visible admin and token-management documentation goes beyond ordinary market-data queries. <br>
Mitigation: Keep routine agent use limited to data lookup endpoints and require human review before token administration or provisioning actions. <br>


## Reference(s): <br>
- [Yyqdata manifest](https://static.yyqyx.com/skill/yyqdata.manifest.json) <br>
- [ClawHub skill page](https://clawhub.ai/kouyusanpi/yyqdata-stock-skill) <br>
- [API quick reference](references/api-quick-reference.md) <br>
- [Full API specification](references/api-full-spec.md) <br>
- [Data catalog](references/data-catalog.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON request bodies and bash/curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an agent-held yyqdata bearer token and outbound HTTP access; responses should preserve trace IDs when reporting failures or empty results.] <br>

## Skill Version(s): <br>
3.5.31 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
