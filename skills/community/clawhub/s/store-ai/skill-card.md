## Description: <br>
舌尖香港门店AI助手 helps store operators use Chinese natural-language requests to query inventory, sales, purchases, operation logs, and weather, and to prepare confirmed store-management API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xingke2023](https://clawhub.ai/user/xingke2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Store employees and trusted remote operators use this skill to manage fresh-food store operations through natural-language inventory, sales, purchase, account, log, and weather workflows. The skill is intended for the specific store-management API at s.xingke888.com and requires an authorized bearer token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can query and update inventory, sales supplements, purchase orders, and other operational store records through an authenticated API. <br>
Mitigation: Restrict use to trusted operators, require confirmation before write operations, and review operation summaries before approving changes. <br>
Risk: The skill requires sensitive bearer-token credentials for the intended store-management system. <br>
Mitigation: Provide the narrowest possible token, avoid sharing passwords when token setup is available, and keep credentials out of user-visible responses. <br>
Risk: Using the skill against the wrong service or store could expose data or modify unintended business records. <br>
Mitigation: Install only when s.xingke888.com is the intended store-management system and verify the store/account context before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xingke2023/store-ai) <br>
- [Store API base URL](https://s.xingke888.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese Markdown responses with operation summaries, confirmation prompts, query results, and single-line curl commands for API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a bearer token and is designed to avoid exposing internal execution details to store staff.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
