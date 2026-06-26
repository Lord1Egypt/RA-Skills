## Description: <br>
Skill Cortex helps an agent find, install, use, learn from, and clean up short-term skills from ClawHub or GitHub when installed skills cannot complete a task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ankwu001](https://clawhub.ai/user/ankwu001) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to let an agent acquire temporary skills for tasks it cannot already handle, route future similar tasks through learned memory, and remove cached skills after use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and run other skills on demand, including candidates found outside ClawHub. <br>
Mitigation: Require affirmative user approval before installing or switching skills, treat GitHub-sourced candidates as unreviewed, and review available scan status before use. <br>
Risk: Reflex mode may skip the execution-plan confirmation for previously successful read-only flows. <br>
Mitigation: Use reflex only for unchanged, read-only skill versions, keep installation notification in place, and avoid reflex use for tasks involving credentials, account data, private files, or network APIs. <br>
Risk: Persistent routing memory could expose sensitive task details if signals include names, dates, paths, or other concrete entities. <br>
Mitigation: Apply the documented entity-filtering rule before storing signals, retaining only verbs, abstract nouns, and generic tool names. <br>


## Reference(s): <br>
- [Skill Cortex README](artifact/README.md) <br>
- [Skill Cortex Design Document](artifact/DESIGN.md) <br>
- [ClawHub](https://clawhub.ai) <br>
- [OpenClaw](https://github.com/openclaw) <br>
- [ClawHub Skill Page](https://clawhub.ai/ankwu001/skill-cortex) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces candidate recommendations, execution plans, failure reports, and local cortex-memory updates.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter states 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
