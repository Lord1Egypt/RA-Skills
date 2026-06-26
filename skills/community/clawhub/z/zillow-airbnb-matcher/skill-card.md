## Description: <br>
Find properties for sale that are already generating Airbnb income. Cross-references Zillow listings with active Airbnb rentals using geo-matching and calculates investment metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Freemountaindeer](https://clawhub.ai/user/Freemountaindeer) <br>

### License/Terms of Use: <br>
UNLICENSED <br>


## Use Case: <br>
Real estate investors, operators, and agents use this skill to compare US for-sale property listings with nearby active short-term rental listings and review revenue estimates, match confidence, and investment metrics before deeper due diligence. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: Live searches send search locations and the user's RapidAPI key to third-party listing APIs. <br>
Mitigation: Use a protected .env file for RAPIDAPI_KEY, keep it out of version control, and monitor RapidAPI usage. <br>
Risk: Investment reports may contain estimates or nearby-property matches rather than verified exact-property income. <br>
Mitigation: Independently verify listing matches, revenue assumptions, local short-term rental rules, and financial conclusions before acting. <br>
Risk: Installation runs a Node/npm-based setup script. <br>
Mitigation: Review the skill and scan results before deployment, then install only in an environment where running npm dependencies is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Freemountaindeer/zillow-airbnb-matcher) <br>
- [Freemountaindeer publisher profile](https://clawhub.ai/user/Freemountaindeer) <br>
- [RapidAPI](https://rapidapi.com) <br>
- [Airbnb13 API on RapidAPI](https://rapidapi.com/3b-data-3b-data-default/api/airbnb13) <br>
- [US Property Market API on RapidAPI](https://rapidapi.com/SwongF/api/us-property-market1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown reports with links, investment metrics, setup commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Live searches require Node.js and a RAPIDAPI_KEY; demo mode can run without an API key.] <br>

## Skill Version(s): <br>
3.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
