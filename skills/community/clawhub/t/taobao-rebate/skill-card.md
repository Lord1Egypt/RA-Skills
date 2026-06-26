## Description: <br>
A Chinese-language rebate assistant that routes users through authorization help, Taobao/JD/Pinduoduo rebate-link generation, product search, balance checks, and withdrawal flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skyfile](https://clawhub.ai/user/skyfile) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to find rebate-eligible shopping results, convert supported marketplace links into rebate links, and manage rebate account guidance such as authorization, balances, and withdrawal requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores WeChat-linked identifiers locally and uses them for account, rebate, and withdrawal flows. <br>
Mitigation: Install only for trusted users and publishers, and review local stored account identifiers before deployment in shared or regulated environments. <br>
Risk: The skill contacts an external rebate backend for product search, rebate-link creation, balance checks, and withdrawal operations. <br>
Mitigation: Confirm the backend endpoint, network policy, and publisher trust before enabling the skill, especially where shopping or account data is sensitive. <br>
Risk: Withdrawal confirmations can trigger real money or account actions. <br>
Mitigation: Require explicit user confirmation for withdrawal steps and review withdrawal behavior before allowing production use. <br>
Risk: Shopping queries may be processed by the workspace model provider without clear user-facing disclosure. <br>
Mitigation: Disclose model-provider processing to users and avoid sending sensitive shopping or account details unless required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/skyfile/taobao-rebate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown user messages with script-backed rebate, search, account, and withdrawal results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Script output is intended to be returned verbatim to the user.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
