## Description: <br>
Import products from Shopify, Wix, WordPress, and Amazon directly into WooCommerce via natural language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[colaliang](https://clawhub.ai/user/colaliang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an OpenClaw agent queue product imports from Shopify, Wix, WordPress, or Amazon into WooCommerce and check import job status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends product import data to a remote Yundian+ API using an API key. <br>
Mitigation: Install only when Yundian+ is trusted for the intended product data and keep YUNDIAN_WOO_IMPORTER_API_KEY private. <br>
Risk: An incorrect or non-HTTPS API endpoint could send import requests to the wrong service. <br>
Mitigation: Verify YUNDIAN_WOO_IMPORTER_API_URL is the intended HTTPS endpoint before use. <br>
Risk: Bulk or all-products imports can affect a large WooCommerce catalog. <br>
Mitigation: Confirm the source store, target store, and product scope before running broad import requests. <br>


## Reference(s): <br>
- [Yundian+ homepage](https://ydplus.net) <br>
- [ClawHub skill listing](https://clawhub.ai/colaliang/yundian-woo-importer) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, configuration, guidance] <br>
**Output Format:** [JSON tool responses and concise status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires YUNDIAN_WOO_IMPORTER_API_KEY and access to the intended Yundian+ API endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
