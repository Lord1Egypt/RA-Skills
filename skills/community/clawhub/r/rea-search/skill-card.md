## Description: <br>
Search realestate.com.au property listings by constructing filtered search, listing, sold-property, and suburb-profile URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JakeLin](https://clawhub.ai/user/JakeLin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to build realestate.com.au URLs for Australian property searches to buy, rent, or review sold listings without an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DuckDuckGo workaround queries share property search terms with DuckDuckGo and may return incomplete or outdated listing snippets. <br>
Mitigation: Use DuckDuckGo only when direct browsing is unavailable, and verify important results directly on realestate.com.au. <br>
Risk: Direct fetching of realestate.com.au pages is commonly rate limited or blocked by anti-bot controls. <br>
Mitigation: Prefer constructing URLs for browser use and avoid treating blocked fetches as evidence that listings do not exist. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JakeLin/rea-search) <br>
- [realestate.com.au buy search URL template](https://www.realestate.com.au/buy/property-{types}-{filters}-in-{location}/list-{page}) <br>
- [realestate.com.au suburb profile URL template](https://www.realestate.com.au/neighbourhoods/{suburb}-{postcode}-{state}) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with constructed URLs and optional web_fetch command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces public URL strings; does not require credentials or return full listing data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
