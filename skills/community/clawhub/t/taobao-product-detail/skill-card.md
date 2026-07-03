## Description: <br>
Fetches full product details from a Taobao or Tmall product page by itemId, including title, price, shop information, images, SKU variants, attributes, and review count. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[browseract-cli](https://clawhub.ai/user/browseract-cli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to collect structured product data from a Taobao or Tmall item page that the user can already access in a logged-in browser session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a logged-in Taobao or Tmall browser session for automated product-data extraction. <br>
Mitigation: Use only for user-directed product pages the user can access, and avoid collecting data outside the user's authorization. <br>
Risk: Batch collection and database-style use may conflict with site rules or create excessive automated traffic. <br>
Mitigation: Keep collection low-volume, include delays between item pages, and confirm that the intended use complies with Taobao/Tmall terms and applicable policies. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/browseract-cli/taobao-product-detail) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, JSON, guidance] <br>
**Output Format:** [JSON product detail data with concise progress and execution guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a logged-in Taobao or Tmall browser session and a product page accessible to the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
