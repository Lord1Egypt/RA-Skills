## Description: <br>
Assesses tight transit connections, recommends delay-ready airport hotels, and checks late-arrival last-mile transport options for travel itineraries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mlyjqx](https://clawhub.ai/user/mlyjqx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-support agents use this skill to flag risky connections, find hotels suitable for delayed late-night arrivals, and identify last-mile transport gaps before or during a trip. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can route itinerary, airport, city, and location-related data to external travel, hotel, and transport MCP providers. <br>
Mitigation: Install it only with trusted providers, control which API keys are available, and disclose external data processing to users. <br>
Risk: Proactive SMS, email, or push travel alerts may contact users unexpectedly. <br>
Mitigation: Keep proactive notifications opt-in and allow users to disable risk checks or alert channels. <br>
Risk: Travel, hotel, and transport recommendations may be inaccurate when provider data is unavailable, delayed, or cached. <br>
Mitigation: Treat outputs as decision support and ask users to confirm time-sensitive itinerary, hotel, and local transport details before relying on them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mlyjqx/travel-risk-checker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown travel risk assessments and recommendations with MCP configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include risk levels, time estimates, hotel options, transport status, and suggested next actions.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter and package.json list 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
