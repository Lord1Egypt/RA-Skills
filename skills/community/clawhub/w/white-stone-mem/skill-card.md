## Description: <br>
White Stone Memory gives agents an on-demand Markdown memory system for knowledge, project notes, error logs, daily reviews, and task tracking with bilingual logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[russellfei](https://clawhub.ai/user/russellfei) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and their operators use this skill to persist reusable work habits, project context, lessons learned, daily summaries, and task state in local Markdown files while loading only the memory needed for the current task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory files can retain sensitive project or personal information beyond the current session. <br>
Mitigation: Avoid storing secrets or sensitive project data unless the configured storage path is acceptable for that information. <br>
Risk: Optional vector search may use a cloud API key or local embedding service depending on configuration. <br>
Mitigation: Verify whether vector search is disabled, uses local Ollama, or uses Gemini API before indexing memory content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/russellfei/white-stone-mem) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Memory entries are stored as local Markdown files; optional vector search can use Gemini API or local Ollama.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata, released 2026-03-03) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
