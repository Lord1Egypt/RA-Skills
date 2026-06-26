## Description: <br>
Constructs or locates compliant virtual test products by category, business identity, product attributes, or item tags, then can clone, reprice, and clean tags for test listings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cpu-hammer](https://clawhub.ai/user/cpu-hammer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketplace QA, operations, and engineering users can use this skill to find or construct virtual test product listings, clone eligible items to test seller accounts, set test prices, and remove inappropriate item tags. It is intended for test-item workflows, not general product administration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can call internal services that mutate marketplace item state, including clone, price, tag, and listing-status operations. <br>
Mitigation: Install only in trusted environments, confirm backend authorization restricts changes to test items and accounts, and require explicit approval before each mutating action. <br>
Risk: The skill sends user and system context to Alibaba internal services while resolving and modifying product records. <br>
Mitigation: Avoid sensitive production data in prompts and limit use to approved internal test-item workflows. <br>
Risk: The category and SPU helper broadens the skill beyond virtual test-item construction. <br>
Mitigation: Remove or disable that helper when the deployment only needs virtual test-product construction. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cpu-hammer/virtual-item-constructor) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/cpu-hammer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown text with command examples and a structured final product summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include product IDs, titles, prices, seller names, item tags, and Taobao item links when construction succeeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact package.json reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
