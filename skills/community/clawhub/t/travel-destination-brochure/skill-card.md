## Description: <br>
Build travel destination scenarios and brochures from a city name by fetching street-level and landmark imagery from OpenStreetCam and Wikimedia Commons, then using VLM Run to generate a travel video and travel plan. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MehediAhamed](https://clawhub.ai/user/MehediAhamed) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to create city-specific travel brochures by collecting open imagery, producing an image manifest, and optionally generating a short travel video and one-day itinerary with VLM Run. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup guidance may encourage unsafe API-key handling or inspection of local environment files. <br>
Mitigation: Use a dedicated VLM Run key through a safe secret mechanism, do not expose .env files to the agent, and do not print API keys in terminal or chat. <br>
Risk: Installer-script setup paths fetch and execute remote installation code. <br>
Mitigation: Prefer pip or package-manager installation paths and review remote installer scripts before using them. <br>
Risk: Images and prompts may be sent to an external VLM Run service for video and itinerary generation. <br>
Mitigation: Only submit images, locations, and prompts that are acceptable for external processing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MehediAhamed/travel-destination-brochure) <br>
- [OpenStreetCam API Reference](references/openstreetcam_api.md) <br>
- [Wikimedia Commons API Reference](references/commons_api.md) <br>
- [OpenStreetCam API Doc](https://api.openstreetcam.org/api/doc.html) <br>
- [Wikimedia Commons API](https://commons.wikimedia.org/w/api.php) <br>
- [MediaWiki API](https://www.mediawiki.org/wiki/Special:MyLanguage/API:Main_page) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Code, Files] <br>
**Output Format:** [Markdown guidance with shell commands; generated artifacts may include image files, JSON manifests, optional video output, and a Markdown travel plan.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.10 or higher and internet access; video and itinerary generation require a VLMRUN_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
