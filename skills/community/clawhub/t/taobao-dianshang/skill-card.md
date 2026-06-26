## Description: <br>
淘宝/千牛商家商品自动发布技能，可帮助商家打开发布页、上传商品图片、填写标题、价格、库存、属性等商品信息，并执行发布或保存草稿流程。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[279458179](https://clawhub.ai/user/279458179) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Taobao/Qianniu sellers and their agents use this skill to automate product listing preparation, including image-based product entry, category adjustment, field completion, dropdown handling, and draft or submit actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can drive a real Taobao/Qianniu seller workflow and may submit a live product listing without a built-in final confirmation. <br>
Mitigation: Configure agents to save drafts by default and require explicit user approval after showing the title, category, images, price, stock, shipping settings, and attributes before any live submit action. <br>
Risk: Automated field entry or dropdown selection can publish incorrect product details if page state, category, or extracted image information is wrong. <br>
Mitigation: Require a human review of all listing fields and category selections before saving or submitting the listing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/279458179/taobao-dianshang) <br>
- [Publisher profile](https://clawhub.ai/user/279458179) <br>
- [Taobao product publish page](https://myseller.taobao.com/home.htm/PublishProduct/index) <br>
- [Qianniu seller center](https://myseller.taobao.com/home.htm/QnworkbenchHome/) <br>
- [Image-based product publishing](https://item.upload.taobao.com/sell/ai/category.htm) <br>
- [Taobao image asset center](https://suc.taobao.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code] <br>
**Output Format:** [Markdown instructions with browser automation commands and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce live browser actions that save drafts or submit Taobao/Qianniu product listings.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
