## Description: <br>
Use this skill when the user needs Twitter/X audience collection through Apify actors (followers/following/both) with optional email enrichment, username extraction from links, normalized row output, or webhook-ready payload building. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hundevmode](https://clawhub.ai/user/hundevmode) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Growth teams, founders, agencies, and operators use this skill to collect Twitter/X follower or following lists through Apify actors, optionally enrich usernames with emails, and produce normalized rows for outreach workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Apify credentials can be exposed if pasted into shared chats, checked into files, or retained in shell history. <br>
Mitigation: Keep APIFY_TOKEN in a secret manager or environment variable and avoid printing or sharing token values. <br>
Risk: Large actor runs and email enrichment can increase cost and may process contact data. <br>
Mitigation: Use modest limits for initial runs and enable email enrichment only with a lawful and appropriate basis to process contact data. <br>
Risk: Untrusted actor IDs could send data to actors outside the intended workflow. <br>
Mitigation: Use trusted Apify actor IDs and review actor configuration before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hundevmode/twitter-x-apify-actors) <br>
- [Actor Contracts](references/actor-contracts.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Apify followers/following actor](https://console.apify.com/actors/bIYXeMcKISYGnHhBG) <br>
- [Apify email enrichment actor](https://console.apify.com/actors/mSaHt2tt3Z7Fcwf0o) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON output from the runner script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APIFY_TOKEN; run-pipeline returns targetUsername, collectType, includeEmails, totalCollected, emailsFound, and rows with username, name, email, sourceType, and collectedAt.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
