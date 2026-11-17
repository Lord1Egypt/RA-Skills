## Description:

Automates the Taobao/Qianniu merchant product publishing workflow, including opening the product page, uploading product images, filling listing details, selecting categories or dropdown values, and submitting or saving a listing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[279458179](https://clawhub.ai/user/279458179)

### License/Terms of Use:

MIT-0

## Use Case:

Taobao/Qianniu merchants or their agent operators use this skill to draft and publish product listings from product images while filling titles, prices, inventory, attributes, categories, and dropdown selections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit live Taobao product listings from a merchant account without a documented final confirmation checkpoint.

Mitigation: Review listing title, price, inventory, category, shipping template, product images, and other details before allowing submission; prefer saving as draft first.

Risk: Dropdown and category automation may select an unintended value if page text or merchant UI state differs from the documented workflow.

Mitigation: Confirm selected category, sale status, age suitability, brand, and other combobox values in the page before submitting the listing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/279458179/skills/taobao-dianshang)
- [Qianniu seller workbench](https://myseller.taobao.com/home.htm/QnworkbenchHome/)
- [Taobao product publishing page](https://myseller.taobao.com/home.htm/PublishProduct/index)
- [Taobao image-based product publishing](https://item.upload.taobao.com/sell/ai/category.htm)
- [Taobao image material center](https://suc.taobao.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code]

**Output Format:** [Markdown with browser automation commands and JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser actions that fill merchant listing fields, click dropdown options, upload images, submit listings, or save drafts.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
