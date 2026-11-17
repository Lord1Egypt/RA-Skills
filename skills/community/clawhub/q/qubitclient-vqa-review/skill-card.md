## Description:

Reviews quantum experiment result plots with Vision Language Models to describe plots, classify outcomes, support scientific reasoning, assess fit reliability, extract parameters, and evaluate experiment status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaqiangsun](https://clawhub.ai/user/yaqiangsun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantum experiment practitioners use this skill to configure and call qubitclient VLM workflows for visual review and question answering over experiment result plots. It supports plot description, outcome classification, scientific reasoning, fit assessment, parameter extraction, and success or failure evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Experiment plots may contain proprietary or sensitive research data and can be sent to a configured VLM endpoint.

Mitigation: Use only approved model providers and endpoint configurations for the data classification, and avoid sending sensitive plots to public endpoints unless approved.

Risk: Dependency drift from installing qubitclient and optional extras may change runtime behavior.

Mitigation: Install in a virtual environment and pin qubitclient plus dependencies for reviewed deployments.

Risk: Vision model analysis can misread plots or extract approximate parameters from images.

Mitigation: Use raw data and numerical fitting tools for authoritative parameter extraction and verify important conclusions before acting on them.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/yaqiangsun/QubitClient/tree/main/skills/qubitclient-vqa-review)
- [ClawHub skill page](https://clawhub.ai/yaqiangsun/skills/qubitclient-vqa-review)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with Python and shell code blocks plus JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes prompt generation, direct task execution, optional streaming output, and parsed JSON result examples.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
