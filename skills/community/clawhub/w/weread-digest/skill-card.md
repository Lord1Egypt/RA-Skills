## Description: <br>
Weread Digest helps agents turn local WeRead highlights and notes into reading statistics, periodic digests, book summaries, cross-book themes, and Markdown knowledge-base archives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ben61405](https://clawhub.ai/user/ben61405) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and reading-workflow builders use this skill to summarize exported WeRead notes, generate weekly or monthly reading reports, identify cross-book themes, and archive selected concepts into a local Markdown or Obsidian knowledge base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads exported WeRead notes that may contain private reading history and personal annotations. <br>
Mitigation: Use it only in environments where the agent may access the local WeRead export directory, and avoid sharing generated reports unless their contents have been reviewed. <br>
Risk: Knowledge-base archiving can write Markdown files into a configured folder. <br>
Mitigation: Review the proposed file list and concept extraction plan before confirming archive actions, as required by the skill workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ben61405/weread-digest) <br>
- [Publisher profile](https://clawhub.ai/user/ben61405) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, summaries, confirmation prompts, shell commands, and optional Markdown knowledge-base files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local WeRead exports and asks for confirmation before knowledge-base archive writes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
