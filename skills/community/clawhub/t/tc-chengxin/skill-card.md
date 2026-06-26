## Description: <br>
Provides online travel search through Tongcheng Chengxin for flights, trains, hotels, vacation products, trip guides, itinerary planning, bus tickets, scenic spots, and tickets using Tongcheng official data with booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luckystarry](https://clawhub.ai/user/luckystarry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-support agents use this skill to search Tongcheng travel inventory for transportation, lodging, scenic tickets, vacation products, trip guides, and itinerary options, then receive formatted results with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel search details such as cities, dates, passenger preferences, and free-text trip intent are sent to Tongcheng's Chengxin API. <br>
Mitigation: Use the skill only when sharing those travel details with the API provider is acceptable, and avoid including unnecessary sensitive personal information in queries. <br>
Risk: The optional CHENGXIN_API_KEY can be exposed if pasted into chat or committed in a local config file. <br>
Mitigation: Configure the API key through OpenClaw secrets/settings or an environment variable, and do not commit config.json containing credentials. <br>
Risk: Booking links and travel availability can be misleading if an agent rewrites or fabricates results after script execution. <br>
Mitigation: Use only booking links and availability returned by the scripts/API, and preserve no-result or authentication guidance from the skill's error-handling flow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/luckystarry/tc-chengxin) <br>
- [Tongcheng Travel Homepage](https://www.ly.com) <br>
- [API Calling Examples](references/api-examples.md) <br>
- [Configuration Guide](references/config.md) <br>
- [Error Handling Guide](references/error-handling.md) <br>
- [Output Format Reference](references/output-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown tables or cards with booking links; plain-text links for WeChat-style channels] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and optionally CHENGXIN_API_KEY; sends travel search details to Tongcheng's Chengxin API.] <br>

## Skill Version(s): <br>
0.9.0 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
