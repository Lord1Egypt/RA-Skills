## Description:

StylePilot is a local-first personal wardrobe assistant that stores clothing metadata and helps generate outfit suggestions or travel packing plans when the user explicitly asks for styling help.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mars2003](https://clawhub.ai/user/mars2003)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use StylePilot to maintain a local wardrobe database, add clothing items with optional images, request outfit recommendations by scene and weather, generate travel packing lists, and record explicit feedback for future reranking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict is suspicious because image import can copy arbitrary readable local files into persistent storage.

Mitigation: Review the skill before installing, only pass photo files intentionally selected by the user, and avoid paths to private documents, keys, profiles, or other sensitive files.

Risk: The current image import behavior may rely on file extension handling rather than confirmed image content.

Mitigation: A safer release should reject non-image extensions, validate actual image content, and use non-deterministic destination names for copied images.

Risk: Wardrobe data and imported images are stored locally and may persist after use.

Mitigation: Provide clear delete and export controls for stored wardrobe data and images before broad deployment.

## Reference(s):

- [StylePilot ClawHub Skill Page](https://clawhub.ai/mars2003/skills/stylepilot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown and text responses with optional JSON returned by the local wardrobe CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI supports init, list, add, outfit, and feedback commands; JSON mode exposes wardrobe counts, selected items, missing categories, outfit IDs, and preference reasons.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
