## Description:

Find properties for sale that are already generating Airbnb income. Cross-references Zillow listings with active Airbnb rentals using geo-matching and calculates investment metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freemountaindeer](https://clawhub.ai/user/freemountaindeer)

### License/Terms of Use:

UNLICENSED

## Use Case:

External users and real estate analysts use this skill to search U.S. ZIP codes or cities, compare for-sale properties with nearby active Airbnb rentals, and review estimated short-term rental investment metrics.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: RapidAPI search requests disclose searched locations to RapidAPI-backed Zillow and Airbnb services.

Mitigation: Use live search only when sharing those locations with the API providers is acceptable; use demo mode when validating the skill without sending external requests.

Risk: RapidAPI keys may be stored in a local .env file or exposed through command-line setup patterns.

Mitigation: Store the key in a protected secret store or environment variable, restrict .env permissions to the owner, avoid passing secrets on the command line, and rotate any key already used that way.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freemountaindeer/skills/zillow-airbnb-matcher)
- [RapidAPI Airbnb13 API](https://rapidapi.com/3b-data-3b-data-default/api/airbnb13)
- [RapidAPI US Property Market API](https://rapidapi.com/SwongF/api/us-property-market1)
- [Setup guide](GUIDE.md)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain text property match report with listing links and investment metrics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live searches require RAPIDAPI_KEY and send search locations to RapidAPI-backed Zillow and Airbnb services; demo mode uses sample data.]

## Skill Version(s):

3.1.0 (source: server release and SKILL.md frontmatter; package.json lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
