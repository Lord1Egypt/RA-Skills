## Description: <br>
Session Context Bridge helps agents save, restore, and switch project session context through structured markdown notes for tasks, decisions, file state, blockers, and environment details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aptratcn](https://clawhub.ai/user/aptratcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to maintain project-local markdown notes for active tasks, decisions, file maps, blockers, and environment state so a later session can resume accurately. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Session notes can accidentally persist passwords, tokens, private keys, raw .env contents, connection strings, internal URLs, or sensitive credential setup details. <br>
Mitigation: Keep secrets out of .context/ files and review saved or restored notes before acting on them. <br>
Risk: Project-local .context/ files may be committed or shared unintentionally. <br>
Mitigation: Add .context/ to .gitignore unless the team intentionally wants the notes versioned. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aptratcn/session-context-bridge) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with reusable file templates and inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces project-local .context/ markdown notes; no runtime automation is included in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
