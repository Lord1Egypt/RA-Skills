## Description: <br>
Calculates Amazon UAE FBA fees, net margin, and dangerous-goods risk for CJ Dropshipping product candidates, ranking SKUs by margin and producing report outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zero2Ai-hub](https://clawhub.ai/user/Zero2Ai-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketplace operators and ecommerce teams use this skill to evaluate CJ Dropshipping products before Amazon UAE FBA launch decisions. It estimates landed cost, FBA fee tier, referral and storage fees, net margin, and dangerous-goods handling posture for one or more SKUs. <br>

### Deployment Geography for Use: <br>
Global, with calculations tailored to Amazon UAE. <br>

## Known Risks and Mitigations: <br>
Risk: The local script can read the input JSON path provided by the user and overwrite .md or .json report files at the selected output base path. <br>
Mitigation: Run it only in a trusted workspace and choose input and output paths deliberately before execution. <br>
Risk: Fee tiers, exchange rates, storage fees, and dangerous-goods handling are estimates that can affect product selection decisions. <br>
Mitigation: Verify final FBA fees, dangerous-goods eligibility, and current marketplace assumptions in Amazon Seller Central before ordering samples or shipping inventory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Zero2Ai-hub/skill-fba-margin-calculator) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown report tables and JSON result arrays, with optional shell commands for local Node.js execution.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads product data from command flags, a JSON file, or stdin; optionally writes paired .md and .json report files at the chosen output base path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
