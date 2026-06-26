## Description: <br>
Generate a 3x3 grid travel blogger-style collage based on user photos and a specific destination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swiftuis](https://clawhub.ai/user/swiftuis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to turn uploaded personal photos and a named destination into a nine-frame travel collage with consistent subject appearance, varied poses, and destination-specific scenes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded photos and facial appearance details may be sent into an image-generation workflow. <br>
Mitigation: Use only photos the user is comfortable processing and avoid sensitive identity, location, or itinerary details in prompts. <br>
Risk: Destination landmark research may rely on external search and can expose private travel intent if the prompt is overly specific. <br>
Mitigation: Keep destination prompts general and omit private timing, lodging, or itinerary details unless the user explicitly needs them. <br>
Risk: Generated collages can contain visual artifacts or inconsistent subject identity across frames. <br>
Mitigation: Review the generated image before sharing and regenerate specific frames when identity, anatomy, or destination details are incorrect. <br>


## Reference(s): <br>
- [Destination Scene Templates](references/destinations.md) <br>
- [Project homepage](https://github.com/qclaw/travel-grid-generator) <br>
- [ClawHub skill page](https://clawhub.ai/swiftuis/travel-grid-generator) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, image generation request, image] <br>
**Output Format:** [Markdown-style prompt guidance and a generated 1:1 image when an image-generation tool is available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses uploaded photos, destination text, researched landmark scenes, and a square 3x3 layout.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
