## Description: <br>
Generates pricing strategy suggestions, market pricing reference reports, and competitive positioning guidance for B2B export businesses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangm-a3](https://clawhub.ai/user/wangm-a3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External business users and agents use this skill to prepare market pricing references, compare competitor pricing, and generate pricing adjustment guidance for export sales decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pricing prompts may include confidential customer lists, margins, proprietary pricing models, or competitor research sent to the Yunlv API. <br>
Mitigation: Use a dedicated API key where possible and avoid submitting confidential business details unless the user trusts the Yunlv service. <br>
Risk: Pricing guidance can be misleading if the skill is used on broad pricing questions without business review. <br>
Mitigation: Confirm the skill is relevant to the pricing scenario and review generated recommendations before acting on them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wangm-a3/yunlv-pricing) <br>
- [Yunlv Homepage](https://yunlvai.com) <br>
- [Yunlv TradeGPT API](https://api.yunlvai.com) <br>
- [Competitor List Template](references/competitor_list_template.md) <br>
- [Price Analysis Report Template](references/price_analysis_report.md) <br>
- [Pricing Strategy Guide](references/pricing_strategy_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports and guidance, with optional JSON examples, configuration snippets, and shell command outputs from the bundled pricing calculator.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require TRADEGPT_API_KEY for Yunlv TradeGPT API requests; generated reports and recommendations should be reviewed before pricing decisions.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and clawhub.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
