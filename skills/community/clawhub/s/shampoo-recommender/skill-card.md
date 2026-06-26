## Description: <br>
娜可露露洗发水推荐助手 helps an agent recommend brand-specific shampoo products based on hair type, scalp concerns, usage scenario, and budget. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crazyXingXing](https://clawhub.ai/user/crazyXingXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to collect basic hair-care requirements and produce concise shampoo recommendations for the 娜可露露 product line. It is especially oriented toward daily care and swimming-related scenarios such as chlorine or saltwater exposure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a brand-specific commercial recommender and may make product guidance sound more definitive than the available product evidence supports. <br>
Mitigation: Review product claims critically and confirm current product details before relying on or publishing recommendations. <br>
Risk: Broad activation wording can cause the skill to engage for generic shampoo queries where the user did not explicitly ask for this brand. <br>
Mitigation: Confirm the user wants 娜可露露 recommendations before narrowing the conversation to that product line. <br>
Risk: Optional Python helper scripts include hard-coded local paths and are not required for normal recommendation use. <br>
Mitigation: Run helper scripts only intentionally after updating paths for the local skill directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/crazyXingXing/shampoo-recommender) <br>
- [Product reference](references/products.md) <br>
- [FAQ](references/faq.md) <br>
- [Usage examples](references/examples.md) <br>
- [Asset guide](assets/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown conversational guidance with optional Python snippets and generated recommendation-card files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include product rationales, use instructions, price ranges, comparison tables, and optional local asset-generation steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence and PACKAGE.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
