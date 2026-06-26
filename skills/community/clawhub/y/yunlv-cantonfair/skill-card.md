## Description: <br>
Generates Canton Fair lead discovery strategies, exhibitor and buyer references, and personalized outreach plans for trade show customer development. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangm-a3](https://clawhub.ai/user/wangm-a3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External trade teams and B2B customer-development users use this skill to plan Canton Fair prospecting, score buyer profiles, organize booth and product-category references, and draft follow-up outreach. The skill can also guide agents through local planner commands and Yunlv MatchGPT API-backed lead-generation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an external Yunlv API and a TRADEGPT_API_KEY while handling lead-generation inputs and prospect data. <br>
Mitigation: Install only if Yunlv API use and credential handling are acceptable; confirm what request data is sent to the API before using real prospect data. <br>
Risk: Generated lead lists, contact details, buyer scores, and outreach drafts may be sensitive or inaccurate. <br>
Mitigation: Manually verify contacts, scores, and compliance obligations before outreach, and treat generated files and messages as sensitive business data. <br>
Risk: Security evidence notes inconsistent data-flow and retention promises for generated lead and outreach files. <br>
Mitigation: Confirm storage locations, retention periods, and deletion behavior before using the skill with live customer or prospect information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangm-a3/yunlv-cantonfair) <br>
- [Yunlv homepage](https://yunlvai.com) <br>
- [Yunlv MatchGPT API](https://api.yunlvai.com) <br>
- [Canton Fair category reference](references/canton_fair_categories.md) <br>
- [Outreach template library](references/outreach_templates.md) <br>
- [Trade show follow-up strategy](references/followup_strategy.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and CLI JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRADEGPT_API_KEY for Yunlv API-backed workflows; generated lead lists, outreach drafts, and planner outputs may contain sensitive prospect data.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and clawhub.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
