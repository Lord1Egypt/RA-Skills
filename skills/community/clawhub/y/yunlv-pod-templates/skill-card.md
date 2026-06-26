## Description: <br>
Yunlv Pod Templates helps users generate POD design keywords, product-title templates, listing copy, pricing references, and launch guidance for custom print products. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangm-a3](https://clawhub.ai/user/wangm-a3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External POD sellers and e-commerce operators use this skill to create AI design prompts, title and listing templates, pricing references, and launch checklists for print-on-demand products across platforms such as Amazon, Etsy, TikTok Shop, and Shopify. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use TRADEGPT_API_KEY and send category or platform descriptions to an external TradeGPT API. <br>
Mitigation: Provide only the minimum needed prompt context, avoid confidential shop strategy or personal data, and manage the API key as a sensitive credential. <br>
Risk: Generated POD designs, titles, and listing copy can still create copyright, trademark, pricing, or platform-compliance issues. <br>
Mitigation: Manually review generated designs, listing text, pricing, and platform policy fit before publishing or selling products. <br>
Risk: Template outputs are reusable starting points and may contain placeholders or generic claims unsuitable for a specific product. <br>
Mitigation: Replace placeholders, adapt platform-specific lengths and claims, and verify each SKU before listing. <br>


## Reference(s): <br>
- [POD design keywords](references/pod_design_keywords.md) <br>
- [POD title templates](references/pod_title_templates.md) <br>
- [POD listing copy](references/pod_listing_copy.md) <br>
- [Yunlv homepage](https://yunlvai.com) <br>
- [Yunlv TradeGPT API](https://api.yunlvai.com) <br>
- [ClawHub skill page](https://clawhub.ai/wangm-a3/yunlv-pod-templates) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance and reusable templates, with JSON output from the bundled CLI script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require TRADEGPT_API_KEY for TradeGPT API-backed usage; template and pricing outputs should be manually reviewed before publication.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and clawhub.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
