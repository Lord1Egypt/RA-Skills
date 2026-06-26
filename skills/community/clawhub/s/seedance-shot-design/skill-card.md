## Description: <br>
Transforms vague video ideas into structured, cinematic Seedance 2.0 prompts with shot design, bilingual output, storyboard segmentation, style references, lighting anchors, and validation checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[woodfantasy](https://clawhub.ai/user/woodfantasy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, developers, and agent users use this skill to turn rough video concepts into copy-ready Seedance 2.0 prompts with cinematic camera movement, timing, lighting, sound, and validation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional CLI guidance may lead users to install or run local tools. <br>
Mitigation: Install only from a trusted source or pinned revision, verify installers before running them, and run the Python validator only when local code execution is intended. <br>
Risk: Video, voice, likeness, or copyrighted reference materials may be uploaded to external generation services without sufficient rights or consent. <br>
Mitigation: Use only materials the user has rights to process, obtain consent for private likeness or voice references, and apply the skill's copyright-safe fallback guidance for sensitive IP. <br>
Risk: Generated prompts may still contain misleading, policy-sensitive, or unsuitable creative direction for a target platform. <br>
Mitigation: Review the generated prompt and the skill's validation checklist before submitting it to Seedance or any connected video-generation workflow. <br>


## Reference(s): <br>
- [Seedance 2.0 Official Platform Specs](references/seedance-specs.md) <br>
- [Camera Movement and Lens Dictionary](references/cinematography.md) <br>
- [Director Style Parameter Mapping Library](references/director-styles.md) <br>
- [Quality Anchors and Post-Processing Vocabulary](references/quality-anchors.md) <br>
- [Vertical Scenario Prompt Templates](references/scenarios.md) <br>
- [Audio and Sound Effect Tag Guide](references/audio-tags.md) <br>
- [Agent Skills Specification](https://agentskills.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with copy-ready prompt code blocks and optional CLI command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs follow the user's language, include a director note and complete Seedance prompt, and may segment videos longer than 15 seconds into separate prompt blocks.] <br>

## Skill Version(s): <br>
1.9.1 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
