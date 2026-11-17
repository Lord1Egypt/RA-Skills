## Description:

Create, improve, evaluate, and package agent skills, including test-case workflows, benchmark review, and trigger-description optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to create new skills, refine existing skills, design eval prompts, run comparative assessments, review benchmark outputs, and optimize trigger descriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The review viewer has unsafe local-server behavior and an HTML injection flaw that could expose evaluation data.

Mitigation: Use static viewer mode where possible, avoid opening review pages for outputs from untrusted skills until HTML embedding is fixed, and do not run the local viewer on a port used by other services.

Risk: The skill can write evaluation artifacts, use the local Claude Code CLI authentication through claude -p, temporarily touch .claude/commands during trigger tests, and leave viewer processes to clean up.

Mitigation: Run it in a controlled workspace, review generated files before reuse, confirm CLI-auth implications, and clean up temporary command files and background viewer processes after evaluation.

## Reference(s):

- [Skill Creator schema reference](artifact/references/schemas.md)
- [ClawHub Skill Creator listing](https://clawhub.ai/yang1002378395-cmyk/skills/skill-creator-cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON snippets, shell command examples, and generated files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create evaluation workspaces, benchmark JSON or Markdown, review HTML, packaged skill archives, and updated SKILL.md content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
