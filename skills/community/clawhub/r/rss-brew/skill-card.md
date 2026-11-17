## Description:

Run and operate the RSS-Brew digest pipeline, including app CLI usage, dry-runs, latest-run inspection, delivery status updates, and retry/finalize-aware operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunsetchow](https://clawhub.ai/user/sunsetchow)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use RSS-Brew to operate an RSS digest pipeline that fetches feeds, scores and ranks articles, enriches selected items, renders digests, and tracks delivery status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dry-run behavior may still commit pipeline state.

Mitigation: Use a throwaway data root for dry-runs and verify manifest changes before using production data.

Risk: The pipeline uses broad network and credential flows for feed ingestion, model scoring, and search enrichment.

Mitigation: Keep feed sources trusted, protect DEEPSEEK_API_KEY and TAVILY_API_KEY, and avoid custom DEEPSEEK_BASE_URL values unless the endpoint is controlled.

Risk: Unpinned dependencies may change behavior before operational use.

Mitigation: Pin dependencies and test the pipeline in an isolated environment before production use.

## Reference(s):

- [README](README.md)
- [Usage Reference](references/usage.md)
- [Operations Reference](references/ops.md)
- [Pipeline Specification](references/pipeline-spec.md)
- [Retry and Finalize Architecture](references/retry-architecture.md)
- [App Architecture](app/docs/architecture.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Files]

**Output Format:** [Markdown guidance with shell command examples; runtime outputs include JSON state, Markdown digests, and PDF digests.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configured data roots and external model/search API credentials during pipeline runs.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata and app/pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
