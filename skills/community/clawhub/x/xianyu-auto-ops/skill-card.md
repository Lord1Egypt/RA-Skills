## Description: <br>
Bilingual Xianyu (闲鱼) listing and lightweight operations workflow for second-hand goods, side-hustle products, and marketplace distribution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinhuadeng](https://clawhub.ai/user/jinhuadeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, operators, and marketplace assistants use this skill to turn product details or SKU data into Xianyu listing packages, buyer reply scripts, pricing guidance, image prompts, and posting checklists in Chinese and English. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated listing copy could contain incorrect pricing, warranty, defect, or delivery claims if source product data is incomplete. <br>
Mitigation: Review generated claims, prices, warranties, and defect disclosures before posting, and provide only SKU or product CSVs intended for agent review. <br>
Risk: Virtual goods, AI services, and training offers can be misleading if delivery scope or support boundaries are vague. <br>
Mitigation: State exactly what is delivered, how delivery happens, what support is included, and what outcomes are not guaranteed. <br>


## Reference(s): <br>
- [Xianyu Auto Ops Playbook](references/playbook.md) <br>
- [AI Services / Training / Installation Template](references/ai-services-template.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jinhuadeng/xianyu-auto-ops) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with bilingual listing copy, bullet lists, optional inline shell commands, and JSON-derived batch summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use a local CSV normalizer for batch listing inputs; outputs should keep assumptions explicit and preserve disclosed defects.] <br>

## Skill Version(s): <br>
0.3.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
