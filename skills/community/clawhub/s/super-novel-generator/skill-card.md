## Description: <br>
Generates Chinese web-novel prompts, outlines, chapter drafts, and continuity memory files from a user's genre, direction, or keywords. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hxmeie](https://clawhub.ai/user/hxmeie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and writing assistants use this skill to turn Chinese web-novel ideas into prompts, volume outlines, chapter drafts, and continuity records for serialized fiction projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and update local novel project files. <br>
Mitigation: Review target paths and generated files before relying on or sharing the workspace. <br>
Risk: The initialization script's --clean option removes or resets generated story output. <br>
Mitigation: Use --clean only when intentionally restarting a novel workspace. <br>
Risk: Continuity memory files may carry sensitive personal information if users add it. <br>
Mitigation: Keep .learnings content fictional or non-sensitive and review memory files before reuse. <br>


## Reference(s): <br>
- [Prompt Completion Guide](artifact/references/prompt-guide.md) <br>
- [Plot Structure Reference](artifact/references/plot-structures.md) <br>
- [Character Arc Reference](artifact/references/character-arcs.md) <br>
- [Antagonist Design Reference](artifact/references/antagonist-design.md) <br>
- [De-AI Writing Reference](artifact/references/de-ai-writing.md) <br>
- [Minimal Examples](artifact/references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown text, local project files, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create or update output/ and .learnings/ files when a persistent novel workspace is requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
