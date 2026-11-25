## Description:

Plans multi-shot AI videos with storyboards, visual anchors, shot grouping, 3D camera-blocking previz, and Seedance video-to-video packs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vargai](https://clawhub.ai/user/vargai)

### License/Terms of Use:

MIT-0

## Use Case:

Video creators, directors, and production teams use it to plan stories and shots, review camera blocking in a 3D animatic, and prepare Seedance reference packs before paid generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports possible project-file exposure and unsafe storyboard-content handling; some components were only partially inspected.

Mitigation: Use a non-sensitive test project first, inspect project contents and handling, and avoid including sensitive files until exposure concerns are resolved.

Risk: Project media may be uploaded to an external service during video generation.

Mitigation: Review the files and destination, authorize uploads before generation, and start with one short run after reviewing cost.

## Reference(s):

- [Story structure for short AI videos](references/story-structure.md)
- [Character, product, and vehicle sheets](references/character-sheets.md)
- [Grouping shots into master scenes](references/scene-grouping.md)
- [Three.js previz](references/threejs-previz.md)
- [Seedance video-to-video pack guide](references/seedance-v2v.md)
- [Seedance 2.5 model guide](https://varg.ai/models/seedance_2_5.md)
- [varg.ai](https://varg.ai)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Code, Configuration instructions, Shell commands]

**Output Format:** [Markdown planning documents, JSON storyboards and packs, JavaScript previz project files, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create project files and preview clips for review.]

## Skill Version(s):

1.0.0 (source: server-resolved release, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
