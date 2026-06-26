## Description: <br>
Virtual User Skill helps agents retrieve local user-research scenarios, generate virtual user profiles, conduct simulated interviews, and summarize product feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chuxin-wenxiang](https://clawhub.ai/user/chuxin-wenxiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product researchers, and product teams use this skill to turn local research scenario data into virtual user personas, interview-style responses, and product-evaluation reports. It is intended for local scenario-library workflows rather than an external API-backed interview agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can over-ingest or expose sensitive user-research data. <br>
Mitigation: Review and minimize source spreadsheets before import, de-identify sensitive fields, and avoid exposing raw scenario JSON or plaintext sample exports. <br>
Risk: Local encrypted data depends on the secrecy of ~/.virtual_user/.key. <br>
Mitigation: Keep the key local, set restrictive file permissions, and do not share, commit, or log the key material. <br>
Risk: Merge and preparation scripts may process unreviewed spreadsheet data from local folders. <br>
Mitigation: Run data merge scripts only after every spreadsheet has been reviewed for scope, provenance, and sensitive content. <br>
Risk: The deployment guide includes an unauthenticated Flask API example that could expose research data if published directly. <br>
Mitigation: Do not expose the API example without authentication, TLS, rate limits, logging controls, and network restrictions. <br>
Risk: Unpinned Python dependencies can change behavior or introduce supply-chain risk. <br>
Mitigation: Pin dependency versions and review dependency updates before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chuxin-wenxiang/virtual-user-skill) <br>
- [SKILL.md](SKILL.md) <br>
- [README.md](README.md) <br>
- [DEPLOYMENT.md](DEPLOYMENT.md) <br>
- [Data Template Guide](data/数据模板说明.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Conversational text, structured JSON search results, Markdown reports, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local vector retrieval over encrypted scenario data; default search_top_k is 20 and the configured report format is Markdown.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
