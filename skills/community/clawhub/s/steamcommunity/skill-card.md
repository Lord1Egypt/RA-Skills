## Description: <br>
Retrieves Steam inventory data and manages trade offers on steamcommunity.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bluesyparty-src](https://clawhub.ai/user/bluesyparty-src) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Steam users use this skill to retrieve Steam inventory JSON, inspect item metadata, and prepare or manage Steam trade offers with curl and jq. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires live Steam cookies, a session ID, and a Steam Web API key, which can expose authenticated account access if logged or shared. <br>
Mitigation: Use a trusted temporary shell, keep credentials out of files and logs, rotate or refresh credentials after use, and avoid committing environment values. <br>
Risk: Trade offer send and accept commands can change ownership of Steam inventory items. <br>
Mitigation: Prefer read-only inventory commands unless trading is intentional, and manually verify the partner, token, asset IDs, item lists, and confirmation prompts before executing trade-changing commands. <br>
Risk: Steam inventory and trade endpoints may be rate-limited or fail when sessions expire. <br>
Mitigation: Space requests out, handle failed responses before retrying, and refresh cookies from a current browser session when authentication stops working. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bluesyparty-src/steamcommunity) <br>
- [Steam Community developer portal](https://steamcommunity.com/dev) <br>
- [Steam Web API key registration](https://steamcommunity.com/dev/apikey) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash and curl command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may return Steam inventory and trade offer JSON through curl and jq.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
