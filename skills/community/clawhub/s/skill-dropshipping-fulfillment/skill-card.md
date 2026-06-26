## Description: <br>
Automates order fulfillment by pushing WooCommerce orders to CJ Dropshipping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zero2Ai-hub](https://clawhub.ai/user/Zero2Ai-hub) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Store operators and developers use this skill to automate WooCommerce order fulfillment through CJ Dropshipping, including SKU-to-variant matching, order submission, WooCommerce status updates, and fulfillment logging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The fulfillment script can submit live CJ Dropshipping orders and update WooCommerce order status using stored credentials. <br>
Mitigation: Use least-privileged WooCommerce and CJ API credentials, run dry-run first, and test with a single order before processing all orders. <br>
Risk: The mapping rebuild script can backfill WooCommerce SKUs and rewrite the supplier selection mapping. <br>
Mitigation: Treat rebuild-mapping.js as a live catalog-mutation tool, run it with --dry-run first, and review mapping output before allowing live writes. <br>
Risk: Credential JSON files are required for WooCommerce and CJ Dropshipping access. <br>
Mitigation: Keep credential files outside the repository with restricted file permissions and provide paths through environment variables. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Zero2Ai-hub/skill-dropshipping-fulfillment) <br>
- [Publisher profile](https://clawhub.ai/user/Zero2Ai-hub) <br>
- [CJ Dropshipping API](https://developers.cjdropshipping.com/api2.0/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples; runtime scripts emit console text and JSON log files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces fulfillment and rejection logs, and can update the CJ supplier selection mapping.] <br>

## Skill Version(s): <br>
1.2.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
