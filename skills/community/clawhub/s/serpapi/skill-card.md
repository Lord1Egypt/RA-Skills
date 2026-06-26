## Description: <br>
Unified search API across Google, Amazon, Yelp, OpenTable, Walmart, and more for searching products, local businesses, restaurants, shopping, images, news, and general web results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ianpcook](https://clawhub.ai/user/ianpcook) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to call SerpAPI from the command line and retrieve structured or human-readable search results across web, shopping, local, image, and news engines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, optional location data, and SerpAPI account usage are sent to SerpAPI. <br>
Mitigation: Use a dedicated or revocable SERPAPI_API_KEY, monitor quota usage, and avoid setting a default location when location reuse is not desired. <br>


## Reference(s): <br>
- [SerpAPI homepage](https://serpapi.com) <br>
- [ClawHub SerpAPI skill page](https://clawhub.ai/ianpcook/serpapi) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, JSON, Text, Guidance] <br>
**Output Format:** [JSON or plain text emitted by a command-line tool] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SERPAPI_API_KEY and may use an optional default location from TOOLS.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
