## Description: <br>
Discover Shopify merchants by category or store name through Lobster Stores. Use when a buyer wants help finding the right merchant for coffee, cookies, supplements, apparel, wellness, pets, oral care, alcohol, or adult products and should complete checkout on the merchant's native Shopify checkout. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abuiles](https://clawhub.ai/user/abuiles) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External buyers and shopping agents use this skill to match a product or category request to the closest Lobster Stores category site, then continue merchant discovery from that site. The skill keeps payment collection outside the agent flow and directs checkout to the selected merchant's native Shopify checkout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent consults live Lobster category pages whose instructions may change after release. <br>
Mitigation: Re-fetch the selected category site's skill.md at the start of a new session and treat that category file as current evidence. <br>
Risk: A user could be steered toward invented or unsupported merchants or domains. <br>
Mitigation: Use only the category domains listed by the skill and do not invent merchants or domains. <br>
Risk: Payment details could be mishandled if checkout is treated as part of the skill flow. <br>
Mitigation: Do not request payment details; direct the customer to complete purchases on the selected merchant's native Shopify checkout. <br>


## Reference(s): <br>
- [Lobster Stores homepage](https://lobsterstores.com) <br>
- [Bread category skill](https://lobsterbread.com/skill.md) <br>
- [Coffee category skill](https://lobsterbrew.com/skill.md) <br>
- [Cookies category skill](https://lobstercookies.com/skill.md) <br>
- [Meat category skill](https://lobstercuts.com/skill.md) <br>
- [Fitness category skill](https://lobsterfit.com/skill.md) <br>
- [Beauty category skill](https://lobsterglow.com/skill.md) <br>
- [Tea category skill](https://lobsterinfuse.com/skill.md) <br>
- [Pets category skill](https://lobsterpets.com/skill.md) <br>
- [Drinks category skill](https://lobsterpour.com/skill.md) <br>
- [Adult wellness category skill](https://lobstersaucy.com/skill.md) <br>
- [Oral care category skill](https://lobstersmile.com/skill.md) <br>
- [Snacks category skill](https://lobstersnacks.com/skill.md) <br>
- [Supplements category skill](https://lobstersupps.com/skill.md) <br>
- [Apparel category skill](https://lobsterthread.com/skill.md) <br>
- [Wellness category skill](https://lobsterwell.com/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown] <br>
**Output Format:** [Markdown with category URLs and shopping guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Directs users to external category skill files and merchant Shopify checkouts; does not collect payment details.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact metadata and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
