## Description:

Build travel destination scenarios and brochures from a city name by fetching street-level and landmark imagery from OpenStreetCam and Wikimedia Commons, then using VLM Run to generate a travel video and travel plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mehediahamed](https://clawhub.ai/user/mehediahamed)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to create destination guides, travel brochures, short travel videos, and one-day itineraries for a specified city using open imagery and optional VLM Run generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance includes remote installer commands that pipe downloaded content directly to a shell.

Mitigation: Remove pipe-to-shell installer paths and prefer package-manager or pinned dependency installation steps before use.

Risk: The skill depends on VLMRUN_API_KEY and includes guidance that could expose secrets if an agent reads or prints environment files.

Mitigation: Store API keys in a secure secret mechanism and prevent agents from reading .env files or printing full keys.

Risk: The skill downloads remote media that is not strongly validated before saving to disk.

Mitigation: Run image downloads in a constrained output directory and review downloaded media before using it in downstream generation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mehediahamed/skills/travel-destination-brochure)
- [Wikimedia Commons API Reference](references/commons_api.md)
- [OpenStreetCam API Reference](references/openstreetcam_api.md)
- [Commons API](https://commons.wikimedia.org/w/api.php)
- [MediaWiki API](https://www.mediawiki.org/wiki/Special:MyLanguage/API:Main_page)
- [OpenStreetCam API Documentation](https://api.openstreetcam.org/api/doc.html)
- [Nominatim Geocoding](https://nominatim.openstreetmap.org/search)
- [VLM Run API Base](https://agent.vlm.run/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and generated artifact paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce image files, JSON manifests, a travel_plan.md file, and optional video output when VLMRUN_API_KEY is configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
