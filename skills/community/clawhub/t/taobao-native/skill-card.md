## Description: <br>
Shopping assistant via Taobao Desktop client for searching products, viewing details, adding items to cart, placing orders, checking orders, requesting shipping, and performing Taobao or Tmall shopping operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flappymonkey](https://clawhub.ai/user/flappymonkey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and shopping agents use this skill to operate an installed Taobao Desktop client for Taobao and Tmall shopping workflows, including search, product comparison, cart actions, order management, seller chat, and ratings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent operate inside a logged-in Taobao Desktop session and perform shopping, messaging, rating, or installation actions. <br>
Mitigation: Require explicit user approval before destructive, public, installation, or purchase-related steps, and confirm the item, seller, price, quantity, and requested action before proceeding. <br>
Risk: Displayed search or default prices may not match the final selected SKU price. <br>
Mitigation: Open the product detail page, inspect exact SKU options, select by element index, wait for the page to refresh pricing, and verify the final SKU price before recommending or purchasing. <br>
Risk: Large command outputs can be truncated by the agent environment. <br>
Mitigation: Write large taobao-native results to a workspace JSON file and read the complete result file before making decisions. <br>


## Reference(s): <br>
- [Taobao Desktop install and download reference](references/install-download.md) <br>
- [ClawHub skill page](https://clawhub.ai/flappymonkey/taobao-native) <br>
- [Taobao Desktop package CDN](https://tblifecdn.taobao.com/taobaopc/ai/latest) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON argument examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce command sequences that call taobao-native and may direct large CLI results to JSON output files.] <br>

## Skill Version(s): <br>
1.0.41 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
