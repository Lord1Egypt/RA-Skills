## Description:

Search and retrieve Magic: The Gathering card data using the Scryfall API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[santidev95](https://clawhub.ai/user/santidev95)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to search, retrieve, and format Magic: The Gathering card data, including card details, images, prices, rulings, legality information, autocomplete suggestions, and random cards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes user-directed network requests to Scryfall for card data, prices, images, rulings, and legality information.

Mitigation: Install with network access scoped to the Scryfall API host and review requested queries before execution.

Risk: Broad trigger wording may activate the skill for ambiguous Magic: The Gathering references.

Mitigation: Narrow trigger metadata or confirm intent when a request could refer to something other than MTG card data.

## Reference(s):

- [Scryfall API](https://api.scryfall.com)
- [Scryfall Search Syntax Reference](references/search_syntax.md)
- [ClawHub Skill Page](https://clawhub.ai/santidev95/skills/scryfall-cards)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, guidance]

**Output Format:** [Markdown and plain text with optional shell command examples and formatted Scryfall API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script returns human-readable card summaries and can include prices, legality details, and image URLs when verbose output is requested.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
