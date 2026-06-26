## Description: <br>
Records browser or API proof artifacts after coding tasks, including videos, screenshots, console logs, API results, and Markdown summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rikisann](https://clawhub.ai/user/rikisann) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and coding agents use this skill after implementation work to run scripted UI or API checks and produce proof artifacts that demonstrate the changed feature. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Proof specs can start arbitrary commands and make browser or API requests against configured targets. <br>
Mitigation: Use only trusted proof specs and review start_command, start_port, base_url, goto targets, and API request definitions before running. <br>
Risk: Generated videos, screenshots, logs, and API results can capture credentials, private data, or sensitive staging details. <br>
Mitigation: Avoid production credentials and sensitive data during proof runs, and inspect or redact generated artifacts before committing or sharing them. <br>
Risk: Setup and proof scripts may install packages or system dependencies, including commands that can invoke sudo or package managers. <br>
Mitigation: Review setup behavior before execution and do not allow unexpected sudo or package-manager changes. <br>


## Reference(s): <br>
- [Proof Spec Reference](references/proof-spec.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML proof specs, shell commands, screenshots, videos, logs, and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces proof-artifacts output directories; browser proofs may include WebM or MP4 video, screenshots, console logs, and proof-summary.md; API proofs may include api-proof.md and api-results.json.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
