## Description:

科研助手 supports scientific research workflows spanning literature review, data analysis and visualization, bioinformatics, drug discovery, manuscript preparation, and grant planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, developers, and external research teams use this skill to plan and produce research artifacts such as literature reviews, analysis scripts, scientific reports, manuscripts, and grant materials. It is intended to assist expert workflows, not replace scientific, ethical, clinical, or regulatory review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may propose command execution and local file operations for research workflows.

Mitigation: Review generated commands before execution, especially commands that mutate data, install packages, access credentials, or run costly analysis.

Risk: Scientific, clinical, or regulated research outputs may be incomplete, incorrect, or unsuitable for direct decision-making.

Mitigation: Use outputs as expert-assistive drafts and require qualified review, ethics approval, and domain validation before clinical, animal, or human-subject use.

Risk: Research workflows can involve API keys or cloud credentials.

Mitigation: Store secrets in environment variables and avoid writing keys into code, logs, reports, or generated files.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks, generated files, and command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local command execution and file outputs for scientific analysis workflows.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
