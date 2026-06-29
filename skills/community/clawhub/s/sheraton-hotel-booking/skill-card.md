## Description: <br>
Provides three Sheraton hotel lookup tools for hotel search, detail retrieval, and package-offer discovery using Fliggy official data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to find Sheraton hotels, inspect hotel details, and compare package offers before completing booking on Fliggy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured proxy endpoint receives hotel destinations, dates, keywords, and the proxy token. <br>
Mitigation: Use only a trusted, approved HTTPS proxy endpoint and protect PROXY_TOKEN as a credential. <br>
Risk: The proxy destination is controlled by an undeclared PROXY_URL environment variable. <br>
Mitigation: Declare and restrict PROXY_URL to the approved proxy host before installation or deployment. <br>
Risk: Displayed prices, availability, and package terms can change after lookup. <br>
Mitigation: Confirm final price, room availability, and booking terms on the linked Fliggy page before purchase. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/sheraton-hotel-booking) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-formatted hotel search results, hotel details, package offers, and booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prices and availability should be verified on the linked Fliggy pages.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
