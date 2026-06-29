## Description: <br>
瑞玥餐饮API helps an agent answer restaurant, reservation, menu, ordering, membership, and transaction questions through merchant tools while keeping user-facing replies in complete Chinese business language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhimibuhui](https://clawhub.ai/user/zhimibuhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Restaurant operators and customer-facing agents use this skill to query shop details, menus, tables, reservations, member information, transaction history, and dining orders for a configured merchant environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read member and transaction records from a live merchant system. <br>
Mitigation: Install only for the intended merchant environment and confirm backend authorization enforces tenant, shop, and user ownership before enabling member or transaction lookups. <br>
Risk: The skill can create, change, or cancel live reservations and dining orders. <br>
Mitigation: Require clear user authorization before booking, ordering, reducing, appending, or canceling, and keep the configured private API endpoint restricted to trusted deployments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhimibuhui/skills/ry-drink) <br>
- [Tool schema](artifact/tools.json) <br>
- [Tool routing guidance](artifact/tool-router.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, guidance] <br>
**Output Format:** [Chinese business replies with silent tool-backed API interactions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [User-facing replies should hide tool names, internal identifiers, order numbers, reservation numbers, and backend error details.] <br>

## Skill Version(s): <br>
1.0.18 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
