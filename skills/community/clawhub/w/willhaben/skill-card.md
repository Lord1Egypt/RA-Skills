## Description:

Create and manage listings on Willhaben.at (Austrian marketplace). Use when the user wants to sell something, create a listing, or mentions Willhaben. Handles photo uploads, generates titles/descriptions/prices, and posts via browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benjaminorthner](https://clawhub.ai/user/benjaminorthner)

### License/Terms of Use:


## Use Case:

External users use this skill to prepare and publish Willhaben marketplace listings from item details and photos. It helps research comparable prices, draft German listing text, estimate package size, and guide browser-based publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate a logged-in Willhaben browser session and publish public ads after user confirmation.

Mitigation: Review listing drafts, uploaded photos, price, shipping options, and final publish action before approving publication.

Risk: Preferences may store location and shipping details locally in the skill folder.

Mitigation: Store only the location precision needed for pickup and avoid saving exact address details unless acceptable.

## Reference(s):

- [Willhaben Bot Setup](references/SETUP.md)
- [Willhaben Categories](references/categories.md)
- [Willhaben Listing Creation](https://www.willhaben.at/iad/anzeigenaufgabe)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with listing drafts, browser automation guidance, and configuration JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce German listing titles and descriptions, price recommendations, package-size estimates, and browser action guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata, released 2026-01-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
