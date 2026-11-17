## Description: <br>
Smart Crawler Free helps agents run a local Notion archive and read-only search workflow for personal knowledge bases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, writers, and knowledge workers use this skill to sync a single Notion workspace into a local archive, check freshness, search notes, run basic read-only SELECT queries, and produce workspace reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CLI sync and export workflows can mirror private Notion workspace content into local storage. <br>
Mitigation: Use a read-only Notion integration token, share only intended pages or databases, set SMART_CRAWLER_HOME deliberately, and confirm before sync, import, reset, delete, or export actions. <br>
Risk: The security summary flags partly inconsistent scope and read-only claims. <br>
Mitigation: Review commands before execution, restrict SQL usage to SELECT queries, and avoid granting write-capable credentials or broad workspace access. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and structured command output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON status snippets and local archive/search configuration guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
