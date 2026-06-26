## Description: <br>
Creates WooCommerce draft product listings with images, variants, and margin calculation from CJ Dropshipping products using product ID and sell price. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zero2Ai-hub](https://clawhub.ai/user/Zero2Ai-hub) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
E-commerce operators and automation agents use this skill to preview or create WooCommerce draft listings from CJ Dropshipping product IDs, including images, variants, pricing, margin checks, and product links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill accesses CJ Dropshipping and WooCommerce APIs using local credential files. <br>
Mitigation: Use staging or limited-scope credentials where possible, keep credential JSON files out of shared folders, logs, and repositories, and verify the configured store URL before execution. <br>
Risk: Normal execution can create WooCommerce product drafts and upload media. <br>
Mitigation: Run with --dry-run first and review product details, pricing, margin, category, and store target before allowing writes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Zero2Ai-hub/skill-dropshipping-product-launcher) <br>
- [Publisher Profile](https://clawhub.ai/user/Zero2Ai-hub) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, API calls] <br>
**Output Format:** [Console text with a machine-readable JSON result block] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run in dry-run mode; normal execution writes draft products and media through CJ Dropshipping and WooCommerce APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
