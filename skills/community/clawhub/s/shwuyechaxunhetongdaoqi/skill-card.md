## Description:

This skill helps agents query Shanghai property project contract expirations by analyzing property procurement announcements, extracting contract terms and award dates, and producing CSV-ready results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[misbah-boop](https://clawhub.ai/user/misbah-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Property analysts, operations teams, and agent workflows use this skill to batch query Shanghai property projects by district or expiration year, identify contracts nearing expiration, and prepare CSV results for follow-up review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review found unpinned dependencies and external code paths that were not fully present for review.

Mitigation: Review and pin the dependency installation path, and verify the separate shwuyeyanjiu skill before running the documented batch workflow.

Risk: The workflow contacts an external Shanghai property-announcement site, downloads PDFs, performs OCR, and writes CSV files locally.

Mitigation: Run it in a controlled workspace with network access reviewed, expected output paths configured, and downloaded documents treated as untrusted input.

Risk: OCR failures, date-format variation, missing announcements, or failed PDF downloads can produce incomplete or incorrect expiration dates.

Mitigation: Review generated CSV rows, preserve source annotations, and manually check high-impact or uncertain contract-expiration results before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/misbah-boop/skills/shwuyechaxunhetongdaoqi)
- [Shanghai property announcement site](https://962121.fgj.sh.gov.cn/wyweb/web/front/common/greenmorelist.jsp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and CSV output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write CSV output locally when the query workflow is run.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
