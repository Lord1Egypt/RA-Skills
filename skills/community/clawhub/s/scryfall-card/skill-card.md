## Description: <br>
Search and retrieve Magic: The Gathering card data using the Scryfall API, including names, types, colors, mana costs, oracle text, images, prices, rulings, legality information, and random cards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[santidev95](https://clawhub.ai/user/santidev95) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to answer Magic: The Gathering card lookup questions, run Scryfall searches, retrieve card details, and format results for agent responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Card names and search queries are sent to Scryfall. <br>
Mitigation: Avoid entering unrelated private information into card searches. <br>
Risk: Frequent automated searches may encounter Scryfall rate limits. <br>
Mitigation: Use the documented 50-100 ms delay between API requests and handle 429 responses with retry behavior. <br>


## Reference(s): <br>
- [Scryfall API](https://api.scryfall.com) <br>
- [Scryfall Search Syntax Reference](references/search_syntax.md) <br>
- [ClawHub skill page](https://clawhub.ai/santidev95/scryfall-card) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with optional shell commands and JSON-formatted API results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses may include Scryfall card fields, prices, legalities, image URLs, and errors returned by Scryfall.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
