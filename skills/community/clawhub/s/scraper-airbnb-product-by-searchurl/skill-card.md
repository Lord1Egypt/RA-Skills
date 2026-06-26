## Description: <br>
Prepare Dataify builder requests for the airbnb.com scraper family rooted at airbnb_product_by-searchurl, including tool selection, parameter collection, and curl command generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to prepare Dataify Airbnb scraper builder requests from a selected tool and user-supplied parameters. It helps assemble environment-variable setup guidance and a ready-to-run curl command for the Dataify builder API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper script can expose a real Dataify API token in terminal output when building a curl command. <br>
Mitigation: Prefer commands that reference DATAIFY_API_TOKEN instead of printing the token value, and redact the Authorization header before sharing generated output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/scraper-airbnb-product-by-searchurl) <br>
- [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [Dataify builder API endpoint](https://scraperapi.dataify.com/builder) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash or PowerShell code blocks and JSON parameter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The primary output is a curl request that may include an Authorization header; generated commands should be reviewed before sharing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
