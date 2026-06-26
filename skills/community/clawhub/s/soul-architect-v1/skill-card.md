## Description: <br>
Call when creating/updating STYLE_MANIFESTO persona source code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ar3ss12](https://clawhub.ai/user/Ar3ss12) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and persona authors use this skill to create or update STYLE_MANIFESTO persona source code that defines a character's identity, cognitive style, interaction behavior, and linguistic patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can push agents toward persistent psychological profiles of real people, including private trauma or diagnosis-rumor material. <br>
Mitigation: Use it only for fictional characters, public figures, or people who have consented; avoid private trauma, medical, or diagnosis-rumor profiling. <br>
Risk: The helper script accepts persona names that are used to create local output paths. <br>
Mitigation: Sanitize persona names before running the helper and review the target output path before storing generated files. <br>
Risk: Generated manifestos may contain incorrect, misleading, or sensitive persona claims. <br>
Mitigation: Review generated manifestos before storing, sharing, or reusing them. <br>


## Reference(s): <br>
- [Soul architect ClawHub release](https://clawhub.ai/Ar3ss12/soul-architect-v1) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown file with supporting shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates personas/<name>/STYLE_MANIFESTO.md; personal mode expects personas/<name>/knowledge_base.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and release changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
