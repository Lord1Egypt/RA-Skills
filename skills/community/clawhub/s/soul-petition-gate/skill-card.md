## Description: <br>
Gives an AI agent a formal, human-reviewed channel to propose changes to protected identity files without allowing self-editing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[waitinchen](https://clawhub.ai/user/waitinchen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give an AI agent a structured petition workflow for proposed changes to SOUL.md, IDENTITY.md, or other protected workspace files while preserving human approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local backend can read, store, modify, and roll back sensitive soul or identity files. <br>
Mitigation: Require authentication on petition routes, expose the service only in a trusted local environment, and keep protected files on an explicit allowlist. <br>
Risk: Petition history and backups may retain sensitive identity content. <br>
Mitigation: Store petition and backup files in protected local paths, restrict filesystem permissions, and review retention needs before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/waitinchen/soul-petition-gate) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Flask Petition Routes](artifact/assets/soul_petition_routes.py) <br>
- [Petition Examples](artifact/examples/petition_examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with JSON, Python, TypeScript, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a Flask blueprint, OpenClaw bootstrap hook guidance, and structured petition examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
