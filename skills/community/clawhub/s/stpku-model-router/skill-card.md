## Description: <br>
Intelligent model routing for OpenClaw that selects from 8 available models based on task type, content length, and quality requirements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stpku](https://clawhub.ai/user/stpku) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to choose Bailian model IDs for coding, writing, analysis, multimodal, and long-context tasks. It can return recommendations through a command-line interface, a Python API, or OpenClaw agent configuration examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Package metadata is not perfectly consistent across the server evidence and artifact documentation. <br>
Mitigation: Verify the publisher, version, and authoritative license before installing or approving the release. <br>
Risk: OpenClaw configuration changes can alter future model routing and costs. <br>
Mitigation: Review proposed primary and fallback model settings before applying them to an OpenClaw configuration. <br>
Risk: Task-based routing can select a suboptimal or higher-cost model when a task is misclassified or unsupported. <br>
Mitigation: Inspect recommendations for high-impact workflows and customize the routing map where local requirements differ. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stpku/stpku-model-router) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Release changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Text or Markdown recommendations with model IDs, command examples, Python snippets, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Model choices are based on local task mappings, content length thresholds, and quality settings; no API key is required by the skill evidence.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence release, metadata.json, CHANGELOG.md, _meta.json; released 2026-03-27) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
