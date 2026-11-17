## Description:

Automatically scans academic reference lists for retracted, corrected, or questionable papers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, editors, reviewers, and developers use this skill to check manuscript references, bibliographies, raw citation lists, or citation files for retractions, expressions of concern, and corrections before relying on cited work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches URLs and calls third-party DOI, PMID, and retraction lookup services, which can expose manuscript or citation metadata.

Mitigation: Use it only when third-party lookups are acceptable, avoid sensitive unpublished manuscripts, and prefer local citation text or trusted HTTPS sources.

Risk: The skill can read local files and write reports to a user-provided output path.

Mitigation: Run it in a sandbox or disposable workspace and set the output path only to an intended report location.

Risk: A clean report can be incomplete when lookups fail, services rate limit requests, or recent retractions are not indexed.

Mitigation: Treat clean results as non-definitive until failed or unchecked lookups are accounted for and important citations are independently reviewed.

## Reference(s):

- [Audit Reference](references/audit-reference.md)
- [Retraction Watch Database](https://retractionwatch.com/)
- [Crossref API](https://api.crossref.org/)
- [PubMed E-utilities](https://www.ncbi.nlm.nih.gov/home/develop/api/)
- [Open Retractions](https://openretractions.com/)
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/retraction-watcher)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown or JSON report with citation statuses, evidence details, recommendations, assumptions, risks, and next checks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write a report file when an output path is provided; otherwise returns the report text to standard output.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
