## Description: <br>
Search and retrieve Magic: The Gathering card data using the Scryfall API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[santidev95](https://clawhub.ai/user/santidev95) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, players, deck builders, and developers use this skill to search Scryfall for Magic: The Gathering card records by name, rules text, color, mana cost, legality, set, price, or related attributes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Card names and search queries are sent to Scryfall over the network. <br>
Mitigation: Avoid submitting sensitive or private deck information in queries when query disclosure is a concern. <br>
Risk: Scryfall requests can fail or return API errors for invalid queries, missing cards, network issues, or rate limits. <br>
Mitigation: Check returned error details and retry only after respecting the documented request delay. <br>


## Reference(s): <br>
- [Scryfall API](https://api.scryfall.com) <br>
- [Scryfall Search Syntax Reference](references/search_syntax.md) <br>
- [ClawHub release page](https://clawhub.ai/santidev95/scryfall-cards) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text with optional shell commands and JSON-derived card details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Scryfall card names, mana costs, types, oracle text, prices, legality, image URLs, set metadata, and error messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
