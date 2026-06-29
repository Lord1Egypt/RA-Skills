## Description: <br>
提供淘宝好券精选频道商品查询工具，展示天猫品牌高优惠券好物合集，优惠券覆盖率90%+，天猫品牌店占比98%+，涵盖洗护清洁、美容护肤、咖啡冲饮、粮油速食、零食特产等全品类，价格多在5-50元区间，支持销量优先、价格升降序、推荐热度4种排序，每页40条共5页200条精选好券。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cn-shopping](https://clawhub.ai/user/cn-shopping) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External shoppers and shopping assistants use this skill to browse Taobao coupon-selected Tmall products, sort product lists, inspect item details, and review channel statistics before opening purchase links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Coupon lookup requests send page, sort choice, and item_id parameters to the publisher's cloud proxy. <br>
Mitigation: Install only if this data flow is acceptable for your use case. <br>
Risk: Product availability, prices, coupon terms, and purchase links may change after the skill returns results. <br>
Mitigation: Verify the product page and coupon terms on Taobao before purchasing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cn-shopping/taobao-haoquan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [JSON content with concise summary text and Markdown-ready image and purchase-link guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only lookup output for paginated coupon lists, item details, and channel statistics.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
