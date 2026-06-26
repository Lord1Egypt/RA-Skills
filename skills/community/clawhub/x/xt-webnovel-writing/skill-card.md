## Description: <br>
A Chinese webnovel-writing agent that routes ideation, outlining, chapter drafting, style analysis, craft revision, anti-AI-tell review, and file-backed project memory through six internal workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaotiewinner](https://clawhub.ai/user/xiaotiewinner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Chinese webnovel writers and writing agents use this skill to plan stories, draft and revise chapters, analyze reference text, check for AI-like prose patterns, and maintain long-running project memory on disk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project writing flows can create or update file-backed memory for a webnovel project. <br>
Mitigation: Use an explicit project_root, keep the project under version control or backups, and request one-time short text with no project memory when persistent files are not desired. <br>
Risk: Long-running story state can drift if chapter outputs are accepted without the skill's verify and persist checks. <br>
Mitigation: Use the documented LOAD, DRAFT, VERIFY, and PERSIST sequence and review the generated chapter_meta.stats before accepting project updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaotiewinner/xt-webnovel-writing) <br>
- [README](README.md) <br>
- [Anti-AI-tells reference](references/anti-ai-tells.md) <br>
- [OpenClaw two-phase enforcement](references/openclaw-enforcement-two-phase.md) <br>
- [OpenClaw hooks setup](references/openclaw-hooks-setup.md) <br>
- [Memory directory schema](webnovel-memory/references/directory-schema.md) <br>
- [Memory write protocol](webnovel-memory/references/write-protocol.md) <br>
- [Two-phase guard hook](hooks/two-phase-guard/HOOK.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Chinese Markdown with structured tables, code blocks, prose drafts, analysis notes, and optional project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Project writing flows may create or update files only under the user-provided project_root; one-time short text can opt out of memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
