## Description: <br>
Long-form web novel creation engine for writing, continuation, editorial review, consistency checking, contradiction detection, and character state management across serialized fiction projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zyuanjia](https://clawhub.ai/user/zyuanjia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Authors, editors, and agent developers use this skill to plan, draft, continue, and review long-form web novels while maintaining outlines, timelines, character state, foreshadowing, and continuity records. It also provides local checking scripts for consistency, rhythm, dialogue quality, hooks, titles, repetition, and related manuscript quality signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local manuscript and project files and can write review notes, reports, tracking tables, caches, and backups. <br>
Mitigation: Confirm the active novel directory before use and review generated files before relying on them. <br>
Risk: Generated continuity reports or JSON tracking updates may be incomplete or inaccurate for a long-running story. <br>
Mitigation: Compare generated outputs against the manuscript, outline, and character state records before accepting them as authoritative. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/zyuanjia/webnovel-writer) <br>
- [README](README.md) <br>
- [Skill Definition](SKILL.md) <br>
- [Usage Examples](references/usage_examples.md) <br>
- [Chapter Checklist](references/checklist.md) <br>
- [Deep Reading Guide](references/deep_reading_guide.md) <br>
- [Character State Machine](references/character_state_machine.md) <br>
- [Foreshadowing Management](references/foreshadowing.md) <br>
- [Outline Design](references/outline_design.md) <br>
- [Writing Tips](references/writing_tips.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, generated review notes, reports, JSON tracking data, backups, and configuration updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include local report, cache, tracking, state, and backup files in the active novel project.] <br>

## Skill Version(s): <br>
3.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
