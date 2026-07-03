## Description: <br>
Searches Taobao and Tmall by keyword and returns paginated product cards with item IDs, titles, prices, shop names, images, sales counts, and tags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[browseract-cli](https://clawhub.ai/user/browseract-cli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to collect Taobao and Tmall product listings for product search, price monitoring, and competitive research from a logged-in browser session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk scraping and stealth multi-session usage may create Taobao/Tmall policy, rate-limit, or account-enforcement risk. <br>
Mitigation: Use the skill only when authorized, prefer conservative single-session runs, and avoid stealth multi-session batch mode unless policy and account risks are understood. <br>
Risk: The skill runs against a logged-in Taobao browser session and can only safely read data the user is permitted to view. <br>
Mitigation: Confirm the user intends to use a logged-in session, stop if login is unavailable, and do not use it to bypass authentication or access controls. <br>
Risk: Search-page data can include sponsored items and displayed coupon or subsidy prices that may differ from final product details. <br>
Mitigation: Treat results as a search-page snapshot and verify important prices, ads, and product details on source pages before making decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/browseract-cli/taobao-keyword-search) <br>
- [Taobao search](https://s.taobao.com/search) <br>
- [Taobao login and home page](https://www.taobao.com) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON product-card arrays with text or markdown guidance for browser navigation and extraction.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports keyword, page, sort, Tmall-only tab, and price-range filters; requires a logged-in Taobao browser session.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
