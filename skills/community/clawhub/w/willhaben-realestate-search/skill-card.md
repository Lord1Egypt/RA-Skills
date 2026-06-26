## Description: <br>
Search willhaben.at real estate listings for apartments and houses via the public web API, with filters for Austrian state, district, price, rooms, and optional listing details such as heating type, building condition, energy class, parking, and floor. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mihaimacarie98](https://clawhub.ai/user/mihaimacarie98) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to search Austrian real estate listings on willhaben.at and collect listing summaries or details for property research and comparison. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to willhaben.at. <br>
Mitigation: Run it only in environments where that network access is acceptable. <br>
Risk: Detail fetching and multi-page searches can generate repeated requests. <br>
Mitigation: Use reasonable page limits and respect willhaben.at terms and rate limits. <br>
Risk: The script uses browser-like request headers. <br>
Mitigation: Review this behavior before deployment in environments with strict network or compliance controls. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mihaimacarie98/willhaben-realestate-search) <br>
- [Publisher Profile](https://clawhub.ai/user/mihaimacarie98) <br>
- [willhaben Search API Endpoint](https://www.willhaben.at/webapi/iad/search/atz/seo/immobilien/{type}/{state}/{district}) <br>
- [willhaben Detail API Endpoint](https://www.willhaben.at/webapi/iad/atverz/{ad_id}) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands; command output is plain text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and the Python requests library; commands may make outbound requests to willhaben.at.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
