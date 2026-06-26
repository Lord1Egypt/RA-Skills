## Description: <br>
Analyzes Xiaohongshu posts about errand and delivery services by filtering keywords and dates, classifying sentiment and feedback categories, and producing Markdown reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qinghuan2000](https://clawhub.ai/user/qinghuan2000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations, product, and research teams use this skill to monitor Xiaohongshu discussion of errand and delivery services, summarize user sentiment, identify recurring feedback themes, and prepare Markdown reports for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may collect and retain more raw social-media content than needed for analysis. <br>
Mitigation: Narrow keywords, date ranges, and result limits before each run, and define retention and redaction rules for raw post data and generated reports. <br>
Risk: The workflow uses a logged-in Chrome session and can interact with a shared KM document. <br>
Mitigation: Run it only from an approved browser profile, verify the target KM document, and review generated Markdown before publishing or inserting it. <br>
Risk: Post text may be sent to the configured internal LLM endpoint. <br>
Mitigation: Confirm the data flow is approved for the content being processed and remove or protect hardcoded credentials before scheduled or shared use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/qinghuan2000/xhs-feedback-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/qinghuan2000) <br>
- [KM report destination](https://km.sankuai.com/collabpage/2751219981) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports and JSON analysis files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include sentiment, service category, feedback category, source links, and representative posts.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
