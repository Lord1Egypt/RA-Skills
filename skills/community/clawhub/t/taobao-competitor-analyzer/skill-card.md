## Description: <br>
Taobao price and competitor comparison assistant that uses browser-visible evidence to compare JD, PDD, and Vipshop, normalize prices, score same-item confidence, and recommend where to buy without login, ordering, or payment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External shoppers and shopping agents use this skill to compare a Taobao product against visible JD, Pinduoduo, and Vipshop offers, normalize price conditions, assess same-item confidence, and decide whether to buy, wait, avoid, or stay with Taobao. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Marketplace prices, coupons, shipping, stock, warranty, and return terms can change or depend on account, address, region, or promotion eligibility. <br>
Mitigation: Use browser-visible evidence, label conditional prices, downgrade uncertain results, and tell the user to recheck final payable price and terms before purchase. <br>
Risk: A lower-priced listing may be a near match, different specification, unclear seller channel, or weaker authenticity or after-sales option. <br>
Mitigation: Normalize specifications and unit basis, score same-item confidence, apply category playbook gates, and avoid strong recommendations without title, price, spec or version, URL, and sufficient seller evidence. <br>
Risk: Shopping workflows can expose sensitive account, identity, address, or payment information if an agent goes beyond comparison. <br>
Mitigation: Stay within browser-visible or user-provided information, do not enter credentials or payment details, and do not submit orders or initiate checkout. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/taobao-competitor-analyzer) <br>
- [Category Playbooks](references/category-playbooks.md) <br>
- [Site Notes](references/site-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown verdict block, comparison table, and concise notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses browser-visible marketplace evidence only; avoids login, order submission, payment, hidden APIs, and scraping shortcuts.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
