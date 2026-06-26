## Description: <br>
自动严格筛选闲鱼个人闲置商品，排除商家、价格区间和不匹配规格，输出按价格排序的候选商品列表。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xxxzhuo](https://clawhub.ai/user/xxxzhuo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Shoppers and purchasing agents use this skill to search Xianyu for second-hand listings, apply strict personal-seller and specification filters, and compare the top matching results by price, region, interest count, and link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search history may include private purchases, sensitive interests, budgets, locations, and item links in plain-text memory files. <br>
Mitigation: Use the skill only after confirming that logging is opt-in and that users can disable logging and delete saved search history. <br>
Risk: Broad activation phrases may trigger marketplace searches or logging when the user did not intend to run the skill. <br>
Mitigation: Narrow activation phrases and ask for user confirmation before accessing Xianyu or saving search details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xxxzhuo/xianyufilter) <br>
- [Publisher profile](https://clawhub.ai/user/xxxzhuo) <br>
- [Xianyu search site](https://www.goofish.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown tables and concise search guidance with item links and price statistics] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May record search time, keywords, result counts, price range, and lowest-price item link in plain-text memory files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and artifact/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
