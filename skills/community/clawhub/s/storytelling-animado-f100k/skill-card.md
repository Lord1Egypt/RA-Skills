## Description:

Turns a raw personal or client story into a 45-90 second vertical reel package with a readable script, an approved animated support-clip plan, optional Higgsfield-generated clips, and a keyword-synchronized manifest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and content teams use this skill to convert a story into a short-form reel workflow: narrative arc selection, camera-ready script, optional animated support clips, and an edit manifest. It is intended for story-based reels, not long-form YouTube, paid ads, or non-story tutorial scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may process personal story details, client examples, and optional business or profile context.

Mitigation: Use only story and profile context the user is comfortable sharing, and avoid identifying clients or students unless the user has explicit permission.

Risk: Higgsfield image or video generation can spend credits and requires connected media-generation access.

Mitigation: Review the proposed clip plan and total credit cost before approval; if Higgsfield is unavailable or balance is insufficient, produce the script, manifest, and prompts without generated clips.

Risk: Incomplete source stories can lead to invented details, unsupported numbers, or misleading claims.

Mitigation: Ask for missing specifics or leave placeholders, and verify numbers, quotes, and data-backed claims before including them in the reel.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/storytelling-animado-f100k)
- [Publisher profile](https://clawhub.ai/user/formula100k)
- [moldes-historia.md](artifact/references/moldes-historia.md)
- [clips-de-apoyo.md](artifact/references/clips-de-apoyo.md)
- [catalogo-clips-higgsfield.md](artifact/references/catalogo-clips-higgsfield.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration, shell commands, media files]

**Output Format:** [Markdown files for GUION.md and MANIFEST.md, plus optional 9:16 video clips when Higgsfield generation is available and approved.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plans at most five support clips of up to six seconds each, requires user approval before spending Higgsfield credits, and can degrade to script plus manifest prompts without generated media.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
