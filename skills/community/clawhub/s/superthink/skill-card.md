## Description: <br>
SuperThink is a deep-dive research and analysis skill that uses an interrogate flow and a four-stage automated Anthropic batch pipeline to produce long-form synthesis and an executive brief. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[inxan3](https://clawhub.ai/user/inxan3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and analysts use SuperThink to turn a scoped research question into a master reasoning brief, parallel deep-dive sections, a full synthesis document, and a concise executive brief. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user topics, scope, and generated research content to Anthropic for batch processing. <br>
Mitigation: Do not run sensitive research unless external processing is acceptable, and use a dedicated Anthropic API key where possible. <br>
Risk: Long-running batch jobs can incur API charges and continue after the initial scope confirmation. <br>
Mitigation: Review estimated cost and expected 6-12 hour runtime before confirming scope, and monitor local batch job state during execution. <br>
Risk: Generated research outputs and job state are retained on local storage. <br>
Mitigation: Delete local outputs, batch job records, and memory notes when retention is not desired. <br>
Risk: Optional webhook or Telegram notifications can disclose completion details to configured destinations. <br>
Mitigation: Leave notification variables unset unless the destination is trusted. <br>
Risk: Generated helper scripts or conversion utilities may affect local files when run. <br>
Mitigation: Review generated helper scripts before executing them, especially scripts that read, write, or convert output files. <br>


## Reference(s): <br>
- [SuperThink ClawHub release page](https://clawhub.ai/inxan3/superthink) <br>
- [Anthropic Messages Batch API](https://api.anthropic.com/v1/messages/batches) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Batch worker implementation spec](artifact/batch-worker-spec.md.md) <br>
- [Markdown to DOCX implementation spec](artifact/md2docx-spec.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, JSON job and state files, shell commands, and optional DOCX output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates persistent local research artifacts including master-brief.md, section Markdown files, synthesis.md, brief.md, pipeline-state.json, batch job files, and an optional .docx executive brief.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
