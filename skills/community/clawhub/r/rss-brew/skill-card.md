## Description: <br>
Run and operate the RSS-Brew digest pipeline, including app CLI usage, dry-runs, latest-run inspection, delivery status updates, and retry/finalize-aware operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunsetchow](https://clawhub.ai/user/sunsetchow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run an RSS digest pipeline, inspect recent runs, perform dry-runs, update delivery status, and troubleshoot retry/finalize behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The pipeline fetches configured feeds and articles, then may send article-derived content to external AI or search providers. <br>
Mitigation: Use mock or dry-run modes first, avoid private or sensitive feeds unless provider sharing is acceptable, and review configured API providers before production use. <br>
Risk: Pipeline execution writes persistent digest and run state under the selected data root. <br>
Mitigation: Choose a deliberate data root, inspect run manifests after execution, and verify delivery status before relying on published outputs. <br>
Risk: Runtime behavior depends on Python dependencies and environment configuration. <br>
Mitigation: Pin and audit dependencies, confirm required environment variables, and prefer the documented app CLI and virtual environment workflow. <br>


## Reference(s): <br>
- [RSS-Brew README](README.md) <br>
- [Usage Reference](references/usage.md) <br>
- [Operations Reference](references/ops.md) <br>
- [Pipeline Specification](references/pipeline-spec.md) <br>
- [Retry / Finalize Architecture](references/retry-architecture.md) <br>
- [App Architecture](app/docs/architecture.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can guide pipeline runs that create persistent run records, digest files, and delivery status updates under the configured data root.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and app/pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
