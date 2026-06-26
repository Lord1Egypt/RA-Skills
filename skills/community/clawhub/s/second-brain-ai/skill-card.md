## Description: <br>
Read, capture, search, relate, and assemble context from a user-specified local Markdown knowledge base, with controlled write operations requiring explicit approval and attribution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage a local Markdown note vault: search past notes, find related notes and backlinks, build context packs, and create or append notes only after explicit write approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read snippets from the Markdown vault configured in SECOND_BRAIN_VAULT, which may expose sensitive personal notes to the agent. <br>
Mitigation: Point SECOND_BRAIN_VAULT at a narrow notes folder and use .secondbrainignore for sensitive areas. <br>
Risk: Write-capable actions can create, append to, or initialize files in the configured vault. <br>
Mitigation: Require explicit confirmation before capture_note, append_note, or init_vault; keep allow_write gates enabled and require append attribution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/second-brain-ai) <br>
- [Publisher profile](https://clawhub.ai/user/harrylabsj) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON tool outputs and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses file-scan mode over the configured SECOND_BRAIN_VAULT; no semantic or vector index is claimed.] <br>

## Skill Version(s): <br>
2.3.3 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
