## Description:

General data annotation skill for image, video, text, and mixed datasets that guides requirement review, model-assisted labeling, structured result generation, and web-based annotation review/editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aowind](https://clawhub.ai/user/aowind)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data teams, and annotation operators use this skill to plan and execute model-assisted labeling jobs over images, videos, text, or mixed datasets, then save structured JSONL results and inspect or edit them in a web viewer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The annotation API and web viewer can expose dataset files and annotation results if deployed beyond a trusted local environment.

Mitigation: Keep the API bound to localhost or a private network, do not expose it publicly, and restrict access to a dedicated annotation results directory.

Risk: The documented Nginx/root deployment flow can introduce host-configuration and broad file-access risk.

Mitigation: Review deployment changes before use, avoid serving from privileged root paths, and deploy in a contained environment with least-privilege filesystem access.

Risk: Datasets may be sent to model providers during annotation.

Mitigation: Use non-sensitive datasets unless the selected model provider and data handling path have been approved.

## Reference(s):

- [Output Formats Reference](artifact/references/output-formats.md)
- [ClawHub Skill Page](https://clawhub.ai/aowind/skills/sjht-data-annotation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON/JSONL examples, shell commands, Python helper code, and HTML viewer configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces annotation plans, JSONL datasets, summaries, generated viewer files, and deployment guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json; CHANGELOG top entry is 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
