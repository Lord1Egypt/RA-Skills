## Description: <br>
Taobao Shopping helps an agent search Taobao products, inspect item details and reviews, add items to a cart, and review cart prices through OpenCLI browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[he2y](https://clawhub.ai/user/he2y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping assistants use this skill to research Taobao or Tmall products, compare price or sales ordering, inspect reviews, and prepare cart additions from a logged-in Chrome session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a logged-in browser session that has access to the user's Taobao account. <br>
Mitigation: Install only if the OpenCLI package and browser bridge are trusted, and use a separate Chrome profile or secondary account where possible. <br>
Risk: Cart actions can change the user's cart without an explicit confirmation requirement in the skill instructions. <br>
Mitigation: Require the agent to confirm the exact item, specification, and price before cart-changing commands; prefer dry-run for add-cart previews. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/he2y/taobao-shopping-skill) <br>
- [Publisher profile](https://clawhub.ai/user/he2y) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with OpenCLI command examples and structured command output formats including table, JSON, YAML, Markdown, and CSV.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a logged-in Chrome session and OpenCLI browser bridge; shopping results may include prices, sales counts, shops, locations, item IDs, specifications, and reviews.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
