## Description:

Search and retrieve Magic: The Gathering card data using the Scryfall API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[santidev95](https://clawhub.ai/user/santidev95)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to search for Magic: The Gathering cards and retrieve card details such as images, prices, rulings, legality, and random card results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Card search terms are sent to Scryfall's public API.

Mitigation: Use the skill for MTG-related lookups and avoid including sensitive personal or proprietary information in card search queries.

Risk: Ambiguous user wording could trigger an unnecessary external card lookup.

Mitigation: Invoke the skill only when the request is clearly about MTG, Magic: The Gathering, card names, deck building, or card information.

Risk: The Scryfall API may return errors or rate-limit responses.

Mitigation: Validate API responses, handle error objects, and follow the documented 50-100ms delay between requests.

## Reference(s):

- [Scryfall API](https://api.scryfall.com)
- [Scryfall Search Syntax Reference](references/search_syntax.md)
- [ClawHub Skill Page](https://clawhub.ai/santidev95/skills/scryfall-card)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with text summaries, API usage examples, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Scryfall card fields, card image URLs, prices, legalities, set details, and API error guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
