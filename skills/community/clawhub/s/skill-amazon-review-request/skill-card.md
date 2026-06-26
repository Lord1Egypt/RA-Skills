## Description: <br>
Sends Amazon review requests for eligible shipped orders using SP-API with retry, deduplication, eligibility checks, and optional dry-run mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zero2Ai-hub](https://clawhub.ai/user/Zero2Ai-hub) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Amazon seller account operators and automation agents use this skill to send review requests for eligible shipped orders through Amazon SP-API. It supports dry runs, retry handling, deduplication, and local run tracking before enabling recurring live sends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live execution can send real customer-facing Amazon review requests. <br>
Mitigation: Run `node scripts/request-reviews.js --dry-run` first, enable live runs only for an Amazon seller account you control, and delay cron scheduling until live-send behavior is approved. <br>
Risk: Order review-request metadata may be sent to Supabase if `~/supabase-api.json` or `SUPABASE_API_PATH` credentials are present. <br>
Mitigation: Remove or restrict Supabase credentials unless external logging is intended, and verify the destination table and access key permissions before live use. <br>
Risk: SP-API credentials grant access needed to fetch orders and send Messaging API requests. <br>
Mitigation: Use least-privilege SP-API credentials with only the required Messaging permission and keep credentials outside shared workspaces. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Zero2Ai-hub/skill-amazon-review-request) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Text, Files] <br>
**Output Format:** [Markdown instructions with CLI commands; runtime console summaries plus JSON and text logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Live runs can send customer-facing Amazon review requests and may sync review-request metadata to Supabase when local Supabase credentials exist.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
