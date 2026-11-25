## Description:

SideQuest: Hire Real People. Use when a task needs a real person: calling a business, checking a store, inspecting an item or vehicle, a pickup or return, waiting in line, first-person video for AI training, translation, or human review of AI output. Funds are held in escrow and released when you approve the proof.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uckhill](https://clawhub.ai/user/uckhill)

### License/Terms of Use:

MIT-0

## Use Case:

AI agents use SideQuest to request real-world help from verified people and receive task-specific proof, such as written answers, photos, checklists, or translations. A human should review each brief and spending limit and approve the task before posting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review rates this release suspicious. It reports an undisclosed $50 account top-up, privacy concerns about sharing task and location details, possible automatic approval of submissions after 72 hours, and an incomplete review because a referenced local path could not be resolved.

Mitigation: Before installing, decide whether the $50 top-up and data sharing are acceptable; set per-quest and daily spending caps, require per-quest approval, share only necessary task details, and review submitted proof promptly. Treat the security assessment as incomplete while the unresolved reference remains unchecked.

## Reference(s):

- [SideQuest API documentation](https://sidequestpays.com/llms.txt)
- [SideQuest OpenAPI specification](https://sidequestpays.com/openapi.json)
- [SideQuest homepage](https://sidequestpays.com)
- [ClawHub skill release](https://clawhub.ai/uckhill/skills/sidequest)

## Skill Output:

**Output Type(s):** [API calls, Structured data, Text, Guidance]

**Output Format:** [HTTP requests and structured JSON responses with task-specific human-submitted proof]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Proof may include notes, checklist answers, photos, location data, and timestamps; task briefs include reward and approval choices.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
