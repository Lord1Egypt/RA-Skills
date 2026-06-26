## Description: <br>
Summarizes visible Postal Savings Bank of China product, billing, and announcement information without supporting login automation, funds movement, payments, or security bypass. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mike47512](https://clawhub.ai/user/mike47512) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to gather concise summaries of public PSBC product and announcement pages, and user-visible billing information only when the user has explicitly allowed inspection of logged-in pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent to inspect logged-in banking bill pages. <br>
Mitigation: Use it for logged-in banking pages only with explicit user intent and limit extraction to visible, non-sensitive summaries. <br>
Risk: Banking workflows can expose credentials, CAPTCHA challenges, transfers, payments, or detailed private account data. <br>
Mitigation: Do not permit login automation, CAPTCHA handling, funds movement, payments, credential exposure, or collection of card numbers, government identifiers, or detailed account data. <br>


## Reference(s): <br>
- [Postal Savings Bank of China website](https://www.psbc.com/) <br>
- [ClawHub skill page](https://clawhub.ai/mike47512/psbc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or concise structured text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries should avoid credentials, card numbers, government identifiers, and detailed private account data.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
