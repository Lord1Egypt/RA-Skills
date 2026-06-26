## Description: <br>
Complete memory system combining Baidu Embedding auto-recall, Git-Notes structured memory, and file-based workspace search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xqicxx](https://clawhub.ai/user/xqicxx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to add persistent memory across sessions, combining semantic recall, structured Git-Notes storage, and workspace file search for decisions, preferences, tasks, and contextual knowledge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation memories and search queries may be stored long term. <br>
Mitigation: Review retention behavior before deployment and avoid storing secrets, regulated data, personal data, or proprietary content unless retention controls are acceptable. <br>
Risk: Configured Baidu embedding use may send memory content or search queries to Baidu. <br>
Mitigation: Use Baidu credentials only in environments where that data flow is approved, and run in degraded mode without credentials when external embedding calls are not acceptable. <br>
Risk: The skill instructs silent memory operation, which can reduce user visibility into what is being stored. <br>
Mitigation: Add user-visible consent, disclosure, review, or deletion controls before using the skill with sensitive or user-specific information. <br>
Risk: Security evidence flags unresolved concerns with privacy claims, .env loading, script quoting, and retention controls. <br>
Mitigation: Review and fix those implementation details before production use, then rescan the release before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xqicxx/triple-memory-baidu-embedding) <br>
- [Baidu Qianfan console](https://console.bce.baidu.com/qianfan/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces memory setup and operation guidance; configured use may persist conversation memories and send embedding requests to Baidu.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
