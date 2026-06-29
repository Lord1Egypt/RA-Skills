## Description: <br>
Analyzes legally obtained ecommerce review text for Amazon, Shopify, and TikTok Shop and returns structured JSON with sentiment themes, complaint causes, improvement suggestions, and reply-template drafts through the Yufluent cloud harness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[metahuan](https://clawhub.ai/user/metahuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ecommerce sellers and operations teams use this skill to turn legally obtained buyer review text into VOC themes, complaint causes, prioritized improvement suggestions, and response drafts for Amazon, Shopify, or TikTok Shop workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive TOKENAPI_KEY credential. <br>
Mitigation: Store the key in an environment variable or approved secret store, do not paste it into prompts or logs, and set TOKENAPI_BASE_URL only to a trusted endpoint. <br>
Risk: Review text is sent to the Yufluent cloud service for analysis. <br>
Mitigation: Remove buyer names, addresses, phone numbers, regulated data, and confidential business data unless the use has been approved. <br>
Risk: Generated reply templates and recommendations may be incomplete or unsuitable for a specific marketplace policy or customer situation. <br>
Mitigation: Have a human review action items and reply drafts before using them in customer-facing communications. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/metahuan/yufluent-clawhub-publish-yufluentcn-review-intel) <br>
- [Yufluent homepage](https://claw.changzhiai.com) <br>
- [OpenClaw integration](https://claw.changzhiai.com/app/openclaw) <br>
- [Skill source overview](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Shell commands, Guidance] <br>
**Output Format:** [Structured JSON insight report, optionally saved to a UTF-8 JSON file, with brief text interpretation by the agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOKENAPI_KEY and sends provided review text to the Yufluent cloud service; avoid PII, regulated data, and confidential business data unless approved.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
