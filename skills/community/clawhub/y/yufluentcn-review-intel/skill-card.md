## Description: <br>
Yufluentcn Review Intel helps agents format cross-border ecommerce buyer reviews, run Yufluent cloud review analysis, and summarize structured sentiment, complaint, praise, action item, and reply-template insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[metahuan](https://clawhub.ai/user/metahuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, ecommerce operators, and their agents use this skill to analyze legally obtained Amazon, Shopify, or TikTok Shop review text for sentiment themes, complaint drivers, product or service improvements, and draft buyer response templates. The skill is intended for internal review intelligence and requires human review before acting on generated recommendations or reply drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review text and product or platform context are sent to Yufluent's cloud service using TOKENAPI_KEY. <br>
Mitigation: Use only review data you are authorized to process and redact names, addresses, order IDs, and other sensitive or regulated data before analysis. <br>
Risk: TOKENAPI_BASE_URL can redirect requests to a different endpoint if configured. <br>
Mitigation: Leave TOKENAPI_BASE_URL unset for the default service or set it only to an endpoint you trust. <br>
Risk: Generated action items and reply templates may be incomplete, inaccurate, or unsuitable for a marketplace policy context. <br>
Mitigation: Treat outputs as drafts for internal review and have a human verify recommendations and buyer replies before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/metahuan/yufluentcn-review-intel) <br>
- [Publisher profile](https://clawhub.ai/user/metahuan) <br>
- [Yufluent homepage](https://claw.changzhiai.com) <br>
- [Yufluent OpenClaw integration](https://claw.changzhiai.com/app/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and structured JSON review insight output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOKENAPI_KEY. Review text can be passed inline or read from a UTF-8 file; optional output can be saved to a JSON file.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
