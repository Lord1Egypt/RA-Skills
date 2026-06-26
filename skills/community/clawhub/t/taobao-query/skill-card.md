## Description: <br>
Query Taobao product prices and product information through a local MCP server, including product search, price comparison, cart/order viewing, and seller chat while prohibiting payment or checkout operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EvenSix66](https://clawhub.ai/user/EvenSix66) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to search Taobao, compare product prices, inspect cart or order information, and communicate with sellers through a configured local Taobao MCP server. It is intended for shopping research and account-session assistance, not payment, checkout, or order confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose a logged-in Taobao session to broad agent actions, including cart and order viewing, browsing history, seller chat, arbitrary navigation, clicks, and text entry. <br>
Mitigation: Use it only with a trusted local MCP endpoint and require explicit confirmation before account-affecting actions or access to cart, order, browsing-history, chat, navigation, click, or text-entry tools. <br>
Risk: A misconfigured TAOBAO_MCP_URL could route shopping-session actions through an untrusted MCP server. <br>
Mitigation: Prefer the localhost MCP URL and verify any custom TAOBAO_MCP_URL before use. <br>
Risk: Shopping workflows can drift toward payment, checkout, or order confirmation. <br>
Mitigation: Keep payment, checkout, order confirmation, authorization, and auto-buy operations blocked; stop before any payment or purchase-finalization page. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/EvenSix66/taobao-query) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, API Calls] <br>
**Output Format:** [Markdown reports with tables, inline links, setup snippets, and MCP call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a running Taobao desktop MCP service and a logged-in Taobao session; payment and checkout actions are explicitly out of scope.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
