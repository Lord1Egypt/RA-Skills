## Description: <br>
Manages household inventory through the local xiwu CLI, including search, item updates, expiration alerts, and purchase-suggestion context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnqxu](https://clawhub.ai/user/johnqxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to query and maintain household inventory, track expiring items, and produce structured context for alerts or restocking workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may automatically run a global pnpm or npm install for xiwu-niangzi when xiwu is missing. <br>
Mitigation: Install and verify the xiwu CLI manually first, or require explicit user approval before any global package installation. <br>
Risk: Household inventory records can reveal sensitive home, food, medicine, or purchasing details. <br>
Mitigation: Avoid storing sensitive household details unless you are comfortable with them being used in local alerts and purchase-suggestion workflows. <br>
Risk: Update and delete workflows can change or remove local inventory records. <br>
Mitigation: Review item IDs, quantities, and delete confirmations carefully before allowing write, update, or remove commands to run. <br>


## Reference(s): <br>
- [Xiwu Inventory on ClawHub](https://clawhub.ai/johnqxu/xiwu-inventory) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Natural-language responses and structured JSON from xiwu CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local xiwu command; inventory data is stored in the local xiwu database.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
