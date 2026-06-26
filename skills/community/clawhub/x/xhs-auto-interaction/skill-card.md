## Description: <br>
Automates Xiaohongshu searches, browsing, likes, and favorites through a local MCP service while tracking interaction history to reduce repeated actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luckychay](https://clawhub.ai/user/luckychay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operators with a logged-in Xiaohongshu account use this skill to run scheduled searches and apply likes and favorites to selected posts while recording local interaction history. It is intended for automated social-media engagement workflows that require review before live account use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automates Xiaohongshu likes and favorites from a logged-in account without per-post approval. <br>
Mitigation: Review the script before execution, use a test account where possible, and add a dry-run or approval step before enabling live engagement. <br>
Risk: Repeated scheduled execution may trigger account, platform-policy, or rate-limit issues. <br>
Mitigation: Keep cron frequency low, monitor logs and history, adjust MAX_ATTEMPTS, and disable scheduling if platform limits appear. <br>
Risk: Log and history files store interaction details in fixed local paths. <br>
Mitigation: Fix hardcoded paths for the deployment environment and periodically delete or protect the log and history files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luckychay/xhs-auto-interaction) <br>
- [Publisher profile](https://clawhub.ai/user/luckychay) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with bash scripts and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local Xiaohongshu MCP service, curl, jq, and a logged-in account.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
