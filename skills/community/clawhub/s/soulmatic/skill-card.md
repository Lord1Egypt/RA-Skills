## Description: <br>
Binds, audits, and evolves agent persona files for anchoring, drift checks, compression, validation, scaffolding, and intentional persona changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lux-sp4rk](https://clawhub.ai/user/lux-sp4rk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Soulmatic to configure, re-anchor, audit, compress, validate, and evolve local persona files such as IDENTITY.md and SOUL.md. It is intended for maintaining agent voice consistency while preserving user safety and direct user corrections as higher priority. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect future assistant behavior by loading and applying local persona files. <br>
Mitigation: Review IDENTITY.md and SOUL.md before activation, and keep user safety instructions and direct user corrections above persona consistency. <br>
Risk: The skill can persist, modify, or delete workspace memory and persona files during configure, compress, evolve, or re-anchor flows. <br>
Mitigation: Require explicit confirmation and a diff before write, delete, compress, evolve, or memory actions; review MEMORY.md, LORE.md, and memory/persona-changelog.md before enabling startup or drift hooks. <br>


## Reference(s): <br>
- [Soulmatic ClawHub listing](https://clawhub.ai/lux-sp4rk/soulmatic) <br>
- [Persona Compression: Archetypal Anchors](https://luxsp4rk.substack.com/p/persona-compression-archetypal-anchors) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated local persona files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read IDENTITY.md and SOUL.md, may propose diffs, and may write local persona or memory files when explicitly confirmed.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
