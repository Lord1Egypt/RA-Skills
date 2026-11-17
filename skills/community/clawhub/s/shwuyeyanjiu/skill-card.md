## Description:

Researches Shanghai residential property bidding, award, and evaluation-result announcements with OCR extraction to summarize project details and calculate saturated income.

This skill is ready for commercial/non-commercial use.

## Publisher:

[misbah-boop](https://clawhub.ai/user/misbah-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and property researchers use this skill to retrieve and analyze project-level announcements from Shanghai's residential property bidding site, extract project area, fee, parking, award, and contract date details from PDFs, and calculate saturated monthly or annual income.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan verdict is suspicious because the release includes extra batch scripts and unsafe local PDF handling beyond the stated project-level research workflow.

Mitigation: Review the skill before installation, run it only in an isolated workspace, and avoid batch or /tmp-scanning scripts unless they are explicitly needed.

Risk: The included behavior can download PDFs and write local outputs such as OCR text or CSV summaries.

Mitigation: Use a private temporary directory, sanitize output paths, clean up downloaded files, and restrict workspace access before running scripts.

Risk: OCR extraction can misread project amounts, dates, fee standards, or cross-line values.

Mitigation: Manually verify extracted values against the source announcements and relevant property service contracts before relying on calculations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/misbah-boop/skills/shwuyeyanjiu)
- [Shanghai residential property announcement list](https://962121.fgj.sh.gov.cn/wyweb/web/front/common/greenmorelist.jsp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and Python code blocks, plus command-line text summaries of extracted project fields and income calculations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce downloaded PDF files, OCR text, and CSV summaries when the included scripts are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
