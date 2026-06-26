## Description: <br>
Travel Cog provides CellCog-powered travel planning, travel research, logistics guidance, and itinerary generation with PDF, interactive HTML, or Markdown deliverables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nitishgargiitd](https://clawhub.ai/user/nitishgargiitd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to research destinations, compare logistics, and generate tailored trip itineraries with practical travel details. It is intended for CellCog-backed planning that may produce PDFs, interactive HTML dashboards, or Markdown itineraries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel queries and generated plans may be sent to the external CellCog service. <br>
Mitigation: Avoid including sensitive personal details unless they are needed for the travel-planning task, and install only if external CellCog processing is acceptable. <br>
Risk: The skill requires a CellCog API key. <br>
Mitigation: Provide the key through the CELLCOG_API_KEY environment variable and handle it as a sensitive credential. <br>


## Reference(s): <br>
- [Travel Cog on ClawHub](https://clawhub.ai/nitishgargiitd/travel-cog) <br>
- [CellCog](https://cellcog.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Travel guidance and itinerary content with optional PDF, interactive HTML, or Markdown deliverables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and CELLCOG_API_KEY; uses the CellCog service for travel research and itinerary generation.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
