## Description:

Generate a 3x3 grid (9-square) travel blogger style collage based on user photos and a specific destination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swiftuis](https://clawhub.ai/user/swiftuis)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn user-provided photos and a destination into a character-consistent 3x3 travel-photo collage prompt and image-generation request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded personal photos may be analyzed to preserve appearance across generated images.

Mitigation: Use only photos the user has permission to provide and avoid retaining or exposing identifying details beyond what is needed for the generation prompt.

Risk: Destination research may rely on current web search results that vary by language, region, and time.

Mitigation: Confirm the selected locations fit the user's requested destination and avoid treating searched locations as server-resolved provenance when provenance is unavailable.

Risk: Generated travel collages may be mistaken for real travel photos.

Mitigation: Present outputs as AI-generated images and revise or remove frames that misrepresent the person, destination, or scene.

## Reference(s):

- [Destination Scene Templates](references/destinations.md)
- [Project Homepage](https://github.com/qclaw/travel-grid-generator)
- [ClawHub Skill Page](https://clawhub.ai/swiftuis/skills/travel-grid-generator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, API calls]

**Output Format:** [Markdown prompt guidance with an image-generation tool call]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses uploaded photos, destination research, nine scene descriptions, and a square image-generation request.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
