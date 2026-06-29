## Description: <br>
ZM 选题策略与内容审核 helps Chinese self-media teams evaluate topics, sharpen viewpoints, design platform-specific structures, review drafts, plan revisions, match audience goals, and assess publication risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerryxn](https://clawhub.ai/user/jerryxn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Chinese-language content creators, editors, and course or community operators use this skill to decide whether a topic is worth publishing, strengthen the main argument, select a platform-appropriate structure, review drafts, and identify concrete revision actions before release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Editorial recommendations may be subjective or misaligned with the publisher's audience, platform, or brand voice. <br>
Mitigation: Use the required platform, target user, content goal, and compliance-boundary inputs, then review the recommendations against the publisher's standards before release. <br>
Risk: Publication guidance could miss compliance, exaggeration, or trust issues in monetization-oriented content. <br>
Mitigation: Apply the skill's final review posture and do not publish items marked NEEDS_REVISION or BLOCKED until the flagged issues are resolved. <br>
Risk: The authoritative security evidence is clean, but installation assurance still depends on reviewing the packaged manifest and instructions. <br>
Mitigation: Review artifact/SKILL.md and the included checklist and templates before installing or delegating the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jerryxn/skills/zm-editorial-strategy-review) <br>
- [AI 可执行性审核表｜编辑审核](artifact/checklists/ai_readiness_checklist.md) <br>
- [最小必填字段｜选题策略与内容审核](artifact/templates/minimum_required_fields.md) <br>
- [可复制给 SubAgent 的执行提示词](artifact/templates/subagent_execution_prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown review notes with topic diagnosis, viewpoint options, structure guidance, draft critique, revision actions, and PASS / NEEDS_REVISION / BLOCKED status when applicable.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires content platform, target audience, content goal, topic or title, core viewpoint, draft or outline path, compliance boundary, and optional case material.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata and artifact/_meta.json; artifact/SKILL.md frontmatter states 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
