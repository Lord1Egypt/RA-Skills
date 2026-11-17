## Description:

Swimlane Arch turns natural-language requests into editable Draw.io XML for horizontal or vertical swimlane diagrams and layered architecture diagrams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leslietong2046-ship-it](https://clawhub.ai/user/leslietong2046-ship-it)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, architects, process analysts, and business teams use this skill to draft business process swimlanes, government approval flows, cross-department workflows, and system architecture diagrams from brief natural-language descriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagram content may leave the local environment when PROCESSON_API_KEY is configured.

Mitigation: Use the default local Draw.io output for confidential diagrams, unset PROCESSON_API_KEY unless cloud export is intentional, and verify the external endpoint before sending sensitive content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leslietong2046-ship-it/skills/swimlane-arch-skill)
- [diagrams.net](https://app.diagrams.net)
- [ProcessOn API endpoint](https://open.pingcode.com/v1/graph)
- [Architecture diagram template](artifact/references/arch-template.xml)
- [Horizontal swimlane template](artifact/references/swimlane-template.xml)
- [Vertical swimlane template](artifact/references/swimlane-vertical-template.xml)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [Draw.io XML (.drawio) with concise completion text and an optional ProcessOn link when cloud export is configured]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to local editable Draw.io XML; when PROCESSON_API_KEY is set, diagram content may be sent to an external ProcessOn-compatible endpoint.]

## Skill Version(s):

1.1.6 (source: server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
