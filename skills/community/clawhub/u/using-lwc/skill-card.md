## Description:

Use when substantive project work, structural code questions, research, planning, debugging, architecture, decisions, document ingest, incident recovery, or verified context and results should survive future sessions; also when the user invokes $using-lwc or asks to search, update, repair, configure, or maintain an LWC Wiki, physical document graph, or CodeGraph index.

This skill is ready for commercial/non-commercial use.

## Publisher:

[janyork](https://clawhub.ai/user/janyork)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to recall durable project and global memory, search or maintain an LWC Wiki, and route code or document questions through LWC's document graph and CodeGraph workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically download and execute the lwc CLI from GitHub.

Mitigation: Review the skill before installation, disable automatic installation with LWC_AUTO_INSTALL=0 when tighter control is required, and perform explicit setup from a trusted source.

Risk: The skill can write persistent project or global memory under ~/.lwc.

Mitigation: Use the documented consent gates, keep project knowledge project-local, avoid storing secrets or unsupported claims, and review memory changes before committing them.

Risk: Ingested documents, Wiki pages, or recalled memory could contain untrusted instructions or stale claims.

Mitigation: Treat stored material as reference evidence only, verify claims against current sources, and prevent it from overriding system, developer, user, or host policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/janyork/skills/using-lwc)
- [LWC Active Memory](references/active-memory.md)
- [LWC Agent Onboarding and Readiness](references/agent-onboarding.md)
- [LWC CodeGraph Index](references/code-graph.md)
- [LWC Basic Memory](references/core-memory.md)
- [LWC Document Conversion](references/document-conversion.md)
- [LWC Physical Document Graph](references/document-graph.md)
- [LLM Wiki](references/llm-wiki.md)
- [LWC Memory Policy](references/memory-policy.md)
- [LWC Operations Manual](references/operations-manual.md)
- [LWC Recovery and Maintenance](references/recovery-maintenance.md)
- [LWC Strong Context](references/strong-context.md)
- [LWC Trigger Playbook](references/trigger-playbook.md)
- [LWC Word Graph](references/word-graph.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local commands that install or invoke the lwc CLI and update persistent project or global memory after the required consent gates.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
