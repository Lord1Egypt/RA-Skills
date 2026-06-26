## Description: <br>
Local SiYuan API integration for notebook, document, block, asset, database/attribute view, and limited SQL operations. Restricted to local HTTP endpoints and environment-based token auth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xybio](https://clawhub.ai/user/xybio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and note automation users use this skill to operate a local SiYuan workspace through reviewed notebook, document, block, asset, database, and limited read-oriented SQL API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automate changes to a user's local SiYuan workspace, including document, block, asset, database, and workspace file operations. <br>
Mitigation: Confirm the target local endpoint, prefer structured SiYuan APIs, ask before destructive operations, and stay within user-requested workspace content. <br>
Risk: The SiYuan API token grants high-trust local access if exposed. <br>
Mitigation: Read the token from SIYUAN_API_TOKEN only, and never hardcode, echo, log, or include it in generated examples beyond placeholders. <br>
Risk: SQL and file APIs can cause broad reads or unintended changes if used without bounds. <br>
Mitigation: Prefer SELECT queries with LIMIT, avoid mutation-heavy SQL, and use file APIs only for clearly requested SiYuan workspace content or assets. <br>
Risk: Network proxying and conversion endpoints expand the skill's attack surface beyond local note management. <br>
Mitigation: Do not use /api/network/forwardProxy, /api/convert/pandoc, or endpoints intended for outbound proxying, external conversion, or indirect execution. <br>


## Reference(s): <br>
- [SiYuan project](https://github.com/siyuan-note/siyuan) <br>
- [SiYuan Safe API Reference](references/safe-api.md) <br>
- [ClawHub skill page](https://clawhub.ai/xybio/siyuan-api) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/xybio) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with JavaScript, SQL, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SIYUAN_API_TOKEN and SIYUAN_API_URL environment variables; outputs should target only a confirmed local SiYuan endpoint.] <br>

## Skill Version(s): <br>
1.4.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
