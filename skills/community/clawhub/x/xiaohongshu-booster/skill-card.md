## Description: <br>
Generate 3 viral-ready Xiaohongshu (Little Red Book) notes from a product, scene, or topic, including titles, body copy, hashtags, cover-image tips, and publish-time recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, social media operators, and marketing teams use this skill to draft Xiaohongshu note variants for products, venues, outfits, and lifestyle topics. It supports CLI and agent workflows for producing copy, hashtag sets, cover guidance, and timing suggestions from a small structured input. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated marketing-style copy may contain claims that are unsuitable or unsupported for sensitive categories such as skincare, supplements, medical-adjacent products, or performance claims. <br>
Mitigation: Review generated claims before use and enable or add disclaimers where appropriate; the security evidence notes that the skill does not publish posts or access accounts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/xiaohongshu-booster) <br>
- [Input schema](artifact/schemas/input.schema.json) <br>
- [Output schema](artifact/schemas/output.schema.json) <br>
- [Xiaohongshu writing templates](artifact/references/templates.md) <br>
- [Xiaohongshu hashtag library](artifact/references/hashtags.md) <br>
- [Xiaohongshu cover image tips](artifact/references/cover-tips.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [JSON notes with Chinese title and body text, hashtag arrays, cover-image guidance, publish-time recommendations, and optional disclaimer metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces 1-5 note variants from a topic plus optional selling points, audience, style, category, and disclaimer settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: skill.json, SKILL.md frontmatter, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
