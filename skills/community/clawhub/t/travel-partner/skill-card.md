## Description: <br>
This skill provides AI-powered virtual travel companion services for international trips, including personalized itineraries, travel narratives, photo prompts, optional AI-generated travel images, and social media content with a companion persona. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wolf-leo](https://clawhub.ai/user/wolf-leo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content creators use this skill to plan international travel experiences and generate itinerary, journal, image-prompt, optional image, vlog, and social-post content for virtual companion scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional OpenAI image generation can incur paid API usage. <br>
Mitigation: Use a budget-limited OpenAI API key and review generation settings before running batch image creation. <br>
Risk: Travel prompts may include sensitive personal itinerary or relationship details. <br>
Mitigation: Avoid sensitive personal details in prompts and prefer general city, landmark, and activity descriptions. <br>
Risk: The skill installs dependencies and writes local output files. <br>
Mitigation: Install dependencies in a virtual environment and use ordinary city or landmark names rather than path-like input when generating files. <br>


## Reference(s): <br>
- [Travel Partner ClawHub release](https://clawhub.ai/wolf-leo/travel-partner) <br>
- [Destination Content Templates](references/destination_templates.md) <br>
- [Cultural Etiquette Guide](references/cultural_etiquette.md) <br>
- [OpenAI Platform](https://platform.openai.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance, image files] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON itinerary files, Markdown travel journals and guides, image prompts, and optional downloaded image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional OpenAI image generation requires OPENAI_API_KEY and writes local output files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
