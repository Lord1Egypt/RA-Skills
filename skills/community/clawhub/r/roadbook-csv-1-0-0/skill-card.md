## Description: <br>
Creates shareable roadbook links from travel itinerary CSV data, including multi-day stops, lodging continuity, and map visualization support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mnhkahn](https://clawhub.ai/user/mnhkahn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to convert structured itinerary details into CSV, submit them to Cyeam services, and return a roadbook URL or QR code for map-based review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trip names, addresses, dates, lodging stops, and notes are sent to external Cyeam services and may be exposed through link-based sharing. <br>
Mitigation: Avoid sensitive home addresses, confidential travel plans, and private notes unless the user accepts temporary external storage and shareable-link access. <br>
Risk: The skill requires a CYEAM_API_KEY credential to create roadbooks. <br>
Mitigation: Confirm the credential is present only when needed and avoid printing or embedding the API key in returned commands, logs, or shared output. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/mnhkahn/roadbook-csv-1-0-0) <br>
- [Cyeam Open Platform developer portal](https://cyeam-open-main-d02895c.zuplo.site/api/~endpoints) <br>
- [Cyeam roadbook viewer](https://www.cyeam.com/tool/roadbook) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API Calls, Configuration guidance] <br>
**Output Format:** [Markdown with CSV snippets, curl commands, returned URLs, and QR code data when provided by the service] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CYEAM_API_KEY and curl; sends itinerary CSV text to Cyeam services.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
