## Description:

Travel Partner provides AI-powered virtual travel companion services for international trips, generating personalized itineraries, travel narratives, image prompts, social media content, and optional AI-generated travel photos with a companion persona.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wolf-leo](https://clawhub.ai/user/wolf-leo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to plan and produce virtual international travel experiences, including itineraries, companion-style journals, travel guides, photo prompts, and social media captions. It can also help agents run bundled scripts that generate local itinerary, manifest, journal, guide, story, and optional image files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image generation can send user prompt data outside the local environment through optional OpenAI API use.

Mitigation: Avoid sensitive personal details in prompts and use a scoped API key when enabling image generation.

Risk: The skill can create local files and has reported path-handling and remote-download weaknesses.

Mitigation: Run it in a dedicated working directory and review generated file paths and downloaded images before using or sharing them.

Risk: The release depends on install-time Python packages without fully pinned versions.

Mitigation: Install dependencies in an isolated environment and prefer pinned dependency versions before production use.

## Reference(s):

- [Travel Partner ClawHub listing](https://clawhub.ai/wolf-leo/skills/travel-partner)
- [Cultural Etiquette Guide](artifact/references/cultural_etiquette.md)
- [Destination Content Templates](artifact/references/destination_templates.md)
- [OpenAI Platform](https://platform.openai.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown, JSON files, plain-text image prompts, and optional PNG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local itinerary, manifest, journal, guide, story, and image files; image generation requires OPENAI_API_KEY and remote API calls.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
