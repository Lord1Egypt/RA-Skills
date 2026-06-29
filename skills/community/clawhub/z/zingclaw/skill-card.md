## Description: <br>
Calls ZingAPI's creative-list endpoint to search ad creatives, materials, delivery records, advertisers, and recent creatives by industry, country or region, platform, keyword, creative type, AI tags, time range, and sort order. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zingfront-ad](https://clawhub.ai/user/zingfront-ad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and marketing analysts use this skill to turn natural-language ad creative search requests into signed ZingAPI creative-list calls and concise result summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ZingAPI credentials can be exposed if users paste environment values, dry-run output, or logs into shared channels. <br>
Mitigation: Configure credentials only through environment variables and avoid sharing dry-run headers, logs, or chat transcripts that may contain credential-derived request metadata. <br>
Risk: The skill sends signed requests to an external ZingAPI production endpoint and may consume account quota. <br>
Mitigation: Use the dry-run mode to inspect request bodies before sending, and run live queries only with an intended ZingAPI customer account. <br>


## Reference(s): <br>
- [ZingAPI creative-list endpoint](https://openapi.dataideaglobal.com/zingapi/v1/creative/list/{customer_name}) <br>
- [Parameters](references/parameters.md) <br>
- [Input Mapping](references/input-mapping.md) <br>
- [Response Fields](references/response-fields.md) <br>
- [Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output is a grouped summary; raw JSON is available on request. The skill requires ZingAPI credentials in environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
